"""
porssisahko_scheduler.py defines scheduled tasks for fetching and inserting electricity price data into the Eprice backend database.

Features:
- Periodically fetches the latest price data from the Pörssisähkö API and inserts it into the database.
- Detects and fills missing hourly price entries by querying the API for specific dates and hours.
- Uses APScheduler to schedule tasks at specified intervals or times.
- Provides synchronous wrappers for running asynchronous tasks in a scheduler context.
- Handles API and database errors with logging for monitoring and debugging.

Dependencies:
- requests for HTTP requests to the external API.
- apscheduler for scheduling background tasks.
- repositories.porssisahko_repository for database operations.
- config.secrets for database configuration.
- asyncio for running async functions in a synchronous context.

Intended Usage:
- Used as part of the backend service to ensure the database is kept up-to-date with the latest and complete price data.
- Can be extended with additional scheduled tasks or triggers as needed.
"""

import asyncio
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
#from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from repositories.porssisahko_repository import PorssisahkoRepository
from config.secrets import DATABASE_URL

# Initialize the repository with the database URL
porssisahko_repository = PorssisahkoRepository(DATABASE_URL)

# The task to fetch data and insert it into the database
async def fetch_and_insert_porssisahko_data():
    """
    Fetch the latest price data from the Pörssisähkö API and insert it into the database.

    Raises:
        requests.RequestException: If there is an error fetching data from the API.
        Exception: For any unexpected errors during data insertion.
    """
    try:
        # Fetch data from the API
        response = requests.get("https://api.porssisahko.net/v1/latest-prices.json")
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()

        # Insert the data into the database using the repository
        await porssisahko_repository.insert_entries(data["prices"])

        print(f"Database successfully updated at {datetime.now()}")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def fetch_and_insert_missing_porssisahko_data(start_datetime_str: str):
    """
    Detect and insert missing hourly price entries into the database.

    Args:
        start_datetime_str (str): The ISO format string representing the start datetime.

    Raises:
        requests.RequestException: If there is an error fetching data from the API.
        Exception: For any unexpected errors during data insertion.
    """
    try:
        # Convert the start_datetime string to a datetime object (db likes ISO format)
        start_datetime = datetime.fromisoformat(start_datetime_str)
        
        # Calculate the end datetime (24 hours later)
        end_datetime = datetime.now() + timedelta(days=1)
        end_datetime = end_datetime.replace(minute=0, second=0, microsecond=0)
        
        # Retrieve missing entries from the repository
        missing_entries = await porssisahko_repository.get_missing_entries(
            start_datetime, end_datetime
        )

        if not missing_entries:
            print(f"No missing entries found between {start_datetime} and {end_datetime}.")
            return

        print(f"Found {len(missing_entries)} missing entries. Fetching data...")

        # Fetch data for the missing entries
        for date, hour in missing_entries:
            # Construct the API URL for the specific date and hour
            api_url = f"https://api.porssisahko.net/v1/price.json?date={date}&hour={hour}"
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()  # Parse the JSON response

            # NOTE: Since there is inconsistency in the API response format, we need to handle both cases:
            # latest prices (utc) and hourly prices (helsinki time)
            # Insert the data into the database -- datetime format:  "2022-11-14THH:00:00.000Z"
            await porssisahko_repository.insert_entry(data["price"], f"{date}T{(hour):02d}:00.000Z", convert_to_helsinki_time=False)

        print(f"Missing data successfully inserted into the database.")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# we need a wrapper to run the async task in a synchronous context
def fetch_and_insert_porssisahko_data_sync():
    """
    Synchronous wrapper to run fetch_and_insert_porssisahko_data in an event loop.
    """
    asyncio.run(fetch_and_insert_porssisahko_data())

def fetch_and_insert_missing_porssisahko_data_sync(start_datetime_str: str):
    """
    Synchronous wrapper to run fetch_and_insert_missing_porssisahko_data in an event loop.

    Args:
        start_datetime_str (str): The ISO format string representing the start datetime.
    """
    asyncio.run(fetch_and_insert_missing_porssisahko_data(start_datetime_str))


# Set up the scheduler
ps_scheduler = BackgroundScheduler()
# Trigger to run the task every day at 14:15
ps_trigger = CronTrigger(hour=14, minute=15)

# NOTE DEBUG: For debugging/testing purposes, you can use an interval trigger to run every 15 seconds or so
#ps_trigger = IntervalTrigger(seconds=10)

ps_scheduler.add_job(fetch_and_insert_porssisahko_data_sync, ps_trigger)
ps_scheduler.start()

# Ensure the scheduler shuts down properly on application exit
def shutdown_scheduler():
    """
    Shut down the APScheduler instance gracefully on application exit.
    """
    print("Shutting down scheduler...")
    ps_scheduler.shutdown()

