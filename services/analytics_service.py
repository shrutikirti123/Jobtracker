from sqlalchemy.orm import Session
from models.job_model import Job
from sqlalchemy import func
from routes.job_routes import search_and_match


def get_dashboard_stats(db: Session, user_id: int):

    total = db.query(Job).filter(Job.user_id == user_id).count()

    applied = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "applied"
    ).count()

    interview = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "interview"
    ).count()

    rejected = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "rejected"
    ).count()

    saved = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "Saved"
    ).count()

    avg_score = db.query(func.avg(Job.match_score)).filter(
        Job.user_id == user_id
    ).scalar()

    return {
        "total_applications": total,
        "applied": applied,
        "interview": interview,
        "rejected": rejected,
        "saved": saved,
        "average_match_score": avg_score or 0
    }