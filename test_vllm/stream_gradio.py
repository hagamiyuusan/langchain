import gradio as gr
import torch
from threading import Thread
from kie_base_llm import LLMBase

custom_llm = LLMBase()
def chat(user_input, history, system_prompt):

    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    model_output = ""
    for new_text in streamer:
        model_output += new_text
        yield model_output
    return model_output


with gr.Blocks(theme=gr.themes.Monochrome(
               font=[gr.themes.GoogleFont("Montserrat"), "Arial", "sans-serif"],
               primary_hue="sky",  # when loading
               secondary_hue="sky", # something with links
               neutral_hue="dark"),) as demo:  #main.

    gr.Markdown(DESCRIPTION)
    gr.Markdown(SYS_PROMPT_EXPLAIN)
    dropdown = gr.Dropdown(choices=prompts, label="Type your own or select a system prompt", value="You are a helpful AI.", allow_custom_value=True)
    chatbot = gr.ChatInterface(fn=chat, additional_inputs=[dropdown])

demo.queue(api_open=False).launch(show_api=False,share=True)