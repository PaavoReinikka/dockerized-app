"""
data_service.py

This module provides service classes for handling data operations in the Eprice backend.
It includes services for fetching and processing Fingrid electricity data and price data,
combining information from external APIs and the database, and providing unified access
to the application's core data models.
"""

from models.data_model import *
from ext_apis.ext_apis import *
from repositories.porssisahko_repository import *
from utils.porssisahko_service_tools import *
from config.secrets import DATABASE_URL
from datetime import datetime
from zoneinfo import ZoneInfo

class FingridDataService:
    """
    Service class for fetching Fingrid data from the external API.
    """

    def __init__(self):
        """
        Initialize the FingridDataService with the external API fetcher.
        """
        self.ext_api_fetcher = FetchFingridData()

    async def fingrid_data(self, dataset_id: int) -> FingridDataPoint:
        """
        Fetch the latest Fingrid data for a given dataset ID.

        Args:
            dataset_id (int): The Fingrid dataset ID.

        Returns:
            FingridDataPoint: The latest data point.
        
        Raises:
            HTTPException: If the API call fails or no data is available.
        """
        return await self.ext_api_fetcher.fetch_fingrid_data(dataset_id)
    
    async def fingrid_data_range(self, dataset_id: int, start_time: datetime, end_time: datetime) -> List[FingridDataPoint]:
        """
        Fetch Fingrid data for a given dataset ID and time range.

        Args:
            dataset_id (int): The Fingrid dataset ID.
            start_time (datetime): Start time in UTC.
            end_time (datetime): End time in UTC.

        Returns:
            List[FingridDataPoint]: List of data points for the given range.

        Raises:
            HTTPException: If the API call fails or no data is available.
        """
        return await self.ext_api_fetcher.fetch_fingrid_data_range(dataset_id, start_time, end_time)


class PriceDataService:
    """
    Service class for handling price data operations, including fetching from the database and external API.
    """

    def __init__(self):
        """
        Initialize the PriceDataService with required repositories and helper services.
        """
        self.ext_api_fetcher = FetchPriceData()
        self.database_fetcher = PorssisahkoRepository(DATABASE_URL)
        self.porssisahko_service_tools = PorssisahkoServiceTools(self.ext_api_fetcher, self.database_fetcher)

    async def price_data_latest(self) -> List[PriceDataPoint]:
        """
        Fetch the latest 48 hours of price data, preferring the database but falling back to the external API if needed.

        Returns:
            List[PriceDataPoint]: List of price data points for the latest 48 hours.

        Raises:
            HTTPException: If the API call fails or no data is available.
        """
        start_date, end_date = self.porssisahko_service_tools.expected_time_range()
        try:
            result = await self.porssisahko_service_tools.fetch_and_process_data(start_date, end_date)
            return result if result else await self.ext_api_fetcher.fetch_price_data_latest()
        except Exception:
            return await self.ext_api_fetcher.fetch_price_data_latest()

    async def price_data_range(self, time_range : TimeRangeRequest) -> List[PriceDataPoint]:
        """
        Fetch price data for a given time range, preferring the database but falling back to the external API if needed.

        Args:
            start_date (datetime): Start of the time range.
            end_date (datetime): End of the time range.

        Returns:
            List[PriceDataPoint]: List of price data points for the given range.

        Raises:
            HTTPException: If the API call fails or no data is available.
        """

        try:
            result = await self.porssisahko_service_tools.fetch_and_process_data(time_range.startTime, time_range.endTime)
            return result if result else await self.ext_api_fetcher.fetch_price_data_range(time_range.startTime, time_range.endTime)
        except Exception:
            return await self.ext_api_fetcher.fetch_price_data_range(time_range.startTime, time_range.endTime)

    async def price_data_today(self) -> List[PriceDataPoint]:
        """
        Fetch price data for the current day in Helsinki time.

        Returns:
            List[PriceDataPoint]: List of today's price data points.

        Raises:
            HTTPException: If the API call fails or no data is available.
        """
        data = await self.price_data_latest()
        if data:
            now_fi = datetime.now(ZoneInfo("Europe/Helsinki"))
            today_fi = now_fi.date()
            filtered_data = [item for item in data if item.startDate.astimezone(ZoneInfo("Europe/Helsinki")).date() == today_fi]
            return sorted(filtered_data, key=lambda x: x.startDate, reverse=False)
        else:
            return await self.ext_api_fetcher.fetch_price_data_today()

    async def price_data_hourly_avg(self, time_range):
        """
        Fetch hourly average price data for a given time range.

        Args:
            time_range (TimeRangeRequest): Start and end time as datetime objects.

        Returns:
            List[PriceHourlyAvgPricePoint]: List of hourly average price points.

        Raises:
            HTTPException: If the API call fails or no data is available.
        """
        data = await self.price_data_range(time_range)
        return self.porssisahko_service_tools.calculate_hourly_avg_price(data)
    

    
    async def price_data_avg_by_weekday(self, time_range: TimeRangeRequest, timezone_hki=False) -> List[PriceAvgByWeekdayPoint]:
        """
        Calculate average price by weekday for a given time range.

        Args:
            time_range (TimeRangeRequest): Start and end time as datetime objects.

        Returns:
            List[PriceAvgByWeekdayPoint]: List of average prices by weekday.
        """
        data = await self.price_data_range(time_range)
        
        return self.porssisahko_service_tools.calculate_avg_by_weekday(data, timezone_hki=timezone_hki)
    