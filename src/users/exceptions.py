from fastapi import HTTPException, status

# Пользователь не найден
UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
)

# Отсутствует идентификатор пользователя
UserIdNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Отсутствует идентификатор пользователя",
)


# Токен истек
TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
)


# Невалидный JWT токен
InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный"
)


# Недостаточно прав
ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав"
)
