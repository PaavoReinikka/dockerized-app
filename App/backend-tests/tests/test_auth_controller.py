import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import random

# Create a pytest-asyncio fixture for the test client
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client

# Test successful user registration
@pytest.mark.asyncio
async def test_register_user(client):
    # create a random email for testing
    random_number = random.randint(0, 99999)
    random_email = f"email{random_number}@user.com"
    response = await client.post(
        "/api/auth/register",
        json={"email": random_email, "password": "newpassword"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Confirmation email sent" in response.json()["message"]

@pytest.mark.asyncio
async def test_register_user_invalid_email(client):
    response = await client.post(
        "/api/auth/register",
        json={"email": "invalid-email", "password": "newpassword"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
    assert "value is not a valid email address: An email address must have an @-sign." in response.json()["message"]

@pytest.mark.asyncio
async def test_register_user_invalid_email_end(client):
    response = await client.post(
        "/api/auth/register",
        json={"email": "invalid-email@", "password": "newpassword"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
    assert "value is not a valid email address: There must be something after the @-sign." in response.json()["message"]


@pytest.mark.asyncio
async def test_register_user_short_password(client):
    # Generate a random email for testing
    random_number = random.randint(0, 99999)
    random_email = f"another{random_number}@user.com"

    # Send a request with a short password
    response = await client.post(
        "/api/auth/register",
        json={"email": random_email, "password": "3"},  # Password is too short
        headers={"Content-Type": "application/json"}
    )

    # Assert the response status code
    assert response.status_code == 422
    assert "Password must be at least 4 characters long" in response.json()["message"]

