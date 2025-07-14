# FastAPI JWT Auth

![JWT Auth](https://img.shields.io/badge/JWT-Auth-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-009485)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

Современное FastAPI приложение с полной JWT-авторизацией, асинхронными задачами и подтверждением аккаунтов по email.

## 🚀 Возможности

- **JWT Авторизация**: Безопасная аутентификация с использованием RSA ключей
- **Email верификация**: Подтверждение регистрации по электронной почте
- **Celery + Redis**: Асинхронная обработка задач для отправки писем
- **SQLAlchemy ORM**: Асинхронная работа с базой данных
- **Docker интеграция**: Быстрый запуск и развертывание
- **Интерактивная обучающая игра**: Изучите JWT авторизацию через веб-интерфейс

## ⚡ Интерактивная обучающий квест

Проект включает интерактивный веб-интерфейс, который пошагово обучает принципам работы JWT-авторизации:

- Регистрация пользователя
- Вход в систему и получение токенов
- Работа с защищенными ресурсами
- Обновление и инвалидация токенов
- Выход из системы

Доступно по адресу: **http://localhost:8000/** после запуска приложения.

## 🛠️ Технологии

- [**FastAPI**](https://fastapi.tiangolo.com/) - Современный веб-фреймворк
- [**Celery**](https://docs.celeryq.dev/) - Асинхронные задачи
- [**Redis**](https://redis.io/) - Брокер сообщений и хранилище
- [**SQLAlchemy**](https://www.sqlalchemy.org/) - SQL ORM
- [**PyJWT**](https://pyjwt.readthedocs.io/) - Работа с JWT токенами
- [**MailDev**](https://maildev.github.io/maildev/) - SMTP сервер для разработки

## 🏃‍♂️ Быстрый старт

# Запуск через Docker Compose

## Клонировать репозиторий
```bash
git clone https://github.com/your-username/fastapi-jwt-auth.git
cd fastapi-jwt-auth
```

## Сгенерировать public + private key и поместить в папку certs
```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

## Запустить контейнеры
```bash
docker compose up -d
```

После запуска будут доступны:

- **API**: [http://localhost:8000](http://localhost:8000)
- **Документация**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Обучающий интерфейс**: [http://localhost:8000/](http://localhost:8000/)
- **Отладка email**: [http://localhost:8080](http://localhost:8080)
- **Мониторинг Celery**: [http://localhost:5556](http://localhost:5556)

# Локальный запуск для разработки


## Создать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# venv\Scripts\activate  # Windows
```

## Установить зависимости
```bash
pip install -r requirements.txt
```

## Запустить Redis
```bash
docker run -d -p 6379:6379 redis:7.2
```

## Запустить MailDev
```bash
docker run -d -p 8080:1080 -p 1025:1025 maildev/maildev
```

## Запустить API
```bash
uvicorn src.main:app --reload
```

## Запустить Celery worker
```bash
celery --app src.celery_app.app worker --pool threads --loglevel INFO
```

## Запустить Flower для мониторинга
```bash
celery --app src.celery_app.app flower
```

## 📝 Основные API эндпоинты

### Аутентификация

- `POST /auth/register` - Регистрация нового пользователя
- `GET /auth/activate` - Активация аккаунта
- `POST /auth/login` - Вход в систему
- `POST /auth/refresh` - Обновление токена
- `POST /auth/logout` - Выход из системы

### Пользователи

- `GET /me` - Получение информации о текущем пользователе
- `PATCH /me` - Обновление профиля пользователя

Разработано с ❤️ на FastAPI и Celery. Делитесь своими мыслями и открывайте issues!

<img src="/image/1" style="display: block; margin: auto;">
<img src="/image/2" style="display: block; margin: auto;">
<img src="/image/3" style="display: block; margin: auto;">
<img src="/image/4" style="display: block; margin: auto;">
<img src="/image/5" style="display: block; margin: auto;">
<img src="/image/6" style="display: block; margin: auto;">
<img src="/image/7" style="display: block; margin: auto;">
<img src="/image/8" style="display: block; margin: auto;">


