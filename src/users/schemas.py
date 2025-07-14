from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from ..auth.schemas import BaseUser


class Profile(BaseModel):
    username: str | None = Field(..., example='user123' ,description="Уникальное имя пользователя")
    bio: str | None = Field(..., example='Junior Python Backend Developer',description="Краткая информация о пользователе")
    is_active: bool | None = Field(...,example=True ,description="Статус активности пользователя")
    birthday: date | None = Field(..., example='1990-01-01', description="Дата рождения пользователя")
    phone_number: str | None = Field(..., example='+79051234567', description="Номер телефона пользователя")
    model_config = ConfigDict(from_attributes=True)


class SUserInfo(BaseUser):
    profile: Profile = Field(
        None, description="Профиль пользователя, содержащий дополнительную информацию"
    )
