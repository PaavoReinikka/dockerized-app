"""
data_model.py

This module defines Pydantic data models used throughout the Eprice backend service.
It includes models for time ranges, Fingrid and price data points, error responses,
and utility base classes for datetime validation.
"""

from pydantic import BaseModel, Field, field_validator, field_serializer
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


HELSINKI_TZ = ZoneInfo("Europe/Helsinki")

class DateTimeValidatedModel(BaseModel):
    """
    Base model that normalizes datetime fields after initialization.

    This model ensures that all datetime fields listed in _datetime_fields are timezone-aware and converted to UTC.
    If a datetime field is naive (lacks tzinfo), it is assumed to be in Europe/Helsinki time and converted to UTC.
    This normalization happens automatically after model initialization, so all downstream code can safely assume
    that these fields are always UTC-aware datetimes.

    Intended for use as a base class for models that include datetime fields which may be provided in various formats.
    """

    _datetime_fields = ('startTime', 'endTime', 'timestamp', 'startDate')

    def model_post_init(self, __context):
        for field_name in self._datetime_fields:
            if hasattr(self, field_name):
                value = getattr(self, field_name)
                if isinstance(value, datetime):
                    setattr(self, field_name, self.assume_helsinki_if_naive(value))

    @staticmethod
    def assume_helsinki_if_naive(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=HELSINKI_TZ)
        return dt.astimezone(ZoneInfo("UTC"))

class StartDateModel(BaseModel):
    """
    Model containing a single startDate field as a datetime object.
    """
    startDate: datetime

class TimeRange(DateTimeValidatedModel):
    """
    Model representing a time range with start and end times in UTC.
    """
    startTime: datetime = Field(
        description="Start time in RFC 3339 format (e.g., 2024-05-01T00:00:00Z).",
        examples=["2024-05-01T00:00:00Z"]
    )
    endTime: datetime = Field(
        description="End time in RFC 3339 format (e.g., 2024-05-02T00:00:00Z).",
        examples=["2024-05-02T00:00:00Z"]
    )

class TimeRangeRequest(TimeRange):
    """
    Request model for endpoints requiring a time range.

    startTime and endTime are UTC-aware datetimes, validated by DateTimeValidatedModel.
    """

    def start_datetime(self) -> datetime:
        return self.startTime

    def end_datetime(self) -> datetime:
        return self.endTime

class FingridDataPoint(TimeRange):
    """
    Model representing a single data point from Fingrid, including a value (in megawatts) and time range.

    Attributes:
        value (float): Value of the data point in megawatts (MW), must be non-negative.
    """
    value: float = Field(
        examples=[7883.61],
        description="Value of the data point in megawatts (MW)."
    )

    @field_validator("value")
    def validate_value_positive(cls, v):
        """
        Validates that the value is non-negative.

        Raises:
            ValueError: If the value is negative.
        """
        if v < 0:
            raise ValueError("value must be non-negative")
        return v

class PriceDataPoint(BaseModel):
    """
    Model representing a single electricity price data point.

    Attributes:
        startDate (datetime): Start time of the price data point. 
            When serialized (returned from the API), this is formatted as a UTC datetime string (RFC 3339, e.g., '2025-06-01T20:00:00Z').
        price (float): Price in euro cents.
    """
    startDate: datetime = Field(
        description="Datetime, returned as naive datetime string in UTC datetime string in RFC 3339 format",
        # examples=["2025-06-01 23:00"] # Uncomment this line if you want to use naive datetime in Helsinki time
        examples=["2025-06-01T20:00:00Z"]
    )
    price: float = Field(
        description="Floating-point number representing the price in euro cents.",
        examples=[0.61]
    )
    # if startDate is wanted as naive datetime in Helsinki time, uncomment the serializer below
    # @field_serializer('startDate')
    # def serialize_start_date(self, dt: datetime, _info):
    #     dt_helsinki = dt.astimezone(HELSINKI_TZ)
    #     naive_helsinki = dt_helsinki.replace(tzinfo=None)
    #     return naive_helsinki.strftime('%Y-%m-%d %H:%M')

    @field_serializer('startDate')
    def serialize_start_date(self, dt: datetime, _info):
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

class HourlyAvgPricePoint(BaseModel):
    """
    Model representing an hourly average price point.

    Attributes:
        hour (int): Hour of the day (0-23) in Helsinki time.
        avgPrice (float): Average price in euro cents for that hour.
    """
    hour: int = Field(
        description="Hour of the day (0-23) in Helsinki time.",
        examples=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    )
    avgPrice: float = Field(
        description="Average price in euro cents for that hour.",
        examples=[0.61]
    )

class PriceAvgByWeekdayPoint(BaseModel):
    """
    Model representing average price by weekday.

    Attributes:
        weekday (int): Day of the week (0=Monday, 6=Sunday).
        avgPrice (float): Average price in euro cents for that weekday.
    """
    weekday: int = Field(
        description="Day of the week (0=Monday, 6=Sunday).",
        examples=[0, 1, 2, 3, 4, 5, 6]
    )
    avgPrice: float = Field(
        description="Average price in euro cents for that weekday.",
        examples=[0.61]
    )

class ErrorResponse(BaseModel):
    """
    Model for error responses returned by the API.

    Attributes:
        error (str): Error message describing the issue.
    """
    error: str = Field(
        description="Error message describing the issue.",
        examples=["An error occurred"]
    )
