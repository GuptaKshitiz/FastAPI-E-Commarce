# crud/crud_category.py
from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import Category
from schemas import CategoryCreate

async def create_category(category_data: CategoryCreate, session: AsyncSession) -> Category:
    """
    Creates a new category.
    """
    db_category = Category.model_validate(category_data)
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category

async def get_all_categories(session: AsyncSession) -> List[Category]:
    """
    Retrieves all categories.
    """
    statement = select(Category)
    result = await session.exec(statement)
    return result.all()

async def get_category_by_id(category_id: int, session: AsyncSession) -> Category | None:
    """
    Retrieves a category by its ID.
    """
    statement = select(Category).where(Category.id == category_id)
    result = await session.exec(statement)
    return result.one_or_none()
