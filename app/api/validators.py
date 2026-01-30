"""Валидаторы для API."""

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models.meeting_room import MeetingRoom
from app.models.reservation import Reservation
from app.models.user import User


async def check_name_duplicate(
    room_name: str,
    session: AsyncSession,
) -> None:
    """Проверить уникальность имени переговорки."""
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Переговорка с таким именем уже существует!",
        )


async def check_meeting_room_exists(
    meeting_room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    """Проверить что переговорка существует."""
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail="Переговорка не найдена!",
        )
    return meeting_room


async def check_reservation_intersections(
    from_reserve: datetime,
    to_reserve: datetime,
    meetingroom_id: int,
    session: AsyncSession,
    reservation_id: int | None = None,
) -> None:
    """Проверить что время бронирования не пересекается с существующими."""
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        from_reserve=from_reserve,
        to_reserve=to_reserve,
        meetingroom_id=meetingroom_id,
        reservation_id=reservation_id,
        session=session,
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations),
        )


async def check_reservation_before_edit(
    reservation_id: int,
    session: AsyncSession,
    user: User,
) -> Reservation:
    """Проверить существование брони и права на редактирование."""
    reservation = await reservation_crud.get(reservation_id, session)
    if not reservation:
        raise HTTPException(status_code=404, detail="Бронь не найдена!")
    if reservation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Невозможно отредактировать или удалить чужую бронь!",
        )
    return reservation
