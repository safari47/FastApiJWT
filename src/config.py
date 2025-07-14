from enum import Enum
from pathlib import Path

from loguru import logger
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AuthJwt(BaseModel):
    private_key_path: Path = Path(__file__).parent / "certs" / "jwt-private.pem"
    public_key_path: Path = Path(__file__).parent / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3
    refresh_token_expire_days: int = 1


class AccessTokenType(str, Enum):
    ACCESS = "access_token_jwt"
    ACCESS_TYPE = "access"
    REFRESH = "refresh_token_jwt"
    REFRESH_TYPE = "refresh"


class Settings(BaseSettings):
    DB_URL: str = f"sqlite+aiosqlite:///db.sqlite3"
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    BASE_URL: str = "http://localhost:8000"
    REDIS_URL: str = "redis://redis:6379/0"
    auth_jwt: AuthJwt = AuthJwt()


# Получаем параметры для загрузки переменных среды
settings = Settings()

logger.add(
    sink="app.log",
    format=settings.FORMAT_LOG,
    level="INFO",
    rotation=settings.LOG_ROTATION,
)
