from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/diagnostics"
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    WEBHOOK_SIGNING_SECRET: str = "change-me-too"
    REDIS_URL: str = "redis://localhost:6379/0"
    DEBUG: bool = False
    PAYMENT_SUCCESS_RATE: float = 0.85

    class Config:
        env_file = ".env"

settings = Settings()
