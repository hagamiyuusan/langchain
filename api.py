import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
hf_token = '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'
from torch import cuda, bfloat16
import transformers
# from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from langchain import HuggingFacePipeline, PromptTemplate
from torch import cuda, bfloat16
import transformers
from transformers import  AutoModelForCausalLM, AutoTokenizer
from transformers import TextStreamer, pipeline
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import LLMChain
from langchain.schema import StrOutputParser
from PIL import Image
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from pydantic import BaseModel
import io
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR,draw_ocr
from numpy import asarray
import base64
import gc
class Item(BaseModel):
    content: str
class Prompt(BaseModel):
    question: str
class ImgBase64(BaseModel):
    image: str
class ModelName(BaseModel):
    model_name : str
class OCR:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.config = Cfg.load_config_from_name('vgg_transformer')
        self.detector = Predictor(self.config)
    def get_ocr(self, image):
        data = asarray(image)
        detect = self.ocr(data, cls = True)
        boxes = [line for line in detect[0]]
        print(boxes)
        result = ""
        for box in boxes:
            top_left     = (int(box[0][0]), int(box[0][1]))
            bottom_right = (int(box[2][0]), int(box[2][1]))
            bounding_box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
            result += self.detector.predict(image.crop(bounding_box), return_prob=False)
            result += "\n"
        return result
 
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)
 
class LLM:
    def __init__(self, model_name = "LR-AI-Labs/vbd-llama2-7B-50b-chat",
                 embedding_name = "keepitreal/vietnamese-sbert"):
        self.model_embeddings = embedding_name
        self.cache_dir = '/home/huy.nguyen/langchain_template/tmp'
        self.model_name_or_path = model_name
        self.model_kwargs = {'device': 'cuda:0'}

 
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path,
                                             trust_remote_code=True,
                                             quantization_config=bnb_config,
                                             token = hf_token)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, use_fast=True, model_kwargs=self.model_kwargs, token = hf_token)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        self.text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=80,
            temperature=0.1,
            top_p=0.95,
            repetition_penalty=1.15,
            streamer=self.streamer,
        )
        self.llm = HuggingFacePipeline(pipeline = self.text_pipeline, model_kwargs={"temperature": 0.1, "max_length":512,'device': 'cuda:0'})
        self.embeddings = HuggingFaceEmbeddings(model_name = self.model_embeddings,  model_kwargs = self.model_kwargs)
        self.db = None
        self.prompt_template = """You are an expert in question and answering. Your goals is to provide user useful answer from provided knowledge. Think step by step and never ignore any step.
                        Remember:
                        - always answer in Vietnamese.
                        - dont try to generate other answers and questions.
                        - to be honest if you don't know, don't try to answer.
 
                        knowledge : {context}
 
 
                        question : {question}
 
                        """
        self.prompt = PromptTemplate(template=self.prompt_template, input_variables=['context', 'question'])
    
    def change_model(self, model_name):
        del self.model
        del self.text_pipeline
        del self.llm
        self.model = AutoModelForCausalLM.from_pretrained(model_name,
                                             trust_remote_code=True,
                                             quantization_config=bnb_config,
                                             token = hf_token)
        
        self.text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=80,
            temperature=0.1,
            top_p=0.95,
            repetition_penalty=1.15,
            streamer=self.streamer,
        )

        self.llm = HuggingFacePipeline(pipeline = self.text_pipeline, model_kwargs={"temperature": 0.1, "max_length":512,'device': 'cuda:0'})
        return "OK"
    def create_db(self, context):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.db = None
        print(context)
        docs = text_splitter.split_text(context)
        self.db = FAISS.from_texts(docs, self.embeddings)
        return self.db
    
    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def result(self, question):
        qa_chain = RetrievalQA.from_chain_type(
            llm = self.llm,
            chain_type="stuff",
            retriever=self.db.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=False,
            chain_type_kwargs={"prompt": self.prompt},
            verbose=True
        )

        return qa_chain(question)
chatbot = LLM()
app = FastAPI()
ocr = OCR()
print("Completed load model")
@app.get('/')
def get():
    return 'Hello World'
@app.post('/upload')
def upload(item: Item):
    chatbot.create_db(item.content)
    return {"result": "done"}
 
@app.post('/respone')
def create_upload_files(prompt : Prompt):
    result = chatbot.result(prompt.question)
    print("1")
    return {"result": result}

# @app.post('/ocr')
# async def get_ocr_from_image(file: UploadFile = File(...)):
#     image = Image.open(io.BytesIO(await file.read()))
#     text = ocr.get_ocr(image)
#     chatbot.create_db(text)
#     return {"result": text}

@app.post('/ocrapi')
async def get_ocr_from_pillow(file: ImgBase64):
    image = Image.open(io.BytesIO(base64.b64decode(file.image)))
    text = ocr.get_ocr(image)
    return {"result": text}

# @app.post('/ocrapi')
# async def get_ocr_from_pillow(file: ImgBase64):
#     image = Image.open(io.BytesIO(base64.b64decode(file.image)))
#     text = ocr.get_ocr(image)
#     return {"result": text}

@app.post('/changemodel')
async def api_change_model(modelname : ModelName):
    try:
        chatbot.change_model(modelname.model_name)
        return {"result" : "done"}
    except NameError:
        return {"error " : NameError}