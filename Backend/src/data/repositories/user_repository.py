from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.data.models.postgres.user import User

class UserRepository:

    async def create_user(self, session: AsyncSession, user_data: dict) -> User:
        user = User(**user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_phone(self, db: AsyncSession, phone: str):
        result = await db.execute(
            select(User).where(User.phone == phone)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id):
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()