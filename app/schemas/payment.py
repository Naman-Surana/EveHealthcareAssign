from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from .booking import BookingResponse

class PaymentRequest(BaseModel):
    booking_id: UUID
    idempotency_key: str | None = None
    force_outcome: str | None = None  # Only used if DEBUG=True

class PaymentResponse(BaseModel):
    id: UUID
    booking_id: UUID
    amount: Decimal
    status: str
    provider_reference: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentWithBookingResponse(BaseModel):
    payment: PaymentResponse
    booking: BookingResponse

class WebhookPayload(BaseModel):
    event_id: str
    payment_id: UUID
    booking_id: UUID
    status: str
    occurred_at: datetime
