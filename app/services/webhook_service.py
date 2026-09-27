from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.webhook_event import WebhookEvent
from app.schemas.payment import WebhookPayload
from app.core.strings import Strings
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class WebhookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_webhook(self, payload: WebhookPayload, raw_body: dict):
        try:
            event = WebhookEvent(
                event_id=payload.event_id,
                payment_id=payload.payment_id,
                payload=raw_body,
                processing_status=Strings.WEBHOOK_RECEIVED
            )
            self.db.add(event)
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            logger.info("duplicate_webhook_event", event_id=payload.event_id)
            return  # True no-op
            
        result = await self.db.execute(select(Payment).where(Payment.id == payload.payment_id).with_for_update())
        payment = result.scalars().first()
        
        if not payment:
            await self.db.execute(select(WebhookEvent).where(WebhookEvent.event_id == payload.event_id).with_for_update())
            event.processing_status = Strings.WEBHOOK_UNRECOGNIZED
            await self.db.commit()
            logger.warning("unrecognized_payment_id", event_id=payload.event_id, payment_id=payload.payment_id)
            return
            
        if payment.status != Strings.STATUS_PENDING:
            if payment.status == payload.status:
                event.processing_status = Strings.WEBHOOK_DUPLICATE_NOOP
            else:
                event.processing_status = Strings.WEBHOOK_CONFLICT_IGNORED
            await self.db.commit()
            return
            
        # First time being settled
        booking_result = await self.db.execute(select(Booking).where(Booking.id == payment.booking_id).with_for_update())
        booking = booking_result.scalars().first()
        
        payment.status = payload.status
        booking.status = Strings.STATUS_CONFIRMED if payload.status == Strings.STATUS_SUCCESS else Strings.STATUS_FAILED
        
        event.processing_status = Strings.WEBHOOK_PROCESSED
        event.processed_at = datetime.now(timezone.utc)
        
        await self.db.commit()
