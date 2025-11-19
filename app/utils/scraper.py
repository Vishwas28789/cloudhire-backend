import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from app.utils.logger import logger


def scrape_job_from_url(url: str) -> Optional[Dict[str, Any]]:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else "Unknown Title"
        
        body_text = soup.get_text(separator='\n', strip=True)
        
        job = {
            "title": title_text,
            "company": "Scraped Company",
            "location": "Not specified",
            "description": body_text[:5000],
            "url": url,
            "source": "url_scrape"
        }
        
        return job
    
    except Exception as e:
        logger.error(f"Failed to scrape URL {url}: {str(e)}")
        return None
