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
        from app.models.job import Job
        from app.models.email_log import EmailLog
        from app.utils.email_sender import EmailSender
        from app.utils.message_builder import build_followup_message
        
        now = datetime.utcnow()
        
        statement = select(Followup).where(
            Followup.is_sent == False,
            Followup.scheduled_date <= now,
            Followup.status == "scheduled"
        )
        
        pending_followups = session.exec(statement).all()
        
        logger.info(f"Found {len(pending_followups)} pending follow-ups")
        
        settings = session.exec(select(Settings).where(Settings.user_id == 1)).first()
        
        for followup in pending_followups:
            try:
                logger.info(f"Processing follow-up {followup.id} for job {followup.job_id}")
                
                job = session.get(Job, followup.job_id)
                if not job:
                    logger.error(f"Job {followup.job_id} not found")
                    followup.status = "failed"
                    session.add(followup)
                    continue
                
                days_since = (datetime.utcnow() - job.application_date).days if job.application_date else 7
                
                use_ai = settings and settings.ai_mode_enabled
                message = build_followup_message(
                    job_title=job.title,
                    company=job.company,
                    days_since=days_since,
                    custom_message=followup.message,
                    use_ai=use_ai,
                    ai_api_key=settings.openai_api_key if settings else None
                )
                
                followup.message = message
                
                email_identities = settings.email_identities if settings else []
                email_sender = EmailSender(email_identities)
                
                subject = f"Following up on {job.title} application"
                
                original_email_statement = select(EmailLog).where(
                    EmailLog.job_id == job.id,
                    EmailLog.email_type == "application"
                ).order_by(EmailLog.created_at.desc())
                original_email = session.exec(original_email_statement).first()
                
                recipient = original_email.recipient_email if original_email else "hr@example.com"
                
                result = email_sender.send_email(
                    recipient=recipient,
                    subject=subject,
                    body=message
                )
                
                email_log = EmailLog(
                    job_id=job.id,
                    recipient_email=recipient,
                    sender_email=result.get("sender", "noreply@example.com"),
                    subject=subject,
                    body=message,
                    email_type="followup",
                    status="sent" if result["success"] else "failed",
                    error_message=result.get("error"),
                    sent_at=datetime.utcnow() if result["success"] else None
                )
                
                session.add(email_log)
                session.flush()
                
                if result["success"]:
                    followup.is_sent = True
                    followup.sent_at = datetime.utcnow()
                    followup.status = "sent"
                    followup.email_log_id = email_log.id
                    logger.info(f"Follow-up {followup.id} sent successfully to {recipient}")
                else:
                    followup.status = "failed"
                    logger.error(f"Follow-up {followup.id} failed: {result.get('error')}")
                
                session.add(followup)
                
            except Exception as e:
                logger.error(f"Error processing follow-up {followup.id}: {str(e)}")
                followup.status = "failed"
                session.add(followup)
        
        session.commit()
        logger.info("Follow-up processing complete")


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
