import datetime
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Request, Response

from ..config import AccessTokenType, settings
from .exceptions import InvalidTokenException, TokenExpiredException, TokenNoFound
from .models import User
from .schemas import BaseUser


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()  # Генерируем соль для хеширования пароля
    pwd_bytes: bytes = password.encode()  # Преобразуем пароль в байты
    return bcrypt.hashpw(
        pwd_bytes, salt
    )  # Хешируем пароль с использованием сгенерированной соли


def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed.encode()
    )  # Проверяем, соответствует ли введенный пароль хешу


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),  # Путь к приватному ключу для подписи JWT
    algorithm: str = settings.auth_jwt.algorithm,  # Алгоритм подписи JWT (например, "RS256")
    expire_timedelta: timedelta = timedelta(
        minutes=settings.auth_jwt.access_token_expire_minutes
    ),  # Время жизни токена в минутах
    jwt_type: str = AccessTokenType.ACCESS_TYPE,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)  # Текущее время в формате UTC
    expire = (
        now + expire_timedelta
    )  # Время истечения токена, добавляемое к текущему времени
    to_encode.update(
        {
            "exp": expire,  # Время истечения токена
            "iat": now,  # Время создания токена
            "jti": str(uuid.uuid4()),  # Уникальный идентификатор токена
            "sub": payload.get("id"),  # Субъект токена, идентификатор пользователя
            "iss": "fastapi-auth",  # Издатель токена (может быть имя вашего приложения)
            "type": jwt_type,
        }
    )
    encoded = jwt.encode(
        payload=to_encode, key=private_key, algorithm=algorithm
    )  # Кодируем JWT с использованием приватного ключа и указанного алгоритма
    return encoded


def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    try:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
            options={"require_exp": True, "verify_signature": True},
        )  # Декодируем JWT с использованием публичного ключа и указанного алгоритма
        return decoded
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except jwt.InvalidTokenError:
        raise InvalidTokenException


def set_access_token_cookie(response: Response, user: BaseUser) -> None:
    jwt_payload = encode_jwt(payload=user.model_dump())
    response.set_cookie(
        key=AccessTokenType.ACCESS.value,
        value=jwt_payload,
        httponly=True,
        # secure=True,
        samesite="lax",
    )


def set_refresh_token_cookie(response: Response, user: BaseUser) -> None:
    jwt_payload = encode_jwt(
        payload={"id": user.id},
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
        jwt_type=AccessTokenType.REFRESH_TYPE,
    )
    response.set_cookie(
        key=AccessTokenType.REFRESH.value,
        value=jwt_payload,
        httponly=True,
        # secure=True,
        samesite="lax",
    )


def get_access_token(request: Request) -> str:
    """Извлекаем access_token из кук."""
    token = request.cookies.get(AccessTokenType.ACCESS.value)
    if not token:
        raise TokenNoFound
    return token


def get_refresh_token(request: Request) -> str:
    """Извлекаем refresh_token из кук."""
    token = request.cookies.get(AccessTokenType.REFRESH.value)
    if not token:
        raise TokenNoFound
    return token
