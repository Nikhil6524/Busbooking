from sqlalchemy import select

from src.data.models.postgres.favourite import Favorite


class FavoriteRepository:

    async def add_favorite(self, db, favorite_data):
        favorite = Favorite(**favorite_data)
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)
        return favorite

    async def get_user_favorite(self, db, user_id, bus_id):
        result = await db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.bus_id == bus_id
            )
        )
        return result.scalar_one_or_none()

    async def remove_favorite(self, db, favorite):
        await db.delete(favorite)
        await db.commit()
        return favorite

    async def get_user_favorites(self, db, user_id):
        result = await db.execute(
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
        )
        return result.scalars().all()