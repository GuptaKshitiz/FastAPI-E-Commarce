# api/categories.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_category
from schemas import CategoryCreate, CategoryPublic

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryPublic)
async def create_new_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new product category.
    """
    new_category = await crud_category.create_category(category_data=category_data, session=session)
    return new_category

@router.get("/", response_model=List[CategoryPublic])
async def get_all_categories_list(
    session: AsyncSession = Depends(get_session)
):
    """
    Get a list of all categories.
    """
    categories = await crud_category.get_all_categories(session=session)
    return categories

@router.get("/{category_id}", response_model=CategoryPublic)
async def get_category_details(
    category_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get details for a specific category by ID.
    """
    category = await crud_category.get_category_by_id(category_id=category_id, session=session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found."
        )
    return category
