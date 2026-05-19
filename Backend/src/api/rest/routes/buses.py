from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.clients.postgres import get_db
from src.data.repositories.bus_repository import BusRepository

router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)

bus_repository = BusRepository()


@router.get("/search")
async def search_buses(
    name: str = Query(..., min_length=1),
    fuzzy: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    return await bus_repository.search_buses_by_name(db, name, fuzzy=fuzzy)
