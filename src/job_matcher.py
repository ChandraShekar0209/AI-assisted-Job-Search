from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

def match_job(profile: str, job: dict) -> dict:
    """Score how well resume matches a job posting"""
    
    prompt = f"""
Compare this profile against the job posting.

Profile:
{profile}

Job Title: {job['title']}
Company: {job['company']}
Description: {job['description']}

Return ONLY valid JSON — no extra text:
{{
    "match_score": <number 0-100>,
    "tier": "<strong/partial/fallback>",
    "matching_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "reason": "<one sentence why>"
}}

Scoring rules:
- strong (60-100): most key skills match
- partial (30-59): some skills match
- fallback (0-29): few or no skills match
"""
    
    response = llm.invoke(prompt)
    
    try:
        result = json.loads(response.content)
    except:
        result = {
            "match_score": 0,
            "tier": "fallback",
            "matching_skills": [],
            "missing_skills": [],
            "reason": "Could not parse match score"
        }
    
    return result


def rank_jobs(profile: str, jobs: list) -> list:
    """Match and rank all jobs against profile"""
    
    ranked = []
    
    for job in jobs:
        print(f"Matching: {job['title']} at {job['company']}...")
        score = match_job(profile, job)
        
        ranked.append({
            **job,
            "match_score":     score["match_score"],
            "tier":            score["tier"],
            "matching_skills": score["matching_skills"],
            "missing_skills":  score["missing_skills"],
            "reason":          score["reason"]
        })
    
    # sort by match score highest to lowest
    ranked.sort(key=lambda x: x["match_score"], reverse=True)
    
    return ranked