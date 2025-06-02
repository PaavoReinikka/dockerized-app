import json
from typing import Dict, List

def filter_files_by_extension(file_dict: Dict[str, str], extensions=('.md', '.txt', '.wsd')) -> Dict[str, str]:
    """
    Filter a dictionary of files to only include those with specified extensions.
    """
    return {k: v for k, v in file_dict.items() if k.endswith(extensions)}

def format_all_docs_json(file_dict: Dict[str, str]) -> List[dict]:
    """
    Format all files as 'complete_file' documents.
    """
    return [
        {"type": "complete_file", "name": k, "content": v}
        for k, v in file_dict.items()
    ]

def format_documents_json(file_dict: Dict[str, str]) -> List[dict]:
    """
    Format filtered files as 'document' or 'markdown document' for further processing.
    """
    docs = []
    for file_path, content in file_dict.items():
        doc_type = "markdown document" if file_path.endswith(".md") else "document"
        docs.append({
            "file": file_path,
            "type": doc_type,
            "content": content
        })
    return docs

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)