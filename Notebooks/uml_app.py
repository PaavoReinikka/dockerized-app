import gradio as gr
from plantuml import PlantUML
import os
import atexit

puml = PlantUML()

def generate_diagram(code):
    puml.processes_file("diagram.puml", code)
    return "diagram.png"  # Return the file path, not bytes

iface = gr.Interface(
    fn=generate_diagram, 
    inputs="text", 
    outputs="image", 
    title="Draw UML Diagrams using PlantUML",
    description="Enter your PlantUML code to generate a UML diagram.",
    theme="default",
)

atexit.register(lambda: os.remove("diagram.puml"))
atexit.register(lambda: os.remove("diagram.png"))
iface.launch()
# on exit, remove the generated file
