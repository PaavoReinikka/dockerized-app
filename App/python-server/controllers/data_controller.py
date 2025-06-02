"""
data_controller.py

This module defines the FastAPI routes for the Eprice backend service. It provides API endpoints for retrieving
and querying electricity production, consumption, wind power, and price data. The endpoints fetch data from
Fingrid and Porssisähkö APIs, and return results as Pydantic models or error responses.

Routes:
    - /api/windpower
    - /api/windpower/range
    - /api/consumption
    - /api/consumption/range
    - /api/production
    - /api/production/range
    - /api/price/range
    - /api/public/data
    - /api/data/today
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from services.data_service import FingridDataService, PriceDataService
from models.data_model import FingridDataPoint, TimeRangeRequest, PriceDataPoint, ErrorResponse
from fastapi import HTTPException

router = APIRouter()
fingrid_data_service = FingridDataService()
price_data_service = PriceDataService()



@router.get("/api/windpower", response_model=FingridDataPoint, responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def get_windpower():
    """
    Get wind power production forecast.

    Fetches forecast data from Fingrid dataset ID 245.

    Returns:
        FingridDataPoint | JSONResponse: A wind power data point or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data(dataset_id=245)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})


@router.post("/api/windpower/range", response_model=List[FingridDataPoint],
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def post_windpower_range(time_range: TimeRangeRequest):
    """
    Get wind power production data for a given time range.

    Fetches data from Fingrid dataset ID 245.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format.

    Returns:
        List[FingridDataPoint] | JSONResponse: List of wind power data points or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data_range(
            dataset_id=245,
            start_time=time_range.startTime,
            end_time=time_range.endTime,
)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})


@router.get("/api/consumption",
    response_model=FingridDataPoint,
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def get_consumption():
    """
    Get electricity consumption forecast.

    Fetches consumption data from Fingrid dataset ID 165.

    Returns:
        FingridDataPoint | JSONResponse: A consumption data point or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data(dataset_id=165)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})


@router.post("/api/consumption/range", response_model=List[FingridDataPoint],
             responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def post_consumption_range(time_range: TimeRangeRequest):
    """
    Get electricity consumption data for a given time range.

    Fetches consumption data from Fingrid dataset ID 165.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format (UTC).

    Returns:
        List[FingridDataPoint] | JSONResponse: List of consumption data points or an error message.
            Each FingridDataPoint's startTime and endTime are returned as UTC datetimes (RFC 3339).
    """
    try:
        return await fingrid_data_service.fingrid_data_range(
            dataset_id=165,
            start_time=time_range.startTime,
            end_time=time_range.endTime
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})


@router.get("/api/production",
    response_model=FingridDataPoint,
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def get_production():
    """
    Get electricity production forecast.

    Fetches production data from Fingrid dataset ID 241.

    Returns:
        FingridDataPoint | JSONResponse: A production data point or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data(dataset_id=241)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})


@router.post("/api/production/range", response_model=List[FingridDataPoint],
            responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def post_production_range(time_range: TimeRangeRequest):
    """
    Get electricity production data for a given time range.

    Fetches production data from Fingrid dataset ID 241.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format (UTC).

    Returns:
        List[FingridDataPoint] | JSONResponse: List of production data points or an error message.
            Each FingridDataPoint's startTime and endTime are returned as UTC datetimes (RFC 3339).
    """
    try:
        return await fingrid_data_service.fingrid_data_range(
            dataset_id=241,
            start_time=time_range.startTime,
            end_time=time_range.endTime
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})


@router.post("/api/price/range",
             response_model=List[PriceDataPoint])
async def post_price_range(time_range: TimeRangeRequest):
    """
    Get price data for a specific time range from the Porssisahko API.

    Args:
        time_range (TimeRangeRequest): Start and end time as UTC datetime objects (RFC 3339).

    Returns:
        List[PriceDataPoint] | JSONResponse: List of price data points or an error message.
            Each PriceDataPoint's startDate is returned as naive datetime in Helsinki time (YYYY-MM-DD HH:MM).
    """

    try:
        return await price_data_service.price_data_range(time_range)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        print(e)
        return JSONResponse({"error":"InternalServerError", "message": str(e)})



@router.get(
    "/api/public/data",
    response_model=List[PriceDataPoint],
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def get_prices():
    """
    Retrieve the latest 48 hours of electricity price data.

    Returns:
        List[PriceDataPoint] | JSONResponse: List of the latest price data points or an error message.
            Each PriceDataPoint's startDate is returned as naive datetime in Helsinki time (YYYY-MM-DD HH:MM).
    """
    try:
        return await price_data_service.price_data_latest()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})


@router.get(
    "/api/data/today",
    response_model=List[PriceDataPoint],
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def get_prices_today():
    """
    Retrieve today's electricity price data for Finland (Europe/Helsinki).

    Returns:
        List[PriceDataPoint] | JSONResponse: List of today's price data points or an error message.
            Each PriceDataPoint's startDate is returned as naive datetime in Helsinki time (YYYY-MM-DD HH:MM).
    """
    try:
        return await price_data_service.price_data_today()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})

@router.post("/api/price/hourlyavg")
async def post_price_hourly_avg(time_range: TimeRangeRequest):
    """
    Get hourly average price data for a specific time range.

    Args:
        time_range (TimeRangeRequest): Start and end time as UTC datetime objects (RFC 3339).

    Returns:
        List[HourlyAvgPricePoint] | JSONResponse: List of hourly average price data points or an error message.
            The 'hour' field is in Helsinki time (0-23).
    """
    try:
        return await price_data_service.price_data_hourly_avg(time_range)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})

@router.post("/api/price/weekdayavg")
async def post_price_weekday_avg_hki(time_range: TimeRangeRequest):
    """
    Get average price data grouped by weekday for a specific time range.

    Args:
        time_range (TimeRangeRequest): Start and end time as either UTC-aware datetimes (RFC 3339) or naive datetimes in Helsinki time.

    Returns:
        List[PriceAvgByWeekdayPoint] | JSONResponse: List of average price data points by weekday or an error message.
            The 'weekday' field is in Helsinki time (0=Monday, 6=Sunday).
    """
    try:
        return await price_data_service.price_data_avg_by_weekday(time_range, timezone_hki=True)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": "HTTPError", "message": e.detail})
    except Exception as e:
        return JSONResponse({"error": "InternalServerError", "message": str(e)})

