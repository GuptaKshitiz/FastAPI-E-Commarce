from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import Product
from schemas import ProductCreate

async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product

async def get_all_products(session: AsyncSession)-> List[Product]:
    statement = select(Product)
    result = await session.exec(statement)
    return result.all()

async def get_product_by_id(product_id: int, session: AsyncSession)-> Product | None:
    statement = select(Product).where(Product.id == product_id)
    result = await session.exec(statement)
    return result.one_or_none()