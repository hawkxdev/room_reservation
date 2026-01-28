"""Pydantic-схемы для модели MeetingRoom."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MeetingRoomBase(BaseModel):
    """Базовая схема переговорки."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    """Схема для создания переговорки."""

    pass


class MeetingRoomUpdate(BaseModel):
    """Схема для обновления переговорки."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_cannot_be_null(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            raise ValueError("Имя переговорки не может быть пустым!")
        return value


class MeetingRoomDB(MeetingRoomBase):
    """Схема переговорки из БД."""

    id: int

    model_config = ConfigDict(from_attributes=True)
