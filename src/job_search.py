import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def search_jobs(role: str, location: str, k: int = 3) -> list:
    """Search JSearch API for real job postings"""
    
    url = "https://jsearch.p.rapidapi.com/search"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    params = {
        "query": f"{role} entry level {location}",
        "page": "1",
        "num_pages": "1",
        "employment_types": "FULLTIME",
        "job_requirements": "under_3_years_experience",
        "date_posted": "week"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        jobs = data.get("data", [])[:k]
        
        if not jobs:
            return []
        
        results = []
        for job in jobs:
            
            # handle salary
            salary = "Not listed"
            if job.get("job_min_salary") and job.get("job_max_salary"):
                salary = f"${job['job_min_salary']:,.0f} - ${job['job_max_salary']:,.0f}/year"
            
            results.append({
                "title":       job.get("job_title", "N/A"),
                "company":     job.get("employer_name", "N/A"),
                "location":    f"{job.get('job_city', '')} {job.get('job_state', '')}".strip(),
                "salary":      salary,
                "posted":      job.get("job_posted_at_datetime_utc", "")[:10],
                "description": job.get("job_description", "")[:300],
                "apply_link":  job.get("job_apply_link", "N/A"),
                "via":         job.get("job_via", "N/A")
            })
        
        print(f"Found {len(results)} jobs for {role} in {location}")
        return results
        
    except Exception as e:
        print(f"Error searching jobs: {str(e)}")
        return []