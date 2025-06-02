
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    CONSTRAINT file_unique_name UNIQUE (name)
);
