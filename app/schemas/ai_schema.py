from typing import Optional, List
from pydantic import BaseModel


class AIGenerateRequest(BaseModel):
    content_type: str
    job_id: Optional[int] = None
    context: Optional[str] = None
    tone: Optional[str] = "professional"


class AIGenerateResponse(BaseModel):
    success: bool
    content: str
    content_type: str
    is_ai_generated: bool
    message: Optional[str] = None


class ManualInputRequest(BaseModel):
    content_type: str
    content: str
    job_id: Optional[int] = None
    metadata: Optional[dict] = None
