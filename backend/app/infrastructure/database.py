from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core import settings


class Base(DeclarativeBase):
    pass


_database = settings.database_settings
_sqlalchemy = settings.sql_alchemy_settings


engine = create_async_engine(
    url=_database.url,
    pool_recycle=_sqlalchemy.ALCHEMY_POOL_RECYCLE,
    pool_size=_sqlalchemy.ALCHEMY_POOL_SIZE,
    max_overflow=_sqlalchemy.ALCHEMY_MAX_OVERFLOW,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_maker() as db:
        yield db


__all__ = [
        'Base',
        'async_session_maker',
        'get_db',
]
