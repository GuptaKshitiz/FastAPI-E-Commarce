# api/products.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_product
from schemas import ProductCreate, ProductPublic

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductPublic)
async def create_new_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new product.
    """
    new_product = await crud_product.create_product(product_data=product_data, session=session)
    return new_product

@router.get("/", response_model=List[ProductPublic])
async def get_all_products_list(
    session: AsyncSession = Depends(get_session)
):
    """
    Get a list of all products.
    """
    products = await crud_product.get_all_products(session=session)
    return products

@router.get("/{product_id}", response_model=ProductPublic)
async def get_product_details(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get details for a specific product by ID.
    """
    product = await crud_product.get_product_by_id(product_id=product_id, session=session)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product
