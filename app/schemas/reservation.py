"""Pydantic-схемы для бронирования переговорок."""

from datetime import datetime, timedelta
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from typing_extensions import Self

# Динамические примеры для Swagger UI.
FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(
    timespec='minutes'
)
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(
    timespec='minutes'
)


class ReservationBase(BaseModel):
    """Базовая схема бронирования."""

    from_reserve: datetime = Field(..., examples=[FROM_TIME])
    to_reserve: datetime = Field(..., examples=[TO_TIME])

    model_config = ConfigDict(extra='forbid')


class ReservationUpdate(ReservationBase):
    """Схема для обновления бронирования."""

    @field_validator('from_reserve')
    @classmethod
    def check_from_reserve_later_than_now(cls, value: datetime) -> datetime:
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @model_validator(mode='after')
    def check_from_reserve_before_to_reserve(self) -> Self:
        if self.from_reserve >= self.to_reserve:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return self


class ReservationCreate(ReservationUpdate):
    """Схема для создания бронирования."""

    meetingroom_id: int


class ReservationDB(ReservationBase):
    """Схема для возвращаемого объекта бронирования."""

    id: int
    meetingroom_id: int
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
