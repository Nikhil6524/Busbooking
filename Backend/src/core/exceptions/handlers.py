from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.exceptions.base import AppException
from src.schemas.error_schema import ErrorResponse, ValidationErrorResponse


def register_exception_handlers(app) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        payload = ErrorResponse(detail=exc.detail).model_dump()
        return JSONResponse(
            status_code=exc.status_code,
            content=payload
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        payload = ErrorResponse(detail=str(exc.detail)).model_dump()
        return JSONResponse(
            status_code=exc.status_code,
            content=payload
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        payload = ValidationErrorResponse(detail=exc.errors()).model_dump()
        return JSONResponse(
            status_code=422,
            content=payload
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        payload = ErrorResponse(detail="Internal server error").model_dump()
        return JSONResponse(
            status_code=500,
            content=payload
        )
