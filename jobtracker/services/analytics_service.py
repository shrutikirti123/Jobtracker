from sqlalchemy import func
from models.job_model import Job


def get_dashboard_stats(db, user_id):

    total_jobs = db.query(Job).filter(
        Job.user_id == user_id
    ).count()

    applied = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "Applied"
    ).count()

    interview = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "Interview"
    ).count()

    offer = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "Offer"
    ).count()

    rejected = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status == "Rejected"
    ).count()

    return {
        "total_jobs": total_jobs,
        "applied": applied,
        "interview": interview,
        "offer": offer,
        "rejected": rejected
    }