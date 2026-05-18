from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.core.services.auth_service import AuthService


class JWTAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        public_routes = [
            "/",
            "/auth/login",
            "/auth/register",
            "/auth/logout",
            "/health",
            "/docs",
            "/openapi.json",
            "/redoc"
        ]

        if request.url.path in public_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization token missing"}
            )

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_access_token(token)

            request.state.user = {
                "user_id": payload.sub,
                "role": payload.role
            }

        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": str(e)}
            )

        return await call_next(request)
