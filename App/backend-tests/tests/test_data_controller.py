import pytest
import pytest_asyncio
from httpx import AsyncClient, Timeout


@pytest_asyncio.fixture
async def client():
    """Fixture for creating an async HTTP client with the test server base URL."""
    timeout = Timeout(10.0)  # timeout 10 sekuntia (voit säätää)
    async with AsyncClient(base_url="http://localhost:8000", timeout=timeout) as client:
        yield client


@pytest_asyncio.fixture
async def auth_client(client):
    """
    Fixture for creating an authenticated HTTP client by logging in
    and storing the session cookie for subsequent requests.
    """
    login_resp = await client.post(
        "/api/auth/login",
        json={"email": "test@test.com", "password": "secret"}
    )
    assert login_resp.status_code == 200
    return client


@pytest.mark.asyncio
async def test_get_prices(auth_client):
    """Test that the public endpoint for retrieving price data returns a list of items with 'startDate' and 'price'."""
    response = await auth_client.get("/api/public/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startDate" in item and "price" in item for item in data)


@pytest.mark.asyncio
async def test_get_prices_today(auth_client):
    """Test that the '/api/data/today' endpoint returns today's prices with the correct structure."""
    response = await auth_client.get("/api/data/today")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startDate" in item and "price" in item for item in data)

@pytest.mark.asyncio
async def test_get_windpower(auth_client):
    """Test that the windpower endpoint returns a valid single record with 'startTime', 'endTime', and 'value'."""
    response = await auth_client.get("/api/windpower")
    assert response.status_code == 200
    data = response.json()
    assert "startTime" in data
    assert "endTime" in data
    assert "value" in data

