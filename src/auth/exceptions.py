from fastapi import HTTPException, status

# Пользователь уже существует
UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)

# Пользователь не найден
UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
)

# Отсутствует идентификатор пользователя
UserIdNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Отсутствует идентификатор пользователя",
)

# Неверная почта или пароль
InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Неверная почта или пароль"
)

# Токен истек
TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
)


# Токен отсутствует в заголовке
TokenNoFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Токен отсутствует в заголовке"
)

# Невалидный JWT токен
InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный"
)
