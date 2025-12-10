from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # The format is postgresql+ASYNC_DRIVER://user:password@host/dbname
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_ecom"
    DATABASE_SYNC_URL: str = "postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/fastapi_ecom"
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()
