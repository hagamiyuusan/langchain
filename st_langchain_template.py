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

PORT = 13579

# def get_ocr_api(content):
#     res = requests.post('http://10.124.69.99:10000/infer',json={'base64_image': content},
#                         params = {'preprocess': True, 'ocr':True}).json()
#     print(res)
#     return res

def get_text(ocr_res):
    text = ''
    phrases = ocr_res["phrases"]
    for phrase in phrases:
        text += phrase['text'] + '\n'
    return text


# def get_ocr(content):
#     api_url = "http://127.0.0.1:13579/ocrapi"
#     question = {"image": content}
#     response = requests.post(api_url, json=question)
#     return response.json()
 
def create_db(content):
    api_url = f"""http://127.0.0.1:13579/upload"""
    question = {"content": content}
    response = requests.post(api_url, json=question)
    return response
 
 
def api_change_model(model_name, top_k, top_p, temperature):
    api_url = "http://127.0.0.1:13579/changemodel"
    question = {"model_name": model_name, "top_k":top_k, "top_p": top_p, "temperature": temperature}
    response = requests.post(api_url, json=question)
    return response.json()["result"]

def generate_response(prompt):
    api_url = "http://127.0.0.1:13579/respone"
    question = {"question": prompt}
    response = requests.post(api_url, json=question)
    print(response.json())
    return response.json()["result"], response.json()['time']

if 'main_model' not in st.session_state:
    st.session_state['model'] = 'LR-AI-Labs/vbd-llama2-7B-50b-chat'
 
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
    st.session_state['temperature']  = 0.1
if 'top_k' not in st.session_state:
    st.session_state['top_k'] = 50
if 'top_p' not in st.session_state:
    st.session_state['top_p'] = 0.9
  
input_container = st.container()
response_container = st.container()
 
# Capture user input and display bot responses
user_input = st.text_input("You: ", "", key="input")
with st.sidebar:
    option = st.selectbox(
        "Which model do you want to use ?",
        ("bkai-foundation-models/vietnamese-llama2-7b-120GB", 
        "LR-AI-Labs/vbd-llama2-7B-50b-chat", 
        "vilm/vinallama-7b",
        "mistralai/Mistral-7B-v0.1",
        "HuggingFaceH4/zephyr-7b-beta",
        "meta-llama/Llama-2-13b-chat-hf",
        "meta-llama/Llama-2-13b-hf"        ),
        index=None,
        placeholder = "Current model :" + st.session_state['model'],
        )
    # with st.spinner("Switching model"):
    #     st.button('Switch model', key='switching_model',
    #     on_click=api_change_model, args=(option, ))


    st.slider('top_k', 0, 50, step = 1, key='top_k')
    st.slider('top_p', 0.0, 1.0, step = 0.1, key='top_p')
    st.slider('Temperature', 0.0, 2.0, step = 0.1, key = 'temperature')

    with st.spinner("Switching model"):
        st.button('Switch model', key='switching_model',
        on_click=api_change_model, args=(option, st.session_state['top_k'], st.session_state['top_p'], st.session_state['temperature'] ))

    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your txt/images files here and click on 'Process'", accept_multiple_files=False)
    if st.button("Process"):
        with st.spinner("Processing"):
            if 'text/plain' in str(pdf_docs.type):
                content = pdf_docs.getvalue().decode("utf-8")
                st.session_state['text'] = content
                st.session_state['image'] = None
                create_db(content)
            else:
                img_str = base64.b64encode(pdf_docs.getvalue()).decode("utf-8")
                im = Image.open(BytesIO(base64.b64decode(img_str)))
                ocr_res = get_OCR(im, preprocess=True)
                text = get_text(ocr_res)
                st.session_state['text'] = text
                st.session_state['image'] = im
                print(text)
                create_db(text)

    if st.session_state['image'] is not None:
        st.image(st.session_state['image'])
    if st.session_state['text'] is not None:
        st.download_button(label = 'Download OCR result', data = st.session_state['text'], file_name = 'result.txt', mime = 'text/plain')
        for line in st.session_state['text'].split('\n'):
            st.write(line)
with response_container:
    if user_input:
        response, time = generate_response(user_input)
        result = response['result']
        result = result.strip() + " (time: " + str(time) + "s)"
        st.session_state.user_responses.append(user_input)
        st.session_state.bot_responses.append(result)
       
    if st.session_state['bot_responses']:
        for i in range(len(st.session_state['bot_responses'])):
            message(st.session_state['user_responses'][i], is_user=True, key=str(i) + '_user', avatar_style="initials", seed="Kavita")
            message(st.session_state['bot_responses'][i], key=str(i), avatar_style="initials", seed="AI",)
 
with input_container:
    display_input = user_input