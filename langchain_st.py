from PyPDF2 import PdfReader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from torch import cuda, bfloat16
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA
from langchain import HuggingFacePipeline, PromptTemplate
from torch import cuda, bfloat16
import transformers
from transformers import  AutoModelForCausalLM, AutoTokenizer
from transformers import TextStreamer, pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import LLMChain
from langchain.schema import StrOutputParser
import streamlit as st

cache_dir = '/home/huynv43/langchain_rag/tmp'
hf_token = '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'
model_embeddings = 'keepitreal/vietnamese-sbert' 
model_llm = 'vilm/vinallama-7b'
model_kwargs = {'device':'cpu'}
encode_kwargs = {'normalize_embeddings': False}


class VectorDatabase:
    def __init__(self):
        self.db = None
        self.embeddings = HuggingFaceEmbeddings(model_name = model_embeddings, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
        print("Initialized")
    def get_text_chunks(self, docs):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(docs)
        return chunks
    def get_vectorstore(self, text_chunks):
        # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=self.embeddings)
        self.db = vectorstore
        return vectorstore



class LLM:
    def __init__(self, db):
        
        self.bnb_config = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=bfloat16)
        
        self.db_entity = db


        self.model = AutoModelForCausalLM.from_pretrained(model_llm,
                                             quantization_config=self.bnb_config,
                                             trust_remote_code=True,
                                             token = hf_token,
                                             cache_dir = cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_llm, use_fast=True, model_kwargs=model_kwargs, token = hf_token, cache_dir = cache_dir)
        
        self.prompt_template = """Trả lời càng ngắn càng tốt. Sử dụng các thông tin trong văn bản sau đây để trả lời câu hỏi ở cuối.  Nếu không biết câu trả lời, bạn chỉ cần nói rằng bạn không biết, đừng cố bịa ra câu trả lời. 

                                Thông tin văn bản : {context}
                                Câu hỏi : {question}

                                """
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        self.text_pipeline = pipeline(
                                "text-generation",
                                model=self.model,
                                tokenizer=self.tokenizer,
                                max_new_tokens=512,
                                temperature=0.1,
                                top_p=0.95,
                                repetition_penalty=1.15,
                                streamer=self.streamer,
                            )
        self.llm = HuggingFacePipeline(pipeline = self.text_pipeline, model_kwargs={"temperature": 0.1, "max_length":512,'device': 'cpu'})

        self.qa_chain = None

        print("Initialized")

    def returnChain(self, document):
        chunks = self.db_entity.get_text_chunks(document)
        db = self.db_entity.get_vectorstore(chunks)
        prompt = PromptTemplate(template=self.prompt_template, input_variables=['context', 'question'])
        qa_chain = RetrievalQA.from_chain_type(
            llm = self.llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt},
            verbose=True
        )

        self.qa_chain = qa_chain

    def answer(self, prompt):
        return self.qa_chain(prompt)['result']

db_entity = VectorDatabase()

llm = LLM(db = db_entity)

def  on_file_upload():
    uploaded_file = st.session_state.uploaded_file
    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        llm.returnChain(content)

st.file_uploader("Upload a file", type=['txt'], key='uploaded_file', on_change=on_file_upload)
query_text = st.text_input('Enter your question:', placeholder = 'Please provide a short summary.')
if st.button('Click me', disabled = llm.qa_chain == None):
    # Call the function and get the result
    result = llm.answer(query_text)
    if len(result):
        st.info(result)







