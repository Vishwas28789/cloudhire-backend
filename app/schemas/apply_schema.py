from typing import Optional
from pydantic import BaseModel, EmailStr


class ApplicationRequest(BaseModel):
    job_id: int
    resume_id: Optional[int] = None
    recipient_email: Optional[EmailStr] = None
    custom_message: Optional[str] = None
    use_ai_message: bool = False


class ApplicationResponse(BaseModel):
    success: bool
    job_id: int
    email_log_id: Optional[int] = None
    resume_path: Optional[str] = None
    message: str
