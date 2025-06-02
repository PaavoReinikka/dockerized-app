
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    file TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT documents_unique_file_type UNIQUE (file, type)
);