import streamlit as st
def returnChain(document):
    print(document)
uploaded_file = st.file_uploader('Upload your corpus', type='txt')
if uploaded_file is not None:
    st.button("Process", key = 'process_db', on_click = returnChain, args=(uploaded_file.read(),) )
