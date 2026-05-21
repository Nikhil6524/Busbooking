from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import get_current_user
from src.core.exceptions import (
    UnauthorizedException,
    NotFoundException,
    ConflictException,
    ForbiddenException
)
from src.data.clients.postgres import get_db
from src.data.models.postgres.bus import Bus
from src.data.models.postgres.booking import Booking
from src.data.models.postgres.schedule import Schedule
from src.data.models.postgres.user import User
from src.schemas.booking_schema import BookingCreate

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post("")
async def create_booking(
    payload: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    async with db.begin():
        schedule_result = await db.execute(
            select(Schedule)
            .where(Schedule.id == payload.schedule_id)
            .with_for_update()
        )
        schedule = schedule_result.scalar_one_or_none()
        if not schedule:
            raise NotFoundException("Schedule not found")

        if schedule.status != "active":
            raise ConflictException("Schedule not active")

        if schedule.available_seats <= 0:
            raise ConflictException("No seats available")

        seat_result = await db.execute(
            select(Booking).where(
                Booking.schedule_id == payload.schedule_id,
                Booking.seat_number == payload.seat_number,
                Booking.booking_status == "confirmed"
            )
        )
        seat_booking = seat_result.scalar_one_or_none()
        if seat_booking:
            raise ConflictException("Seat already booked")

        booking = Booking(
            user_id=user_id,
            schedule_id=payload.schedule_id,
            seat_number=payload.seat_number,
            booking_status="confirmed"
        )
        db.add(booking)
        schedule.available_seats -= 1

    await db.refresh(booking)
    return booking


@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    async with db.begin():
        booking_result = await db.execute(
            select(Booking)
            .where(Booking.id == booking_id)
            .with_for_update()
        )
        booking = booking_result.scalar_one_or_none()
        if not booking:
            raise NotFoundException("Booking not found")

        if str(booking.user_id) != user_id:
            raise ForbiddenException()

        if booking.booking_status == "cancelled":
            return {"message": "Booking already cancelled"}

        schedule_result = await db.execute(
            select(Schedule)
            .where(Schedule.id == booking.schedule_id)
            .with_for_update()
        )
        schedule = schedule_result.scalar_one_or_none()
        if schedule:
            schedule.available_seats += 1

        booking.booking_status = "cancelled"

    return {"message": "Booking cancelled"}


@router.get("/history")
async def booking_history(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    result = await db.execute(
        select(Booking)
        .where(Booking.user_id == user_id)
        .order_by(Booking.booking_date.desc())
    )
    return result.scalars().all()


@router.get("/current")
async def current_booking(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    result = await db.execute(
        select(Booking, Schedule, Bus, User)
        .join(Schedule, Booking.schedule_id == Schedule.id)
        .join(Bus, Schedule.bus_id == Bus.id)
        .join(User, Booking.user_id == User.id)
        .where(
            Booking.user_id == user_id,
            Booking.booking_status == "confirmed",
            Schedule.status == "active"
        )
        .order_by(Booking.booking_date.desc())
    )

    bookings = []
    for booking, schedule, bus, user in result.all():
        passenger_name = (user.email or '').split('@', 1)[0] or user.name
        bookings.append({
            "id": str(booking.id),
            "seat_number": booking.seat_number,
            "booking_status": booking.booking_status,
            "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
            "passenger_name": passenger_name,
            "bus_name": bus.bus_name,
            "departure_date": schedule.journey_date.isoformat() if schedule.journey_date else None,
            "departure_time": schedule.departure_time.isoformat() if schedule.departure_time else None,
        })

    return bookings
