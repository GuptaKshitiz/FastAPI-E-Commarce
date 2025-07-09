from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from model.models import Product
from schemas import ProductCreate

async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    # 2. Re-fetch the new product with its relationships eagerly loaded
    #    This is necessary for the response model.
    get_new_product = await session.get(
        Product,
        db_product.id,
        options=[selectinload(Product.category), selectinload(Product.reviews)],
    )
    return get_new_product

async def get_all_products(session: AsyncSession)-> List[Product]:
    statement = (
        select(Product)
        .options(
            selectinload(Product.category),
            selectinload(Product.reviews) # Eager load reviews and their associated users
        )
    )
    result = await session.exec(statement)
    return result.unique().all()

async def get_product_by_id(product_id: int, session: AsyncSession)-> Product | None:
    statement = (
        select(Product)
        .where(Product.id == product_id)
        .options(
            selectinload(Product.category),
            selectinload(Product.reviews)
        )
    )
    result = await session.exec(statement)
    return result.one_or_none()