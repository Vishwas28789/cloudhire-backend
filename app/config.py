import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost/cloudhire_nexus")
    
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    
    session_secret: str = os.getenv("SESSION_SECRET", "change-this-in-production")
    
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("SMTP_USERNAME", None)
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD", None)
    
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
