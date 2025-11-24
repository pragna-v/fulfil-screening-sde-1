from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/fulfil"
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    UPLOAD_DIR: str = "/code/tmp"

    class Config:
        env_file = ".env"

settings = Settings()
