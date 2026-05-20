from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import get_current_user
from src.core.exceptions import (
    UnauthorizedException,
    NotFoundException,
    ConflictException
)
from src.data.clients.postgres import get_db
from src.data.models.postgres.bus import Bus
from src.data.repositories.favorite_repository import FavoriteRepository
from src.schemas.favorite_schema import FavoriteCreate

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)

favorite_repository = FavoriteRepository()


@router.post("")
async def add_favorite(
    payload: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    bus_result = await db.execute(
        select(Bus).where(Bus.id == payload.bus_id)
    )
    bus = bus_result.scalar_one_or_none()
    if not bus:
        raise NotFoundException("Bus not found")

    existing = await favorite_repository.get_user_favorite(
        db,
        user_id,
        payload.bus_id
    )
    if existing:
        raise ConflictException("Favorite already exists")

    return await favorite_repository.add_favorite(
        db,
        {
            "user_id": user_id,
            "bus_id": payload.bus_id
        }
    )


@router.delete("/{bus_id}")
async def remove_favorite(
    bus_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    favorite = await favorite_repository.get_user_favorite(db, user_id, bus_id)
    if not favorite:
        raise NotFoundException("Favorite not found")

    await favorite_repository.remove_favorite(db, favorite)
    return {"message": "Favorite removed"}


@router.get("")
async def list_favorites(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise UnauthorizedException()

    return await favorite_repository.get_user_favorites(db, user_id)
