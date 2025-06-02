import pytest
import pytest_asyncio
from httpx import AsyncClient

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client

@pytest_asyncio.fixture
async def auth_client(client):
    # Kirjaudu sisään ja tallenna cookie clientiin
    login_resp = await client.post(
        "/api/auth/login",
        json={"email": "test@test.com", "password": "secret"}
    )
    assert login_resp.status_code == 200
    return client

@pytest.mark.asyncio
async def test_get_prices(auth_client):
    response = await auth_client.get("/api/public/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startDate" in item and "price" in item for item in data)

@pytest.mark.asyncio
async def test_get_prices_today(auth_client):
    response = await auth_client.get("/api/data/today")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("startDate" in item and "price" in item for item in data)

@pytest.mark.asyncio
async def test_get_windpower(auth_client):
    response = await auth_client.get("/api/windpower")
    assert response.status_code == 200
    data = response.json()
    assert "startTime" in data
    assert "endTime" in data
    assert "value" in data

@pytest.mark.asyncio
async def test_post_windpower_range(auth_client):
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
    response = await auth_client.get("/api/consumption")
    assert response.status_code == 200
    data = response.json()
    assert "startTime" in data
    assert "endTime" in data
    assert "value" in data

@pytest.mark.asyncio
async def test_post_consumption_range(auth_client):
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
    response = await auth_client.get("/api/production")
    assert response.status_code == 200
    data = response.json()
    assert "startTime" in data
    assert "endTime" in data
    assert "value" in data

@pytest.mark.asyncio
async def test_post_production_range(auth_client):
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
    payload = {
        "startTime": "2024-05-01T03:00:00Z",
        "endTime": "2024-05-01T00:00:00Z"
    }
    response = await auth_client.post("/api/windpower/range", json=payload)
    assert response.status_code in (400, 422, 500)
    data = response.json()
    assert "error" in data