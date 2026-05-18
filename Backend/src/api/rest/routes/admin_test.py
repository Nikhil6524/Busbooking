from fastapi import APIRouter, Depends

from src.api.rest.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin Test"]
)


@router.get("/test")
async def admin_test(
    admin=Depends(require_admin)
):
    return {
        "message": "Admin authorization successful",
        "admin": admin
    }