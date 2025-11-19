from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.settings import Settings
from app.models.job import Job
from app.schemas.ai_schema import AIGenerateRequest, AIGenerateResponse, ManualInputRequest
from app.utils.ai_engine import AIEngine
from app.utils.logger import logger

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/generate", response_model=AIGenerateResponse)
async def generate_ai_content(
    request: AIGenerateRequest,
    session: Session = Depends(get_session)
):
    statement = select(Settings).where(Settings.user_id == 1)
    settings = session.exec(statement).first()
    
    if not settings or not settings.ai_mode_enabled:
        return AIGenerateResponse(
            success=False,
            content="",
            content_type=request.content_type,
            is_ai_generated=False,
            message="AI mode is not enabled. Please enable it in settings and provide an API key."
        )
    
    ai_engine = AIEngine(api_key=settings.openai_api_key)
    
    if not ai_engine.is_available():
        return AIGenerateResponse(
            success=False,
            content="",
            content_type=request.content_type,
            is_ai_generated=False,
            message="AI engine not available. Please check your API key."
        )
    
    job_description = ""
    job_title = "Cloud Engineer"
    company = "Company"
    
    if request.job_id:
        job = session.get(Job, request.job_id)
        if job:
            job_description = job.description
            job_title = job.title
            company = job.company
    
    content = ""
    
    if request.content_type == "resume_bullets":
        template_type = request.context or "architect"
        content = ai_engine.generate_resume_bullets(job_description, template_type, "")
    
    elif request.content_type == "summary":
        content = ai_engine.generate_summary(job_description or request.context or "")
    
    elif request.content_type == "recruiter_message":
        tone = request.tone or "professional"
        content = ai_engine.generate_recruiter_message(job_title, company, tone)
    
    elif request.content_type == "followup_message":
        content = ai_engine.generate_followup_message(job_title, company, 7)
    
    else:
        return AIGenerateResponse(
            success=False,
            content="",
            content_type=request.content_type,
            is_ai_generated=False,
            message=f"Unknown content type: {request.content_type}"
        )
    
    return AIGenerateResponse(
        success=True,
        content=content,
        content_type=request.content_type,
        is_ai_generated=True,
        message="Content generated successfully"
    )


@router.post("/manual-input")
async def submit_manual_input(request: ManualInputRequest):
    return {
        "success": True,
        "content_type": request.content_type,
        "message": "Manual content received and stored successfully",
        "content_length": len(request.content)
    }
