from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path


def generate_resume_pdf(
    name: str,
    email: str,
    phone: Optional[str],
    linkedin_url: Optional[str],
    summary: str,
    bullets: List[str],
    template_type: str,
    output_path: str,
    job_title: Optional[str] = None
) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5282'),
        spaceAfter=6,
        spaceBefore=12,
        borderWidth=1,
        borderColor=colors.HexColor('#2c5282'),
        borderPadding=4
    )
    
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6
    )
    
    story = []
    
    story.append(Paragraph(name, title_style))
    
    contact_info = f"{email}"
    if phone:
        contact_info += f" | {phone}"
    if linkedin_url:
        contact_info += f" | LinkedIn: {linkedin_url}"
    
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 0.2*inch))
    
    if job_title:
        objective = f"Objective: {template_type.title()} position in {job_title}"
        story.append(Paragraph(objective, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Professional Summary", heading_style))
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Key Skills & Experience", heading_style))
    for bullet in bullets:
        bullet_text = bullet.strip()
        if bullet_text.startswith('-') or bullet_text.startswith('•'):
            bullet_text = bullet_text[1:].strip()
        story.append(Paragraph(f"• {bullet_text}", bullet_style))
    
    story.append(Spacer(1, 0.15*inch))
    
    if template_type == "architect":
        story.append(Paragraph("Cloud Architecture Expertise", heading_style))
        story.append(Paragraph(
            "Specialized in designing and implementing scalable cloud solutions across AWS, Azure, and GCP platforms.",
            styles['Normal']
        ))
    elif template_type == "support":
        story.append(Paragraph("Technical Support Excellence", heading_style))
        story.append(Paragraph(
            "Proven track record in providing exceptional cloud infrastructure support and troubleshooting.",
            styles['Normal']
        ))
    elif template_type == "devops":
        story.append(Paragraph("DevOps & Automation", heading_style))
        story.append(Paragraph(
            "Expert in CI/CD pipelines, infrastructure as code, and cloud automation tools.",
            styles['Normal']
        ))
    
    doc.build(story)
    
    return output_path
