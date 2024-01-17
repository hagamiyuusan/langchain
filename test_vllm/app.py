# LangChain ConversationalRetrievalChain app that streams output to gradio interface
from threading import Thread
import gradio as gr
from queue import SimpleQueue
from typing import Any, Dict, List, Union
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.llms import HuggingFaceTextGenInference
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain import PromptTemplate, LLMChain

# Load the files from the path


# Split text into chunks


# Define model and vector store

job_done = object()  # signals the processing is done

# Lets set up our streaming
class StreamingGradioCallbackHandler(BaseCallbackHandler):
    """Callback handler - works with LLMs that support streaming."""

    def __init__(self, q: SimpleQueue):
        self.q = q

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        while not self.q.empty():
            try:
                self.q.get(block=False)
            except SimpleQueue.empty:
                continue

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.q.put(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.q.put(job_done)

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Run when LLM errors."""
        self.q.put(job_done)


# Initializes the LLM
q = SimpleQueue()
llm = HuggingFaceTextGenInference(
    inference_server_url="http://localhost:8000/generate",
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.15,
    streaming=True,
    callbacks=[StreamingGradioCallbackHandler(q)]
)

# Define prompts and initialize conversation chain
template_peft = """
                User: {content} \n Bot :
                """
prompt_peft = PromptTemplate(template=template_peft, input_variables=['content'])
chain_peft = LLMChain(llm = llm, prompt = prompt_peft, verbose=True)
# Set up chat history and streaming for Gradio Display
def process_question(question):
    result = chain_peft(question)
    return result["text"]


def add_text(history, text):
    history = history + [(text, None)]
    return history, ""


def streaming_chat(history):
    user_input = history[-1][0]
    thread = Thread(target=process_question, args=(user_input,))
    thread.start()
    history[-1][1] = ""
    while True:
        next_token = q.get(block=True)  # Blocks until an input is available
        if next_token is job_done:
            break
        history[-1][1] += next_token
        yield history
    thread.join()


# Creates A gradio Interface
with gr.Blocks() as demo:
    Langchain = gr.Chatbot(label="Langchain Response", height=500)
    Question = gr.Textbox(label="Question")
    Question.submit(add_text, [Langchain, Question], [Langchain, Question]).then(
        streaming_chat, Langchain, Langchain
    )
demo.queue().launch()