from core.celery_app import celery
from services.job_search_service import search_jobs
from services.match_service import extract_job_skills, calculate_match
from services.resume_service import extract_resume_text, extract_skills


@celery.task
def discover_jobs_task(resume_path: str, keyword: str):

    resume_text = extract_resume_text(resume_path)

    resume_skills = extract_skills(resume_text)

    jobs = search_jobs(keyword)

    results = []

    for job in jobs:

        job_skills = extract_job_skills(job["description"])

        match = calculate_match(resume_skills, job_skills)

        results.append({
            "title": job["title"],
            "company": job["company"],
            "score": match["score"],
            "url": job["url"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:10]