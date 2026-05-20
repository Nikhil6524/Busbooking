from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.clients.postgres import get_db
from src.data.repositories.route_repository import RouteRepository
from src.schemas.route_schema import RouteResponse

router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)

route_repository = RouteRepository()


@router.get("", response_model=list[RouteResponse])
async def list_routes(
    db: AsyncSession = Depends(get_db)
):
    return await route_repository.get_all_routes(db)
