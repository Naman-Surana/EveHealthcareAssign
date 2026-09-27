import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.models.payment import Payment
from app.models.booking import Booking
from app.core.strings import Strings
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
import uuid
import hmac
import hashlib
import json
from datetime import datetime, timezone

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def setup_payment(db_session: AsyncSession):
    dummy_booking = Booking(
        user_id=uuid.uuid4(),
        test_id=uuid.uuid4(),
        centre_id=uuid.uuid4(),
        appointment_datetime=datetime.now(timezone.utc),
        amount=500.0,
        status=Strings.STATUS_PENDING
    )
    db_session.add(dummy_booking)
    await db_session.commit()
    await db_session.refresh(dummy_booking)
    
    payment = Payment(
        booking_id=dummy_booking.id,
        idempotency_key="webhook_test_key",
        amount=500.0,
        status=Strings.STATUS_PENDING
    )
    db_session.add(payment)
    await db_session.commit()
    await db_session.refresh(payment)
    return {"booking": dummy_booking, "payment": payment}

def generate_signature(payload: dict) -> str:
    body = json.dumps(payload).encode()
    return hmac.new(
        settings.WEBHOOK_SIGNING_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

async def test_webhook_success(async_client: AsyncClient, setup_payment: dict):
    payment_id = setup_payment["payment"].id
    booking_id = setup_payment["booking"].id
    
    payload = {
        "event_id": "evt_12345",
        "payment_id": str(payment_id),
        "booking_id": str(booking_id),
        "status": Strings.STATUS_SUCCESS,
        "occurred_at": datetime.now(timezone.utc).isoformat()
    }
    
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    signature = hmac.new(settings.WEBHOOK_SIGNING_SECRET.encode(), body, hashlib.sha256).hexdigest()
    
    response = await async_client.post(
        "/api/v1/payments/webhook/",
        headers={"X-Webhook-Signature": signature, "Content-Type": "application/json"},
        content=body
    )
    
    assert response.status_code == 200

async def test_webhook_invalid_signature(async_client: AsyncClient):
    payload = {
        "event_id": "evt_12345",
        "payment_id": str(uuid.uuid4()),
        "booking_id": str(uuid.uuid4()),
        "status": Strings.STATUS_SUCCESS,
        "occurred_at": datetime.now(timezone.utc).isoformat()
    }
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    
    response = await async_client.post(
        "/api/v1/payments/webhook/",
        headers={"X-Webhook-Signature": "invalid_signature", "Content-Type": "application/json"},
        content=body
    )
    
    assert response.status_code == 401
