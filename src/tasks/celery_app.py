from celery import Celery

from src.config import settings


celery_instance = Celery(
    main="task",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ],
)


celery_instance.conf.beat_schedule = {
    "luboe_nazvanie": {
        "task": "booking_today_checking",
        "schedule": 5
    }
}