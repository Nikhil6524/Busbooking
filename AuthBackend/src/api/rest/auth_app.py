from fastapi import FastAPI

from src.api.middleware.auth import JWTAuthMiddleware
from src.api.rest.routes.auth import router as auth_router
from src.api.rest.routes.health import router as health_router

app = FastAPI(
    title="Authentication Service"
)

app.add_middleware(JWTAuthMiddleware)

app.include_router(health_router)
app.include_router(auth_router)
