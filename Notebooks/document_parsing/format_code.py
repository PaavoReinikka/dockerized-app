import json
from typing import List, Dict, Any

def load_code_data(path: str) -> List[dict]:
    """Load code data from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_code_chunks(
    code_data: List[dict],
    text_splitter,
    embedding_model,
    doc_class=None
) -> List[dict]:
    """
    Chunk and embed code entries for storage or further processing.

    Args:
        code_data: List of code entries (dicts with keys like file, code, docstring, etc.)
        text_splitter: A text splitter instance (e.g., RecursiveCharacterTextSplitter)
        embedding_model: Embedding model with .embed_query(text)
        doc_class: Optional, a Document class to wrap chunks (e.g., langchain_core.documents.Document)

    Returns:
        List of dicts (or Documents) with chunked code, metadata, and embedding.
    """
    results = []
    for entry in code_data:
        docstring = entry.get("docstring", "")
        code_text = entry.get("code", "")
        full_text = f"{docstring}\n{code_text}" if docstring else code_text

        # Chunk the code
        chunks = text_splitter.split_text(full_text)
        for chunk in chunks:
            # Prepare metadata: include all keys except file, type, code, docstring, and start_line
            metadata = {k: v for k, v in entry.items() if k not in ["file", "type", "code", "docstring", "start_line"]}
            meta = {
                "file": entry.get("file", ""),
                "type": entry.get("type", ""),
                "metadata": metadata if metadata else None
            }
            embedding = embedding_model.embed_query(chunk)
            if doc_class:
                doc = doc_class(page_content=chunk, metadata=meta)
                results.append((doc, embedding))
            else:
                results.append({
                    "chunk": chunk,
                    "metadata": meta,
                    "embedding": embedding
                })
    return results

