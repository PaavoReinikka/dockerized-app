import gradio as gr
import os
import subprocess

last_mtime = None

def check_and_generate_diagram():
    global last_mtime
    if os.path.exists("diagram.puml"):
        mtime = os.path.getmtime("diagram.puml")
        if last_mtime != mtime:
            with open("diagram.puml", "r") as f:
                code = f.read()
            if not code.strip().startswith("@startuml"):
                code = f"@startuml\n{code}\n@enduml\n"
                with open("diagram.puml", "w") as f2:
                    f2.write(code)
            jar_path = os.path.expanduser("~/plantuml.jar")
            subprocess.run(["java", "-jar", jar_path, "-tpng", "diagram.puml"])
            last_mtime = mtime
    if os.path.exists("diagram.png"):
        return "diagram.png"
    return None

def uml_viewer():
    with gr.Blocks() as uml:
        gr.Markdown("# UML Diagram Viewer")
        output_image = gr.Image(label="Generated Diagram", interactive=False)
        timer = gr.Timer(2)
        timer.tick(check_and_generate_diagram, outputs=output_image)
        refresh_button = gr.Button("Refresh")
        refresh_button.click(check_and_generate_diagram, outputs=output_image)
        uml.load(check_and_generate_diagram, outputs=output_image)
    return uml