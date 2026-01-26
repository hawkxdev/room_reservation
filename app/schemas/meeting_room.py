"""Pydantic-схемы для модели MeetingRoom."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MeetingRoomBase(BaseModel):
    """Базовая схема переговорки."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    """Схема для создания переговорки."""

    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomDB(MeetingRoomCreate):
    """Схема переговорки из БД."""

    id: int

    model_config = ConfigDict(from_attributes=True)
