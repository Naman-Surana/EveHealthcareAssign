from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.exceptions import DomainException, domain_exception_handler
from app.core.config import settings
from app.core.database import engine, Base

app = FastAPI(
    title="Diagnostic Test Booking & Payment Simulation",
    description="Backend API for SDE Intern assignment.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Create all tables (for dev purposes, use alembic for production)
        await conn.run_sync(Base.metadata.create_all)
