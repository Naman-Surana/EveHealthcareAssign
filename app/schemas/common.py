from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    page: int
    page_size: int
    total: int

class ErrorDetails(BaseModel):
    current_status: Optional[str] = None
    # Add other flexible details if necessary

class ErrorModel(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None

class ErrorEnvelope(BaseModel):
    error: ErrorModel
