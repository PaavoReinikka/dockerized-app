"""
porssisahko_service_tools.py

This module provides helper services for handling electricity price data time ranges, 
converting database results to application models, and filling missing data entries 
from external APIs. It is used to unify and process price data from both the database 
and external sources for the Eprice backend.
"""

from models.data_model import *
from ext_apis.ext_apis import *
from repositories.porssisahko_repository import *
from utils.porssisahko_service_tools import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class PorssisahkoServiceTools:
    """
    PorssisahkoServiceTools has functions for time range calculations, data conversion, and filling missing entries.
    """

    def __init__(self, ext_api_fetcher: FetchPriceData, porssisahko_repository: PorssisahkoRepository):
        """
        Initialize the PorssisahkoServiceTools with external API and database fetchers.
        """
        self.ext_api_fetcher = ext_api_fetcher
        self.database_fetcher = porssisahko_repository

    def expected_time_range(self) -> tuple[datetime, datetime]:
        """
        Calculate the expected time range for the latest 48 hours based on Helsinki time.

        Returns:
            tuple[datetime, datetime]: Start and end datetimes (naive, Europe/Helsinki time).
        """
        now_naive = datetime.now(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)
        if now_naive.hour >= 14:
            end_time = (now_naive + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            end_time = (now_naive + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = (end_time - timedelta(hours=48)).replace(tzinfo=None)
        return start_time, end_time

    def convert_to_price_data(self, data: List[dict]) -> List[PriceDataPoint]:
        """
        Convert a list of database dicts to a sorted list of PriceDataPoint objects in UTC.

        Args:
            data (List[dict]): List of dicts with 'datetime' and 'price'.

        Returns:
            List[PriceDataPoint]: Sorted list of PriceDataPoint objects (startDate in UTC).
        """
        if not data:
            return []
        return sorted([
            PriceDataPoint(
                startDate=item["datetime"].astimezone(ZoneInfo("UTC")),
                price=item["price"]
            ) for item in data
        ], key=lambda x: x.startDate, reverse=False)

    async def fill_missing_entries(self, result: List[PriceDataPoint], missing_entries: List[PriceDataPoint]):
        """
        Fetch and insert missing price data entries from the external API.

        Args:
            result (List[PriceDataPoint]): List to append new data points to (modified in place).
            missing_entries (List[PriceDataPoint]): List of missing data points to fetch.

        Side effects:
            Updates the result list and inserts new entries into the database.
        """
        try:
            for missing in missing_entries:
                time_range = TimeRange(startTime=missing.startDate, endTime=missing.startDate)
                fetched = await self.ext_api_fetcher.fetch_price_data_range(time_range)
                if not fetched:
                    continue

                datapoint = fetched[0]
                utc_dt = datapoint.startDate
                iso_str = (utc_dt + timedelta(hours=0)).replace(microsecond=0).isoformat().replace("+00:00", "Z")

                result.append(PriceDataPoint(
                    startDate=utc_dt,
                    price=datapoint.price
                ))
                await self.database_fetcher.insert_entry(
                    price=datapoint.price,
                    iso_date=iso_str
                )
        except Exception as e:
            print(f"Error filling missing entries: {e}")
            raise

    async def fetch_and_process_data(self, time_range:TimeRange) -> List[PriceDataPoint]:
        """
        Fetch and process price data from the database, fill missing entries from the external API if needed.

        Args:
            start_date (datetime): Start of the time range.
            end_date (datetime): End of the time range.

        Returns:
            List[PriceDataPoint]: Sorted list of price data points for the range, including filled-in values if needed.
        """


        start_naive_hki = time_range.startTime.astimezone(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)
        end_naive_hki = time_range.endTime.astimezone(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)


        raw_data = await self.database_fetcher.get_entries(
            start_date=start_naive_hki,
            end_date=end_naive_hki,
            select_columns="datetime, price"
        )


        result = self.convert_to_price_data(raw_data)

        missing_entries = self.find_missing_entries_utc(
            time_range.startTime.astimezone(ZoneInfo("UTC")),
            time_range.endTime.astimezone(ZoneInfo("UTC")),
            result
        )
        if missing_entries:
            await self.fill_missing_entries(result, missing_entries)

        return sorted(result, key=lambda x: x.startDate, reverse=False)

    def find_missing_entries_utc(self, start_date_utc: datetime, end_date_utc: datetime, data_utc: List[PriceDataPoint]):
        """
        Find missing hourly entries in the given UTC time range.

        Args:
            start_date_utc (datetime): Start of the UTC time range.
            end_date_utc (datetime): End of the UTC time range.
            data_utc (List[PriceDataPoint]): List of available data points.

        Returns:
            List[StartDateModel]: List of StartDateModel objects for missing hours (all in UTC).
        """
        result = []
        current_date_utc = start_date_utc
        while current_date_utc <= end_date_utc:
            if not any(item.startDate == current_date_utc for item in data_utc):
                result.append(StartDateModel(startDate=current_date_utc))
            current_date_utc += timedelta(hours=1)
        result.sort(key=lambda x: x.startDate, reverse=False)
        return result

    def calculate_hourly_avg_price(self, data):
        """
        Calculate hourly average prices from a list of price data points.

        Args:
            data (List[PriceDataPoint]): List of price data points.

        Returns:
            List[PriceHourlyAvgPricePoint]: List of hourly average price points. Hours are in Helsinki time.
        """
        hourly_avg = {}
        for point in data:
            hour = point.startDate.astimezone(ZoneInfo("Europe/Helsinki")).hour
            hourly_avg.setdefault(hour, []).append(point.price)

        result = [
            HourlyAvgPricePoint(
                hour=hour,
                avgPrice=round(sum(prices) / len(prices), 3)
            )
            for hour, prices in hourly_avg.items()
        ]
        return sorted(result, key=lambda x: x.hour)
    
    def calculate_avg_by_weekday(self, data: List[PriceDataPoint]) -> List[PriceAvgByWeekdayPoint]:
        """
        Calculate average price by weekday from a list of price data points.

        Args:
            data (List[PriceDataPoint]): List of price data points.

        Returns:
            List[PriceAvgByWeekdayPoint]: List of average prices by weekday.
        """
        tz = ZoneInfo("Europe/Helsinki")
        weekday_prices = {}
        for point in data:
            dt = point.startDate.astimezone(tz) if tz else point.startDate
            weekday = dt.weekday()
            weekday_prices.setdefault(weekday, []).append(point.price)

        result = [
            PriceAvgByWeekdayPoint(
                weekday=weekday,
                avgPrice=round(sum(prices) / len(prices), 3)
            )
            for weekday, prices in weekday_prices.items()
        ]
        return sorted(result, key=lambda x: x.weekday)
