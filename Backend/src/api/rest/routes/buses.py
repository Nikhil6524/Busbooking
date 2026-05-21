from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.bus_service import BusService
from src.data.clients.postgres import get_db
from src.schemas.bus_schema import BusResponse

router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)

bus_service = BusService()


@router.get("", response_model=list[BusResponse])
async def list_buses(
    db: AsyncSession = Depends(get_db)
):
    return await bus_service.list_buses(db)


@router.get("/search")
async def search_buses(
    name: str = Query(..., min_length=1),
    fuzzy: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    return await bus_service.search_buses(db, name, fuzzy=fuzzy)
