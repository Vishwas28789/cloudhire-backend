from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr


class EmailIdentity(BaseModel):
    email: EmailStr
    password: str
    smtp_server: Optional[str] = "smtp.gmail.com"
    smtp_port: Optional[int] = 587


class SettingsUpdate(BaseModel):
    ai_mode_enabled: Optional[bool] = None
    openai_api_key: Optional[str] = None
    email_identities: Optional[List[Dict[str, str]]] = None
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    followup_delay_days: Optional[int] = None
    auto_apply_enabled: Optional[bool] = None
    message_tone: Optional[str] = None
    blacklisted_companies: Optional[List[str]] = None
    notification_webhook: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class SettingsResponse(BaseModel):
    id: int
    user_id: int
    ai_mode_enabled: bool
    followup_delay_days: int
    auto_apply_enabled: bool
    message_tone: str
    blacklisted_companies: List[str]
    
    class Config:
        from_attributes = True
