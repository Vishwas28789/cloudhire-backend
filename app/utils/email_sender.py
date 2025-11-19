import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional, Dict, List
from pathlib import Path
from app.utils.logger import logger
from app.config import settings


class EmailSender:
    def __init__(self, email_identities: Optional[List[Dict[str, str]]] = None):
        self.email_identities = email_identities or []
        self.current_identity_index = 0
    
    def _get_next_identity(self) -> Optional[Dict[str, str]]:
        if not self.email_identities:
            return {
                "email": settings.smtp_username or "noreply@example.com",
                "password": settings.smtp_password or "",
                "smtp_server": settings.smtp_server,
                "smtp_port": settings.smtp_port
            }
        
        identity = self.email_identities[self.current_identity_index]
        self.current_identity_index = (self.current_identity_index + 1) % len(self.email_identities)
        
        return identity
    
    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachment_path: Optional[str] = None,
        sender_override: Optional[str] = None
    ) -> Dict[str, any]:
        try:
            identity = self._get_next_identity()
            
            if not identity:
                return {
                    "success": False,
                    "error": "No email identity configured"
                }
            
            sender_email = sender_override or identity.get("email")
            password = identity.get("password", "")
            smtp_server = identity.get("smtp_server", settings.smtp_server)
            smtp_port = identity.get("smtp_port", settings.smtp_port)
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            if attachment_path and Path(attachment_path).exists():
                with open(attachment_path, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype='pdf')
                    attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=Path(attachment_path).name
                    )
                    msg.attach(attachment)
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                if password:
                    server.login(sender_email, password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {recipient}")
            return {
                "success": True,
                "sender": sender_email,
                "recipient": recipient
            }
        
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
