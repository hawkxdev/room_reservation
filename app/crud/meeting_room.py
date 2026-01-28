"""CRUD-класс для модели MeetingRoom."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


class CRUDMeetingRoom(
    CRUDBase[MeetingRoom, MeetingRoomCreate, MeetingRoomUpdate]
):
    """CRUD для переговорок со специфичным методом."""

    async def get_room_id_by_name(
        self,
        room_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить id переговорки по имени."""
        result = await session.execute(
            select(MeetingRoom.id).where(MeetingRoom.name == room_name)
        )
        return result.scalars().first()


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
