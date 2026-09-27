from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CentreCreate(BaseModel):
    name: str
    address: str
    city: str
    state: str | None = None
    pincode: str | None = None

class CentreResponse(BaseModel):
    id: UUID
    name: str
    address: str
    city: str
    state: str | None
    pincode: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class CentreSummary(BaseModel):
    id: UUID
    name: str
    city: str

    class Config:
        from_attributes = True
