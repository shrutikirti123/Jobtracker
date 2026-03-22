from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.user_model import User
from models.job_model import Job
from schemas.job_schema import JobCreate, JobResponse, ExternalJobSave
from services.match_service import calculate_match, extract_job_skills
from services.resume_service import extract_resume_text, extract_skills
from services.job_search_service import search_jobs
from tasks.ai_tasks import analyze_resume_ai_task
from tasks.job_tasks import discover_jobs_task
from utils.dependencies import get_db, get_current_user
from utils.logger import logger
from core.limiter import limiter
from core.celery_app import celery
from celery.result import AsyncResult

router = APIRouter()

# ----------------------------
# Create Job
# ----------------------------
@router.post("", response_model=JobResponse)
@limiter.limit("20/minute")
def create_job(
    request: Request,
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_job = Job(
        title=job.title,
        company=job.company,
        description=job.description,
        status=job.status,
        user_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# ----------------------------
# Get Jobs
# ----------------------------
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

    if status:
        query = query.filter(Job.status == status)

    jobs = query.offset((page - 1) * limit).limit(limit).all()

    return jobs


# ----------------------------
# Discover Jobs
# ----------------------------
@router.get("/discover")
@limiter.limit("20/minute")
def discover_jobs(
    request: Request,
    keyword: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not keyword:
        return []

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    try:
        resume_text = extract_resume_text(resume_path)
        resume_skills = extract_skills(resume_text)
    except:
        resume_skills = []

    try:
        jobs = search_jobs(keyword)
    except Exception as e:
        logger.error(f"Job search failed: {e}")
        return []

    results = []

    for job in jobs:

        job_skills = extract_job_skills(job.get("description", ""))

        match = calculate_match(resume_skills, job_skills)

        results.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "description": job.get("description"),
            "match_score": match["score"],
            "missing_skills": match["missing_skills"],
            "url": job.get("url")
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return results[:10]


# ----------------------------
# Save External Job
# ----------------------------
@router.post("/save-external", response_model=JobResponse)
def save_external_job(
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


# ----------------------------
# Background Discovery
# ----------------------------
@router.post("/discover-background")
def discover_background(
    request: Request,
    keyword: str,
    current_user: User = Depends(get_current_user)
):

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    task = discover_jobs_task.delay(resume_path, keyword, current_user.id)

    return {"task_id": task.id}


# ----------------------------
# Celery Task Status
# ----------------------------
@router.get("/task/{task_id}")
def get_task_result(task_id: str):

    task = AsyncResult(task_id, app=celery)

    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }

# ----------------------------
# Match Resume to Job
# ----------------------------
@router.get("/{job_id}/match")
def match_resume_to_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    try:
        resume_text = extract_resume_text(resume_path)
        resume_skills = extract_skills(resume_text)
    except:
        resume_skills = []

    job_skills = extract_job_skills(job.description)

    result = calculate_match(resume_skills, job_skills)

    return {
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "match_score": result["score"],
        "matching_skills": result["matching_skills"],
        "missing_skills": result["missing_skills"]
    }

# ----------------------------
# Dynamic Routes (LAST)
# ----------------------------
@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = status

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

    return {"message": "Job deleted"}