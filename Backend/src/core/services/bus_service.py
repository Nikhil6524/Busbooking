from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories.bus_repository import BusRepository


class BusService:
    def __init__(self) -> None:
        self._bus_repository = BusRepository()

    async def list_buses(self, db: AsyncSession):
        return await self._bus_repository.get_all_buses(db)

    async def search_buses(self, db: AsyncSession, name: str, fuzzy: bool = False):
        return await self._bus_repository.search_buses_by_name(db, name, fuzzy=fuzzy)
