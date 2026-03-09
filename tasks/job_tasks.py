from core.celery_app import celery
from database import SessionLocal
from models.job_model import Job
from models.user_model import User
from services.job_search_service import search_jobs
from services.resume_service import extract_resume_text, extract_skills
from services.match_service import extract_job_skills, calculate_match


@celery.task
def discover_jobs_task(resume_path, keyword, user_id):

    db = SessionLocal()

    resume_text = extract_resume_text(resume_path)
    resume_skills = extract_skills(resume_text)

    jobs = search_jobs(keyword)

    saved = []

    for job in jobs:
        existing = db.query(Job).filter(Job.job_url == job["url"]).first()
        if existing:
            continue

        job_skills = extract_job_skills(job["description"])

        match = calculate_match(resume_skills, job_skills)

        new_job = Job(
            title=job["title"],
            company=job["company"],
            description=job["description"],
            job_url=job["url"],
            status="discovered",
            user_id=user_id
    )

    db.add(new_job)

    saved.append(job["title"])

    db.commit()
    db.close()

    return saved