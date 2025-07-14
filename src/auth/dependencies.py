from typing import AsyncGenerator

from fastapi import Depends
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.dao_class import UserDAO
from ..database.database import async_session_maker
from .exceptions import (
    InvalidCredentialsException,
    TokenExpiredException,
    UserIdNotFoundException,
    UserNotFoundException,
)
from .schemas import BaseUser, UserEmail, UserId, UserIn
from .utils import check_password, decode_jwt, get_refresh_token


async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия с автоматическим коммитом."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия без автоматического коммита."""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def validate_auth_user(
    user: UserIn, session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    logger.info(f"Проверка пользователя {user.email} на существование в базе данных")
    if not (
        user_data := await UserDAO().find_one_or_none(
            session=session, filters=UserEmail(email=user.email)
        )
    ):
        logger.warning(f"Пользователь {user.email} не найден")
        raise InvalidCredentialsException
    logger.info(f"Пользователь {user_data.email} найден, проверка пароля ")
    if not check_password(password=user.password, hashed=user_data.hashed_password):
        logger.warning(f"Неверный пароль для пользователя {user.email}")
        raise InvalidCredentialsException
    logger.info(f"Пользователь {user.email} успешно аутентифицирован")
    return BaseUser.model_validate(user_data)


async def check_refresh_token(
    token: str = Depends(get_refresh_token),
    session: AsyncSession = Depends(get_session_without_commit),
) -> BaseUser:
    """
    Проверка refresh-токена.
    Если токен не валиден, выбрасывается исключение InvalidCredentialsException.
    """
    try:
        payload = decode_jwt(token=token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except PyJWTError:
        raise InvalidCredentialsException
    if not (user_id := payload.get("sub")):
        raise UserIdNotFoundException
    if not (
        user := await UserDAO().find_one_or_none(
            session=session, filters=UserId(id=user_id)
        )
    ):
        raise UserNotFoundException
    return BaseUser.model_validate(user)
