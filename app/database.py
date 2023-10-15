from collections.abc import AsyncGenerator

from app.config import database_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from functools import wraps

engine = create_async_engine(database_settings.database_url, future=True, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncSession | AsyncGenerator:
    async with async_session() as session:
        yield session
    await session.close()


def with_async_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper