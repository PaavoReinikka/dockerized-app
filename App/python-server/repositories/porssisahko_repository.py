"""
porssisahko_repository.py defines the PorssisahkoRepository class for price data operations in the Eprice backend.

The repository provides asynchronous methods for:
- Inserting single or multiple price entries into the porssisahko table.
- Retrieving entries within a date range.
- Finding missing hourly entries within a date range.

All operations interact directly with a PostgreSQL database using asyncpg for asynchronous access.
This repository is intended to be used by service and controller layers to abstract database logic
from business and API logic.

Dependencies:
- asyncpg for asynchronous PostgreSQL operations.
- utils.porssisahko_tools for entry conversion utilities.

Intended Usage:
- Instantiate with a database connection URL.
- Use in services or controllers for all price data-related database actions.
"""

import asyncpg
from utils.porssisahko_tools import convert_to_porssisahko_entry
from datetime import datetime

class PorssisahkoRepository:
    """
    Repository class for price data operations in the Eprice backend.

    Provides asynchronous methods for inserting and retrieving price entries,
    as well as finding missing entries. Interacts directly with the PostgreSQL
    database using asyncpg.

    Args:
        database_url (str): The database connection URL.
    """
    def __init__(self, database_url: str):
        """
        Initialize the PorssisahkoRepository with a database connection URL.

        Args:
            database_url (str): The database connection URL.
        """
        self.database_url = database_url

    async def insert_entry(self, price: float, iso_date: str, predicted: bool = False, convert_to_helsinki_time: bool = True):
        """
        Insert a single entry into the porssisahko table.

        Args:
            price (float): The price value.
            iso_date (str): The date in ISO 8601 format.
            predicted (bool): Indicates if the price is predicted. Default is False.

        Raises:
            asyncpg.PostgresError: If a database error occurs.
        """
        conn = None
        try:
            # Convert the entry to the correct format
            entry = convert_to_porssisahko_entry(price, iso_date, predicted, convert_to_helsinki_time)

            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

            # Insert the entry into the database
            await conn.execute(
                """
                INSERT INTO porssisahko (datetime, date, year, month, day, hour, weekday, price)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (Datetime) DO NOTHING
                """,
                entry["datetime"],
                entry["date"],
                entry["year"],
                entry["month"],
                entry["day"],
                entry["hour"],
                entry["weekday"],
                entry["price"]
            )
        except asyncpg.PostgresError as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                await conn.close()

    async def insert_entries(self, entries: list, convert_to_helsinki_time: bool = True):
        """
        Insert multiple entries into the porssisahko table.

        Args:
            entries (list[dict]): A list of dictionaries containing the data to insert.

        Raises:
            asyncpg.PostgresError: If a database error occurs.
        """
        conn = None
        try:
            # Convert entries to the correct format
            formatted_entries = [
                convert_to_porssisahko_entry(entry["price"], entry["startDate"], predicted=entry.get("predicted", False), convert_to_helsinki_time=convert_to_helsinki_time)
                for entry in entries
            ]

            # Prepare the insert query
            insert_query = """
                INSERT INTO porssisahko (datetime, date, year, month, day, hour, weekday, price)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (Datetime) DO NOTHING
            """
            # Create a list of tuples for the entries
            values = [
                (
                    entry["datetime"],
                    entry["date"],
                    entry["year"],
                    entry["month"],
                    entry["day"],
                    entry["hour"],
                    entry["weekday"],
                    entry["price"]
                )
                for entry in formatted_entries
            ]

            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

            # Execute the insert query with the list of values
            await conn.executemany(insert_query, values)
        except asyncpg.PostgresError as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                await conn.close()

    async def get_entries(self, start_date: datetime, end_date: datetime, select_columns: str = "*"):
        """
        Retrieve entries from the porssisahko table between two dates.

        Args:
            start_date (datetime): The start date as a datetime object.
            end_date (datetime): The end date as a datetime object.
            select_columns (str): The columns to select from the table. Default is "*".

        Returns:
            list[dict]: A list of dictionaries containing the data for each entry.

        Raises:
            asyncpg.PostgresError: If a database error occurs.
        """
        conn = None
        try:
            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

            # Execute the query
            rows = await conn.fetch(
                f"""
                SELECT {select_columns}
                FROM porssisahko
                WHERE datetime BETWEEN $1 AND $2
                """,
                start_date,
                end_date
            )

            # Convert rows to a list of dictionaries
            return [dict(row) for row in rows]
        except asyncpg.PostgresError as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                await conn.close()

    async def get_missing_entries(self, start_date: datetime, end_date: datetime):
        """
        Retrieve missing hourly entries from the porssisahko table between two dates.

        Args:
            start_date (datetime): The start date as a datetime object.
            end_date (datetime): The end date as a datetime object.

        Returns:
            list[tuple]: A list of tuples where each tuple contains the date (YYYY-MM-DD) and hour (0-23).

        Raises:
            asyncpg.PostgresError: If a database error occurs.
        """
        conn = None
        try:
            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

            # Execute the query to find missing entries
            rows = await conn.fetch(
                """
                WITH date_range AS (
                    SELECT generate_series(
                        $1::TIMESTAMP,
                        $2::TIMESTAMP,
                        '1 hour'::INTERVAL
                    ) AS datetime
                )
                SELECT dr.datetime
                FROM date_range dr
                LEFT JOIN porssisahko p ON dr.datetime = p.datetime
                WHERE p.datetime IS NULL
                """,
                start_date,
                end_date
            )

            # Return the missing entries as a list of tuples
            return [
                (row["datetime"].strftime("%Y-%m-%d"), row["datetime"].hour)
                for row in rows
            ]
        except asyncpg.PostgresError as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                await conn.close()