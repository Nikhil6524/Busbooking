from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import httpx

from src.config.settings import settings


class AuthProxyMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, auth_service_url: str | None = None) -> None:
        super().__init__(app)
        base_url = auth_service_url or settings.AUTH_SERVICE_URL
        self.auth_service_url = base_url.rstrip("/")

    async def dispatch(self, request: Request, call_next):
        public_routes = [
            "/",
            "/health",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]

        if request.url.path in public_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        cookie_token = request.cookies.get("access_token")

        if (not auth_header or not auth_header.startswith("Bearer ")) and cookie_token:
            auth_header = f"Bearer {cookie_token}"

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization token missing"}
            )

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.auth_service_url}/auth/me",
                    headers={"Authorization": auth_header}
                )
        except httpx.RequestError:
            return JSONResponse(
                status_code=503,
                content={"detail": "Auth service unavailable"}
            )

        if response.status_code != 200:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized"}
            )

        data = response.json() if response.content else {}
        user = data.get("user")

        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized"}
            )

        request.state.user = user

        return await call_next(request)
