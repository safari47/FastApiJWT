from loguru import logger
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.models import Profile, User
from .dao import BaseDAO


class UserDAO(BaseDAO):
    model = User

    async def register_user(self, session: AsyncSession, values: BaseModel):
        # Регистрация нового пользователя
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(
            f"Добавление записи {self.model.__name__} с параметрами: {values_dict}"
        )
        try:
            new_instance = self.model(**values_dict)
            session.add(new_instance)
            logger.info(f"Запись {self.model.__name__} успешно добавлена.")
            await session.flush()
            profile = Profile(id=new_instance.id)
            session.add(profile)
            return new_instance

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise


class ProfileDAO(BaseDAO):
    model = Profile

    async def update_profile(
        self, session: AsyncSession, filters: BaseModel, values: BaseModel
    ):
        # Обновление профиля пользователя
        filter_dict = filters.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(
            f"Обновление профиля {self.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}"
        )
        try:
            query = (
                update(self.model)
                .where(*[getattr(self.model, k) == v for k, v in filter_dict.items()])
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            await session.flush()
            user = await UserDAO().find_one_or_none_by_id(
                session, data_id=filter_dict["id"]
            )
            return user
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении профиля: {e}")
            raise
