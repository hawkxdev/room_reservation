"""CRUD-функции для модели MeetingRoom."""

from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


async def create_meeting_room(
        new_room: MeetingRoomCreate,
) -> MeetingRoom:
    """Создание переговорки в БД."""
    new_room_data = new_room.model_dump()
    db_room = MeetingRoom(**new_room_data)

    async with AsyncSessionLocal() as session:
        session.add(db_room)
        await session.commit()

    return db_room
