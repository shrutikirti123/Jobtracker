from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal
from models.user_model import User
from models.job_model import Job
from schemas.user_schema import UserCreate, UserResponse
from utils.security import hash_password, verify_password
from utils.auth import create_access_token, verify_token
from utils.dependencies import get_db, get_current_user
from utils.logger import logger
from core.limiter import limiter
from fastapi import Request

router = APIRouter()

# login route
@router.post("/login")
@limiter.limit("20/minute")
def login(request: Request,form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {form_data.username}")

    user = db.query(User).filter(User.email.ilike( form_data.username.strip())).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}

# -------------------------
# SIGNUP
# -------------------------
@router.post("/signup")
@limiter.limit("20/minute")
def signup(request: Request, user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email.lower().strip(),
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}