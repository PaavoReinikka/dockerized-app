import gradio as gr
import os
from utils.db_calls import get_all_files

# Load files and prepare lookup
all_files = get_all_files()
file_names = [file["name"] for file in all_files]
file_dict = {file["name"]: file["content"] for file in all_files}

def detect_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".py", ".js", ".json", ".html", ".css", ".sh", ".java", ".c", ".cpp", ".ts"]:
        return "code"
    elif ext in [".md", ".markdown"]:
        return "markdown"
    else:
        return "text"

def read_file(file_path):
    content = file_dict.get(file_path, "File not found.")
    file_type = detect_type(file_path)
    return content, file_type

with gr.Blocks(fill_height=True) as app:
    with gr.Row():
        with gr.Column():
            file_dropdown = gr.Dropdown(choices=file_names, label="Select a file")
            code_view = gr.Code(label="File Content", visible=False)
            md_view = gr.Markdown(label="File Content", visible=False)
            text_view = gr.Textbox(label="File Content", lines=35, interactive=True, visible=False)

            def update_view(file_path):
                content, file_type = read_file(file_path)
                # Hide all, show one
                return (
                    gr.update(visible=file_type == "code", value=content if file_type == "code" else None),
                    gr.update(visible=file_type == "markdown", value=content if file_type == "markdown" else None),
                    gr.update(visible=file_type == "text", value=content if file_type == "text" else None),
                )

            file_dropdown.change(
                update_view,
                inputs=file_dropdown,
                outputs=[code_view, md_view, text_view]
            )

if __name__ == "__main__":
    app.launch()