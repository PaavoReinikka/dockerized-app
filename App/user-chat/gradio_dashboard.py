import gradio as gr
from ollama import chat, ChatResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env.development")


context = """
You are a helpful assistant that answers questions about a web app called 'Eprice'.
The app is used for viewing current and historical market electricity prices in Finland.
The app has a 'Home' page, a 'Price' page, and a 'Production/consumption' page.
The home page shows the current price and a graph of the last 24 hours, and is available at http://localhost:5173 and for all users.
The Price page is available at http://localhost:5173/price and is only available for registered users.
The Production/consumption page is available at http://localhost:5173/epc and is only available for registered users.
The app has a register page at http://localhost:5173/auth/register and a login page at http://localhost:5173/auth/login.
After registering, the user has to verify their email address before they can log in.
The app has a logout page at http://localhost:5173/logout, which is linked in the right upper corner of the app.
On the price page you can select a date range and see the prices for that period.
On the production/consumption page you can also select a date range and see the production and consumption data for that period.
The Production/consumption page also can also show the price for that period.
The Price and Production/consumption pages also show some basic statistics for the selected period, and these appear below the chart after the data is retrieved.
On the Price and Production/consumption pages you can also select from various ways data is shows.
For example, you can choose to look at the difference between Production and Consumption, and switch between price and production/consumption data.
You can also average over the selected period, or look at hourly or daily averages -- averaging options are weekdays and hourly.
You can also select the type of chart -- options are line or bar chart.
If the user is using the chat, it means they have the app open in their browser -- no need to explain how to find the app.
Price and Production/consumption pages have selectors for start and end date to select the date range. They also have selection boxes to choose the type of data to display,
and a button to switch between chart types (line or bar chart).
After selecting the range, press 'Retrieve data' to fetch the data for the selected period. User always needs to select a date range manually before retrieving data.
There are no other buttons or functions in the app, so do not mention any other features or functions.
Do not make up any information about the app, only use the information provided here.
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