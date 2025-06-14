-- Migration script to create the fingrid table
CREATE TABLE IF NOT EXISTS fingrid (
    id SERIAL PRIMARY KEY,
    datetime_orig TEXT NOT NULL, -- Original column for original datetime in text format
    datetime TIMESTAMP NOT NULL, -- Original column for datetime
    date DATE NOT NULL, -- New column for the date
    year INT NOT NULL, -- Year, etc. for statistics
    month INT NOT NULL,
    day INT NOT NULL,
    hour INT NOT NULL,
    weekday INT NOT NULL,
    dataset_id INT NOT NULL DEFAULT 0,
    value NUMERIC(10, 3) NOT NULL,
    predicted BOOLEAN NOT NULL DEFAULT FALSE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add a unique constraint to prevent duplicate rows (date and time)
ALTER TABLE fingrid
    ADD CONSTRAINT unique_datetime_fg UNIQUE (datetime, dataset_id);