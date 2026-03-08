from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user_model import User
from utils.auth import verify_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user