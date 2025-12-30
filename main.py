# main.py
from fastapi import FastAPI, Request, status
from api import user, product, category, review, weather
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from core.config import get_settings
from fastapi_cache import FastAPICache 

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0
    )

    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    yield
    await redis_client.close()


# Create the main FastAPI application instance.
# The metadata parameters like title, description, etc., are optional
# and primarily used for the automatic API documentation.
app = FastAPI(
    title="FastAPI E-Com",
    version="1.0",
    lifespan=lifespan
)

async def validation_exception_handler(request: Request, exc:RequestValidationError):
    friendly_error = []
    for error_details in exc.errors():
        where_it_is = "->".join(str(part) for part in error_details["loc"])
        what_went_wrong = error_details["msg"]
        friendly_error.append({"field": where_it_is, "message": what_went_wrong})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"validation_issues":friendly_error}
    )

app.add_exception_handler(RequestValidationError, validation_exception_handler)
# --- Include API Routers ---
# Connect the modular endpoint files from the /api directory to the main app.
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(product.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(review.router, prefix="/api/v1/reviews", tags=["Reviews"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])

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
