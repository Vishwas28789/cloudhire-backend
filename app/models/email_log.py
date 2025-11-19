from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class EmailLog(SQLModel, table=True):
    __tablename__ = "email_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="jobs.id")
    resume_id: Optional[int] = Field(default=None, foreign_key="resumes.id")
    
    recipient_email: str = Field(max_length=255)
    sender_email: str = Field(max_length=255)
    
    subject: str = Field(max_length=500)
    body: str = Field(max_length=10000)
    
    email_type: str = Field(default="application", max_length=50)
    
    has_attachment: bool = Field(default=False)
    attachment_path: Optional[str] = Field(default=None, max_length=500)
    
    status: str = Field(default="pending", max_length=50)
    error_message: Optional[str] = Field(default=None, max_length=1000)
    
    sent_at: Optional[datetime] = Field(default=None)
    
    email_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
