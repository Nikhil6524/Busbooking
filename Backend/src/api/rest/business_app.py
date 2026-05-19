from fastapi import FastAPI

from src.api.middleware.auth_proxy import AuthProxyMiddleware
from src.api.rest.routes.admin import router as admin_router
from src.api.rest.routes.health import router as health_router
from src.api.rest.routes.profile import router as profile_router
from src.api.rest.routes.bookings import router as bookings_router
from src.api.rest.routes.buses import router as buses_router

app = FastAPI(
    title="Business Service"
)

app.add_middleware(AuthProxyMiddleware)

app.include_router(health_router)
app.include_router(profile_router)
app.include_router(admin_router)
app.include_router(bookings_router)
app.include_router(buses_router)
