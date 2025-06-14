"""
Gradio app for a chat interface that streams responses from a chat manager.
This app uses a chat manager to handle conversation history and retrieve relevant information from project documents.
The chat can use tools to search for information in the project documents, and is also
capable of generating diagrams using PlantUML and can reference the documents used in its responses.
"""

import gradio as gr
from chat_manager_with_tools import ChatManagerWithTools
import dotenv
dotenv.load_dotenv(".env.private")

chat_manager = ChatManagerWithTools()

async def chat_stream(messages, _):
    response = ""
    async for chunk in chat_manager.stream_response(messages):
        response += chunk
        yield response

app = gr.ChatInterface(
        fn=chat_stream,
        type="messages",
        title="Eprice project knowledge base.",
        autoscroll=True,
        theme="soft",
    )

if __name__ == "__main__":
    app.queue().launch(pwa=True)