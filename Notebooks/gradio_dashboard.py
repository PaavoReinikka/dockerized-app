import gradio as gr
from ollama import chat, ChatResponse
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv(".env.development")


context = """
You are a helpful assistant that answers questions about a web app called 'Eprice'.
The app is used for viewing current and historical market electricity prices in Finland.
The app has a Home page, a Prices page, and a Production/consumption page.
The home page shows the current price and a graph of the last 24 hours.
On the prices page you can select a date range and see the prices for that period.
On the production/consumption page you can also select a date range and see the production and consumption data for that period.
The Production/consumption page also can also show the price for that period.
The Prices and Production/consumption pages also show some basic statistics for the selected period, such as the average value, the max value, the min value, and the standard deviation.
On the Prices and Production/consumption pages you can also select from various ways data is shows.
For example, you can choose to look at the difference between Production and Consumption, and switch between price and production/consumption data.
You can also average over the selected period, or look at hourly or daily averages -- averaging options are weekdays and hourly.
You can also select the type of chart -- options are line or bar chart.
The app is built using Python, FastAPI (backend), Svelte and JS (frontend), PostgreSQL (database) for caching data (to guarantee fast response times), and an open source LLM (Ollama) for the chat interface.
The app also has this chat interface that allows you to ask questions about the app and get answers.
The chat is placed on the lower right corner of the app, and you can click on it to open the chat window.
"""

class ChatManager:
    """
    A class to manage chat interactions, including maintaining conversation history and handling system messages.
    This class uses the Ollama chat API to send messages and receive responses.
    Attributes:
        system_message (str): The initial system message that sets the context for the chat.
        history (list): A list of messages that maintains the conversation history.
        self_model (str): The model used for generating responses.
    """

    def __init__(self, system_message="You are a helpful assistant."):
        self.system_message = system_message
        self.history = [{"role": "system", "content": self.system_message}]
        self.self_model = "llama3.2"

    def set_system_message(self, message: str):
        self.system_message = message
        self.history = [{"role": "system", "content": self.system_message}] + [
            msg for msg in self.history if msg["role"] != "system"
        ]

    def send_message(self, message: str, history: list = None):
        self.append_message(message)
        response: ChatResponse = chat(
            model=self.self_model,
            messages=self.history,
            stream=True,
        )
        output = ""
        for chunk in response:
            output += chunk.message.content
            yield output

        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": output})

        if len(self.history) > 11:
            self.history = [self.history[0]] + self.history[-10:]
    
    def clear_history(self):
        self.history = [{"role": "system", "content": self.system_message}]
        return "History cleared."

    def append_message(self, message: str):
        self.history.append({"role": "user", "content": message})

    def get_history(self):
        return self.history

# Initialize the chat manager
chat_manager = ChatManager(system_message=context)
app = gr.ChatInterface(
    title="Eprice Chat",
    description="Open source language model.",
    fn=chat_manager.send_message,
    type="messages",
    autoscroll=True,
)
app.launch(pwa=True, share=False)