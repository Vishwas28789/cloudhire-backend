from typing import Optional
from app.utils.ai_engine import AIEngine


def build_application_message(
    job_title: str,
    company: str,
    custom_message: Optional[str] = None,
    use_ai: bool = False,
    tone: str = "professional",
    ai_api_key: Optional[str] = None
) -> str:
    if custom_message:
        return custom_message
    
    if use_ai and ai_api_key:
        ai_engine = AIEngine(api_key=ai_api_key)
        return ai_engine.generate_recruiter_message(job_title, company, tone)
    
    default_template = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With extensive experience in cloud technologies and infrastructure management, I am confident I would be a valuable addition to your team.

I have attached my resume for your review. I would welcome the opportunity to discuss how my skills and experience align with your needs.

Thank you for your consideration.

Best regards"""
    
    return default_template


def build_followup_message(
    job_title: str,
    company: str,
    days_since: int,
    custom_message: Optional[str] = None,
    use_ai: bool = False,
    ai_api_key: Optional[str] = None
) -> str:
    if custom_message:
        return custom_message
    
    if use_ai and ai_api_key:
        ai_engine = AIEngine(api_key=ai_api_key)
        return ai_engine.generate_followup_message(job_title, company, days_since)
    
    default_template = f"""Dear Hiring Manager,

I recently applied for the {job_title} position at {company} and wanted to follow up on my application. I remain very interested in this opportunity and would appreciate any update on the hiring process.

Thank you for your time and consideration.

Best regards"""
    
    return default_template
