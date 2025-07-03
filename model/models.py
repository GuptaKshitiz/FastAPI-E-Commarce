from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: str = "customer"
    reviews: List["Review"] = Relationship(back_populates="user")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    products: List["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    category: Category = Relationship(back_populates="product")
    reviews: List["Review"] = Relationship(back_populates="product")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    rating: int

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="review")

    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="review")