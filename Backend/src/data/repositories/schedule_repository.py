from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.postgres.schedule import Schedule


class ScheduleRepository:

    async def create_schedule(self, db: AsyncSession, schedule_data: dict):
        schedule = Schedule(**schedule_data)
        db.add(schedule)
        await db.commit()
        await db.refresh(schedule)
        return schedule

    async def get_schedule_by_id(self, db: AsyncSession, schedule_id):
        result = await db.execute(
            select(Schedule).where(Schedule.id == schedule_id)
        )
        return result.scalar_one_or_none()

    async def update_schedule(self, db: AsyncSession, schedule_id, schedule_data: dict):
        schedule = await self.get_schedule_by_id(db, schedule_id)
        if not schedule:
            return None

        for key, value in schedule_data.items():
            setattr(schedule, key, value)

        await db.commit()
        await db.refresh(schedule)
        return schedule

    async def get_available_schedules(self, db: AsyncSession, route_id):
        result = await db.execute(
            select(Schedule).where(
                Schedule.route_id == route_id,
                Schedule.available_seats > 0,
                Schedule.status == "active"
            )
        )
        return result.scalars().all()

    async def delete_schedule(self, db: AsyncSession, schedule_id):
        schedule = await self.get_schedule_by_id(db, schedule_id)
        if schedule:
            await db.delete(schedule)
            await db.commit()
        return schedule