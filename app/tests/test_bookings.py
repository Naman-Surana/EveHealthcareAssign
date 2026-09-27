import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.models.user import User
from app.models.centre import DiagnosticCentre
from app.models.test import DiagnosticTest
from app.core.security import create_access_token
from app.core.strings import Strings
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def auth_headers(test_user: User):
    token = create_access_token(str(test_user.id), test_user.role)
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def setup_test_data(db_session: AsyncSession):
    centre = DiagnosticCentre(name="Test Centre", address="123 St", city="Test City")
    db_session.add(centre)
    await db_session.commit()
    await db_session.refresh(centre)
    
    test_item = DiagnosticTest(
        centre_id=centre.id,
        name="Test 1",
        price=500.0,
        is_active=True
    )
    db_session.add(test_item)
    await db_session.commit()
    await db_session.refresh(test_item)
    return {"centre": centre, "test": test_item}

async def test_create_booking_success(async_client: AsyncClient, auth_headers: dict, setup_test_data: dict):
    future_date = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    response = await async_client.post(
        "/api/v1/bookings/",
        headers=auth_headers,
        json={
            "test_id": str(setup_test_data["test"].id),
            "appointment_datetime": future_date
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == Strings.STATUS_PENDING
    assert data["amount"] == "500.0"

async def test_create_booking_past_date(async_client: AsyncClient, auth_headers: dict, setup_test_data: dict):
    past_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    response = await async_client.post(
        "/api/v1/bookings/",
        headers=auth_headers,
        json={
            "test_id": str(setup_test_data["test"].id),
            "appointment_datetime": past_date
        }
    )
    assert response.status_code == 422
    assert "future" in str(response.json())
