CREATE TABLE IF NOT EXISTS porssisahko (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL, -- Original column for datetime
    date DATE NOT NULL, -- New column for the date
    year INT NOT NULL, -- Year, etc. for statistics
    month INT NOT NULL,
    day INT NOT NULL,
    hour INT NOT NULL,
    weekday INT NOT NULL,
    price NUMERIC(10, 3) NOT NULL,
    predicted BOOLEAN NOT NULL DEFAULT FALSE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add a unique constraint to prevent duplicate rows (date and time)
ALTER TABLE porssisahko
    ADD CONSTRAINT unique_datetime UNIQUE (datetime);
