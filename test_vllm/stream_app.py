import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
from threading import Thread
import transformers
from torch import cuda, bfloat16
import time

from PIL import Image
import numpy as np
import requests
import os
os.environ["CUDA_VISIBLE_DEVICES"]="1"
from awq import AutoAWQForCausalLM
from resources import birth_examples, birth_schema, medical_schema, medical_examples, passport_examples, passport_schema, invoices_examples, invoices_schema
from resources import template_kie, template_general
from utils import get_OCR
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

quant_path = "TheBloke/Mistral-7B-v0.1-AWQ"
quant_file = "model.safetensors"
# ocr = OCR()
import io
import base64
count = 0

schema = medical_schema.strip()
examples = medical_examples.strip()

current_mode  = "KIE"
template = template_kie
def update_mode(mode):
    global current_mode
    current_mode = mode
def update_schema(input_text):
    global schema
    schema = input_text
def update_examples(input_text):
    global examples
    examples = input_text

def update_prompt(schema_des, examples_des):
    global schema
    global examples
    schema = schema_des    
    examples = examples_des

js = "(x) => confirm('Press a button!')"

def process_dropdown_value(choice):
    if choice == 'birth_certificates':
        schema_src = birth_schema
        examples_src = birth_examples
        update_schema(birth_schema)
        update_examples(birth_examples)
    elif choice == 'passports':
        schema_src = passport_schema
        examples_src = passport_examples
        update_schema(passport_schema)
        update_examples(passport_examples)
    elif choice == 'prescriptions':
        schema_src =  medical_schema
        examples_src = medical_examples
        update_schema(medical_schema)
        update_examples(medical_examples)
    elif choice == 'invoices':
        schema_src = invoices_schema
        examples_src = invoices_examples
        update_schema(invoices_schema)
        update_examples(invoices_examples)
    return schema_src, examples_src
# model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1",
#                                             trust_remote_code=True,
#                                             quantization_config=bnb_config,
#                                             device_map = 'auto',
#                                             do_sample=False )
# tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", torch_dtype=torch.float16, use_fast = True, device = 'auto')
model = AutoAWQForCausalLM.from_quantized(quant_path, quant_file, safetensors=True, fuse_layers=False, device_map='auto')
tokenizer = AutoTokenizer.from_pretrained(quant_path, trust_remote_code=True)

def image_to_base64(image):
    image = Image.fromarray(image.astype('uint8'), 'RGB')
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    result_ocr = get_OCR(img_str)
    content = get_text(result_ocr)
    return content

def get_text(ocr_res):
    text = ''
    phrases = ocr_res["phrases"]
    for phrase in phrases:
        text += phrase['text'] + '\n'
    return text

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [[1, 2],[1, 1, 730, 28747],[1, 8789],[1, 1247, 13, 28747],[1, 1247, 28747],[1, 1867, 730, 28767]]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False
def return_msg(msg):
    return msg
def open_modal():
    pass



custom_js = """
document.getElementById('myPopup').style.display = 'block';
document.getElementById('myPopup').style.right = '-400px';  // Start outside the screen
setTimeout(function() {
    document.getElementById('myPopup').style.transition = 'right 0.5s';
    document.getElementById('myPopup').style.right = '15px';  // Slide in
}, 100);

document.getElementById('closePopup').onclick = function() {
    document.getElementById('myPopup').style.display = 'none';
}
"""
def predict(message, history):

    # history_transformer_format = history + [[message, ""]]
    stop = StopOnTokens()
    global schema, examples, template, current_mode
    if current_mode == "KIE":
        formatted_template = template_kie.format(schema = schema, examples = examples, content = message)
    else:
        formatted_template = template_general.format(content = message)
    print(formatted_template)
    # messages = "".join(["".join(["\n<human>:"+item[0], "\n<bot>:"+item[1]])  #curr_system_message +
    #             for item in history_transformer_format])
    model_inputs = tokenizer([formatted_template], return_tensors="pt").to("cuda")
    streamer = TextIteratorStreamer(tokenizer, timeout=20., skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=1024,
        do_sample=False,
        top_p=0.95,
        top_k=20,
        temperature=1.0,
        num_beams=1,
        repetition_penalty = 1.15,
        stopping_criteria=StoppingCriteriaList([stop])
        )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()
    start = time.time()
    partial_message  = ""
    global count
    count = 0
    for new_token in streamer:
        print(new_token)
        if new_token != '<' and new_token !='```':
            count+=1
            partial_message += new_token
            yield partial_message
    end = time.time()
    print(end-start)
    print(f"""{count/(end-start)} tokens per second""")
with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Chat interface"):
            with gr.Row():
                with gr.Column(scale = 1):
                    mode_selector = gr.Radio(choices=["KIE", "General"], label="Select Mode", value="KIE")
                    mode_selector.change(fn=update_mode, inputs=mode_selector, outputs=None)
                    image_input = gr.Image(label="Upload Image")
                    convert_button = gr.Button("Get OCR Text")
                    output_textbox = gr.Textbox(label="OCR Result", interactive=False, show_copy_button=True)
                    convert_button.click(fn=image_to_base64, inputs=image_input,
                                          outputs=[output_textbox])
                with gr.Column(scale = 2):
                    chat_interface = gr.ChatInterface(predict, autofocus=False)
                    output_textbox.change(fn = return_msg, inputs = output_textbox, outputs = chat_interface)

        with gr.Tab("Settings"):
            with gr.Row():
                with gr.Column(scale = 1):
                    with gr.Accordion("Schema", open=False):
                        schema_input = gr.Textbox(label="Enter your Schema", value=schema, lines = 20)
                        schema_button = gr.Button("Update Schema")
                        schema_button.click(fn=update_schema, inputs = schema_input, outputs=None)
                with gr.Column(scale = 1):
                    with gr.Accordion("Examples", open=False):
                        examples_input = gr.Textbox(label="Enter your Examples", value = examples, lines = 20)
                        examples_button = gr.Button("Update Examples")
                        examples_button.click(fn=update_examples, inputs=examples_input, outputs=None)
                        # show_modal_button = gr.Button("Show Examples")
                        # show_modal_button.click(None, None, None, js = custom_js)

            document = gr.Dropdown([
                "passports", "birth_certificates", "prescriptions", "invoices"
            ],
            value="prescriptions",
            label="Select Document Type")
            document.change(fn=process_dropdown_value, inputs=document, outputs=[schema_input, examples_input])


demo.launch(server_name="0.0.0.0", server_port=8003, share=False)