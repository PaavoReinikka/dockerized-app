"""
Gradio app for a chat interface that streams responses from a chat manager.
This app uses a chat manager to handle conversation history and retrieve relevant information from project documents.
The chat manager is initialized with an agent that can use tools to search for information in the project documents.
The agent is capable of generating diagrams using PlantUML and can reference the documents used in its responses.
"""

import gradio as gr
from agent_manager import AgentManager
from autoloading_uml import uml_viewer
from langchain.schema import HumanMessage, AIMessage
import dotenv
dotenv.load_dotenv(".env.private")

chat_manager = AgentManager()

    
# clear all files from diagrams/ directory
def clear_diagrams():
    import os
    diagrams_dir = os.path.join(os.path.dirname(__file__), "diagrams")
    for filename in os.listdir(diagrams_dir):
        file_path = os.path.join(diagrams_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def lc_messages_to_gradio_history(messages):
    """
    Convert a list of LangChain messages to Gradio chat history format:
    List of [user_msg, assistant_msg] pairs.
    """
    history = []
    user_msg = None
    for msg in messages:
        if isinstance(msg, HumanMessage):
            user_msg = msg.content
        elif isinstance(msg, AIMessage) and user_msg is not None:
            history.append([user_msg, msg.content])
            user_msg = None
    return history


async def chat_stream(messages, _):
    async for chunk in chat_manager.stream_response(messages, mem=True):
        yield chunk


with gr.Blocks(fill_height=True) as app:
    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            gr.Markdown("# UML Diagrams")
            uml_viewer()
        with gr.Column(scale=1):
            gr.ChatInterface(
                fn=chat_stream,
                type="messages",
                title="Knowledge Base Agent",
                autoscroll=True,
            )


if __name__ == "__main__":
    clear_diagrams()  # Clear diagrams directory on startup
    app.queue().launch()