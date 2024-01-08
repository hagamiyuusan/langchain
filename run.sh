exec uvicorn api:app --host 127.0.0.1 --port 13579 &
exec streamlit run st_langchain_template.py  --server.port 8001