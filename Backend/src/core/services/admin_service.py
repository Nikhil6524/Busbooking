from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.data.repositories.bus_repository import BusRepository
from src.data.repositories.route_repository import RouteRepository
from src.data.repositories.schedule_repository import ScheduleRepository
from src.schemas.admin_schema import AdminAddRequest, AdminDeleteRequest, AdminUpdateRequest


class AdminService:
    def __init__(self) -> None:
        self._bus_repository = BusRepository()
        self._route_repository = RouteRepository()
        self._schedule_repository = ScheduleRepository()

    async def admin_add(self, db: AsyncSession, payload: AdminAddRequest, admin_id: str):
        if payload.entity == "bus":
            bus_data = payload.data.model_dump()
            if not bus_data.get("owner_id"):
                bus_data["owner_id"] = admin_id
            return await self._bus_repository.create_bus(db, bus_data)

        if payload.entity == "route":
            return await self._route_repository.create_route(db, payload.data.model_dump())

        return await self._schedule_repository.create_schedule(db, payload.data.model_dump())

    async def admin_update(self, db: AsyncSession, payload: AdminUpdateRequest):
        if payload.entity == "bus":
            bus = await self._bus_repository.update_bus(
                db,
                payload.id,
                payload.data.model_dump(exclude_unset=True)
            )
            if not bus:
                raise NotFoundException("Bus not found")
            return bus

        if payload.entity == "route":
            route = await self._route_repository.update_route(
                db,
                payload.id,
                payload.data.model_dump(exclude_unset=True)
            )
            if not route:
                raise NotFoundException("Route not found")
            return route

        schedule = await self._schedule_repository.update_schedule(
            db,
            payload.id,
            payload.data.model_dump(exclude_unset=True)
        )
        if not schedule:
            raise NotFoundException("Schedule not found")
        return schedule

    async def admin_delete(self, db: AsyncSession, payload: AdminDeleteRequest):
        if payload.entity == "bus":
            bus = await self._bus_repository.delete_bus_cascade(db, payload.id)
            if not bus:
                raise NotFoundException("Bus not found")
            return {"message": "Bus deleted"}

        if payload.entity == "route":
            route = await self._route_repository.delete_route(db, payload.id)
            if not route:
                raise NotFoundException("Route not found")
            return {"message": "Route deleted"}

        schedule = await self._schedule_repository.delete_schedule(db, payload.id)
        if not schedule:
            raise NotFoundException("Schedule not found")
        return {"message": "Schedule deleted"}

    async def create_bus(self, db: AsyncSession, bus_data: dict, admin_id: str):
        if not bus_data.get("owner_id"):
            bus_data["owner_id"] = admin_id
        return await self._bus_repository.create_bus(db, bus_data)

    async def update_bus(self, db: AsyncSession, bus_id: int, bus_data: dict):
        bus = await self._bus_repository.update_bus(db, bus_id, bus_data)
        if not bus:
            raise NotFoundException("Bus not found")
        return bus

    async def delete_bus(self, db: AsyncSession, bus_id: int):
        bus = await self._bus_repository.delete_bus_cascade(db, bus_id)
        if not bus:
            raise NotFoundException("Bus not found")
        return {"message": "Bus deleted"}

    async def create_route(self, db: AsyncSession, route_data: dict):
        return await self._route_repository.create_route(db, route_data)

    async def update_route(self, db: AsyncSession, route_id: int, route_data: dict):
        route = await self._route_repository.update_route(db, route_id, route_data)
        if not route:
            raise NotFoundException("Route not found")
        return route

    async def delete_route(self, db: AsyncSession, route_id: int):
        route = await self._route_repository.delete_route(db, route_id)
        if not route:
            raise NotFoundException("Route not found")
        return {"message": "Route deleted"}

    async def create_schedule(self, db: AsyncSession, schedule_data: dict):
        return await self._schedule_repository.create_schedule(db, schedule_data)

    async def update_schedule(self, db: AsyncSession, schedule_id: int, schedule_data: dict):
        schedule = await self._schedule_repository.update_schedule(db, schedule_id, schedule_data)
        if not schedule:
            raise NotFoundException("Schedule not found")
        return schedule

    async def delete_schedule(self, db: AsyncSession, schedule_id: int):
        schedule = await self._schedule_repository.delete_schedule(db, schedule_id)
        if not schedule:
            raise NotFoundException("Schedule not found")
        return {"message": "Schedule deleted"}
