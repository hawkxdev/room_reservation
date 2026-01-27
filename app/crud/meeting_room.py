"""CRUD-функции для модели MeetingRoom."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession,
) -> MeetingRoom:
    """Создание переговорки в БД."""
    new_room_data = new_room.model_dump()
    db_room = MeetingRoom(**new_room_data)
    session.add(db_room)
    await session.commit()
    return db_room


async def get_room_id_by_name(
        room_name: str,
        session: AsyncSession,
) -> Optional[int]:
    """Получить id переговорки по имени."""
    result = await session.execute(
        select(MeetingRoom.id).where(MeetingRoom.name == room_name)
    )
    db_room_id = result.scalars().first()
    return db_room_id
