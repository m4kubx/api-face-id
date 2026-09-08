from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://faceuser:facepass@postgres:5432/facesaas"
    REDIS_URL: str = "redis://redis:6379"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    API_KEY: str = "your-api-key"
    UPLOAD_DIR: str = "/app/uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_ORIGINS: str = "*"
    FACE_MODEL: str = "ArcFace"
    FACE_DETECTOR: str = "retinaface"
    VERIFICATION_THRESHOLD: float = 0.4

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
