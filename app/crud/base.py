"""Базовый класс для CRUD-операций."""

from typing import Generic, Optional, Sequence, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс с универсальными CRUD-методами."""

    def __init__(self, model: type[ModelType]) -> None:
        """Инициализация с моделью SQLAlchemy."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получить объект по ID."""
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> Sequence[ModelType]:
        """Получить все объекты модели."""
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> ModelType:
        """Создать новый объект."""
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Обновить существующий объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
