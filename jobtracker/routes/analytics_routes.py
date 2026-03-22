from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
from models.user_model import User
from services.analytics_service import get_dashboard_stats

router = APIRouter()

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    stats = get_dashboard_stats(db, current_user.id)

    return stats