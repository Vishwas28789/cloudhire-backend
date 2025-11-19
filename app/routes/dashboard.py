from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import Dict, Any
from collections import defaultdict
from app.db import get_session
from app.models.job import Job
from app.models.resume import Resume
from app.models.email_log import EmailLog

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/metrics")
async def get_dashboard_metrics(session: Session = Depends(get_session)):
    all_jobs = session.exec(select(Job)).all()
    all_resumes = session.exec(select(Resume)).all()
    all_emails = session.exec(select(EmailLog)).all()
    
    total_applications = len([j for j in all_jobs if j.applied])
    
    callback_count = len([j for j in all_jobs if j.application_status in ["interviewing", "offered"]])
    offer_count = len([j for j in all_jobs if j.application_status == "offered"])
    
    callback_rate = (callback_count / total_applications * 100) if total_applications > 0 else 0
    offer_rate = (offer_count / total_applications * 100) if total_applications > 0 else 0
    
    country_stats = defaultdict(lambda: {"applied": 0, "callbacks": 0, "offers": 0})
    for job in all_jobs:
        if job.applied and job.country:
            country = job.country
            country_stats[country]["applied"] += 1
            if job.application_status in ["interviewing", "offered"]:
                country_stats[country]["callbacks"] += 1
            if job.application_status == "offered":
                country_stats[country]["offers"] += 1
    
    role_stats = defaultdict(lambda: {"applied": 0, "callbacks": 0, "offers": 0})
    for job in all_jobs:
        if job.applied and job.classification:
            role = job.classification
            role_stats[role]["applied"] += 1
            if job.application_status in ["interviewing", "offered"]:
                role_stats[role]["callbacks"] += 1
            if job.application_status == "offered":
                role_stats[role]["offers"] += 1
    
    template_stats = defaultdict(lambda: {"used": 0, "callbacks": 0, "offers": 0})
    for resume in all_resumes:
        template = resume.template_type
        template_stats[template]["used"] += resume.times_used
        template_stats[template]["callbacks"] += resume.callback_count
        template_stats[template]["offers"] += resume.offer_count
    
    timeline_data = []
    date_groups = defaultdict(int)
    for job in all_jobs:
        if job.applied and job.application_date:
            date_key = job.application_date.strftime("%Y-%m-%d")
            date_groups[date_key] += 1
    
    for date_key in sorted(date_groups.keys()):
        timeline_data.append({
            "date": date_key,
            "applications": date_groups[date_key]
        })
    
    return {
        "overview": {
            "total_jobs": len(all_jobs),
            "total_applications": total_applications,
            "pending_applications": len(all_jobs) - total_applications,
            "callback_count": callback_count,
            "offer_count": offer_count,
            "callback_rate": round(callback_rate, 2),
            "offer_rate": round(offer_rate, 2)
        },
        "country_success": dict(country_stats),
        "role_success": dict(role_stats),
        "template_success": dict(template_stats),
        "timeline": timeline_data
    }
