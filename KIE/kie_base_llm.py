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
from langchain import LLMChain
from langchain import HuggingFacePipeline, PromptTemplate

model_name = "nguyenhuy/mistralai-Code-Instruct-Finetune-test"
tokenizer = "nguyenhuy/mistralai-Code-Instruct-Finetune-test"

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)
class LLMBase:
    def __init__(self, model_name=model_name, top_k = 20, top_p = 0.95, temperature = 0.001):
        self.model_name = model_name
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name,
                                            trust_remote_code=True,
                                            quantization_config=bnb_config,
                                            token = hf_token,
                                            device_map = 'auto',
                                            do_sample=False 
                                            )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True, device = "auto", token = hf_token)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        self.tokenizer.padding_side = "right"
        self.text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            do_sample=True,
            max_new_tokens = 768,
            temperature = self.temperature,
            top_k = self.top_k,
            top_p = self.top_p,
            repetition_penalty=1.15,
            streamer=self.streamer
        )
        self.template = """
                        ### Instruction:
                            You are medical expert, and medical data engineer with many years on working with complex medical receipt structure. 
                            I need you parse, detect, recognize and convert following medical receipt OCR image result into structure medical receipt format. 
                            the outout mus be a well-formed json object.```json, dont tell anymore.

                            ### Input:
                            {content}
                            ### Output:

                    """.strip()
        self.template_peft = """
                        User: {content} \n Bot :
                        """
        self.prompt_peft = PromptTemplate(template=self.template_peft, input_variables=['content'])
        self.prompt = PromptTemplate(template=self.template, input_variables=['context'])

        self.llm = HuggingFacePipeline(pipeline = self.text_pipeline)
        
        self.chain = LLMChain(llm = self.llm, prompt = self.prompt, verbose=True)
        self.chain_peft = LLMChain(llm = self.llm, prompt = self.prompt_peft, verbose=True)
       
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
    def response(self, content, peft = True):
        if peft:
            return self.chain_peft(content)
        return self.chain(content)
        