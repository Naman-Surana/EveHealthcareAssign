from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.user import User
from app.schemas.payment import PaymentRequest
from app.core.exceptions import DomainException
from app.core.strings import Strings
from app.core.config import settings
import uuid
import random

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def initiate_payment(self, user: User, data: PaymentRequest) -> tuple[Payment, Booking]:
        # Lock booking row
        result = await self.db.execute(select(Booking).where(Booking.id == data.booking_id).with_for_update())
        booking = result.scalars().first()
        
        if not booking:
            await self.db.rollback()
            raise DomainException(code=Strings.CODE_BOOKING_NOT_FOUND, message=Strings.ERR_BOOKING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        
        if booking.user_id != user.id:
            await self.db.rollback()
            raise DomainException(code=Strings.CODE_NOT_OWNER, message=Strings.ERR_NOT_OWNER, status_code=status.HTTP_403_FORBIDDEN)
            
        idemp_key = data.idempotency_key or f"booking:{data.booking_id}:init"
        
        existing_result = await self.db.execute(select(Payment).where(Payment.idempotency_key == idemp_key))
        existing_payment = existing_result.scalars().first()
        if existing_payment:
            await self.db.commit()
            fresh_payment = await self.db.scalar(select(Payment).where(Payment.id == existing_payment.id))
            fresh_booking = await self.db.scalar(select(Booking).where(Booking.id == booking.id))
            return fresh_payment, fresh_booking
            
        if booking.status != Strings.STATUS_PENDING:
            current_status = booking.status
            await self.db.rollback()
            raise DomainException(code=Strings.CODE_BOOKING_NOT_PAYABLE, message=Strings.ERR_BOOKING_NOT_PAYABLE, status_code=status.HTTP_409_CONFLICT, details={"current_status": current_status})
            
        payment = Payment(
            booking_id=booking.id,
            idempotency_key=idemp_key,
            amount=booking.amount,
            status=Strings.STATUS_PENDING
        )
        self.db.add(payment)
        
        # Simulate provider
        outcome = Strings.STATUS_SUCCESS
        if settings.DEBUG and data.force_outcome:
            outcome = data.force_outcome
        elif random.random() > settings.PAYMENT_SUCCESS_RATE:
            outcome = Strings.STATUS_FAILED
            
        payment.status = outcome
        payment.provider_reference = f"mock_txn_{uuid.uuid4().hex[:8]}"
        
        booking.status = Strings.STATUS_CONFIRMED if outcome == Strings.STATUS_SUCCESS else Strings.STATUS_FAILED
        
        await self.db.commit()
        fresh_payment = await self.db.scalar(select(Payment).where(Payment.id == payment.id))
        fresh_booking = await self.db.scalar(select(Booking).where(Booking.id == booking.id))
        
        return fresh_payment, fresh_booking
