"""
porssisahko_tools.py provides utility functions for working with price data and database readiness in the Eprice backend.

Features:
- Asynchronous function to wait for the PostgreSQL database to become available before starting the application.
- Conversion utility to transform price and ISO 8601 date data into a dictionary format suitable for the porssisahko table.

Intended Usage:
- Used by repository and service layers to ensure database readiness and to prepare data for insertion into the porssisahko table.
- Can be extended with additional utilities for price data processing as needed.

Dependencies:
- asyncpg for asynchronous PostgreSQL operations.
- Python standard library modules: datetime and time.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
import asyncpg
import time

async def wait_for_database(database_url):
    """
    Wait for the database to be ready by attempting to connect to it.

    Args:
        database_url: The URL of the database to connect to.

    Raises:
        Exception: If the database is not ready after multiple attempts.
        (logs attempts and failure)
    """
    max_retries = 10
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            conn = await asyncpg.connect(database_url)
            await conn.close()
            print("Database is ready.")
            return
        except Exception as e:
            print(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    raise Exception("Database is not ready after multiple attempts.")


def convert_to_porssisahko_entry(price, iso_date, predicted=False, convert_to_helsinki_time=True):
    """
    Converts a price and ISO 8601 date into a dictionary for the porssisahko table.

    Args:
        price (float): The price value.
        iso_date (str): The date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
        predicted (bool): Indicates if the price is predicted. Default is False.
    Returns:
        dict: A dictionary with keys: Datetime, Date, Year, Month, Day, Hour, Weekday, Price, Predicted.
    Raises:
        ValueError: If the ISO date is not in the correct format.
    """
    try:
        if convert_to_helsinki_time:
            # Parse the ISO date string to a UTC datetime
            dt_utc = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
            # Convert to Helsinki time
            dt_helsinki = dt_utc.astimezone(ZoneInfo("Europe/Helsinki"))
            dt_naive = dt_helsinki.replace(tzinfo=None)
        else:
            # Parse the ISO date string to a naive datetime (UTC)
            dt_naive = datetime.fromisoformat(iso_date.replace("Z", "+00:00")).replace(tzinfo=None)
        # Extract the weekday
        weekday = dt_naive.weekday()

        # Return the dictionary
        return {
            "datetime": dt_naive,  # Use offset-naive datetime
            "date": dt_naive.date(),  # Extract the date part
            "year": dt_naive.year,
            "month": dt_naive.month,
            "day": dt_naive.day,
            "hour": dt_naive.hour,
            "weekday": weekday,
            "price": price,
            "predicted": predicted
        }
    except ValueError as e:
        # Handle invalid date format or parsing errors
        raise ValueError(f"Invalid ISO date format: {iso_date}. Error: {e}")


