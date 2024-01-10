import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
hf_token = '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'
from torch import cuda, bfloat16
import transformers
# from langchain.memory import ConversationBufferMemory
from torch import cuda, bfloat16
import transformers
from transformers import  AutoModelForCausalLM, AutoTokenizer
from transformers import TextStreamer, pipeline
import io
import gc
import torch
from langchain_experimental.llms import JsonFormer
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

model_name = "nguyenhuy/mistralai-Code-Instruct-Finetune-test"
tokenizer = "nguyenhuy/mistralai-Code-Instruct-Finetune-test"

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)
class LLMBase:
    def __init__(self, model_name=model_name, top_k = 20, top_p = 0.95, temperature = 0.01):
        self.model_name = model_name
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name,
                                            trust_remote_code=True,
                                            quantization_config=bnb_config,
                                            token = hf_token,
                                            device_map = 'auto'
                                            )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True, device = "auto", token = hf_token)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        self.text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            do_sample=True,
            max_new_tokens = 1024,
            temperature = self.temperature,
            top_k = self.top_k,
            top_p = self.top_p,
            repetition_penalty=1.15,
            streamer=self.streamer
        )

        self.default_data_points =  """
        {
        "current_institute": "name of the hospital or clinic issuing the prescription",
        "name": "patient full name",
        "gender": "patient gender",
        "birth": "date of birth",
        "age": "patient age",
        "address": "patient address",
        "tel_customer": "patient phone number",
        "id_bhyt": "health insurance card number",
        "diagnosis": "diagnosis",
        "drugs": [{
            "drug_name": "drug name",
            "drug_dose": "drug dosage, usage and instructions",
            "drug_quantity": "drug duantity"
        }],
        "date_in": "issued date",
        "doctor_name": "doctor full name",
        }
        """
        self.json_schema = {
            "type": "object",
            "properties": {
                "current_institute": {"type": "string"},
                "patient_name": {"type": "string"},
                "gender": {"type": "string"},
                "birth": {"type": "string"},
                "age": {"type": "string"},
                "address": {"type": "string"},
                "tel_customer": {"type": "string"},
                "id_bhyt": {"type": "string"},
                "diagnosis": {"type": "string"},
                "drugs": {
                    "type": "array",
                    "drugs": {
                        "type": "object",
                        "properties": {
                            "drug_name": {"type": "string"},
                            "drug_dose": {"type": "string"},
                            "drug_quantity": {"type": "string"}
                        }
                    }
                },
                "date_in": {"type": "string"},
                "doctor_name": {"type": "string"},                
            }
        }
        self.template = """
                                        Instruction:
                    You are medical expert, and medical data engineer with many years on working with complex medical receipt structure. 
                    I need you parse, detect, recognize and convert following medical receipt OCR image result into structure medical receipt format. 
                    the outout mus be a well-formed json object.```json
                    
                    ### Input:
                    {content}
                    ### Output:
                    """.strip()
        self.builder = JsonFormer(json_schema = self.json_schema, pipeline = self.text_pipeline)
    def change_model(self, model_name, top_k = 50, top_p = 0.9, temperature = 0.1):
        try:
            del self.model
            del self.text_pipeline
            del self.builder
            del self.tokenizer
            gc.collect()
            torch.cuda.empty_cache()
        except:
            pass
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True,
                                                       device_map = "auto",
                                                       )

        self.model = AutoModelForCausalLM.from_pretrained(model_name,
                                             trust_remote_code=True,
                                             quantization_config=bnb_config,
                                             device_map = "auto")
        
        self.text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens = 512,
            temperature = self.temperature,
            top_k = self.top_k,
            top_p = self.top_p,
            repetition_penalty=1.15,
            streamer=self.streamer,
        )
        self.builder = JsonFormer(json_schema = self.json_schema, pipeline = self.text_pipeline)
    def response(self, content):
        formatted_prompt = self.template.format(content = content,
            data_points = self.default_data_points)
        return self.builder.predict(formatted_prompt, stop = ["AI ASSISTANT:", "Human:"])