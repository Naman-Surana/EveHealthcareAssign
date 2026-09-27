from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import DomainException
from app.core.strings import Strings
from app.core.config import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def signup(self, data: SignupRequest) -> User:
        result = await self.db.execute(select(User).where(User.email == data.email))
        if result.scalars().first():
            raise DomainException(
                code=Strings.CODE_EMAIL_EXISTS,
                message=Strings.ERR_EMAIL_EXISTS,
                status_code=status.HTTP_409_CONFLICT
            )
        
        user = User(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            hashed_password=get_password_hash(data.password),
            role=Strings.ROLE_PATIENT
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, data: LoginRequest) -> str:
        result = await self.db.execute(select(User).where(User.email == data.email))
        user = result.scalars().first()
        if not user or not verify_password(data.password, user.hashed_password):
            raise DomainException(
                code=Strings.CODE_INVALID_CREDENTIALS,
                message=Strings.ERR_INVALID_CREDENTIALS,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        access_token = create_access_token(subject=user.id, role=user.role)
        return access_token
