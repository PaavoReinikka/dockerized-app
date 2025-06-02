
CREATE TABLE code (
    id SERIAL PRIMARY KEY,
    file TEXT NOT NULL,
    type TEXT NOT NULL, -- 'function', 'class', 'document', etc.
    name TEXT,
    docstring TEXT,
    start_line INTEGER,
    code TEXT,
    embedding VECTOR(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);