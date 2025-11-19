from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class Job(SQLModel, table=True):
    __tablename__ = "jobs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    title: str = Field(max_length=500)
    company: str = Field(max_length=300)
    location: str = Field(max_length=300)
    country: Optional[str] = Field(default=None, max_length=100)
    
    description: str = Field(max_length=10000)
    url: Optional[str] = Field(default=None, max_length=1000)
    source: str = Field(default="manual", max_length=100)
    
    classification: Optional[str] = Field(default=None, max_length=100)
    
    has_visa_sponsorship: bool = Field(default=False)
    visa_keywords: List[str] = Field(default=[], sa_column=Column(JSON))
    
    salary_min: Optional[int] = Field(default=None)
    salary_max: Optional[int] = Field(default=None)
    salary_currency: Optional[str] = Field(default=None, max_length=10)
    
    score: Optional[int] = Field(default=None)
    score_breakdown: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    applied: bool = Field(default=False)
    application_date: Optional[datetime] = Field(default=None)
    application_status: str = Field(default="pending", max_length=50)
    
    job_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
