import gradio as gr
from plantuml import PlantUML
import os
import atexit

class GradioPlantUMLInterface:
    def __init__(self):
        self.plantuml = PlantUML()

    def generate_diagram(self, uml_code):
        self.plantuml.processes_file("diagram.puml", uml_code)
        return "diagram.png"

    def reload_image(self):
        # Just return the current image path if it exists
        return "diagram.png" if os.path.exists("diagram.png") else None

    def create_interface(self):
        default_image = "diagram.png" if os.path.exists("diagram.png") else None
        with gr.Blocks() as demo:
            with gr.Row():
                uml_code = gr.Textbox(label="UML Code")
                generate_button = gr.Button("Generate Diagram")
                refresh_button = gr.Button("Refresh Image")
            diagram = gr.Image(label="Diagram", interactive=True, value=default_image)

            generate_button.click(
                fn=self.generate_diagram,
                inputs=uml_code,
                outputs=diagram
            )
            refresh_button.click(
                fn=self.reload_image,
                inputs=None,
                outputs=diagram
            )

        return demo

if __name__ == "__main__":
    atexit.register(lambda: os.remove("diagram.puml") if os.path.exists("diagram.puml") else None)
    atexit.register(lambda: os.remove("diagram.png") if os.path.exists("diagram.png") else None)
    interface = GradioPlantUMLInterface()
    demo = interface.create_interface()
    demo.launch()