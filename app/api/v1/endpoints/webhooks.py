from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.payment import WebhookPayload
from app.services.webhook_service import WebhookService
from app.core.config import settings
import hmac
import hashlib
import json

router = APIRouter()

@router.post("/webhook/", status_code=status.HTTP_200_OK)
async def handle_webhook(request: Request, payload: WebhookPayload, db: AsyncSession = Depends(get_db)):
    signature = request.headers.get("X-Webhook-Signature")
    if not signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature")
        
    body = await request.body()
    expected_signature = hmac.new(
        settings.WEBHOOK_SIGNING_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
        
    service = WebhookService(db)
    raw_body = json.loads(body)
    await service.process_webhook(payload, raw_body)
    return {"status": "ok"}
