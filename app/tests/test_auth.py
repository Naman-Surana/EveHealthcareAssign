import pytest
from httpx import AsyncClient
from app.models.user import User

pytestmark = pytest.mark.asyncio

async def test_signup_success(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/signup",
        json={
            "full_name": "New User",
            "email": "newuser@example.com",
            "phone": "9876543210",
            "password": "StrongPassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data

async def test_signup_existing_email(async_client: AsyncClient, test_user: User):
    response = await async_client.post(
        "/api/v1/auth/signup",
        json={
            "full_name": "Another User",
            "email": test_user.email,
            "password": "StrongPassword123"
        }
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "EMAIL_EXISTS"

async def test_login_success(async_client: AsyncClient, test_user: User):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

async def test_login_failure(async_client: AsyncClient, test_user: User):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "INVALID_CREDENTIALS"
