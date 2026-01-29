"""Эндпоинты для работы с переговорными комнатами."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.meeting_room import (
    MeetingRoomCreate,
    MeetingRoomDB,
    MeetingRoomUpdate,
)
from app.schemas.reservation import ReservationDB

router = APIRouter()

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
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    "/",
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(session: SessionDep):
    """Получение списка всех переговорок."""
    all_rooms = await meeting_room_crud.get_multi(session)
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
    updated_room = await meeting_room_crud.update(room, obj_in, session)
    return updated_room


@router.delete(
    "/{room_id}",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def delete_meeting_room_by_id(room_id: int, session: SessionDep):
    """Удаление переговорки по id."""
    room = await check_meeting_room_exists(room_id, session)
    deleted_room = await meeting_room_crud.remove(room, session)
    return deleted_room


@router.get(
    "/{meeting_room_id}/reservations",
    response_model=list[ReservationDB],
)
async def get_reservations_for_room(
    meeting_room_id: int,
    session: SessionDep,
):
    """Получение будущих бронирований переговорки."""
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
    return reservations
