from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import get_session_with_commit
from ..auth.models import User
from ..auth.schemas import UserId
from ..database.dao_class import ProfileDAO
from .dependencies import get_current_user
from .schemas import Profile, SUserInfo

router = APIRouter(tags=["Users"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    description="Получение информации о текущем пользователе",
    response_model=SUserInfo,
)
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    return SUserInfo.model_validate(user_data)


@router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    description="Обновление информации о текущем пользователе",
    response_model=SUserInfo,
)
async def update_me(
    profile: Profile,
    user_data: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit),
) -> SUserInfo:
    user_data = await ProfileDAO().update_profile(
        session=session, filters=UserId(id=user_data.id), values=profile
    )
    return SUserInfo.model_validate(user_data)
