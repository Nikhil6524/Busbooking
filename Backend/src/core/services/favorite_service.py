from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictException, NotFoundException
from src.data.models.postgres.bus import Bus
from src.data.repositories.favorite_repository import FavoriteRepository


class FavoriteService:
    def __init__(self) -> None:
        self._favorite_repository = FavoriteRepository()

    async def add_favorite(self, db: AsyncSession, user_id: str, bus_id: int):
        bus_result = await db.execute(select(Bus).where(Bus.id == bus_id))
        bus = bus_result.scalar_one_or_none()
        if not bus:
            raise NotFoundException("Bus not found")

        existing = await self._favorite_repository.get_user_favorite(db, user_id, bus_id)
        if existing:
            raise ConflictException("Favorite already exists")

        return await self._favorite_repository.add_favorite(
            db,
            {
                "user_id": user_id,
                "bus_id": bus_id,
            }
        )

    async def remove_favorite(self, db: AsyncSession, user_id: str, bus_id: int):
        favorite = await self._favorite_repository.get_user_favorite(db, user_id, bus_id)
        if not favorite:
            raise NotFoundException("Favorite not found")

        await self._favorite_repository.remove_favorite(db, favorite)

    async def list_favorites(self, db: AsyncSession, user_id: str):
        return await self._favorite_repository.get_user_favorites(db, user_id)
