from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from uuid import UUID
from decimal import Decimal
from app.core.strings import Strings

class BookingCreate(BaseModel):
    test_id: UUID
    appointment_datetime: datetime

    @field_validator('appointment_datetime')
    @classmethod
    def check_future_date(cls, v: datetime):
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        if v < datetime.now(timezone.utc):
            raise ValueError(Strings.ERR_PAST_DATE)
        return v

class BookingResponse(BaseModel):
    id: UUID
    test_id: UUID
    centre_id: UUID
    appointment_datetime: datetime
    amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
