from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import BookingService
from app.api.v1.deps import get_current_user
from app.models.user import User
import uuid

router = APIRouter()

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(data: BookingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = BookingService(db)
    return await service.create_booking(current_user, data)

@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(booking_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = BookingService(db)
    return await service.cancel_booking(current_user, booking_id)
