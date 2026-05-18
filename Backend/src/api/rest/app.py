from fastapi import FastAPI

from src.api.middleware.auth import JWTAuthMiddleware
from src.api.rest.routes.profile import router as profile_router
from src.api.rest.routes.admin_test import router as admin_test_router

app = FastAPI(
    title="Bus Booking Backend"
)

app.add_middleware(JWTAuthMiddleware)

app.include_router(profile_router)
app.include_router(admin_test_router)