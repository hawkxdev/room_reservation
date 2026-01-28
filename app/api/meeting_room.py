"""Эндпоинты для работы с переговорными комнатами."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.meeting_room import (
    create_meeting_room,
    delete_meeting_room,
    get_room_id_by_name,
    read_all_rooms_from_db,
    read_room_from_db,
    update_meeting_room,
)
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import (
    MeetingRoomCreate,
    MeetingRoomDB,
    MeetingRoomUpdate,
)

router = APIRouter(
    prefix="/meeting_rooms",
    tags=["Meeting Rooms"],
)

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    "/",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: SessionDep,
):
    """Создание новой переговорки."""
    await check_name_duplicate(meeting_room.name, session)
    new_room = await create_meeting_room(meeting_room, session)
    return new_room


@router.get(
    "/",
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(session: SessionDep):
    """Получение списка всех переговорок."""
    all_rooms = await read_all_rooms_from_db(session)
    return all_rooms


@router.get(
    "/{room_id}",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def get_meeting_room(room_id: int, session: SessionDep):
    """Получение переговорки по id."""
    return await check_meeting_room_exists(room_id, session)


@router.patch(
    "/{room_id}",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def update_meeting_room_by_id(
    room_id: int,
    obj_in: MeetingRoomUpdate,
    session: SessionDep,
):
    """Обновление переговорки по id."""
    room = await check_meeting_room_exists(room_id, session)
    if obj_in.name is not None and obj_in.name != room.name:
        await check_name_duplicate(obj_in.name, session)
    updated_room = await update_meeting_room(room, obj_in, session)
    return updated_room


@router.delete(
    "/{room_id}",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def delete_meeting_room_by_id(room_id: int, session: SessionDep):
    """Удаление переговорки по id."""
    room = await check_meeting_room_exists(room_id, session)
    deleted_room = await delete_meeting_room(room, session)
    return deleted_room


async def check_name_duplicate(room_name: str, session: AsyncSession) -> None:
    """Проверить уникальность имени переговорки."""
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Переговорка с таким именем уже существует!",
        )


async def check_meeting_room_exists(
    room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    """Проверить, что переговорка существует."""
    meeting_room = await read_room_from_db(room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail="Переговорка не найдена!",
        )
    return meeting_room
