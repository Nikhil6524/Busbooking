from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import require_admin
from src.data.clients.postgres import get_db
from src.data.repositories.bus_repository import BusRepository
from src.data.repositories.route_repository import RouteRepository
from src.data.repositories.schedule_repository import ScheduleRepository
from src.schemas.admin_schema import (
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


@router.post("/buses")
async def create_bus(
    payload: BusCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await bus_repository.create_bus(db, payload.model_dump())


@router.put("/buses/{bus_id}")
async def update_bus(
    bus_id: str,
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


@router.post("/routes")
async def create_route(
    payload: RouteCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await route_repository.create_route(db, payload.model_dump())


@router.put("/routes/{route_id}")
async def update_route(
    route_id: str,
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


@router.post("/schedules")
async def create_schedule(
    payload: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await schedule_repository.create_schedule(db, payload.model_dump())


@router.put("/schedules/{schedule_id}")
async def update_schedule(
    schedule_id: str,
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
