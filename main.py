# main.py
from fastapi import FastAPI
from api import user, product, category, review
from fastapi.middleware.cors import CORSMiddleware

# Create the main FastAPI application instance.
# The metadata parameters like title, description, etc., are optional
# and primarily used for the automatic API documentation.
app = FastAPI()

# --- Include API Routers ---
# Connect the modular endpoint files from the /api directory to the main app.
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(product.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(review.router, prefix="/api/v1/reviews", tags=["Reviews"])

# Add this section
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm that the API is running.
    """
    return {"message": "Welcome to the E-commerce API!"}

# To run this application:
# 1. Make sure you are in the root directory of your project.
# 2. Run the command: uvicorn main:app --reload
