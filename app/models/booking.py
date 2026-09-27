from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from app.core.database import Base, GUID
from app.core.strings import Strings
import uuid

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False, index=True)
    test_id = Column(GUID(), ForeignKey("diagnostic_tests.id"), nullable=False)
    centre_id = Column(GUID(), ForeignKey("diagnostic_centres.id"), nullable=False)
    appointment_datetime = Column(DateTime(timezone=True), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default=Strings.STATUS_PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
