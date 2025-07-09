# db.py
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from .config import settings

# The engine is created the same way, just with the import from sqlmodel
engine = create_async_engine(settings.DATABASE_URL, echo=True)

async def get_session():
    """
    Dependency that provides a database session, handles transactions,
    and ensures the session is closed.
    """
    async_session = AsyncSession(engine, expire_on_commit=False)
    async with async_session as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise