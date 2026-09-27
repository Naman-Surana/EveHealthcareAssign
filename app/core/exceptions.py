from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.schemas.common import ErrorEnvelope, ErrorModel

class DomainException(Exception):
    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorEnvelope(
            error=ErrorModel(
                code=exc.code,
                message=exc.message,
                details=exc.details
            )
        ).model_dump(exclude_none=True)
    )
