from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.route_service import RouteService
from src.data.clients.postgres import get_db
from src.schemas.route_schema import RouteResponse

router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)

route_service = RouteService()


@router.get("", response_model=list[RouteResponse])
async def list_routes(
    db: AsyncSession = Depends(get_db)
):
    return await route_service.list_routes(db)
