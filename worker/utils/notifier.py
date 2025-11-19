import requests
from typing import Optional
from app.utils.logger import logger


def send_webhook_notification(webhook_url: str, message: dict) -> bool:
    try:
        response = requests.post(webhook_url, json=message, timeout=5)
        response.raise_for_status()
        logger.info(f"Webhook notification sent successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to send webhook notification: {str(e)}")
        return False


def notify_new_job(job_title: str, company: str, score: int, webhook_url: Optional[str] = None):
    if not webhook_url:
        return
    
    message = {
        "event": "new_job",
        "title": job_title,
        "company": company,
        "score": score
    }
    
    send_webhook_notification(webhook_url, message)
