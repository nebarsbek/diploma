from contextlib import asynccontextmanager
import sys
from fastapi import FastAPI
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from app.api import pizzas, orders, auth
from app.core.configs import settings

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield

app = FastAPI(
    title="Pizza Delivery API",
    version="1.0.0",
    description="API for Pizza Delivery app",
    lifespan=lifespan,
)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"], # Разрешаем все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"], # Разрешаем все заголовки
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pizzas.router, prefix="/pizzas", tags=["Pizzas"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
