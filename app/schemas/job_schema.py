from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    country: Optional[str] = None
    description: str
    url: Optional[str] = None
    source: str = "manual"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    job_metadata: Optional[Dict[str, Any]] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    application_status: Optional[str] = None
    applied: Optional[bool] = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    country: Optional[str]
    description: str
    url: Optional[str]
    source: str
    classification: Optional[str]
    has_visa_sponsorship: bool
    visa_keywords: List[str]
    score: Optional[int]
    score_breakdown: Optional[Dict[str, Any]]
    applied: bool
    application_status: str
    application_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobSearch(BaseModel):
    query: Optional[str] = None
    classification: Optional[str] = None
    country: Optional[str] = None
    min_score: Optional[int] = None
    has_visa_sponsorship: Optional[bool] = None
    applied: Optional[bool] = None
    limit: int = Field(default=50, le=200)
    offset: int = Field(default=0, ge=0)
