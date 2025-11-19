from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class Settings(SQLModel, table=True):
    __tablename__ = "settings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=1)
    
    ai_mode_enabled: bool = Field(default=False)
    
    openai_api_key: Optional[str] = Field(default=None, max_length=500)
    
    email_identities: List[Dict[str, str]] = Field(default=[], sa_column=Column(JSON))
    
    smtp_server: Optional[str] = Field(default=None, max_length=200)
    smtp_port: Optional[int] = Field(default=587)
    smtp_use_tls: bool = Field(default=True)
    
    followup_delay_days: int = Field(default=7)
    
    auto_apply_enabled: bool = Field(default=False)
    
    message_tone: str = Field(default="professional", max_length=50)
    
    blacklisted_companies: List[str] = Field(default=[], sa_column=Column(JSON))
    
    notification_webhook: Optional[str] = Field(default=None, max_length=500)
    
    preferences: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
