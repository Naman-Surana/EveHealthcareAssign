from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.core.database import get_db
from app.schemas.centre import CentreCreate, CentreResponse, CentreSummary
from app.schemas.test import TestResponse, TestCreate
from app.schemas.common import PaginatedResponse
from app.models.centre import DiagnosticCentre
from app.models.test import DiagnosticTest
from app.api.v1.deps import require_admin
import uuid

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[CentreSummary])
async def list_centres(
    city: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = select(DiagnosticCentre)
    if city:
        query = query.where(DiagnosticCentre.city == city)
        
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar() or 0
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    centres = result.scalars().all()
    
    return PaginatedResponse(
        items=centres,
        page=page,
        page_size=page_size,
        total=total
    )

@router.post("/", response_model=CentreResponse, status_code=201)
async def create_centre(data: CentreCreate, db: AsyncSession = Depends(get_db), _: None = Depends(require_admin)):
    centre = DiagnosticCentre(**data.model_dump())
    db.add(centre)
    await db.commit()
    await db.refresh(centre)
    return centre
