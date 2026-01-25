"""Pydantic-схемы для модели MeetingRoom."""

from typing import Optional

from pydantic import BaseModel, Field


class MeetingRoomCreate(BaseModel):
    """Схема для создания переговорки."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
