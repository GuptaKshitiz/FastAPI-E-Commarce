# crud/crud_user.py
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import User
from schemas import UserCreate
from core.security import get_password_hash

async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    """
    Creates a new user in the database.
    """
    # Hash the user's password before storing it
    hashed_password = get_password_hash(user_data.password)
    
    # Create a User instance, excluding the plain password and including the hashed one
    user_dict = user_data.model_dump(exclude={"password"})
    db_user = User(**user_dict, password=hashed_password)
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    
    return db_user

async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    """
    Retrieves a user by their ID.
    """
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    return result.one_or_none()

async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    """
    Retrieves a user by their username.
    """
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.one_or_none()
