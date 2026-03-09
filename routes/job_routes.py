from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from models.job_model import Job
from schemas.job_schema import ExternalJobSave, JobCreate, JobResponse
from services.match_service import calculate_match, extract_job_skills
from services.resume_service import extract_resume_text, extract_skills
from utils.dependencies import get_db, get_current_user
from services.job_search_service import search_jobs
from core.limiter import limiter
from fastapi import Request
from utils.logger import logger
from services.ai_service import analyze_resume_match
from tasks.job_tasks import discover_jobs_task
from celery.result import AsyncResult
from core.celery_app import celery


router = APIRouter()

# Create a new job
@router.post("", response_model=JobResponse)
@limiter.limit("20/minute")
def create_job(
    request: Request,
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} creating job {job.title}")

    new_job = Job(
        title=job.title,
        company=job.company,
        status=job.status,
        description=job.description,
        user_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

# Match resume to a specific job
@router.get("/{job_id}/match")
@limiter.limit("20/minute")
def match_resume_to_job(
    request: Request,
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    resume_text = extract_resume_text(resume_path)

    resume_skills = extract_skills(resume_text)

    job_skills = extract_job_skills(job.description)

    result = calculate_match(resume_skills, job_skills)

    analysis = analyze_resume_match(resume_skills, job.description)

    return {
        "job": job.title,
        "company": job.company,
        "match_score": result["score"],
        "matching_skills": result["matching_skills"],
        "missing_skills": result["missing_skills"],
        "ai_analysis": analysis
    }

# Get job recommendations based on resume
@router.get("/recommendations")
@limiter.limit("20/minute")
def get_recommendations(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    resume_text = extract_resume_text(resume_path)

    resume_skills = extract_skills(resume_text)

    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()

    recommendations = []

    for job in jobs:

        job_skills = extract_job_skills(job.description)

        result = calculate_match(resume_skills, job_skills)

        recommendations.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "score": result["score"]
        })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations


# Search and match jobs from external API (used by analytics service)
@router.get("/discover")
@limiter.limit("20/minute")
def discover_jobs(
    request: Request,
    keyword: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

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
            "match_score": match["score"],
            "missing_skills": match["missing_skills"],
            "url": job["url"]
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return results[:10]

@router.post("/discover-background")
def discover_background(
    request: Request,
    keyword: str,
    current_user: User = Depends(get_current_user)
):

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    task = discover_jobs_task.delay(resume_path, keyword, current_user.id)

    return {"task_id": task.id}

@router.get("/task/{task_id}")
def get_task_result(task_id: str):

    task = AsyncResult(task_id,  app=celery)

    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }

#search jobs from remotive api
@router.get("/search")
@limiter.limit("20/minute")
def search_jobs_api(request: Request, keyword: str):
    logger.info(f"External job search for keyword: {keyword}")
    jobs = search_jobs(keyword)

    return jobs

# Search and match jobs from external API
@router.get("/search-match")
@limiter.limit("20/minute")
def search_and_match(
    request: Request,
    keyword: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

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
            "match_score": match["score"],
            "url": job["url"]
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return results

# Save external job to user's job list
@router.post("/save-external", response_model=JobResponse)
@limiter.limit("20/minute")
def save_external_job(
    request: Request,
    job: ExternalJobSave,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_job = Job(
        title=job.title,
        company=job.company,
        description=job.description,
        status="Saved",
        user_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

# Get user's jobs with optional filtering and pagination
@router.get("", response_model=list[JobResponse])
@limiter.limit("20/minute")
def get_jobs(
    request: Request,
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Job).filter(Job.user_id == current_user.id)

    # filtering
    if status:
        query = query.filter(Job.status == status)

    # pagination
    jobs = query.offset((page - 1) * limit).limit(limit).all()

    return jobs