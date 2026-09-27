from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class DiagnosticCentre(Base):
    __tablename__ = "diagnostic_centres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(160), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(80), nullable=False, index=True)
    state = Column(String(80), nullable=True)
    pincode = Column(String(10), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
