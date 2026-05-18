from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models.postgres.bus import Bus


class BusRepository:

    async def create_bus(self, db: AsyncSession, bus_data: dict):
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