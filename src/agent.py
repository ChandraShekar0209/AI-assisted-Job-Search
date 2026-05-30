from src.resume_parser import load_resume, extract_profile
from src.job_search import search_jobs
from src.job_matcher import rank_jobs
from dotenv import load_dotenv

load_dotenv()

def run_job_agent(
    resume_path: str,
    role: str,
    location: str,
    k: int = 3
) -> list:
    """
    Main agent — parses resume, searches jobs,
    matches and ranks results
    """
    
    print("\n🔍 Step 1 — Parsing resume...")
    vs = load_resume(resume_path)
    profile = extract_profile(vs)
    print("✅ Resume parsed successfully")
    
    print(f"\n🔍 Step 2 — Searching jobs for {role} in {location}...")
    jobs = search_jobs(role, location, k=k*2)
    # fetch more than k so matcher has enough to filter
    
    if not jobs:
        print("❌ No jobs found — try different role or location")
        return []
    
    print(f"✅ Found {len(jobs)} jobs to match against")
    
    print("\n🔍 Step 3 — Matching jobs against your resume...")
    ranked = rank_jobs(profile, jobs)
    
    # return top k results
    final = ranked[:k]
    
    print(f"\n✅ Done — returning top {len(final)} matches\n")
    
    return final, profile


def format_results(results: list) -> str:
    """Format ranked jobs for display"""
    
    output = ""
    
    # group by tier
    strong   = [j for j in results if j["tier"] == "strong"]
    partial  = [j for j in results if j["tier"] == "partial"]
    fallback = [j for j in results if j["tier"] == "fallback"]
    
    def format_job(job, i):
        # fix None location
        location = job['location'] if job['location'] != "None None" else "Remote / Not specified"
        salary   = job['salary'] if job['salary'] != "Not listed" else "Not disclosed"
        
        return f"""
**{i}. {job['title']}**
🏢 Company: {job['company']}
📍 Location: {location}
💰 Salary: {salary}
📊 Match: {job['match_score']}%
✅ You have: {', '.join(job['matching_skills'])}
❌ You need: {', '.join(job['missing_skills'])}
💡 {job['reason']}
🔗 Apply: {job['apply_link']}
"""
    
    i = 1
    
    if strong:
        output += "## 🟢 Strong Matches (60%+)\n"
        for job in strong:
            output += format_job(job, i)
            i += 1
    
    if partial:
        output += "\n## 🟡 Partial Matches (30-59%)\n"
        for job in partial:
            output += format_job(job, i)
            i += 1
    
    if fallback:
        output += "\n## 🔴 Fallback Matches (role + location only)\n"
        for job in fallback:
            output += format_job(job, i)
            i += 1
    
    return output