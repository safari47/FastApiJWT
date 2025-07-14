from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Response, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from ..celery_app.tasks.email import send_verification_email
from ..config import AccessTokenType
from ..database.dao_class import UserDAO
from .dependencies import (
    check_refresh_token,
    get_session_with_commit,
    validate_auth_user,
)
from .exceptions import UserAlreadyExistsException, UserNotFoundException
from .models import User
from .schemas import UserCreateResponse, UserEmail, UserId, UserIn, UserInDB
from .utils import hash_password, set_access_token_cookie, set_refresh_token_cookie

app = APIRouter(prefix="/auth", tags=["AuthJWT"])


@app.post(
    "/register",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    description="Регистрация пользователя",
)
async def register_user(
    user: Annotated[UserIn, Body(default=..., description="Данные пользователя")],
    session: AsyncSession = Depends(get_session_with_commit),
) -> UserCreateResponse:
    """
    Регистрация нового пользователя.
    Если пользователь с таким именем уже существует, выбрасывается исключение UserAlreadyExistsException.
    """
    logger.info(f"Проверка пользователя {user.email} на существование в базе данных")
    if user_data := await UserDAO().find_one_or_none(
        session=session, filters=UserEmail(email=user.email)
    ):
        logger.warning(f"Пользователь {user.email} уже существует")
        raise UserAlreadyExistsException

    user_data = await UserDAO().register_user(
        session=session,
        values=UserInDB(email=user.email, hashed_password=hash_password(user.password)),
    )
    # Запуск задачи отправки письма для активации
    task = send_verification_email.delay(email=user.email, user_id=user_data.id)
    logger.info(f"Пользователь {user.email} успешно зарегистрирован")
    return UserCreateResponse()


@app.post(
    "/login", status_code=status.HTTP_200_OK, description="Авторизация пользователя"
)
async def login_user(
    response: Response,
    user: UserIn = Depends(validate_auth_user),
) -> dict:
    """
    Авторизация пользователя.
    Если пользователь с таким именем не существует или пароль неверный, выбрасывается исключение
    InvalidCredentialsException.
    """
    set_access_token_cookie(response=response, user=user)
    set_refresh_token_cookie(response=response, user=user)
    return {"ok": True, "message": "Авторизация успешна!"}


@app.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response) -> dict:
    response.delete_cookie(key=AccessTokenType.ACCESS.value)
    response.delete_cookie(key=AccessTokenType.REFRESH.value)
    return {"message": "Пользователь успешно вышел из системы"}


@app.post("/refresh", status_code=status.HTTP_200_OK, description="Обновление токенов")
async def refresh_tokens(
    response: Response,
    user: User = Depends(check_refresh_token),
) -> dict:
    """
    Обновление токенов.
    Если refresh-токен не валиден, выбрасывается исключение InvalidCredentialsException.
    """
    set_access_token_cookie(response=response, user=user)
    return {"ok": True, "message": "Токены успешно обновлены!"}


@app.get("/activate", status_code=status.HTTP_200_OK, description="Активация аккаунта")
async def activate_account(
    user_id: Annotated[UserId, Query(..., description="ID пользователя")],
    session: AsyncSession = Depends(get_session_with_commit),
):
    """
    Активация аккаунта пользователя.
    """
    if (
        user_data := await UserDAO().find_one_or_none_by_id(
            session=session, data_id=user_id.id
        )
    ) and not user_data.profile.is_active:
        user_data.profile.is_active = True
        session.add(user_data)
        logger.info(f"Аккаунт пользователя {user_data.email} успешно активирован")
        return {"message": "Аккаунт успешно активирован!"}
    logger.warning(f"Пользователь с ID {user_id.id} не найден или уже активирован")
    raise UserNotFoundException
