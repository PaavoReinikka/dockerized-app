import asyncpg
from utils.fingrid_service_tools import convert_to_fingrid_entry
from datetime import datetime

class FingridRepository:
    """
    Repository class for Fingrid data operations.

    Provides asynchronous methods for inserting and retrieving Fingrid entries,
    as well as finding missing entries. Interacts directly with the PostgreSQL
    database using asyncpg.

    Args:
        database_url (str): The database connection URL.
    """
    def __init__(self, database_url: str):
        """
        Initialize the FingridRepository with a database connection URL.

        Args:
            database_url (str): The database connection URL.
        """
        self.database_url = database_url
    
    async def insert_entry(self, value: float, iso_date: str, predicted: bool = False, convert_to_helsinki_time: bool = True, dataset_id: int = 0):
        """
        Insert a single entry into the fingrid table.

        Args:
            value (float): The value to insert.
            iso_date (str): The datetime in ISO 8601 format (UTC).
            predicted (bool): Indicates if the value is predicted. Default is False.
            convert_to_helsinki_time (bool): Whether to convert datetime to Helsinki time. Default is True.
            dataset_id (int): The dataset ID. Default is 0.

        Raises:
            asyncpg.PostgresError: If a database error occurs.
        """
        conn = None
        try:
            # Convert the entry to the correct format
            entry = convert_to_fingrid_entry(value, iso_date, predicted, convert_to_helsinki_time, dataset_id)

            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

            # Insert the entry into the database
            await conn.execute(
                """
                INSERT INTO fingrid (datetime_orig,datetime,date,year,month,day,hour,weekday,dataset_id,value)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (datetime, dataset_id) DO NOTHING
                """,
                entry["datetime_orig"],  # datetime_orig in UTC time zone aware format
                entry["datetime"],       # datetime in Helsinki time (naive)
                entry["date"],
                entry["year"],
                entry["month"],
                entry["day"],
                entry["hour"],
                entry["weekday"],
                entry["dataset_id"],
                entry["value"]
            )
        except asyncpg.PostgresError as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                await conn.close()

    async def get_entries(self, start_date: datetime, end_date: datetime, dataset_id, select_columns: str = "*"):
        """
        Retrieve entries from the fingrid table between two datetimes for a specific dataset.

        Args:
            start_date (datetime): The start datetime (inclusive).
            end_date (datetime): The end datetime (inclusive).
            dataset_id (int): The dataset ID to filter by.
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
                FROM fingrid
                WHERE datetime BETWEEN $1 AND $2
                AND dataset_id = $3
                """,
                start_date,
                end_date,
                dataset_id
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
        Find missing hourly datetimes in the fingrid table between two datetimes.

        Args:
            start_date (datetime): The start datetime (inclusive).
            end_date (datetime): The end datetime (inclusive).

        Returns:
            list[tuple]: A list of tuples where each tuple contains the date (YYYY-MM-DD) and hour (0-23)
                         for each missing hour in the range.

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
                LEFT JOIN fingrid p ON dr.datetime = p.datetime
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