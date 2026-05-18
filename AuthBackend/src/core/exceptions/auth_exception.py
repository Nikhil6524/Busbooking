class AuthException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidCredentialsException(AuthException):
    pass


class UserAlreadyExistsException(AuthException):
    pass


class InvalidTokenException(AuthException):
    pass


class ForbiddenAccessException(AuthException):
    pass
