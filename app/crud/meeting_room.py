"""CRUD-функции для модели MeetingRoom."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


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


async def read_all_rooms_from_db(session: AsyncSession) -> list[MeetingRoom]:
    """Получить все переговорки из БД."""
    result = await session.execute(select(MeetingRoom))
    db_rooms = list(result.scalars().all())
    return db_rooms


async def read_room_from_db(
    room_id: int,
    session: AsyncSession,
) -> Optional[MeetingRoom]:
    """Получить переговорку по id."""
    result = await session.execute(
        select(MeetingRoom).where(MeetingRoom.id == room_id)
    )
    db_room = result.scalars().first()
    return db_room


async def update_meeting_room(
    db_room: MeetingRoom,
    obj_in: MeetingRoomUpdate,
    session: AsyncSession,
) -> MeetingRoom:
    """Обновить переговорку в БД."""
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_room, field, value)
    await session.commit()
    return db_room


async def delete_meeting_room(
    db_room: MeetingRoom,
    session: AsyncSession,
) -> MeetingRoom:
    """Удалить переговорку из БД."""
    await session.delete(db_room)
    await session.commit()
    return db_room
