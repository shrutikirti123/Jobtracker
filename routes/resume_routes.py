from fastapi import APIRouter, Depends,      HTTPException   
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from database import SessionLocal
from models.user_model import User
from models.job_model import Job
from utils.auth import verify_token
from services.resume_service import extract_resume_text, extract_skills
from utils.dependencies import get_current_user, get_db
from tasks.resume_tasks import process_resume 
from core.limiter import limiter
from fastapi import Request

router = APIRouter()

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

