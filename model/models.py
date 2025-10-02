# models.py
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: str = "customer"

    # This relationship is named "reviews"
    reviews: List["Review"] = Relationship(back_populates="user")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    # This relationship is named "products"
    products: List["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    price: float
    category_id: int = Field(foreign_key="category.id")
    
    # Corrected: back_populates now points to "products" in the Category model
    category: Category = Relationship(back_populates="products") 
    
    # This relationship is named "reviews"
    reviews: List["Review"] = Relationship(back_populates="products")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    rating: int

    user_id: int = Field(foreign_key="user.id")
    # Corrected: back_populates now points to "reviews" in the User model
    user: User = Relationship(back_populates="reviews")

    product_id: int = Field(foreign_key="product.id")
    # Corrected: back_populates now points to "reviews" in the Product model
    products: Product = Relationship(back_populates="reviews")


class ProductOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    item: str
    status: str = Field(default="Order Is Placed")