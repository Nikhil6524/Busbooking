from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories.route_repository import RouteRepository


class RouteService:
    def __init__(self) -> None:
        self._route_repository = RouteRepository()

    async def list_routes(self, db: AsyncSession):
        return await self._route_repository.get_all_routes(db)
