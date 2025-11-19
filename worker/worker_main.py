import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.db import engine
from app.models.followup import Followup
from app.models.job import Job
from app.models.settings import Settings
from app.utils.logger import logger


def process_pending_followups():
    logger.info("Processing pending follow-ups...")
    
    with Session(engine) as session:
        now = datetime.utcnow()
        
        statement = select(Followup).where(
            Followup.is_sent == False,
            Followup.scheduled_date <= now,
            Followup.status == "scheduled"
        )
        
        pending_followups = session.exec(statement).all()
        
        logger.info(f"Found {len(pending_followups)} pending follow-ups")
        
        for followup in pending_followups:
            logger.info(f"Processing follow-up {followup.id} for job {followup.job_id}")


def auto_apply_workflow():
    logger.info("Running auto-apply workflow...")
    
    with Session(engine) as session:
        settings = session.exec(select(Settings).where(Settings.user_id == 1)).first()
        
        if not settings or not settings.auto_apply_enabled:
            logger.info("Auto-apply is disabled")
            return
        
        statement = select(Job).where(
            Job.applied == False,
            Job.score >= 70
        ).limit(5)
        
        jobs = session.exec(statement).all()
        
        logger.info(f"Found {len(jobs)} high-scoring jobs for auto-apply")


def cleanup_old_logs():
    logger.info("Cleaning up old logs...")


def main():
    logger.info("Starting CloudHire Nexus Worker...")
    
    scheduler = BlockingScheduler()
    
    scheduler.add_job(
        process_pending_followups,
        'interval',
        minutes=30,
        id='process_followups',
        next_run_time=datetime.now()
    )
    
    scheduler.add_job(
        auto_apply_workflow,
        'interval',
        hours=6,
        id='auto_apply',
        next_run_time=datetime.now() + timedelta(minutes=1)
    )
    
    scheduler.add_job(
        cleanup_old_logs,
        'interval',
        days=1,
        id='cleanup_logs'
    )
    
    logger.info("Worker scheduler started")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Worker shutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
