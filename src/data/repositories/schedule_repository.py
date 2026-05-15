from sqlalchemy import select
from data.models.postgres.schedule import Schedule


class ScheduleRepository:

    async def create_schedule(self, db, schedule_data):
        schedule = Schedule(**schedule_data)
        db.add(schedule)
        await db.commit()
        await db.refresh(schedule)
        return schedule

    async def get_available_schedules(self, db, route_id):
        result = await db.execute(
            select(Schedule).where(
                Schedule.route_id == route_id,
                Schedule.available_seats > 0,
                Schedule.status == "active"
            )
        )
        return result.scalars().all()