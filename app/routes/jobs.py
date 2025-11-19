from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.db import get_session
from app.models.job import Job
from app.models.user import User
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse, JobSearch
from app.utils.classification import classify_job, is_excluded_role
from app.utils.visa_detector import detect_visa_sponsorship
from app.utils.scoring import calculate_job_score
from app.utils.parser import parse_csv_jobs, extract_job_from_text
from app.utils.scraper import scrape_job_from_url
from app.utils.logger import logger

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("", response_model=List[JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session)
):
    statement = select(Job).offset(skip).limit(limit).order_by(Job.created_at.desc())
    jobs = session.exec(statement).all()
    return jobs


@router.post("", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.id == 1)).first()
    
    classification = classify_job(job_data.title, job_data.description)
    
    if is_excluded_role(job_data.title, job_data.description):
        raise HTTPException(status_code=400, detail="This job role is excluded based on your preferences")
    
    has_visa, visa_keywords = detect_visa_sponsorship(job_data.description)
    
    score_data = {"score": 50, "breakdown": {}}
    if user:
        score_data = calculate_job_score(
            job_title=job_data.title,
            job_description=job_data.description,
            job_classification=classification,
            job_location=job_data.location,
            job_country=job_data.country,
            has_visa=has_visa,
            salary_min=job_data.salary_min,
            salary_max=job_data.salary_max,
            user_role_preferences=user.role_preferences,
            user_country_preferences=user.country_preferences,
            user_min_salary=user.min_salary,
            user_visa_required=user.visa_required
        )
    
    job = Job(
        **job_data.dict(),
        classification=classification,
        has_visa_sponsorship=has_visa,
        visa_keywords=visa_keywords,
        score=score_data["score"],
        score_breakdown=score_data["breakdown"]
    )
    
    session.add(job)
    session.commit()
    session.refresh(job)
    
    return job


@router.get("/search", response_model=List[JobResponse])
async def search_jobs(
    search: JobSearch = Depends(),
    session: Session = Depends(get_session)
):
    statement = select(Job)
    
    if search.classification:
        statement = statement.where(Job.classification == search.classification)
    
    if search.country:
        statement = statement.where(Job.country == search.country)
    
    if search.min_score:
        statement = statement.where(Job.score >= search.min_score)
    
    if search.has_visa_sponsorship is not None:
        statement = statement.where(Job.has_visa_sponsorship == search.has_visa_sponsorship)
    
    if search.applied is not None:
        statement = statement.where(Job.applied == search.applied)
    
    if search.query:
        statement = statement.where(
            Job.title.contains(search.query) | Job.description.contains(search.query)
        )
    
    statement = statement.offset(search.offset).limit(search.limit).order_by(Job.score.desc())
    
    jobs = session.exec(statement).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    session: Session = Depends(get_session)
):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)
    
    job.updated_at = datetime.utcnow()
    
    session.add(job)
    session.commit()
    session.refresh(job)
    
    return job


@router.delete("/{job_id}")
async def delete_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    session.delete(job)
    session.commit()
    
    return {"message": "Job deleted successfully"}


@router.post("/import/csv")
async def import_jobs_from_csv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    try:
        content = await file.read()
        csv_text = content.decode('utf-8')
        
        jobs_data = parse_csv_jobs(csv_text)
        
        created_jobs = []
        for job_data in jobs_data:
            job_create = JobCreate(**job_data)
            
            classification = classify_job(job_create.title, job_create.description)
            has_visa, visa_keywords = detect_visa_sponsorship(job_create.description)
            
            job = Job(
                **job_create.dict(),
                classification=classification,
                has_visa_sponsorship=has_visa,
                visa_keywords=visa_keywords,
                score=50
            )
            
            session.add(job)
            created_jobs.append(job)
        
        session.commit()
        
        return {
            "message": f"Successfully imported {len(created_jobs)} jobs",
            "count": len(created_jobs)
        }
    
    except Exception as e:
        logger.error(f"CSV import failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")


@router.post("/import/text")
async def import_job_from_text(
    text: str,
    session: Session = Depends(get_session)
):
    try:
        job_data = extract_job_from_text(text)
        job_create = JobCreate(**job_data)
        
        classification = classify_job(job_create.title, job_create.description)
        has_visa, visa_keywords = detect_visa_sponsorship(job_create.description)
        
        job = Job(
            **job_create.dict(),
            classification=classification,
            has_visa_sponsorship=has_visa,
            visa_keywords=visa_keywords,
            score=50
        )
        
        session.add(job)
        session.commit()
        session.refresh(job)
        
        return job
    
    except Exception as e:
        logger.error(f"Text import failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")


@router.post("/import/url")
async def import_job_from_url(
    url: str,
    session: Session = Depends(get_session)
):
    job_data = scrape_job_from_url(url)
    
    if not job_data:
        raise HTTPException(status_code=400, detail="Failed to scrape job from URL")
    
    job_create = JobCreate(**job_data)
    
    classification = classify_job(job_create.title, job_create.description)
    has_visa, visa_keywords = detect_visa_sponsorship(job_create.description)
    
    job = Job(
        **job_create.dict(),
        classification=classification,
        has_visa_sponsorship=has_visa,
        visa_keywords=visa_keywords,
        score=50
    )
    
    session.add(job)
    session.commit()
    session.refresh(job)
    
    return job


@router.get("/status/overview")
async def get_status_overview(session: Session = Depends(get_session)):
    total_jobs = session.exec(select(Job)).all()
    
    total_count = len(total_jobs)
    applied_count = len([j for j in total_jobs if j.applied])
    pending_count = total_count - applied_count
    
    return {
        "total_jobs": total_count,
        "applied": applied_count,
        "pending": pending_count,
        "by_status": {
            "pending": len([j for j in total_jobs if j.application_status == "pending"]),
            "applied": len([j for j in total_jobs if j.application_status == "applied"]),
            "interviewing": len([j for j in total_jobs if j.application_status == "interviewing"]),
            "offered": len([j for j in total_jobs if j.application_status == "offered"]),
            "rejected": len([j for j in total_jobs if j.application_status == "rejected"])
        }
    }
