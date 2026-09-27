from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from .centre import CentreSummary

class TestCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    duration_minutes: int | None = None
    is_active: bool = True

class TestUpdate(BaseModel):
    price: Decimal | None = Field(None, gt=0)
    is_active: bool | None = None

class TestResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: Decimal
    duration_minutes: int | None
    is_active: bool
    centre: CentreSummary

    class Config:
        from_attributes = True
