from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from src.auth.router import app as auth_router
from src.database.database import create_tables
from src.users.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    logger.info(f"Creating database tables")
    await create_tables()
    logger.info("Database tables created successfully")
    yield
    logger.info("Stopping application...")


templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


app = FastAPI(title="My FastAPI", version="1.0.0", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)


# Маршрут для отображения главной страницы
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Формируем кастомный ответ
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Ошибка валидации данных",
            "details": exc.errors(),  # Список ошибок валидации
            "body": exc.body,  # Тело запроса, которое вызвало ошибку
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
