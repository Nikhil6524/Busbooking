from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str  
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    ADMIN_EMAIL: str
    class Config:
        env_file = ".env"  

settings = Settings() 