from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # The format is postgresql+ASYNC_DRIVER://user:password@host/dbname
    DATABASE_URL: str = "postgresql+asyncpg://postgres:root@localhost/fastapi_ecom"

    class Config:
        env_file = ".env"

settings = Settings()