# main.py
# FastAPI REST API for AI Job Search Agent

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
import logging

from src.agent import run_job_agent
from src.resume_parser import load_resume, extract_profile
from src.job_search import search_jobs
from src.job_matcher import rank_jobs

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api.log")
    ]
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AI Job Search Agent",
    description="Upload your resume and get matched job postings instantly",
    version="1.0.0"
)


# request model
class JobSearchRequest(BaseModel):
    role: str
    location: str
    k: Optional[int] = 3


# response models
class JobResult(BaseModel):
    title: str
    company: str
    location: str
    salary: str
    match_score: int
    tier: str
    matching_skills: list
    missing_skills: list
    reason: str
    apply_link: str


# health check endpoint
@app.get("/health")
async def health_check():
    logger.info("Health check called")
    return {
        "status": "healthy",
        "service": "AI Job Search Agent",
        "version": "1.0.0"
    }


# main search endpoint
@app.post("/search")
async def search_jobs_endpoint(
    role: str,
    location: str,
    k: int = 3,
    resume: UploadFile = File(...)
):
    logger.info(f"Search request — role: {role}, location: {location}, k: {k}")

    # validate file
    if not resume.filename.endswith(".pdf"):
        logger.warning(f"Invalid file type: {resume.filename}")
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )

    # save uploaded PDF to temp file
    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:
            content = await resume.read()
            tmp.write(content)
            tmp_path = tmp.name

        logger.info(f"Resume saved to temp file: {tmp_path}")

        # run agent
        results, profile = run_job_agent(
            resume_path=tmp_path,
            role=role,
            location=location,
            k=k
        )

        logger.info(f"Agent completed — {len(results)} results returned")

        return JSONResponse(content={
            "status": "success",
            "role": role,
            "location": location,
            "profile_summary": profile[:500],
            "total_results": len(results),
            "results": results
        })

    except Exception as e:
        logger.error(f"Search failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

    finally:
        # clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
            logger.debug("Temp file cleaned up")


# profile only endpoint
@app.post("/profile")
async def extract_profile_endpoint(
    resume: UploadFile = File(...)
):
    logger.info("Profile extraction request")

    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await resume.read()
            tmp.write(content)
            tmp_path = tmp.name

        vs = load_resume(tmp_path)
        profile = extract_profile(vs)

        logger.info("Profile extracted successfully")

        return JSONResponse(content={
            "status": "success",
            "profile": profile
        })

    except Exception as e:
        logger.error(f"Profile extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# jobs only endpoint — no resume needed
@app.get("/jobs")
async def get_jobs(
    role: str,
    location: str,
    k: int = 5
):
    logger.info(f"Jobs request — role: {role}, location: {location}")

    try:
        jobs = search_jobs(role, location, k=k)
        logger.info(f"Found {len(jobs)} jobs")

        return JSONResponse(content={
            "status": "success",
            "role": role,
            "location": location,
            "total": len(jobs),
            "jobs": jobs
        })

    except Exception as e:
        logger.error(f"Job search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))