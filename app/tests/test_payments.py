import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.models.user import User
from app.models.booking import Booking
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
async def setup_booking(db_session: AsyncSession, test_user: User):
    import uuid
    dummy_centre_id = uuid.uuid4()
    dummy_test_id = uuid.uuid4()
    
    booking = Booking(
        user_id=test_user.id,
        test_id=dummy_test_id,
        centre_id=dummy_centre_id,
        appointment_datetime=datetime.now(timezone.utc) + timedelta(days=2),
        amount=500.0,
        status=Strings.STATUS_PENDING
    )
    db_session.add(booking)
    await db_session.commit()
    await db_session.refresh(booking)
    return booking

async def test_initiate_payment_success(async_client: AsyncClient, auth_headers: dict, setup_booking: Booking):
    response = await async_client.post(
        "/api/v1/payments/",
        headers=auth_headers,
        json={
            "booking_id": str(setup_booking.id),
            "force_outcome": Strings.STATUS_SUCCESS
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["payment"]["status"] == Strings.STATUS_SUCCESS
    assert data["booking"]["status"] == Strings.STATUS_CONFIRMED

async def test_idempotent_payment_initiation(async_client: AsyncClient, auth_headers: dict, setup_booking: Booking):
    # First request
    idemp_key = "test_key_123"
    response1 = await async_client.post(
        "/api/v1/payments/",
        headers=auth_headers,
        json={
            "booking_id": str(setup_booking.id),
            "idempotency_key": idemp_key,
            "force_outcome": Strings.STATUS_SUCCESS
        }
    )
    assert response1.status_code == 200
    
    # Second request with same idempotency key
    response2 = await async_client.post(
        "/api/v1/payments/",
        headers=auth_headers,
        json={
            "booking_id": str(setup_booking.id),
            "idempotency_key": idemp_key,
            "force_outcome": Strings.STATUS_FAILED
        }
    )
    assert response2.status_code == 200
    
    # Should return same result, not the new forced outcome
    data1 = response1.json()
    data2 = response2.json()
    assert data1["payment"]["id"] == data2["payment"]["id"]
    assert data2["payment"]["status"] == Strings.STATUS_SUCCESS
