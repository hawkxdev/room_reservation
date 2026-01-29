"""Эндпоинты для бронирования переговорок."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_before_edit,
    check_reservation_intersections,
)
from app.core.db import get_async_session
from app.crud.reservation import reservation_crud
from app.schemas.reservation import (
    ReservationCreate,
    ReservationDB,
    ReservationUpdate,
)

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post("/", response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: SessionDep,
):
    """Создать бронирование переговорки."""
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(
        from_reserve=reservation.from_reserve,
        to_reserve=reservation.to_reserve,
        meetingroom_id=reservation.meetingroom_id,
        session=session,
    )
    new_reservation = await reservation_crud.create(reservation, session)
    return new_reservation


@router.get("/", response_model=list[ReservationDB])
async def get_all_reservations(session: SessionDep):
    """Получить список всех бронирований."""
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete("/{reservation_id}", response_model=ReservationDB)
async def delete_reservation(
    reservation_id: int,
    session: SessionDep,
):
    """Удалить бронирование."""
    reservation = await check_reservation_before_edit(reservation_id, session)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch("/{reservation_id}", response_model=ReservationDB)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: SessionDep,
):
    """Обновить время бронирования."""
    reservation = await check_reservation_before_edit(reservation_id, session)
    await check_reservation_intersections(
        from_reserve=obj_in.from_reserve,
        to_reserve=obj_in.to_reserve,
        meetingroom_id=reservation.meetingroom_id,
        session=session,
        reservation_id=reservation_id,
    )
    reservation = await reservation_crud.update(reservation, obj_in, session)
    return reservation
