"""Настройка подключения к базе данных."""


from collections.abc import AsyncGenerator

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""

    pass


class CommonMixin:
    """Миксин с общими полями для всех моделей."""

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессий."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
