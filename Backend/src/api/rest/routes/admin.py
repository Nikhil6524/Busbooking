from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import require_admin
from src.data.clients.postgres import get_db
from src.data.repositories.bus_repository import BusRepository
from src.data.repositories.route_repository import RouteRepository
from src.data.repositories.schedule_repository import ScheduleRepository
from src.schemas.admin_schema import (
    AdminAddRequest,
    AdminUpdateRequest,
    AdminDeleteRequest,
    BusCreate,
    BusUpdate,
    RouteCreate,
    RouteUpdate,
    ScheduleCreate,
    ScheduleUpdate
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

bus_repository = BusRepository()
route_repository = RouteRepository()
schedule_repository = ScheduleRepository()


@router.post("/add")
async def admin_add(
    payload: AdminAddRequest,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    if payload.entity == "bus":
        bus_data = payload.data.model_dump()
        if not bus_data.get("owner_id"):
            bus_data["owner_id"] = str(admin.id)
        return await bus_repository.create_bus(db, bus_data)

    if payload.entity == "route":
        return await route_repository.create_route(db, payload.data.model_dump())

    return await schedule_repository.create_schedule(db, payload.data.model_dump())


@router.put("/update")
async def admin_update(
    payload: AdminUpdateRequest,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    if payload.entity == "bus":
        bus = await bus_repository.update_bus(
            db,
            payload.id,
            payload.data.model_dump(exclude_unset=True)
        )
        if not bus:
            raise HTTPException(status_code=404, detail="Bus not found")
        return bus

    if payload.entity == "route":
        route = await route_repository.update_route(
            db,
            payload.id,
            payload.data.model_dump(exclude_unset=True)
        )
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        return route

    schedule = await schedule_repository.update_schedule(
        db,
        payload.id,
        payload.data.model_dump(exclude_unset=True)
    )
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.delete("/delete")
async def admin_delete(
    payload: AdminDeleteRequest,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    if payload.entity == "bus":
        bus = await bus_repository.delete_bus_cascade(db, payload.id)
        if not bus:
            raise HTTPException(status_code=404, detail="Bus not found")
        return {"message": "Bus deleted"}

    if payload.entity == "route":
        route = await route_repository.delete_route(db, payload.id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        return {"message": "Route deleted"}

    schedule = await schedule_repository.delete_schedule(db, payload.id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted"}


@router.post("/buses")
async def create_bus(
    payload: BusCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    bus_data = payload.model_dump()
    if not bus_data.get("owner_id"):
        bus_data["owner_id"] = str(admin.id)
    return await bus_repository.create_bus(db, bus_data)


@router.put("/buses/{bus_id}")
async def update_bus(
    bus_id: int,
    payload: BusUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    bus = await bus_repository.update_bus(
        db,
        bus_id,
        payload.model_dump(exclude_unset=True)
    )
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus


@router.delete("/buses/{bus_id}")
async def delete_bus(
    bus_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    bus = await bus_repository.delete_bus_cascade(db, bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return {"message": "Bus deleted"}


@router.post("/routes")
async def create_route(
    payload: RouteCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await route_repository.create_route(db, payload.model_dump())


@router.put("/routes/{route_id}")
async def update_route(
    route_id: int,
    payload: RouteUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    route = await route_repository.update_route(
        db,
        route_id,
        payload.model_dump(exclude_unset=True)
    )
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.delete("/routes/{route_id}")
async def delete_route(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    route = await route_repository.delete_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return {"message": "Route deleted"}


@router.post("/schedules")
async def create_schedule(
    payload: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await schedule_repository.create_schedule(db, payload.model_dump())


@router.put("/schedules/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    payload: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    schedule = await schedule_repository.update_schedule(
        db,
        schedule_id,
        payload.model_dump(exclude_unset=True)
    )
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.delete("/schedules/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    schedule = await schedule_repository.delete_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted"}
