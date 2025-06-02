-- Create a temporary table for staging the data
CREATE TEMP TABLE porssisahko_staging (
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

-- Load data into the temporary table
COPY porssisahko_staging (datetime, date, year, month, day, hour, weekday, price)
FROM '/data/porssisahko.csv'
WITH CSV HEADER DELIMITER ';';

-- Insert unique rows into the target table
INSERT INTO porssisahko (datetime, date, year, month, day, hour, weekday, price)
SELECT datetime, date, year, month, day, hour, weekday, price
FROM porssisahko_staging
ON CONFLICT (datetime) DO NOTHING;

-- Drop the temporary table
DROP TABLE porssisahko_staging;
