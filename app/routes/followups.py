from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta
from app.db import get_session
from app.models.followup import Followup
from app.models.job import Job
from app.models.email_log import EmailLog
from app.models.settings import Settings
from app.utils.email_sender import EmailSender
from app.utils.message_builder import build_followup_message
from app.utils.logger import logger

router = APIRouter(prefix="/api/followups", tags=["followups"])


@router.get("", response_model=List[Followup])
async def list_followups(
    pending_only: bool = False,
    session: Session = Depends(get_session)
):
    statement = select(Followup).order_by(Followup.scheduled_date)
    
    if pending_only:
        statement = statement.where(Followup.is_sent == False)
    
    followups = session.exec(statement).all()
    return followups


@router.post("/{job_id}")
async def schedule_followup(
    job_id: int,
    days_delay: int = 7,
    session: Session = Depends(get_session)
):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not job.applied:
        raise HTTPException(status_code=400, detail="Cannot schedule follow-up for unapplied job")
    
    scheduled_date = datetime.utcnow() + timedelta(days=days_delay)
    
    followup = Followup(
        job_id=job.id,
        scheduled_date=scheduled_date,
        followup_type="email",
        status="scheduled"
    )
    
    session.add(followup)
    session.commit()
    session.refresh(followup)
    
    return followup


@router.post("/{followup_id}/send")
async def send_followup(
    followup_id: int,
    session: Session = Depends(get_session)
):
    followup = session.get(Followup, followup_id)
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    
    if followup.is_sent:
        raise HTTPException(status_code=400, detail="Follow-up already sent")
    
    job = session.get(Job, followup.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    settings = session.exec(select(Settings).where(Settings.user_id == 1)).first()
    
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
    recipient = "hr@example.com"
    
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
    
    if result["success"]:
        followup.is_sent = True
        followup.sent_at = datetime.utcnow()
        followup.status = "sent"
        followup.email_log_id = email_log.id
    else:
        followup.status = "failed"
    
    session.add(followup)
    session.commit()
    
    return {
        "success": result["success"],
        "followup_id": followup.id,
        "message": "Follow-up sent successfully" if result["success"] else f"Failed: {result.get('error')}"
    }


@router.delete("/{followup_id}")
async def cancel_followup(
    followup_id: int,
    session: Session = Depends(get_session)
):
    followup = session.get(Followup, followup_id)
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    
    session.delete(followup)
    session.commit()
    
    return {"message": "Follow-up cancelled successfully"}
