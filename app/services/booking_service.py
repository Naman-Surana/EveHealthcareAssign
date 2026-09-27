from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status
from app.models.booking import Booking
from app.models.test import DiagnosticTest
from app.models.user import User
from app.schemas.booking import BookingCreate
from app.core.exceptions import DomainException
from app.core.strings import Strings
from uuid import UUID

class BookingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_booking(self, user: User, data: BookingCreate) -> Booking:
        result = await self.db.execute(select(DiagnosticTest).where(DiagnosticTest.id == data.test_id))
        test = result.scalars().first()
        if not test:
            raise DomainException(code=Strings.CODE_TEST_NOT_FOUND, message=Strings.ERR_TEST_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        if not test.is_active:
            raise DomainException(code=Strings.CODE_TEST_INACTIVE, message=Strings.ERR_TEST_INACTIVE, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        booking = Booking(
            user_id=user.id,
            test_id=test.id,
            centre_id=test.centre_id,
            appointment_datetime=data.appointment_datetime,
            amount=test.price,
            status=Strings.STATUS_PENDING
        )
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def cancel_booking(self, user: User, booking_id: UUID) -> Booking:
        result = await self.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = result.scalars().first()
        
        if not booking:
            raise DomainException(code=Strings.CODE_BOOKING_NOT_FOUND, message=Strings.ERR_BOOKING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        
        if booking.user_id != user.id and user.role != Strings.ROLE_ADMIN:
            raise DomainException(code=Strings.CODE_NOT_OWNER, message=Strings.ERR_NOT_OWNER, status_code=status.HTTP_403_FORBIDDEN)
        
        if booking.status == Strings.STATUS_CANCELLED:
            raise DomainException(code=Strings.CODE_INVALID_TRANSITION, message=Strings.ERR_ALREADY_CANCELLED, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        if booking.status == Strings.STATUS_CONFIRMED and booking.appointment_datetime < now:
            raise DomainException(code=Strings.CODE_INVALID_TRANSITION, message=Strings.ERR_PAST_APPOINTMENT, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        booking.status = Strings.STATUS_CANCELLED
        await self.db.commit()
        await self.db.refresh(booking)
        return booking
