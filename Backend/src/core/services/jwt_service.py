from jose import jwt, JWTError

from src.config.settings import settings


class JWTService:

    @staticmethod
    def verify_access_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            return {
                "user_id": payload.get("sub"),
                "role": payload.get("role")
            }

        except JWTError:
            raise Exception("Invalid or expired token")