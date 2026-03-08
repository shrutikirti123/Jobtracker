from core.celery_app import celery
from services.resume_service import extract_resume_text, extract_skills

@celery.task
def process_resume(file_path):

    text = extract_resume_text(file_path)
    skills = extract_skills(text)

    return skills