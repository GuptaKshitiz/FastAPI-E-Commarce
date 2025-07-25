# schemas.py
from typing import List, Optional
from sqlmodel import SQLModel

# These models are used for API input/output validation and are distinct from the database models.
# This allows us to control what data is exposed via the API.

# Shared properties for a user
class UserBase(SQLModel):
    username: str
    role: str = "customer"

# Properties for creating a new user (input)
class UserCreate(UserBase):
    password: str

# Properties to return from the API (output), excluding the password
class UserPublic(UserBase):
    id: int

# Shared properties for a category
class CategoryBase(SQLModel):
    name: str

# Properties for creating a new category (input)
class CategoryCreate(CategoryBase):
    pass

# Properties to return from the API (output)
class CategoryPublic(CategoryBase):
    id: int

# Shared properties for a review
class ReviewBase(SQLModel):
    text: str
    rating: int

# Properties for creating a new review (input)
class ReviewCreate(ReviewBase):
    product_id: int
    # user_id will be taken from the current authenticated user in a later part

# Public model for a review, including the user who wrote it
class ReviewPublic(ReviewBase):
    id: int
    user: UserPublic # Nested model to show user details

# Shared properties for a product
class ProductBase(SQLModel):
    name: str
    description: str
    price: float

# Properties for creating a new product (input)
class ProductCreate(ProductBase):
    category_id: int

# Public model for a product, including nested category and review info
class ProductPublic(ProductBase):
    id: int
    category: CategoryPublic
    reviews: List[ReviewPublic] = []

# To avoid circular imports, we can create specific models for nested data
# that don't have their own nested relationships.

class CategoryPublicWithProducts(CategoryPublic):
    products: List[ProductPublic] = []

class UserPublicWithReviews(UserPublic):
    reviews: List[ReviewPublic] = []
