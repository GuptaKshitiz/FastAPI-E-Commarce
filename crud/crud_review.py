# crud/crud_review.py
from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import Review
from schemas import ReviewCreate

async def create_review(review_data: ReviewCreate, user_id: int, session: AsyncSession) -> Review:
    """
    Creates a new review for a product.
    Note: In a real app, user_id would come from the authenticated user token.
    """
    review_dict = review_data.model_dump()
    db_review = Review(**review_dict, user_id=user_id)
    
    session.add(db_review)
    await session.commit()
    await session.refresh(db_review)
    return db_review

async def get_reviews_for_product(product_id: int, session: AsyncSession) -> List[Review]:
    """
    Retrieves all reviews for a specific product.
    """
    statement = select(Review).where(Review.product_id == product_id)
    result = await session.exec(statement)
    return result.all()
