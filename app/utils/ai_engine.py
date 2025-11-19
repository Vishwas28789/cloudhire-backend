from typing import Optional, Dict, Any
from openai import OpenAI
from app.config import settings
from app.utils.logger import logger


class AIEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        self.client = None
        
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def generate_resume_bullets(self, job_description: str, template_type: str, context: str = "") -> str:
        if not self.is_available():
            return "AI mode not available. Please provide resume bullets manually."
        
        try:
            prompt = f"""Generate 5-7 professional resume bullet points for a {template_type} role.
            
Job Description:
{job_description}

Additional Context:
{context}

Focus on cloud technologies, infrastructure, and relevant skills. Use action verbs and quantify achievements where possible.
Format each bullet point on a new line starting with a dash (-)."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer specializing in cloud and DevOps roles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            return f"AI generation error: {str(e)}"
    
    def generate_recruiter_message(self, job_title: str, company: str, tone: str = "professional") -> str:
        if not self.is_available():
            return "AI mode not available. Please provide message manually."
        
        try:
            tone_guidance = {
                "professional": "formal and professional",
                "warm": "friendly and warm while remaining professional",
                "confident": "confident and assertive",
                "startup": "casual and enthusiastic, suitable for startup culture"
            }
            
            style = tone_guidance.get(tone, "professional")
            
            prompt = f"""Write a brief recruiter outreach email for a {job_title} position at {company}.
            
Tone: {style}

The email should:
- Be 4-5 sentences maximum
- Express genuine interest in the role
- Highlight relevant cloud/DevOps experience briefly
- Request an opportunity to discuss further
- Be personalized to the company

Do not include subject line, just the email body."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at writing professional job application emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            return f"AI generation error: {str(e)}"
    
    def generate_followup_message(self, job_title: str, company: str, days_since: int) -> str:
        if not self.is_available():
            return "AI mode not available. Please provide message manually."
        
        try:
            prompt = f"""Write a polite follow-up email for a {job_title} position at {company}.
            
It has been {days_since} days since the initial application.

The email should:
- Be 3-4 sentences
- Politely inquire about the status
- Reiterate interest
- Remain professional and not pushy

Do not include subject line, just the email body."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at writing professional follow-up emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            return f"AI generation error: {str(e)}"
    
    def generate_summary(self, job_description: str) -> str:
        if not self.is_available():
            return "AI mode not available."
        
        try:
            prompt = f"""Provide a 2-3 sentence professional summary tailored to this job description:

{job_description}

The summary should highlight cloud/DevOps expertise and align with the role requirements."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            return f"AI generation error: {str(e)}"
