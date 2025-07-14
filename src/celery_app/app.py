from celery import Celery

from ..config import settings

celery = Celery(
    "src.celery_app.app",
    backend=settings.REDIS_URL,
    broker=settings.REDIS_URL,
    include=["src.celery_app.tasks.email"],
)

