from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


class ResumeCreate(BaseModel):
    job_id: Optional[int] = None
    template_type: str = "architect"
    bullets: List[str] = []
    summary: Optional[str] = None
    use_ai: bool = False
    content: Optional[Dict[str, Any]] = None


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    job_id: Optional[int]
    resume_name: str
    template_type: str
    file_path: Optional[str]
    is_ai_generated: bool
    generation_mode: str
    times_used: int
    callback_count: int
    offer_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
