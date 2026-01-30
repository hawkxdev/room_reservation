"""CRUD-операции для бронирования переговорок."""

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(
    CRUDBase[Reservation, ReservationCreate, ReservationUpdate]
):
    """CRUD для бронирования переговорок."""

    async def get_reservations_at_the_same_time(
        self,
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: int | None = None,
        session: AsyncSession,
    ) -> list[Reservation]:
        """Найти бронирования пересекающиеся по времени."""
        statement = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve,
            ),
        )
        if reservation_id is not None:
            statement = statement.where(Reservation.id != reservation_id)
        result = await session.execute(statement)
        return list(result.scalars().all())

    async def get_future_reservations_for_room(
        self,
        room_id: int,
        session: AsyncSession,
    ) -> list[Reservation]:
        """Получить будущие бронирования для переговорки."""
        result = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now(),
            )
        )
        return list(result.scalars().all())

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> list[Reservation]:
        """Получить бронирования текущего пользователя."""
        result = await session.execute(
            select(Reservation).where(Reservation.user_id == user.id)
        )
        return list(result.scalars().all())


reservation_crud = CRUDReservation(Reservation)
