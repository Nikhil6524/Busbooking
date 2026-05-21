class AppException(Exception):
    def __init__(self, detail: str, status_code: int) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class BadRequestException(AppException):
    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(detail, 400)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(detail, 401)


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(detail, 403)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(detail, 404)


class ConflictException(AppException):
    def __init__(self, detail: str = "Conflict") -> None:
        super().__init__(detail, 409)


class ServiceUnavailableException(AppException):
    def __init__(self, detail: str = "Service unavailable") -> None:
        super().__init__(detail, 503)
