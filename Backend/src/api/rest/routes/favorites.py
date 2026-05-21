from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import get_current_user
from src.core.exceptions import UnauthorizedException
from src.core.services.favorite_service import FavoriteService
from src.data.clients.postgres import get_db
from src.schemas.favorite_schema import FavoriteCreate

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)

favorite_service = FavoriteService()


@router.post("")
async def add_favorite(
    payload: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    return await favorite_service.add_favorite(db, user_id, payload.bus_id)


@router.delete("/{bus_id}")
async def remove_favorite(
    bus_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    await favorite_service.remove_favorite(db, user_id, bus_id)
    return {"message": "Favorite removed"}


@router.get("")
async def list_favorites(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    return await favorite_service.list_favorites(db, user_id)
