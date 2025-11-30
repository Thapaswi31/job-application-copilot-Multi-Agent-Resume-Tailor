# my_agent/tools_job_scraper.py
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any

def scrape_job_posting(url: str) -> Dict[str, Any]:
    """
    Scrape a single job posting page and extract structured fields.
    If the site blocks scraping (403, etc.), return an error payload instead of raising.
    """
    try:
        resp = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; ADK-JobScraper/1.0)"
            },
        )
    except Exception as e:
        return {
            "url": url,
            "error": f"request_failed: {e}",
            "title": None,
            "job_description": None,
            "skills": [],
        }

    if resp.status_code != 200:
        return {
            "url": url,
            "error": f"http_status_{resp.status_code}",
            "title": None,
            "job_description": None,
            "skills": [],
        }

    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.find(["h1", "h2"])
    title = title_tag.get_text(strip=True) if title_tag else None

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = "\n".join(
        line.strip()
        for line in soup.get_text("\n", strip=True).splitlines()
        if line.strip()
    )

    SKILL_KEYWORDS = [
        "python", "java", "javascript", "typescript", "sql", "django",
        "flask", "react", "angular", "aws", "gcp", "azure", "kubernetes",
        "docker", "machine learning", "llm", "pandas", "spark",
    ]
    lower = text.lower()
    skills = sorted({s for s in SKILL_KEYWORDS if s in lower})

    return {
        "url": url,
        "error": None,
        "title": title,
        "job_description": text,
        "skills": skills,
    }
