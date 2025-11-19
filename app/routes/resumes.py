from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from pathlib import Path
from app.db import get_session
from app.models.resume import Resume
from app.models.job import Job
from app.models.user import User
from app.models.settings import Settings
from app.schemas.resume_schema import ResumeCreate, ResumeResponse
from app.utils.pdf_resume import generate_resume_pdf
from app.utils.ai_engine import AIEngine
from app.utils.logger import logger

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


@router.post("/new", response_model=ResumeResponse)
async def create_resume(
    resume_data: ResumeCreate,
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.id == 1)).first()
    if not user:
        user = User(
            name="Vishwas",
            email="user@example.com",
            role_preferences=["cloud engineer"]
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    
    settings = session.exec(select(Settings).where(Settings.user_id == 1)).first()
    
    bullets = resume_data.bullets
    summary = resume_data.summary or "Experienced cloud professional"
    is_ai_generated = False
    
    job_title = None
    if resume_data.job_id:
        job = session.get(Job, resume_data.job_id)
        if job:
            job_title = job.title
    
    if resume_data.use_ai and settings and settings.ai_mode_enabled:
        ai_engine = AIEngine(api_key=settings.openai_api_key)
        
        if ai_engine.is_available():
            if not bullets or len(bullets) == 0:
                job_desc = ""
                if resume_data.job_id:
                    job = session.get(Job, resume_data.job_id)
                    if job:
                        job_desc = job.description
                
                bullets_text = ai_engine.generate_resume_bullets(
                    job_desc,
                    resume_data.template_type,
                    ""
                )
                bullets = [b.strip() for b in bullets_text.split('\n') if b.strip()]
            
            if not summary or summary == "Experienced cloud professional":
                job_desc = ""
                if resume_data.job_id:
                    job = session.get(Job, resume_data.job_id)
                    if job:
                        job_desc = job.description
                
                summary = ai_engine.generate_summary(job_desc)
            
            is_ai_generated = True
    
    resume_count = len(session.exec(select(Resume)).all()) + 1
    resume_name = f"Vishwas_Cloud_Resume_{resume_count:03d}.pdf"
    
    output_path = f"generated_resumes/{resume_name}"
    
    try:
        generate_resume_pdf(
            name=user.name,
            email=user.email,
            phone=user.phone,
            linkedin_url=user.linkedin_url,
            summary=summary,
            bullets=bullets,
            template_type=resume_data.template_type,
            output_path=output_path,
            job_title=job_title
        )
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
    
    resume = Resume(
        user_id=user.id,
        job_id=resume_data.job_id,
        resume_name=resume_name,
        template_type=resume_data.template_type,
        file_path=output_path,
        content=resume_data.content or {},
        bullets=bullets,
        summary=summary,
        is_ai_generated=is_ai_generated,
        generation_mode="ai" if is_ai_generated else "manual"
    )
    
    session.add(resume)
    session.commit()
    session.refresh(resume)
    
    return resume


@router.get("/history", response_model=List[ResumeResponse])
async def get_resume_history(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session)
):
    statement = select(Resume).offset(skip).limit(limit).order_by(Resume.created_at.desc())
    resumes = session.exec(statement).all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: int, session: Session = Depends(get_session)):
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.get("/{resume_id}/download")
async def download_resume(resume_id: int, session: Session = Depends(get_session)):
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.file_path or not Path(resume.file_path).exists():
        raise HTTPException(status_code=404, detail="Resume file not found")
    
    return FileResponse(
        path=resume.file_path,
        media_type="application/pdf",
        filename=resume.resume_name
    )


@router.delete("/{resume_id}")
async def delete_resume(resume_id: int, session: Session = Depends(get_session)):
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if resume.file_path and Path(resume.file_path).exists():
        Path(resume.file_path).unlink()
    
    session.delete(resume)
    session.commit()
    
    return {"message": "Resume deleted successfully"}
