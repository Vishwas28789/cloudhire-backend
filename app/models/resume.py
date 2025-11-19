from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class Resume(SQLModel, table=True):
    __tablename__ = "resumes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=1)
    job_id: Optional[int] = Field(default=None, foreign_key="jobs.id")
    
    resume_name: str = Field(max_length=300)
    template_type: str = Field(default="architect", max_length=50)
    
    file_path: Optional[str] = Field(default=None, max_length=500)
    
    content: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    
    bullets: List[str] = Field(default=[], sa_column=Column(JSON))
    summary: Optional[str] = Field(default=None, max_length=2000)
    
    is_ai_generated: bool = Field(default=False)
    generation_mode: str = Field(default="manual", max_length=20)
    
    times_used: int = Field(default=0)
    callback_count: int = Field(default=0)
    offer_count: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
