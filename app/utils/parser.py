import csv
import io
from typing import List, Dict, Any


def parse_csv_jobs(csv_content: str) -> List[Dict[str, Any]]:
    jobs = []
    
    try:
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            job = {
                "title": row.get("title", row.get("Title", "")),
                "company": row.get("company", row.get("Company", "")),
                "location": row.get("location", row.get("Location", "")),
                "country": row.get("country", row.get("Country", None)),
                "description": row.get("description", row.get("Description", "")),
                "url": row.get("url", row.get("URL", None)),
                "source": "csv_import"
            }
            
            if job["title"] and job["company"]:
                jobs.append(job)
    
    except Exception as e:
        raise ValueError(f"Failed to parse CSV: {str(e)}")
    
    return jobs


def extract_job_from_text(text: str) -> Dict[str, Any]:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    job = {
        "title": lines[0] if len(lines) > 0 else "Untitled Position",
        "company": lines[1] if len(lines) > 1 else "Unknown Company",
        "location": lines[2] if len(lines) > 2 else "Not specified",
        "description": '\n'.join(lines[3:]) if len(lines) > 3 else text,
        "source": "text_paste"
    }
    
    return job
