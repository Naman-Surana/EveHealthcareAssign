from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
