import gradio as gr
from autoloading_uml import uml_viewer  # or from .app2 if in a package

def chat_ui():
    with gr.Blocks() as chat:
        gr.Markdown("# Chat")
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        msg.submit(lambda m, h: (h + [[m, "Hi!"]], ""), [msg, chatbot], [chatbot, msg])
    return chat

with gr.Blocks() as app:
    with gr.Row():
        chat_ui()
        uml_viewer()

app.launch()