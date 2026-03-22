from fastapi import APIRouter, Depends,      HTTPException   
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from database import SessionLocal
from models.user_model import User
from models.job_model import Job
from utils.auth import verify_token
from services.resume_service import extract_resume_text, extract_skills
from services.match_service import extract_job_skills, calculate_match
from services.job_search_service import search_jobs
from utils.dependencies import get_current_user, get_db
from tasks.resume_tasks import process_resume 
from core.limiter import limiter
from fastapi import Request
from collections import Counter

router = APIRouter()

@router.get("/analyze")
def analyze_resume(current_user: User = Depends(get_current_user)):

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    try:
        text = extract_resume_text(resume_path)
        skills = extract_skills(text)
    except:
        skills = []

    suggestions = [
        "Add more cloud experience (AWS/GCP)",
        "Include containerization tools like Docker",
        "Mention CI/CD tools like Jenkins or GitHub Actions"
    ]

    return {
        "skills": skills,
        "suggestions": suggestions
    }
# Upload resume and extract skills

@router.post("/upload-resume")
@limiter.limit("20/minute")
def upload_resume(request: Request, file: UploadFile = File(...), current_user: User = Depends(get_current_user)):

    file_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    process_resume.delay(file_path)

    return {"message": "Resume uploaded. Processing started."}

# Match resume to a specific job
@router.get("/skills")
@limiter.limit("20/minute")
def analyze_resume(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    file_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    text = extract_resume_text(file_path)

    skills = extract_skills(text)

    return {"skills": skills}

# Match resume to a specific job
@router.get("/insights")
def resume_insights(current_user: User = Depends(get_current_user)):

    resume_path = f"resumes/{current_user.id}_{current_user.name}_resume.pdf"

    try:
        resume_text = extract_resume_text(resume_path)
        resume_skills = extract_skills(resume_text)
    except:
        resume_skills = []

    # fetch sample jobs
    jobs = search_jobs("python")

    missing_skills = []

    for job in jobs:

        job_skills = extract_job_skills(job.get("description", ""))

        for skill in job_skills:
            if skill.lower() not in [s.lower() for s in resume_skills]:
                missing_skills.append(skill)

    skill_counts = Counter(missing_skills)

    top_missing = skill_counts.most_common(10)

    return {
        "detected_skills": resume_skills,
        "top_missing_skills": [
            {"skill": skill, "jobs": count}
            for skill, count in top_missing
        ]
    }