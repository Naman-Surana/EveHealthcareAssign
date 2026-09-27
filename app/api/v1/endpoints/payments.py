from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.payment import PaymentRequest, PaymentWithBookingResponse
from app.services.payment_service import PaymentService
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PaymentWithBookingResponse)
async def initiate_payment(data: PaymentRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = PaymentService(db)
    payment, booking = await service.initiate_payment(current_user, data)
    return PaymentWithBookingResponse(payment=payment, booking=booking)
