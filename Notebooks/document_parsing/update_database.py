from parse_code import *
from parse_files import *
from parse_contents import *
import psycopg
import dotenv

import json
import os
from helpers import *

from transformers import AutoModel, AutoTokenizer

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector

import numpy as np
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
# Load environment variables from .env file
dotenv.load_dotenv("../.env.private")


#########################################################
# Drop or truncate existing tables
truncate_table("documents")
truncate_table("files")
truncate_table("code")

try:
    drop_table("langchain_pg_collection", cascade=True)
    drop_table("langchain_pg_embedding")
except Exception as e:
    print(f"Error dropping tables: {e}")

#########################################################
# Load the model
model_name = "BAAI/bge-small-en" # "BAAI/bge-large-en-v1.5"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
# Create the embeddings object
embedding_model = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
# define text splitters
headers_to_split_on = [
    ("#", "Heading 1"),
    ("##", "Sub heading"),
    ("###", "Sub-sub heading"),
]

# Initialize the Markdown splitter
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer,
    chunk_size=512,
    chunk_overlap=50,
)

# Initialize the PostgreSQL connection
connection_string = "postgresql+psycopg://username:password@localhost:5432/database"
collection_name = "project_documents"
vector_store = PGVector(
    embeddings=embedding_model,
    collection_name=collection_name,
    connection=connection_string,
)

#########################################################

with open("../data/project_files.txt", "r") as f:
    file_dict = json.load(f)
    all_docs = file_dict.copy()

for key in list(file_dict.keys()):
    if not key.endswith(('.md', '.txt', '.wsd')):
        del file_dict[key]

all_docs_json = []
for key, value in all_docs.items():
    all_docs_json.append({
        "type": "complete_file",
        "name": key,
        "content": value
    })

documents_json = []
for file_path, content in file_dict.items():
    doc_type = "markdown document" if file_path.endswith(".md") else "document"
    documents_json.append({
        "file": file_path,
        "type": doc_type,
        "content": content
    })

documents_dicts = []
markdown_documents_dicts = []
for doc in documents_json:
    if doc["type"] == "document":
        documents_dicts.append(doc)
    elif doc["type"] == "markdown document":
        markdown_documents_dicts.append(doc)
    else:
        raise ValueError(f"Unknown document type: {doc['type']}")
    
with open('../data/backend_code.txt', 'r', encoding='utf-8') as f:
    code_data = json.load(f)



# Store all documents in the database
all_documents = documents_dicts + markdown_documents_dicts
save_documents_to_db(all_documents, embedding_model)
save_code_to_db(code_data, embedding_model)
save_files_to_db(all_docs_json)

# chunk and embed the documents
all_documents = documents_dicts + markdown_documents_dicts
data = []
for doc in all_documents:
    if doc["type"] == "document":
        chunks = text_splitter.split_text(doc["content"])
        for chunk in chunks:
            embedding = embedding_model.embed_query(chunk)
            data.append({
                "file": doc["file"],
                "type": doc["type"],
                "content": chunk,
                "metadata": None,
                "embedding": embedding
            })
    elif doc["type"] == "markdown document":
        chunks = markdown_splitter.split_text(doc["content"])
        for chunk in chunks:
            subchunks = text_splitter.split_text(chunk.page_content)
            for subchunk in subchunks:
                embedding = embedding_model.embed_query(subchunk)
                data.append({
                    "file": doc["file"],
                    "type": doc["type"],
                    "content": subchunk,
                    "metadata": join_metadata(chunk.metadata),
                    "embedding": embedding_model.embed_query(subchunk)
                })

# Convert to Documents
documents = []
embeddings_list = []
for item in data:
    doc = Document(
        page_content=item['content'],
        metadata={
            'file': item['file'],
            'type': item['type'],
            'heading': item['metadata'],
        }
    )
    documents.append(doc)


# Chunk and embed code files, matching doc structure
code_chunks = []
for entry in code_data:
    # Combine docstring and code for context, or just use code
    docstring = entry.get("docstring", "")
    code_text = entry.get("code", "")
    full_text = f"{docstring}\n{code_text}" if docstring else code_text

    # Chunk the code
    chunks = text_splitter.split_text(full_text)
    for chunk in chunks:
        # Prepare metadata: include all keys except file, type, code, docstring, and start_line
        metadata = {k: v for k, v in entry.items() if k not in ["file", "type", "code", "docstring", "start_line"]}
        doc = Document(
            page_content=chunk,
            metadata={
                "file": entry.get("file", ""),
                "type": entry.get("type", ""),
                "metadata": metadata if metadata else None
            }
        )
        embedding = embedding_model.embed_query(chunk)
        code_chunks.append((doc, embedding))


code_documents = [doc for doc, _ in code_chunks]
# combine code and other documents
documents.extend(code_documents)

# add documents to the vector store
vector_store.add_documents(documents=documents)