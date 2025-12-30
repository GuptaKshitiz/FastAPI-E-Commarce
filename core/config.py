from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # The format is postgresql+ASYNC_DRIVER://user:password@host/dbname
    DATABASE_URL: str = "postgresql+asyncpg://postgres:root@localhost:5432/Fastapi-ecom"
    SECRET_KEY: str
    ALGORITHM: str
    API_AUTH_KEY: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()