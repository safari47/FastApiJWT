from fastapi import Depends
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_session_without_commit
from ..auth.schemas import UserId
from ..auth.utils import decode_jwt, get_access_token
from ..database.dao_class import UserDAO
from .exceptions import (
    InvalidTokenException,
    TokenExpiredException,
    UserIdNotFoundException,
    UserNotFoundException,
)


async def get_current_user(
    token: str = Depends(get_access_token),
    session: AsyncSession = Depends(get_session_without_commit),
):
    try:
        payload = decode_jwt(token=token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except PyJWTError:
        raise InvalidTokenException
    if not (user_id := payload.get("sub")):
        raise UserIdNotFoundException
    if not (
        user := await UserDAO().find_one_or_none(
            session=session, filters=UserId(id=user_id)
        )
    ):
        raise UserNotFoundException
    return user
