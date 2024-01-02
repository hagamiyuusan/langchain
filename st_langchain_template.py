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

PORT = 13578

def get_ocr_api(content):
    res = requests.post('http://10.124.69.99:10000/infer',json={'base64_image': content},
                        params = {'preprocess': True, 'ocr':True}).json()
    
    return res

def get_ocr(content):
    api_url = "http://127.0.0.1:13578/ocrapi"
    question = {"image": content}
    response = requests.post(api_url, json=question)
    return response.json()
 
def create_db(content):
    api_url = "http://127.0.0.1:13578/upload"
    question = {"content": content}
    response = requests.post(api_url, json=question)
    return response
 
 
def generate_response(prompt):
    api_url = "http://127.0.0.1:13578/respone"
    question = {"question": prompt}
    response = requests.post(api_url, json=question)
    return response.json()["result"]


 
# Initialize session state variables
if 'user_responses' not in st.session_state:
    st.session_state['user_responses'] = ["Tôi nên làm gì đây ?"]
if 'bot_responses' not in st.session_state:
    st.session_state['bot_responses'] = ["""Bạn có thể upload ảnh hoặc file txt ở sidebar, sau đó hỏi tôi vài câu. """]
 
input_container = st.container()
response_container = st.container()
 
# Capture user input and display bot responses
user_input = st.text_input("You: ", "", key="input")
with st.sidebar:
    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your txt/images files here and click on 'Process'", accept_multiple_files=False)
    if st.button("Process"):
        with st.spinner("Processing"):
            if 'text/plain' in str(pdf_docs.type):
                content = pdf_docs.getvalue().decode("utf-8")
                create_db(content)
            else:
                img_str = base64.b64encode(pdf_docs.getvalue()).decode("utf-8")
                im = Image.open(BytesIO(base64.b64decode(img_str)))
                
                content = get_ocr(img_str)
                st.image(im)
                st.text_area("OCR result", content)
                create_db(content['result'])
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.user_responses.append(user_input)
        st.session_state.bot_responses.append(response)
       
    if st.session_state['bot_responses']:
        for i in range(len(st.session_state['bot_responses'])):
            message(st.session_state['user_responses'][i], is_user=True, key=str(i) + '_user', avatar_style="initials", seed="Kavita")
            message(st.session_state['bot_responses'][i], key=str(i), avatar_style="initials", seed="AI",)
 
with input_container:
    display_input = user_input