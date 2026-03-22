from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from utils.dependencies import get_current_user, get_db
from models.user_model import User

router = APIRouter()

@router.get("/me")
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }