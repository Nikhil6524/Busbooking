from fastapi import APIRouter, Depends, Request

from src.api.rest.dependencies import get_current_user

router = APIRouter(
    prefix="",
    tags=["Profile"]
)


@router.get("/profile")
async def profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "JWT Verified Successfully",
        "user": current_user
    }


@router.get("/profile/token")
async def profile_token(
    request: Request,
    current_user=Depends(get_current_user)
):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else ""

    return {
        "message": "JWT Received Successfully",
        "token": token,
        "user": current_user
    }