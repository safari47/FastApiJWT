from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserId(BaseModel):
    id: str = Field(
        ...,
        description="Уникальный идентификатор пользователя",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class UserEmail(BaseModel):
    email: EmailStr = Field(
        ..., description="Email пользователя", example="users@example.com"
    )
    model_config = ConfigDict(from_attributes=True)


class UserPwd(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Пароль пользователя",
        example="strongpassword123",
    )


class UserIn(UserPwd, UserEmail):
    pass


class UserInDB(UserEmail):
    hashed_password: str = Field(
        ...,
        description="Хешированный пароль пользователя",
        example="$2b$12$KIX9z5Z1e8f3a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u",
    )


class BaseUser(UserEmail, UserId):
    pass


class UserCreateResponse(BaseModel):
    detail: str = Field(
        default="Пользователь успешно создан",
        description="Сообщение об успешном создании пользователя",
    )
