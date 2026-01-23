"""Модель переговорной комнаты."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class MeetingRoom(CommonMixin, Base):
    """Переговорная комната."""

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
