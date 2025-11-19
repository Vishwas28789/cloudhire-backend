from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Followup(SQLModel, table=True):
    __tablename__ = "followups"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="jobs.id")
    email_log_id: Optional[int] = Field(default=None, foreign_key="email_logs.id")
    
    scheduled_date: datetime
    
    followup_type: str = Field(default="email", max_length=50)
    
    message: Optional[str] = Field(default=None, max_length=5000)
    
    is_sent: bool = Field(default=False)
    sent_at: Optional[datetime] = Field(default=None)
    
    status: str = Field(default="scheduled", max_length=50)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
