"""Модель переговорной комнаты."""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, CommonMixin

if TYPE_CHECKING:
    from app.models.reservation import Reservation


class MeetingRoom(CommonMixin, Base):
    """Переговорная комнаты."""

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    reservations: Mapped[list['Reservation']] = relationship(cascade='delete')
