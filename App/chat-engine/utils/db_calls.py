"""
    Helper functions for managing database operations related to code and documents.
    This module provides functions to save, load, and retrieve code and document entries,
    including their embeddings, from a PostgreSQL database using the pgvector extension.
    Functions assume that the database schema is already set up with appropriate tables.
"""
import os
import psycopg
import numpy as np


def save_code_to_db(code_data, embedding_model):
    # Connect to the database
    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    # Table should already exist
    # Insert code data into the table
    for entry in code_data:
        embdedding = embedding_model.embed_query(entry["docstring"])
        cur.execute("""
            INSERT INTO code (file, type, name, docstring, start_line, code, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (file, type, name, start_line) DO NOTHING
        """, (
            entry["file"],
            entry["type"],
            entry["name"],
            entry["docstring"],
            entry["start_line"],
            entry["code"],
            embdedding
        ))
    
    conn.commit()
    cur.close()
    conn.close()

def load_code_from_db():
    # Connect to the database
    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    # Fetch all code data from the table
    cur.execute("SELECT file, type, name, docstring, start_line, code FROM code")
    rows = cur.fetchall()

    # Convert rows to a list of dictionaries
    code_data = []
    for row in rows:
        code_data.append({
            "file": row[0],
            "type": row[1],
            "name": row[2],
            "docstring": row[3],
            "start_line": row[4],
            "code": row[5]
        })

    cur.close()
    conn.close()
    
    return code_data


def get_most_similar_code_from_db(embedding_model, query, n=5):
    import psycopg
    import os

    # Embed the query
    query_embedding = embedding_model.embed_query(query)
    # Ensure it's a list of floats (pgvector expects this format)
    query_embedding = list(map(float, np.array(query_embedding).flatten()))

    # Connect to the database
    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    # Use the <-> operator for L2 distance (or use <#> for cosine distance if pgvector >= 0.5.0)
    cur.execute("""
        SELECT file, type, name, docstring, start_line, code, embedding
        FROM code
        ORDER BY embedding <-> %s
        LIMIT %s
    """, (query_embedding, n))

    rows = cur.fetchall()
    code_data = []
    for row in rows:
        code_data.append({
            "file": row[0],
            "type": row[1],
            "name": row[2],
            "docstring": row[3],
            "start_line": row[4],
            "code": row[5],
            "embedding": row[6]
        })

    cur.close()
    conn.close()
    return code_data

def retrieve_similar_code(query_embedding, n=5):
    """
    Retrieve the n most similar code entries from the database using an embedded query vector.

    Args:
        query_embedding (list or np.ndarray): The query embedding vector.
        n (int): Number of results to return.

    Returns:
        List[dict]: List of code entries with metadata and code.
    """
    # Ensure embedding is a flat list of floats
    if not isinstance(query_embedding, list):
        import numpy as np
        query_embedding = list(map(float, np.array(query_embedding).flatten()))

    # Connect to the database
    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    # Perform similarity search using pgvector
    cur.execute("""
        SELECT file, type, name, docstring, start_line, code, embedding
        FROM code
        ORDER BY embedding <-> %s::vector
        LIMIT %s
    """, (query_embedding, n))

    rows = cur.fetchall()
    code_data = []
    for row in rows:
        code_data.append({
            "file": row[0],
            "type": row[1],
            "name": row[2],
            "docstring": row[3],
            "start_line": row[4],
            "code": row[5],
            "embedding": row[6]
        })

    cur.close()
    conn.close()
    return code_data

def get_code_by_file_name(file_name):
    """
    Retrieve code entries from the database by file name.

    Args:
        file_name (str): The name of the file to search for.

    Returns:
        List[dict]: List of code entries with metadata and code.
    """
    # Connect to the database
    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    # Perform the query
    cur.execute("""
        SELECT file, type, name, docstring, start_line, code
        FROM code
        WHERE file = %s
    """, (file_name,))

    rows = cur.fetchall()
    code_data = []
    for row in rows:
        code_data.append({
            "file": row[0],
            "type": row[1],
            "name": row[2],
            "docstring": row[3],
            "start_line": row[4],
            "code": row[5]
        })

    cur.close()
    conn.close()
    # if no rows are found, return an entry with empty values
    if not code_data:
        code_data.append({
            "file": file_name,
            "type": "",
            "name": "",
            "docstring": "not available",
            "start_line": 0,
            "code": "# not available"
        })
    return code_data

def save_documents_to_db(documents, embedding_model):
    """
    Save document chunks (with embeddings) to the documents table in the database.

    Args:
        documents (list): List of dicts with keys 'file', 'type', 'content', and optionally 'embedding'.
        embedding_model: Embedding model with an embed_query method.
    """
    import psycopg
    import os
    import numpy as np

    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    for doc in documents:
        # Compute embedding if not already present
        embedding = doc.get("embedding")
        if embedding is None:
            embedding = embedding_model.embed_query(doc["content"])
        # Ensure embedding is a flat list of floats
        embedding = list(map(float, np.array(embedding).flatten()))

        cur.execute("""
            INSERT INTO documents (file, type, content, embedding)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (file, type) DO NOTHING
        """, (
            doc["file"],
            doc["type"],
            doc["content"],
            embedding
        ))

    conn.commit()
    cur.close()
    conn.close()


def load_documents_from_db():
    """
    Retrieve all document entries from the documents table.

    Returns:
        list: List of dictionaries with document metadata and content.
    """
    import psycopg
    import os

    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT file, type, content, embedding
        FROM documents
    """)

    rows = cur.fetchall()
    documents = []
    for row in rows:
        documents.append({
            "file": row[0],
            "type": row[1],
            "content": row[2],
            "embedding": row[3] if row[3] is not None else None
        })

    cur.close()
    conn.close()
    
    return documents


def save_files_to_db(files):
    """
    Save all files to the documents table in the database (no embedding).
    Args:
        files (list): List of dicts with keys 'file', 'type', 'content'.
    """
    import psycopg
    import os

    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    for doc in files:
        cur.execute("""
            INSERT INTO files (name, type, content)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (
            doc["name"],
            doc["type"],
            doc["content"]
        ))

    conn.commit()
    cur.close()
    conn.close()

def get_file_by_name(file_name):
    """
    Retrieve a single document entry from the database by file name.

    Args:
        file_name (str): The name of the file to search for.

    Returns:
        dict or None: Document entry with metadata and content, or None if not found.
    """
    import psycopg
    import os

    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT name, type, content
        FROM files
        WHERE name = %s
        LIMIT 1
    """, (file_name,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "name": row[0],
            "type": row[1],
            "content": row[2]
        }
    else:
        return None

def get_all_files():
    """
    Retrieve all file entries from the database.

    Returns:
        list: List of dictionaries with file metadata and content.
    """
    import psycopg
    import os

    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT name, type, content
        FROM files
    """)

    rows = cur.fetchall()
    files = []
    for row in rows:
        files.append({
            "name": row[0],
            "type": row[1],
            "content": row[2]
        })

    cur.close()
    conn.close()
    
    return files

def truncate_table(table_name):
    """
    Truncate (remove all rows from) a table.
    Args:
        table_name (str): Name of the table to truncate.
    """
    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()
    cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
    conn.commit()
    cur.close()
    conn.close()

def drop_table(table_name, cascade=False):
    """
    Drop a table from the database.
    Args:
        table_name (str): Name of the table to drop.
        cascade (bool): Whether to use CASCADE option.
    """
    conn = psycopg.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()
    sql = f"DROP TABLE IF EXISTS {table_name} {'CASCADE' if cascade else ''};"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()