from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import require_admin
from src.core.services.admin_service import AdminService
from src.data.clients.postgres import get_db
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

admin_service = AdminService()


@router.post("/add")
async def admin_add(
    payload: AdminAddRequest,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.admin_add(db, payload, str(admin.id))


@router.put("/update")
async def admin_update(
    payload: AdminUpdateRequest,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.admin_update(db, payload)


@router.delete("/delete")
async def admin_delete(
    payload: AdminDeleteRequest,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.admin_delete(db, payload)


@router.post("/buses")
async def create_bus(
    payload: BusCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.create_bus(db, payload.model_dump(), str(admin.id))


@router.put("/buses/{bus_id}")
async def update_bus(
    bus_id: int,
    payload: BusUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.update_bus(db, bus_id, payload.model_dump(exclude_unset=True))


@router.delete("/buses/{bus_id}")
async def delete_bus(
    bus_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.delete_bus(db, bus_id)


@router.post("/routes")
async def create_route(
    payload: RouteCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.create_route(db, payload.model_dump())


@router.put("/routes/{route_id}")
async def update_route(
    route_id: int,
    payload: RouteUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.update_route(db, route_id, payload.model_dump(exclude_unset=True))


@router.delete("/routes/{route_id}")
async def delete_route(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.delete_route(db, route_id)


@router.post("/schedules")
async def create_schedule(
    payload: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.create_schedule(db, payload.model_dump())


@router.put("/schedules/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    payload: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.update_schedule(db, schedule_id, payload.model_dump(exclude_unset=True))


@router.delete("/schedules/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin)
):
    return await admin_service.delete_schedule(db, schedule_id)
