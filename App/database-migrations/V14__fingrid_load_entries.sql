-- Create a temporary table for staging the data
CREATE TEMP TABLE fingrid_staging (
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

-- Load data into the temporary table
COPY fingrid_staging (datetime_orig, datetime, date, year, month, day, hour, weekday, dataset_id, value)
FROM '/data/fingrid_hourly.csv' 
DELIMITER ';' CSV HEADER;


INSERT INTO fingrid (datetime_orig, datetime, date, year, month, day, hour, weekday, dataset_id, value)
SELECT datetime_orig, datetime, date, year, month, day, hour, weekday, dataset_id, value
FROM fingrid_staging
ON CONFLICT (datetime, dataset_id) DO NOTHING;

DROP TABLE fingrid_staging;
