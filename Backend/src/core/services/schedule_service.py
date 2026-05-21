from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.data.models.postgres.booking import Booking
from src.data.models.postgres.bus import Bus
from src.data.models.postgres.schedule import Schedule
from src.data.repositories.schedule_repository import ScheduleRepository


def build_seat_labels(total_seats: int) -> list[str]:
    letters = ["A", "B", "C", "D"]
    seats = []
    for index in range(total_seats):
        row = index // len(letters) + 1
        letter = letters[index % len(letters)]
        seats.append(f"{row}{letter}")

    return seats


class ScheduleService:
    def __init__(self) -> None:
        self._schedule_repository = ScheduleRepository()

    async def list_schedules(self, db: AsyncSession):
        return await self._schedule_repository.get_all_schedules(db)

    async def search_schedules(
        self,
        db: AsyncSession,
        source: str,
        destination: str,
        journey_date: date | None = None,
    ):
        return await self._schedule_repository.search_schedules(
            db,
            source.strip(),
            destination.strip(),
            journey_date,
        )

    async def search_schedules_with_details(
        self,
        db: AsyncSession,
        source: str,
        destination: str,
        journey_date: date | None = None,
    ):
        return await self._schedule_repository.search_schedules_with_details(
            db,
            source.strip(),
            destination.strip(),
            journey_date,
        )

    async def list_schedules_with_details(self, db: AsyncSession):
        return await self._schedule_repository.get_all_schedules_with_details(db)

    async def get_schedule_seat_map(self, db: AsyncSession, schedule_id: int):
        schedule_result = await db.execute(
            select(Schedule, Bus)
            .join(Bus, Bus.id == Schedule.bus_id)
            .where(Schedule.id == schedule_id)
        )
        row = schedule_result.first()
        if not row:
            raise NotFoundException("Schedule not found")

        schedule, bus = row

        booking_result = await db.execute(
            select(Booking.seat_number)
            .where(
                Booking.schedule_id == schedule.id,
                Booking.booking_status == "confirmed"
            )
        )
        booked_seats = sorted({seat for (seat,) in booking_result.all()})

        all_seats = build_seat_labels(bus.total_seats)
        booked_set = set(booked_seats)
        available_seat_numbers = [seat for seat in all_seats if seat not in booked_set]

        return {
            "total_seats": bus.total_seats,
            "available_seats": len(available_seat_numbers),
            "booked_seats": booked_seats,
            "available_seat_numbers": available_seat_numbers,
        }
