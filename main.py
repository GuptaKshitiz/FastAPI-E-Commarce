# main.py
from fastapi import FastAPI
from api import users, products, categories, reviews

# Create the main FastAPI application instance.
# The metadata parameters like title, description, etc., are optional
# and primarily used for the automatic API documentation.
app = FastAPI()

# --- Include API Routers ---
# Connect the modular endpoint files from the /api directory to the main app.
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])


@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm that the API is running.
    """
    return {"message": "Welcome to the E-commerce API!"}

# To run this application:
# 1. Make sure you are in the root directory of your project.
# 2. Run the command: uvicorn main:app --reload