@pytest.mark.asyncio
async def test_post_windpower_range(auth_client):
    """Test that the windpower range endpoint returns a list of windpower data within the specified time range."""
    payload = {
        "startTime": "2024-05-01T00:00:00Z",
        "endTime": "2024-05-01T03:00:00Z"
    }
    response = await auth_client.post("/api/windpower/range", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startTime" in item and "endTime" in item and "value" in item for item in data)

@pytest.mark.asyncio
async def test_get_consumption(auth_client):
    """Test that the consumption endpoint returns an object with 'startTime', 'endTime', and 'value'."""
    response = await auth_client.get("/api/consumption")
    assert response.status_code == 200
    data = response.json()
    assert "startTime" in data
    assert "endTime" in data
    assert "value" in data

@pytest.mark.asyncio
async def test_post_consumption_range(auth_client):
    """Test that the consumption range endpoint returns a list of data for the specified time range."""
    payload = {
        "startTime": "2024-05-01T00:00:00Z",
        "endTime": "2024-05-01T03:00:00Z"
    }
    response = await auth_client.post("/api/consumption/range", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startTime" in item and "endTime" in item and "value" in item for item in data)

@pytest.mark.asyncio
async def test_get_production(auth_client):
    """Test that the production endpoint returns an object with 'startTime', 'endTime', and 'value'."""
    response = await auth_client.get("/api/production")
    assert response.status_code == 200
    data = response.json()
    assert "startTime" in data
    assert "endTime" in data
    assert "value" in data

@pytest.mark.asyncio
async def test_post_production_range(auth_client):
    """Test that the production range endpoint returns a list of production data for a given time range."""
    payload = {
        "startTime": "2024-05-01T00:00:00Z",
        "endTime": "2024-05-01T03:00:00Z"
    }
    response = await auth_client.post("/api/production/range", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startTime" in item and "endTime" in item and "value" in item for item in data)

@pytest.mark.asyncio
async def test_post_price_range(auth_client):
    """Test that the price range endpoint returns a list of prices for the specified time range."""
    payload = {
        "startTime": "2024-05-01T00:00:00Z",
        "endTime": "2024-05-01T03:00:00Z"
    }
    response = await auth_client.post("/api/price/range", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startDate" in item and "price" in item for item in data)

@pytest.mark.asyncio
async def test_post_windpower_range_invalid_time(auth_client):
    """Test that posting a time range where endTime is before startTime results in an error."""
    payload = {
        "startTime": "2024-05-01T03:00:00Z",
        "endTime": "2024-05-01T00:00:00Z"
    }
    response = await auth_client.post("/api/windpower/range", json=payload)
    assert response.status_code in (400, 422, 500)
    data = response.json()
    assert "error" in data

@pytest.mark.asyncio
async def test_post_price_range_missing_fields(auth_client):
    """Test that the price range endpoint returns an error if required fields are missing."""
    payload = {"startTime": "2024-05-01T00:00:00Z"}  # Missing endTime
    response = await auth_client.post("/api/price/range", json=payload)
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_post_production_range_invalid_format(auth_client):
    """Test that the production range endpoint returns an error on invalid date formats."""
    payload = {
        "startTime": "not-a-date",
        "endTime": "also-not-a-date"
    }
    response = await auth_client.post("/api/production/range", json=payload)
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_protected_route_requires_auth(client):
    """Test that accessing a protected route without authentication returns a 401 or 403 status code."""
    response = await client.get("/api/production")
    assert response.status_code in (401, 403)

@pytest.mark.asyncio
async def test_post_windpower_range_empty_result(auth_client):
    """Test that querying windpower for a time range with no data returns an empty list."""
    payload = {
        "startTime": "1900-01-01T00:00:00Z",
        "endTime": "1900-01-01T03:00:00Z"
    }
    response = await auth_client.post("/api/windpower/range", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

@pytest.mark.asyncio
async def test_post_on_get_endpoint(auth_client):
    """Test that making a POST request to a GET-only endpoint returns a 405 or 404 error."""
    response = await auth_client.post("/api/windpower")
    assert response.status_code in (405, 404)

@pytest.mark.asyncio
async def test_post_price_hourlyavg_success(auth_client):
    """
    Test successful POST request to /api/price/hourlyavg endpoint with valid time range.
    
    Verifies that the response status code is 200, response data is a list, 
    and each item contains 'hour' and 'price' keys.
    """
    payload = {
        "startTime": "2024-05-01T00:00:00Z",
        "endTime": "2024-05-01T12:00:00Z"
    }
    response = await auth_client.post("/api/price/hourlyavg", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("hour" in item and "price" in item for item in data)

@pytest.mark.asyncio
async def test_post_price_hourlyavg_invalid_time(auth_client):
    """
    Test POST request to /api/price/hourlyavg with invalid startTime format.
    
    Expects a 400, 422 or 500 status code and an error message in the response.
    """
    payload = {
        "startTime": "invalid-date",
        "endTime": "2024-05-01T12:00:00Z"
    }
    response = await auth_client.post("/api/price/hourlyavg", json=payload)
    assert response.status_code in (400, 422, 500)
    data = response.json()
    assert "error" in data

@pytest.mark.asyncio
async def test_post_price_hourlyavg_missing_fields(auth_client):
    """
    Test POST request to /api/price/hourlyavg missing the endTime field.
    
    Expects a 400 or 422 status code due to validation error.
    """
    payload = {
        "startTime": "2024-05-01T00:00:00Z"
        # endTime puuttuu
    }
    response = await auth_client.post("/api/price/hourlyavg", json=payload)
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_post_price_weekdayavg_success(auth_client):
    """
    Test successful POST request to /api/price/weekdayavg endpoint with valid time range.
    
    Verifies that the response status code is 200, response data is a list,
    and each item contains 'weekday' and 'price' keys.
    """
    payload = {
        "startTime": "2024-05-01T00:00:00Z",
        "endTime": "2024-05-07T23:59:59Z"
    }
    response = await auth_client.post("/api/price/weekdayavg", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("weekday" in item and "price" in item for item in data)

@pytest.mark.asyncio
async def test_post_price_weekdayavg_invalid_time(auth_client):
    """
    Test POST request to /api/price/weekdayavg with invalid startTime and endTime formats.
    
    Expects a 400, 422 or 500 status code and an error message in the response.
    """
    payload = {
        "startTime": "not-a-date",
        "endTime": "also-not-a-date"
    }
    response = await auth_client.post("/api/price/weekdayavg", json=payload)
    assert response.status_code in (400, 422, 500)
    data = response.json()
    assert "error" in data

@pytest.mark.asyncio
async def test_post_price_weekdayavg_missing_fields(auth_client):
    """
    Test POST request to /api/price/weekdayavg missing the startTime field.
    
    Expects a 400 or 422 status code due to validation error.
    """
    payload = {
        "endTime": "2024-05-01T23:59:59Z"
        # startTime puuttuu
    }
    response = await auth_client.post("/api/price/weekdayavg", json=payload)
    assert response.status_code in (400, 422)
