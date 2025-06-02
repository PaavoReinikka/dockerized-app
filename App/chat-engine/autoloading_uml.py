"""
Gradio component for viewing and refreshing a PlantUML diagram.
This component checks for changes in the PlantUML file and regenerates the diagram if necessary.
"""

import gradio as gr
import os
import subprocess

# This is to keep track of the last modification time of the PlantUML file
last_mtime = None

def get_diagram_paths():
    # Always resolve relative to this script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    diagrams_dir = os.path.join(base_dir, "diagrams")
    puml_path = os.path.join(diagrams_dir, "diagram.puml")
    png_path = os.path.join(diagrams_dir, "diagram.png")
    return puml_path, png_path


def check_and_generate_diagram():
    global last_mtime
    puml_path, png_path = get_diagram_paths()
    if os.path.exists(puml_path):
        mtime = os.path.getmtime(puml_path)
        if last_mtime != mtime:
            with open(puml_path, "r") as f:
                code = f.read()
            if not code.strip().startswith("@startuml"):
                code = f"@startuml\n{code}\n@enduml\n"
                with open(puml_path, "w") as f2:
                    f2.write(code)
            jar_path = os.path.expanduser("~/plantuml.jar")
            subprocess.run(["java", "-jar", jar_path, "-tpng", puml_path], cwd=os.path.dirname(puml_path))
            last_mtime = mtime
    if os.path.exists(png_path):
        return png_path
    return None

def uml_viewer():
    with gr.Blocks() as uml:
        output_image = gr.Image(label="Generated Diagram", interactive=False)
        timer = gr.Timer(2)
        timer.tick(check_and_generate_diagram, outputs=output_image)
        refresh_button = gr.Button("Refresh")
        refresh_button.click(check_and_generate_diagram, outputs=output_image)
        uml.load(check_and_generate_diagram, outputs=output_image)
    return uml