from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.middleware.auth_proxy import AuthProxyMiddleware
from src.api.rest.routes.admin import router as admin_router
from src.api.rest.routes.health import router as health_router
from src.api.rest.routes.profile import router as profile_router
from src.api.rest.routes.bookings import router as bookings_router
from src.api.rest.routes.buses import router as buses_router
from src.api.rest.routes.favorites import router as favorites_router
from src.api.rest.routes.routes import router as routes_router
from src.api.rest.routes.schedules import router as schedules_router
from src.core.exceptions import register_exception_handlers

app = FastAPI(
    title="Business Service"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.add_middleware(AuthProxyMiddleware)

app.include_router(health_router)
app.include_router(profile_router)
app.include_router(admin_router)
app.include_router(bookings_router)
app.include_router(buses_router)
app.include_router(favorites_router)
app.include_router(routes_router)
app.include_router(schedules_router)
