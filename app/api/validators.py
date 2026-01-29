"""Валидаторы для API."""

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models.meeting_room import MeetingRoom


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
) -> None:
    """Проверить что время бронирования не пересекается с существующими."""
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        from_reserve=from_reserve,
        to_reserve=to_reserve,
        meetingroom_id=meetingroom_id,
        session=session,
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations),
        )
