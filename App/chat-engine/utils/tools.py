"""Tools for interacting with the database to retrieve file information."""

from .db_calls import (
    get_file_by_name,
)
import os
import subprocess
from langchain.tools import tool

@tool
def get_project_directory_structure_tool() -> str:
    """
    Returns the project directory structure as a string.
    The structure shows what files and directories are available in the project.
    The input argument is ignored.
    
    Returns:
        str: The directory structure as a formatted string.
    """
    # Get the project directory
    fname = "./data/project_structure.txt"
    # Run the command to get the directory structure
    with open(fname, "r") as f:
        lines = f.readlines()
    # Format the output
    output = """
    Project Directory Structure:
    """
    for line in lines:
        output += f"{line.strip()}\n"
    return output
    

@tool
def get_file_by_name_tool(file_name: str) -> str:
    """
    Retrieve a single document entry from the database by file name. Preferably use the full path.
    If multiple files have the same name, list all matches and ask for the full path.

    Args:
        file_name (str): The name of the file to retrieve. Should start with './' for relative paths.
    Returns:
        str: A formatted string with the file name, type, and content if found.
             If multiple files match, lists all matches and asks for the full path.
             If no file is found, returns a message indicating that.
    """
    from .db_calls import get_file_by_name, get_all_files

    # Try direct match (full path)
    result = get_file_by_name(file_name)
    if result:
        return f"File: {result['name']}\nType: {result['type']}\nContent:\n{result['content']}"

    # If not found, try matching by filename only
    all_files = get_all_files()
    matches = [f for f in all_files if os.path.basename(f["name"]) == os.path.basename(file_name)]

    if not matches:
        return f"No file found with name: {file_name}"

    if len(matches) == 1:
        f = matches[0]
        return f"File: {f['name']}\nType: {f['type']}\nContent:\n{f['content']}"

    # Multiple matches
    match_list = "\n".join(f"- {f['name']}" for f in matches)
    return (
        f"Multiple files found with the name '{os.path.basename(file_name)}':\n"
        f"{match_list}\n"
        "Please specify the full file path."
    )


def _save_plantuml_code(code: str) -> str:
    diagrams_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")
    diagrams_dir = os.path.abspath(diagrams_dir)
    os.makedirs(diagrams_dir, exist_ok=True)
    diagram_path = os.path.join(diagrams_dir, "diagram.puml")
    with open(diagram_path, "w") as f:
        f.write(code)
    return diagram_path


@tool
def generate_plantuml_diagram_from_file_tool(file_name: str) -> str:
    """
    Loads PlantUML code from a file in the database and saves it to ./diagrams/diagram.puml for rendering.
    Returns a message indicating the diagram was generated.
    """
    # Ensure file_name starts with ./
    if not file_name.startswith("./"):
        file_name = "./" + file_name
    file_entry = get_file_by_name(file_name)
    if not file_entry or "content" not in file_entry:
        return f"No file found with name: {file_name}"
    code = file_entry["content"].strip()
    if not code.startswith("@startuml"):
        code = f"@startuml\n{code}\n@enduml"
    diagram_path = _save_plantuml_code(code)
    return f"The diagram should be rendered automatically -- refresh the image is it's not showing up."

@tool
def generate_plantuml_diagram_from_code_tool(plantuml_code: str) -> str:
    """
    Saves PlantUML code (provided as a string) to ./diagrams/diagram.puml for rendering.
    Returns a message indicating the file was saved.
    """
    code = plantuml_code.strip()
    if not code.startswith("@startuml"):
        code = f"@startuml\n{code}\n@enduml"
    diagram_path = _save_plantuml_code(code)
    return f"The diagram should be rendered automatically -- refresh the image is it's not showing up."