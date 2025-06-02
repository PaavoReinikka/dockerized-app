import gradio as gr
import os
import subprocess

# Store the last modification time in a global variable
last_mtime = None

def check_and_generate_diagram():
    global last_mtime
    if os.path.exists("diagram.puml"):
        mtime = os.path.getmtime("diagram.puml")
        if last_mtime != mtime:
            with open("diagram.puml", "r") as f:
                code = f.read()
            # Ensure @startuml/@enduml
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

with gr.Blocks() as app:
    gr.Markdown("# UML Diagram Viewer")
    output_image = gr.Image(label="Generated Diagram", interactive=False)
    
    timer = gr.Timer(2)
    # Timer tick: check and update image
    timer.tick(check_and_generate_diagram, outputs=output_image)
    # Manual refresh button
    #refresh_button = gr.Button("Refresh")
    #refresh_button.click(check_and_generate_diagram, outputs=output_image)
    # Show image on app load
    app.load(check_and_generate_diagram, outputs=output_image)

app.launch()