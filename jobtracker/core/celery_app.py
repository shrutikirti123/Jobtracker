from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "jobtracker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.job_tasks", "tasks.ai_tasks"]
)

celery.conf.task_routes = {
    "tasks.*": {"queue": "default"}
}