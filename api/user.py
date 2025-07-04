# api/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_user
from schemas import UserCreate, UserPublic

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_new_user(
    user_data: UserCreate, 
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new user.
    """
    user = await crud_user.get_user_by_username(username=user_data.username, session=session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this username already exists.",
        )
    
    new_user = await crud_user.create_user(user_data=user_data, session=session)
    return new_user

@router.get("/{user_id}", response_model=UserPublic)
async def get_user_details(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get details for a specific user by ID.
    """
    user = await crud_user.get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )
    return user
