"""some helper functions for document processing"""
import subprocess

# count tokens in the results
def count_tokens(text, tokenizer):
    tokens = tokenizer.encode(text)
    return len(tokens)

def count_all_tokens(texts, tokenizer):
    total_tokens = 0
    for text in texts:
        tokens = tokenizer.encode(text)
        total_tokens += len(tokens)
    return total_tokens

def join_metadata(metadata):
    key, value = list(metadata.items())[0]
    return f"{key}: {value}"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    assert result.returncode == 0, f"Command '{command}' failed with error: {result.stderr}"

def format_document(doc):
    # Join all metadata key-value pairs as "key: value"
    meta_str = "\n".join(f"{k}: {v}" for k, v in doc.metadata.items())
    # Combine metadata and content for the prompt
    return f"{meta_str}\n{doc.page_content}"
def format_documents(docs):
    return "\n\n".join(format_document(doc) for doc in docs)

def format_code_entry(entry):
    meta = [
        f"file: {entry.get('file', '')}",
        f"type: {entry.get('type', '')}",
        f"name: {entry.get('name', '')}",
        f"start_line: {entry.get('start_line', '')}"
    ]
    docstring = entry.get('docstring', '')
    code = entry.get('code', '')
    meta_str = ", ".join(meta)
    docstring_str = f"\nDocstring:\n{docstring}" if docstring else ""
    return f"{meta_str}\n{docstring_str}\ncontent:\n{code}"
