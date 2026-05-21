from fastapi import FastAPI

from src.api.middleware.auth import JWTAuthMiddleware
from src.api.rest.routes.profile import router as profile_router
from src.api.rest.routes.admin_test import router as admin_test_router
from src.api.rest.routes.bookings import router as bookings_router
from src.api.rest.routes.favorites import router as favorites_router
from src.api.rest.routes.routes import router as routes_router
from src.api.rest.routes.schedules import router as schedules_router
from src.core.exceptions import register_exception_handlers

app = FastAPI(
    title="Bus Booking Backend"
)

register_exception_handlers(app)

app.add_middleware(JWTAuthMiddleware)

app.include_router(profile_router)
app.include_router(admin_test_router)
app.include_router(bookings_router)
app.include_router(favorites_router)
app.include_router(routes_router)
app.include_router(schedules_router)