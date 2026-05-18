from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.clients.postgres import get_db
from src.schemas.auth_schema import (
    UserRegister,
    UserLogin
)
from src.core.services.auth_service import AuthService
from src.api.rest.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service = AuthService()


@router.post("/register")
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await auth_service.register_user(
            db,
            user_data
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
async def login_user(
    login_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    try:
        token_payload = await auth_service.login_user(
            db,
            login_data
        )

        response.set_cookie(
            key="access_token",
            value=token_payload["access_token"],
            httponly=True,
            samesite="lax",
            path="/"
        )

        return token_payload

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user)
):
    return {
        "message": "JWT Verified",
        "user": current_user
    }


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )

    return {
        "message": "Logged out"
    }
