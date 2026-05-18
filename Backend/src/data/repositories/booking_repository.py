from sqlalchemy import select
from data.models.postgres.booking import Booking


class BookingRepository:

    async def create_booking(self, db, booking_data):
        booking = Booking(**booking_data)
        db.add(booking)
        await db.commit()
        await db.refresh(booking)
        return booking

    async def get_user_bookings(self, db, user_id):
        result = await db.execute(
            select(Booking).where(Booking.user_id == user_id)
        )
        return result.scalars().all()

    async def cancel_booking(self, db, booking_id):
        result = await db.execute(
            select(Booking).where(Booking.id == booking_id)
        )
        booking = result.scalar_one_or_none()

        if booking:
            booking.booking_status = "cancelled"
            await db.commit()

        return booking