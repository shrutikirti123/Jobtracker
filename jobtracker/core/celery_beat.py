from core.celery_app import celery

celery.conf.beat_schedule = {
    "discover-jobs-every-6-hours": {
        "task":                     "tasks.job_tasks.discover_jobs_for_all_users",
        "schedule": 21600,
        "args": ("resumes/1_shruti_resume.pdf", "python")
    }
}