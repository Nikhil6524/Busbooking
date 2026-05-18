from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.config.settings import settings
from src.schemas.auth_schema import TokenPayload, UserLogin, UserRegister
from src.core.exceptions.auth_exception import AuthenticationException
from src.data.repositories.user_repository import UserRepository

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class AuthService:

    def __init__(self) -> None:
        self.user_repository = UserRepository()

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    @staticmethod
    def create_access_token(
        user_id: str,
        role: str
    ) -> str:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": user_id,
            "role": role,
            "exp": expire
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def verify_access_token(token: str) -> TokenPayload:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            return TokenPayload(**payload)

        except JWTError:
            raise AuthenticationException(
                "Invalid or expired token"
            )

    async def register_user(self, db, user_data: UserRegister):
        existing_user = await self.user_repository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise AuthenticationException(
                "User already exists"
            )

        user_payload = user_data.model_dump(exclude={"password"})
        user_payload["password_hash"] = self.hash_password(
            user_data.password
        )

        user = await self.user_repository.create_user(
            db,
            user_payload
        )

        token = self.create_access_token(
            str(user.id),
            user.role
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    async def login_user(self, db, login_data: UserLogin):
        user = await self.user_repository.get_by_email(
            db,
            login_data.email
        )

        if not user:
            raise AuthenticationException(
                "Invalid credentials"
            )

        if not self.verify_password(
            login_data.password,
            user.password_hash
        ):
            raise AuthenticationException(
                "Invalid credentials"
            )

        token = self.create_access_token(
            str(user.id),
            user.role
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }