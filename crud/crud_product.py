from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import Product
from schemas import ProductCreate
from sqlalchemy.orm import selectinload

async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    exec_query = (select(Product).where(
        Product.id == db_product.id).\
            options(selectinload(Product.reviews)).\
                options(selectinload(Product.category))
    )
    egar_load = await session.exec(exec_query)
    return egar_load.one()

async def get_all_products(session: AsyncSession)-> List[Product]:
    statement = (select(Product)\
                 .options(selectinload(Product.reviews))\
                 .options(selectinload(Product.category))
    )
    result = await session.exec(statement)
    return result.all()

async def get_product_by_id(product_id: int, session: AsyncSession)-> Product | None:
    statement = (
        select(Product).where(Product.id == product_id)\
        .options(selectinload(Product.reviews))\
        .options(selectinload(Product.category))
    )
    result = await session.exec(statement)
    return result.one_or_none()