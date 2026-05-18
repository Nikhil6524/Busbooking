from sqlalchemy import select
from data.models.postgres.favourite import Favorite


class FavoriteRepository:

    async def add_favorite(self, db, favorite_data):
        favorite = Favorite(**favorite_data)
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)
        return favorite

    async def get_user_favorites(self, db, user_id):
        result = await db.execute(
            select(Favorite).where(Favorite.user_id == user_id)
        )
        return result.scalars().all()