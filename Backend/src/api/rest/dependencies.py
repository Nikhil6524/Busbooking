from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.data.clients.postgres import get_db
from src.data.repositories.user_repository import UserRepository


def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return request.state.user


async def require_admin(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user = get_current_user(request)
    user_id = user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    repo = UserRepository()
    db_user = await repo.get_by_id(db, user_id)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if db_user.email.lower() != settings.ADMIN_EMAIL.lower():
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return db_user