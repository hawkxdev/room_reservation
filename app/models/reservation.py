"""Модель бронирования переговорок."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class Reservation(CommonMixin, Base):
    """Бронирование переговорной комнаты."""

    from_reserve: Mapped[datetime] = mapped_column(DateTime)
    to_reserve: Mapped[datetime] = mapped_column(DateTime)
    meetingroom_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('meetingroom.id')
    )
