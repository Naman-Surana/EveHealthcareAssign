from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.sql import func
from app.core.database import Base, GUID
import uuid

class DiagnosticTest(Base):
    __tablename__ = "diagnostic_tests"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    centre_id = Column(GUID(), ForeignKey("diagnostic_centres.id"), nullable=False, index=True)
    name = Column(String(160), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
