# db.py
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# The engine is created the same way, just with the import from sqlmodel
engine = create_async_engine(get_settings().DATABASE_URL, echo=True)

AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)

async def get_session():
    """
    Dependency that provides a database session, handles transactions,
    and ensures the session is closed.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise