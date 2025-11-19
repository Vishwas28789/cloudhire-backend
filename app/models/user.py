from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    email: str = Field(max_length=255, unique=True, index=True)
    phone: Optional[str] = Field(default=None, max_length=50)
    linkedin_url: Optional[str] = Field(default=None, max_length=500)
    
    role_preferences: List[str] = Field(default=[], sa_column=Column(JSON))
    country_preferences: List[str] = Field(default=[], sa_column=Column(JSON))
    excluded_roles: List[str] = Field(default=[], sa_column=Column(JSON))
    
    min_salary: Optional[int] = Field(default=None)
    max_salary: Optional[int] = Field(default=None)
    salary_currency: str = Field(default="USD", max_length=10)
    
    visa_required: bool = Field(default=False)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
