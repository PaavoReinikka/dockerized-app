import gradio as gr
from ollama import chat, ChatResponse
#from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()

'''
Form of ollama response (key, value pairs):
('model', 'llama3.2')
('created_at', '2025-04-09T11:00:25.809762663Z')
('done', True)
('done_reason', 'stop')
('total_duration', 6226280507)
('load_duration', 1044162763)
('prompt_eval_count', 32)
('prompt_eval_duration', 437000000)
('eval_count', 89)
('eval_duration', 4743000000)
('message', Message(role='assistant', content="I'm doing well, ...", images=None, tool_calls=None))
'''

class ChatManager:
    def __init__(self):
        self.history = []
        self.self_model = "llama3.2"

    def send_message(self, message: str) -> str:
        # append the message to the history and send it to the model
        # TODO: check history length and truncate if necessary
        # TODO: history condensation
        self.append_message(message)
        response: ChatResponse = chat(
            model=self.self_model,
            messages=self.history,
            stream=False,
        )
        
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": response.message.content})
        return response.message.content
    
    def clear_history(self):
        # Clear the history of messages
        self.history = []
        return "History cleared."
    
    def append_message(self, message: str):
        # Append a message to the history
        self.history.append({"role": "user", "content": message})
        

    def get_history(self):
        # Return the history of messages
        return self.history
    
'''    
# Initialize the chat manager
chat_manager = ChatManager()
demo = gr.Interface(
    fn=chat_manager.send_message,
    # define the inputs: a text box and a slider for number of tokens [10, 100],
    # and a slider for temperature [0.0, 1.0]
    inputs=[
        gr.Textbox(label="Input Text", placeholder="Enter your text here..."),
    ],
    # define the output: a text box that shows the history of messages
    outputs=gr.Textbox(label="Response", placeholder="Response will appear here..."),

    # set the title and description of the app
    title="LLM Chatbot",
    description="A simple chatbot using Ollama's LLM.",
    # set the theme of the app
    theme="default",
)

demo.launch(share=True)
'''

# this is the simplest way get a chatbot running
dboard=gr.load_chat("http://localhost:11434/v1/", 
             model="llama3.2")
dboard.launch(pwa=True)