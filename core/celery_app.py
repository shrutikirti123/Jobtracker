from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "jobtracker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.job_tasks"]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery.conf.beat_schedule = {
    "discover-jobs-every-6-hours": {
        "task": "tasks.job_tasks.discover_jobs_for_all_users",
        "schedule": 21600,
    }
}