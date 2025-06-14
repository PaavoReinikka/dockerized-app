from models.data_model import *
from ext_apis.ext_apis import *
from repositories.fingrid_repository import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class FingridServiceTools:
    """
    Utility class for Fingrid-related data operations.

    Provides methods for fetching, processing, and filling missing Fingrid data
    using the repository and external API fetcher.
    """
    def __init__(self, ext_api_fetcher, fingrid_repository):
        """
        Initialize FingridServiceTools.

        Args:
            ext_api_fetcher: External API fetcher instance for Fingrid data.
            fingrid_repository: FingridRepository instance for database operations.
        """
        self.fingrid_repository = fingrid_repository
        self.ext_api_fetcher = ext_api_fetcher

    async def fetch_and_process_data(self, time_range: TimeRange, dataset_id: int):
        """
        Fetch and process Fingrid data for a given time range and dataset.

        Args:
            time_range (TimeRange): The time range for which to fetch data.
            dataset_id (int): The Fingrid dataset ID.

        Returns:
            List[FingridDataPoint]: Sorted list of Fingrid data points for the range.

        Raises:
            Exception: If fetching or processing fails.
        """
        try:
            start_naive_hki = time_range.startTime.astimezone(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)
            end_naive_hki = time_range.endTime.astimezone(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)

            raw_data = await self.fingrid_repository.get_entries(
                start_date=start_naive_hki,
                end_date=end_naive_hki,
                dataset_id=dataset_id,
                select_columns="datetime, value, dataset_id"
            )

            result = self.convert_to_fingrid_data(raw_data)

            missing_entries = self.find_missing_entries_utc(time_range, result, dataset_id)
            if missing_entries:
                print(f"Database has {len(missing_entries)} entries missing in the range {time_range.startTime} to {time_range.endTime} with dataset ID {dataset_id}.")
                await self.fill_missing_entries(result, missing_entries, dataset_id)
            return sorted(result, key=lambda x: x.startTime, reverse=False)
        except Exception as e:
            print(f"Error while fetching and processing data: {e}")
            raise

    def convert_to_fingrid_data(self, data: list[dict]) -> list[FingridDataPoint]:
        """
        Convert a list of database dictionaries to a sorted list of FingridDataPoint objects in UTC.

        Args:
            data (list[dict]): List of dicts with 'datetime' and 'value' keys.

        Returns:
            list[FingridDataPoint]: Sorted list of FingridDataPoint objects (startTime in UTC).
        """
        if not data:
            return []
        return sorted([
            FingridDataPoint(
                startTime=item["datetime"].astimezone(ZoneInfo("UTC")),
                endTime=(item["datetime"] + timedelta(hours=1)).astimezone(ZoneInfo("UTC")),
                value=float(item["value"])
            ) for item in data
        ], key=lambda x: x.startTime, reverse=False)

    def find_missing_entries_utc(self, time_range: TimeRange, data_utc: list[FingridDataPoint], dataset_id: int) -> list[StartDateModel]:
        """
        Find missing hourly entries in the given UTC time range.

        Args:
            time_range (TimeRange): The UTC time range to check.
            data_utc (list[FingridDataPoint]): List of available data points in UTC.
            dataset_id (int): The dataset ID (not used in logic, for compatibility).

        Returns:
            list[StartDateModel]: List of StartDateModel objects for missing hours (all in UTC).

        Raises:
            Exception: If an error occurs during processing.
        """
        result = []
        current_date_utc = time_range.startTime
        try:
            while current_date_utc <= time_range.endTime:
                if not any(item.startTime == current_date_utc for item in data_utc):
                    result.append(StartDateModel(startDate=current_date_utc))
                current_date_utc += timedelta(hours=1)
            result.sort(key=lambda x: x.startDate, reverse=False)
        except Exception as e:
            print(f"Error while finding missing entries: {e}")
            raise
        return result

    async def fill_missing_entries(self, result: list[FingridDataPoint], missing_entries: list[StartDateModel], dataset_id: int):
        """
        Fetch and insert missing Fingrid data entries from the external API.

        Args:
            result (list[FingridDataPoint]): List to append new data points to (modified in place).
            missing_entries (list[StartDateModel]): List of missing data points to fetch.
            dataset_id (int): The dataset ID.

        Side effects:
            Updates the result list and inserts new entries into the database.

        Raises:
            Exception: If an error occurs during fetching or insertion.
        """
        self.result = result
        if not missing_entries:
            return
        start_time_utc_aware = min(missing_entries, key=lambda x: x.startDate).startDate
        end_time_utc_aware = max(missing_entries, key=lambda x: x.startDate).startDate
        time_range = TimeRange(startTime=start_time_utc_aware, endTime=end_time_utc_aware + timedelta(hours=1))
        
        try:
            # Fetch data for entire range of missing entries
            fetched_range = await self.ext_api_fetcher.fetch_fingrid_data_range(dataset_id, time_range)
            if not fetched_range:
                print("No data fetched for the missing entries range.")
                return
            print(f"Fetched {len(fetched_range)} entries for the range {time_range.startTime} to {time_range.endTime} from external API for dataset ID {dataset_id}.")
            counter = 0
            for entry in fetched_range:
                if any(item.startTime == entry.startTime for item in result):
                    continue
                utc_dt = entry.startTime
                iso_str = (utc_dt + timedelta(hours=0)).replace(microsecond=0).isoformat().replace("+00:00", "Z")

                result.append(FingridDataPoint(
                    startTime=utc_dt,
                    endTime=utc_dt + timedelta(hours=1),
                    value=entry.value
                ))
                await self.fingrid_repository.insert_entry(
                    value=entry.value,
                    iso_date=iso_str,
                    dataset_id=dataset_id
                )
                counter += 1
            print(f"Inserted {counter} missing entries into the database for dataset ID {dataset_id}.")
        except Exception as e:
            print(f"Error while filling missing entries: {e}")

def convert_to_fingrid_entry(value, iso_date, predicted=False, convert_to_helsinki_time=True, dataset_id=-1):
    """
    Convert a value and ISO 8601 date string into a dictionary for the fingrid table.

    Args:
        value (float): The value to insert.
        iso_date (str): The date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
        predicted (bool): Indicates if the value is predicted. Default is False.
        convert_to_helsinki_time (bool): Whether to convert datetime to Helsinki time. Default is True.
        dataset_id (int): The dataset ID.

    Returns:
        dict: A dictionary with keys: datetime_orig, datetime, date, year, month, day, hour, weekday, dataset_id, value, predicted.

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
        weekday = dt_naive.weekday()
        return {
            "datetime_orig": iso_date,
            "datetime": dt_naive,
            "date": dt_naive.date(),
            "year": dt_naive.year,
            "month": dt_naive.month,
            "day": dt_naive.day,
            "hour": dt_naive.hour,
            "weekday": weekday,
            "dataset_id": dataset_id,
            "value": value,
            "predicted": predicted
        }
    except ValueError as e:
        raise ValueError(f"Invalid ISO date format: {iso_date}. Error: {e}")


