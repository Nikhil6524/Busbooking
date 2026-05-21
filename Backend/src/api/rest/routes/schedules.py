from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.schedule_service import ScheduleService
from src.data.clients.postgres import get_db
from src.schemas.bus_schema import BusResponse
from src.schemas.route_schema import RouteResponse
from src.schemas.schedule_schema import (
    ScheduleResponse,
    SeatMapResponse,
    CombinedScheduleSearchResponse
)

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)

schedule_service = ScheduleService()


@router.get("", response_model=list[ScheduleResponse])
async def list_schedules(
    db: AsyncSession = Depends(get_db)
):
    return await schedule_service.list_schedules(db)


@router.get("/search", response_model=list[ScheduleResponse])
async def search_schedules(
    source: str = Query(..., min_length=1),
    destination: str = Query(..., min_length=1),
    journey_date: date | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await schedule_service.search_schedules(db, source, destination, journey_date)


@router.get("/search/combined", response_model=list[CombinedScheduleSearchResponse])
async def search_schedules_combined(
    source: str = Query(..., min_length=1),
    destination: str = Query(..., min_length=1),
    journey_date: date | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    rows = await schedule_service.search_schedules_with_details(db, source, destination, journey_date)

    return [
        CombinedScheduleSearchResponse(
            schedule=ScheduleResponse.model_validate(schedule),
            route=RouteResponse.model_validate(route),
            bus=BusResponse.model_validate(bus)
        )
        for schedule, route, bus in rows
    ]


@router.get("/details/all", response_model=list[CombinedScheduleSearchResponse])
async def list_schedules_with_details(
    db: AsyncSession = Depends(get_db)
):
    rows = await schedule_service.list_schedules_with_details(db)
    return [
        CombinedScheduleSearchResponse(
            schedule=ScheduleResponse.model_validate(schedule),
            route=RouteResponse.model_validate(route),
            bus=BusResponse.model_validate(bus)
        )
        for schedule, route, bus in rows
    ]


@router.get("/{schedule_id}/seats", response_model=SeatMapResponse)
async def get_schedule_seats(
    schedule_id: int,
    db: AsyncSession = Depends(get_db)
):
    seat_map = await schedule_service.get_schedule_seat_map(db, schedule_id)
    return SeatMapResponse(**seat_map)
