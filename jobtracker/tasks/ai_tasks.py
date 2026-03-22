from core.celery_app import celery
from services.ai_service import analyze_resume_match


@celery.task
def analyze_resume_ai_task(resume_skills, job_description):

    result = analyze_resume_match(resume_skills, job_description)

    return result