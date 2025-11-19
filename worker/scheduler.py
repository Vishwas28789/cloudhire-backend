from datetime import datetime, timedelta
from sqlmodel import Session
from app.models.followup import Followup
from app.models.job import Job
from app.models.settings import Settings
from app.db import engine
from app.utils.logger import logger


def schedule_automatic_followup(job_id: int):
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if not job or not job.applied:
            return
        
        settings = session.exec(
            session.query(Settings).where(Settings.user_id == 1)
        ).first()
        
        delay_days = settings.followup_delay_days if settings else 7
        
        scheduled_date = datetime.utcnow() + timedelta(days=delay_days)
        
        followup = Followup(
            job_id=job.id,
            scheduled_date=scheduled_date,
            followup_type="email",
            status="scheduled"
        )
        
        session.add(followup)
        session.commit()
        
        logger.info(f"Scheduled follow-up for job {job_id} on {scheduled_date}")
