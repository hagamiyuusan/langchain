from kie_base_llm import LLMBase
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
import requests
st.title(":violet[Chat Bot via Streamlit]")
colored_header(label='', description='', color_name='gray-30')
from PIL import Image
from io import BytesIO
import numpy as np
import base64
from utils import get_OCR


def get_text(ocr_res):
    text = ''
    phrases = ocr_res["phrases"]
    for phrase in phrases:
        text += phrase['text'] + '\n'
    return text
if 'peft' not in st.session_state:
    st.session_state['peft'] = False
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = 'nguyenhuy/mistralai-Code-Instruct-Finetune-test'
if 'model' not in st.session_state:
    st.session_state['model'] = LLMBase(model_name=st.session_state['model_name'])
 
# Initialize session state variables
if 'user_responses' not in st.session_state:
    st.session_state['user_responses'] = ["Tôi nên làm gì đây ?"]
if 'bot_responses' not in st.session_state:
    st.session_state['bot_responses'] = ["""Bạn có thể upload ảnh hoặc file txt ở sidebar, sau đó hỏi tôi vài câu. """]
if 'image' not in st.session_state:
    st.session_state['image'] = None
if 'text' not in st.session_state:
    st.session_state['text'] = None
if 'temperature' not in st.session_state:
    st.session_state['temperature']  = 0.01
if 'top_k' not in st.session_state:
    st.session_state['top_k'] = 50
if 'top_p' not in st.session_state:
    st.session_state['top_p'] = 0.9

def change_model(model_name, top_k, top_p, temperature):
    st.session_state['model'].change_model(model_name=model_name, top_k=top_k, top_p=top_p, temperature=temperature)
    st.session_state['model_name'] = model_name
def generate_response(content, peft):
    response = st.session_state['model'].response(content, peft)
    return response

input_container = st.container()
response_container = st.container()
user_input = st.text_input("You: ", "", key="input")

with st.sidebar:
    option = st.selectbox(
        "Which model do you want to use ?",
        ("bkai-foundation-models/vietnamese-llama2-7b-120GB", 
        "LR-AI-Labs/vbd-llama2-7B-50b-chat", 
        "nguyenhuy/mistralai-Code-Instruct-Finetune-test",
        "mistralai/Mistral-7B-v0.1",
        "HuggingFaceH4/zephyr-7b-beta",
        "meta-llama/Llama-2-13b-chat-hf",
        "meta-llama/Llama-2-13b-hf"),
        index=None,
        placeholder = "Current model :" + st.session_state['model_name'],
        )
    # with st.spinner("Switching model"):
    #     st.button('Switch model', key='switching_model',
    #     on_click=api_change_model, args=(option, ))


    st.slider('top_k', 0, 50, step = 1, key='top_k')
    st.slider('top_p', 0.0, 1.0, step = 0.1, key='top_p')
    st.slider('Temperature', 0.0, 2.0, step = 0.01, key = 'temperature')
    
    with st.spinner("Switching model"):
        st.button('Switch model', key='switching_model',
        on_click = change_model, args=(option, st.session_state['top_k'], st.session_state['top_p'], st.session_state['temperature'] ))
    on = st.toggle('KIE', value = False)

    if on:
        st.session_state['peft'] = True
    if not on:
        st.session_state['peft'] = False
    

    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your txt/images files here and click on 'Process'", accept_multiple_files=False)
    if st.button("Process"):
        with st.spinner("Processing"):
            if 'text/plain' in str(pdf_docs.type):
                content = pdf_docs.getvalue().decode("utf-8")
                st.session_state['text'] = content
                st.session_state['image'] = None

            else:
                img_str = base64.b64encode(pdf_docs.getvalue()).decode("utf-8")
                im = Image.open(BytesIO(base64.b64decode(img_str)))
                ocr_res = get_OCR(im, preprocess=True)
                content = get_text(ocr_res)
                st.session_state['text'] = content
                st.session_state['image'] = im

    if st.session_state['image'] is not None:
        st.image(st.session_state['image'])
    if st.session_state['text'] is not None:
        st.download_button(label = 'Download OCR result', data = st.session_state['text'], file_name = 'result.txt', mime = 'text/plain')
        for line in st.session_state['text'].split('\n'):
            st.write(line)
with response_container:
    if user_input:
        response = generate_response(user_input, peft = st.session_state['peft'])
        result = response['text']
        print(result)
        st.session_state.user_responses.append(user_input)
        st.session_state.bot_responses.append(result)

    if st.session_state['bot_responses']:
        for i in range(len(st.session_state['bot_responses'])):
            message(st.session_state['user_responses'][i], is_user=True, key=str(i) + '_user', avatar_style="initials", seed="Kavita")
            message(st.session_state['bot_responses'][i], key=str(i), avatar_style="initials", seed="AI")
with input_container:
    display_input = user_input