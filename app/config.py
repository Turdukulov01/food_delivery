from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/food_delivery"
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    NOTIFICATION_SERVICE_URL: str = "http://notification-service:8002"
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
