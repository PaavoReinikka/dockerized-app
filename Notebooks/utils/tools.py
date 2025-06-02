"""Tools for interacting with the database to retrieve file information."""

from .db_calls import (
    get_file_by_name,
)
import os
import subprocess
from langchain.tools import tool


@tool
def get_file_by_name_tool(file_name: str) -> str:
    """
    Retrieve a single document entry from the database by file name.
    
    Args:
        file_name (str): The name of the file to search for.
    
    Returns:
        str: The document entry with metadata and content, or a message if not found.
    """
    # check if the filename doesn't start with ./
    # if it does not, add it
    if not file_name.startswith("./"):
        file_name = "./" + file_name
    result = get_file_by_name(file_name)
    if not result:
        return f"No file found with name: {file_name}"
    # Format result for LLM output
    return f"File: {result['name']}\nType: {result['type']}\nContent:\n{result['content']}"

@tool
def generate_plantuml_diagram_tool(plantuml_code: str) -> str:
    """
    Generates a UML diagram from PlantUML code and saves it as ./diagrams/diagram.png.
    Returns a message indicating the diagram was created.
    """
    os.makedirs("./diagrams", exist_ok=True)
    puml_path = "./diagrams/diagram.puml"
    png_path = "./diagrams/diagram.png"
    # Ensure code is wrapped with @startuml/@enduml
    code = plantuml_code.strip()
    if not code.startswith("@startuml"):
        code = f"@startuml\n{code}\n@enduml"
    with open(puml_path, "w") as f:
        f.write(code)
    jar_path = os.path.expanduser("~/plantuml.jar")
    subprocess.run(["java", "-jar", jar_path, "-tpng", puml_path, "-o", "."], cwd="./diagrams")
    if os.path.exists(png_path):
        return "A new UML diagram has been generated and saved to ./diagrams/diagram.png."
    else:
        return "Failed to generate the UML diagram."