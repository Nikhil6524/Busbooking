from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.data.clients.postgres import get_db
from src.data.models.postgres.booking import Booking
from src.data.models.postgres.bus import Bus
from src.data.models.postgres.schedule import Schedule
from src.data.repositories.schedule_repository import ScheduleRepository
from src.schemas.bus_schema import BusResponse
from src.schemas.route_schema import RouteResponse
from src.schemas.schedule_schema import (
    ScheduleResponse,
    SeatMapResponse,
    CombinedScheduleSearchResponse
)

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)

schedule_repository = ScheduleRepository()


def build_seat_labels(total_seats: int) -> list[str]:
    letters = ["A", "B", "C", "D"]
    seats = []
    for index in range(total_seats):
        row = index // len(letters) + 1
        letter = letters[index % len(letters)]
        seats.append(f"{row}{letter}")

    return seats


@router.get("", response_model=list[ScheduleResponse])
async def list_schedules(
    db: AsyncSession = Depends(get_db)
):
    return await schedule_repository.get_all_schedules(db)


@router.get("/search", response_model=list[ScheduleResponse])
async def search_schedules(
    source: str = Query(..., min_length=1),
    destination: str = Query(..., min_length=1),
    journey_date: date | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await schedule_repository.search_schedules(
        db,
        source.strip(),
        destination.strip(),
        journey_date
    )


@router.get("/search/combined", response_model=list[CombinedScheduleSearchResponse])
async def search_schedules_combined(
    source: str = Query(..., min_length=1),
    destination: str = Query(..., min_length=1),
    journey_date: date | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    rows = await schedule_repository.search_schedules_with_details(
        db,
        source.strip(),
        destination.strip(),
        journey_date
    )

    return [
        CombinedScheduleSearchResponse(
            schedule=ScheduleResponse.model_validate(schedule),
            route=RouteResponse.model_validate(route),
            bus=BusResponse.model_validate(bus)
        )
        for schedule, route, bus in rows
    ]


@router.get("/details/all", response_model=list[CombinedScheduleSearchResponse])
async def list_schedules_with_details(
    db: AsyncSession = Depends(get_db)
):
    rows = await schedule_repository.get_all_schedules_with_details(db)
    return [
        CombinedScheduleSearchResponse(
            schedule=ScheduleResponse.model_validate(schedule),
            route=RouteResponse.model_validate(route),
            bus=BusResponse.model_validate(bus)
        )
        for schedule, route, bus in rows
    ]


@router.get("/{schedule_id}/seats", response_model=SeatMapResponse)
async def get_schedule_seats(
    schedule_id: int,
    db: AsyncSession = Depends(get_db)
):
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
    available_seat_numbers = [seat for seat in all_seats if seat not in set(booked_seats)]

    return SeatMapResponse(
        total_seats=bus.total_seats,
        available_seats=len(available_seat_numbers),
        booked_seats=booked_seats,
        available_seat_numbers=available_seat_numbers
    )
