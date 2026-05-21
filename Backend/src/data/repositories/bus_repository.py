from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException
from src.data.models.postgres.bus import Bus
from src.data.models.postgres.booking import Booking
from src.data.models.postgres.favourite import Favorite
from src.data.models.postgres.route import Route
from src.data.models.postgres.schedule import Schedule


class BusRepository:

    async def create_bus(self, db: AsyncSession, bus_data: dict):
        bus_id = bus_data.get("id")
        if bus_id is not None:
            existing_bus = await self.get_bus_by_id(db, bus_id)
            if existing_bus:
                raise ConflictException("Bus already exists")

        bus = Bus(**bus_data)
        db.add(bus)
        await db.commit()
        await db.refresh(bus)
        return bus

    async def get_all_buses(self, db: AsyncSession):
        result = await db.execute(select(Bus))
        return result.scalars().all()

    async def get_bus_by_id(self, db: AsyncSession, bus_id):
        result = await db.execute(
            select(Bus).where(Bus.id == bus_id)
        )
        return result.scalar_one_or_none()

    async def search_buses_by_name(self, db: AsyncSession, name: str, fuzzy: bool = False):
        search_value = name.strip()
        if not search_value:
            return []

        if fuzzy:
            # Simple fuzzy: allow gaps between characters in order.
            pattern = "%" + "%".join(search_value) + "%"
        else:
            pattern = f"%{search_value}%"

        result = await db.execute(
            select(Bus).where(Bus.bus_name.ilike(pattern))
        )
        return result.scalars().all()

    async def update_bus(self, db: AsyncSession, bus_id, bus_data: dict):
        bus = await self.get_bus_by_id(db, bus_id)
        if not bus:
            return None

        for key, value in bus_data.items():
            setattr(bus, key, value)

        await db.commit()
        await db.refresh(bus)
        return bus

    async def delete_bus(self, db: AsyncSession, bus_id):
        bus = await self.get_bus_by_id(db, bus_id)
        if bus:
            await db.delete(bus)
            await db.commit()
        return bus

    async def delete_bus_cascade(self, db: AsyncSession, bus_id: int):
        bus = await self.get_bus_by_id(db, bus_id)
        if not bus:
            return None

        schedule_ids = await db.execute(
            select(Schedule.id).where(Schedule.bus_id == bus_id)
        )
        schedule_ids = [row[0] for row in schedule_ids.all()]

        if schedule_ids:
            await db.execute(
                delete(Booking).where(Booking.schedule_id.in_(schedule_ids))
            )

        await db.execute(delete(Schedule).where(Schedule.bus_id == bus_id))
        await db.execute(delete(Route).where(Route.bus_id == bus_id))
        await db.execute(delete(Favorite).where(Favorite.bus_id == bus_id))
        await db.execute(delete(Bus).where(Bus.id == bus_id))
        await db.commit()
        return bus

    async def delete_all_buses(self, db: AsyncSession):
        await db.execute(delete(Bus))
        await db.commit()