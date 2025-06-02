# this script populates the porssisahko table in the database
# NOTE: environment variables are loaded by docker compose

# whatever dependencies you need, add them
# to Dockerfile or create a requirements.txt file
import psycopg2 # pip install psycopg2-binary
import pandas as pd
import sys


def populate_db(df):

    conn = psycopg2.connect() # env is already loaded by docker compose
    cursor = conn.cursor()

    # Juho, Markus:
    # the table creation is handled by migrations (let's not do it in scripts)

    # Insert data into the table (on conflict do nothing)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO porssisahko (datetime, date, year, month, day, hour, weekday, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (Datetime) DO NOTHING
        """, (row['datetime'], row['date'], row['year'], row['month'], row['day'], row['hour'], row['weekday'], row['price']))
    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Data populated successfully.")
    print(f"Inserted {len(df)} rows into the database.")

if __name__ == "__main__":
    # csv file has been cleaned and is in the correct format
    filename = sys.argv[1]
    df = pd.read_csv(filename, sep=";", encoding="utf-8")
    # Populate the database
    populate_db(df)
    