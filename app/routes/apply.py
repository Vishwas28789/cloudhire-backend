from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.db import get_session
from app.models.job import Job
from app.models.resume import Resume
from app.models.email_log import EmailLog
from app.models.settings import Settings
from app.schemas.apply_schema import ApplicationRequest, ApplicationResponse
from app.utils.email_sender import EmailSender
from app.utils.message_builder import build_application_message
from app.utils.logger import logger

router = APIRouter(prefix="/api/apply", tags=["apply"])


@router.post("/{job_id}", response_model=ApplicationResponse)
async def apply_to_job(
    job_id: int,
    request: ApplicationRequest,
    session: Session = Depends(get_session)
):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.applied:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    
    settings = session.exec(select(Settings).where(Settings.user_id == 1)).first()
    
    resume = None
    if request.resume_id:
        resume = session.get(Resume, request.resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
    
    recipient = request.recipient_email or "hr@example.com"
    
    use_ai = request.use_ai_message and settings and settings.ai_mode_enabled
    tone = settings.message_tone if settings else "professional"
    
    message = build_application_message(
        job_title=job.title,
        company=job.company,
        custom_message=request.custom_message,
        use_ai=use_ai,
        tone=tone,
        ai_api_key=settings.openai_api_key if settings else None
    )
    
    subject = f"Application for {job.title} position"
    
    email_identities = settings.email_identities if settings else []
    email_sender = EmailSender(email_identities)
    
    attachment_path = resume.file_path if resume else None
    
    result = email_sender.send_email(
        recipient=recipient,
        subject=subject,
        body=message,
        attachment_path=attachment_path
    )
    
    email_log = EmailLog(
        job_id=job.id,
        resume_id=resume.id if resume else None,
        recipient_email=recipient,
        sender_email=result.get("sender", "noreply@example.com"),
        subject=subject,
        body=message,
        email_type="application",
        has_attachment=attachment_path is not None,
        attachment_path=attachment_path,
        status="sent" if result["success"] else "failed",
        error_message=result.get("error"),
        sent_at=datetime.utcnow() if result["success"] else None
    )
    
    session.add(email_log)
    
    if result["success"]:
        job.applied = True
        job.application_date = datetime.utcnow()
        job.application_status = "applied"
        
        if resume:
            resume.times_used += 1
        
        session.add(job)
        if resume:
            session.add(resume)
    
    session.commit()
    session.refresh(email_log)
    
    return ApplicationResponse(
        success=result["success"],
        job_id=job.id,
        email_log_id=email_log.id,
        resume_path=attachment_path,
        message="Application submitted successfully" if result["success"] else f"Application failed: {result.get('error')}"
    )
