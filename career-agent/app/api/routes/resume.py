import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.models.job import Job
from app.models.application import Application
from app.agents.orchestrator import CareerOrchestrator
from app.schemas.application import ResumeRequest, ResumeResponse

router = APIRouter()
orchestrator = CareerOrchestrator()


@router.post("/tailor", summary="Generate tailored resume and cover letter")
async def tailor_resume(data: ResumeRequest, db: AsyncSession = Depends(get_db)):
    dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == data.candidate_id))
    dna = dna_result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA not found")

    job_result = await db.execute(select(Job).where(Job.id == data.job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")

    job_data = {
        "job_id": job.id, "title": job.title, "company": job.company,
        "location": job.location, "description": job.description,
        "salary_min": job.salary_min, "salary_max": job.salary_max,
    }

    result = await orchestrator.run_resume_tailor(json.loads(dna.raw_json), job_data, {})

    # Upsert application record
    app_result = await db.execute(
        select(Application).where(
            Application.candidate_id == data.candidate_id,
            Application.job_id == data.job_id,
        )
    )
    application = app_result.scalar_one_or_none()
    if application is None:
        application = Application(candidate_id=data.candidate_id, job_id=data.job_id)
        db.add(application)

    application.resume_version = result.get("version", "v1")
    application.resume_content = result.get("resume_markdown", "")
    application.cover_letter_content = result.get("cover_letter_markdown", "")
    application.status = "resume_ready"
    await db.commit()
    await db.refresh(application)

    return {
        "application_id": application.id,
        "candidate_id": data.candidate_id,
        "job_id": data.job_id,
        "resume_version": application.resume_version,
        "resume_content": application.resume_content,
        "cover_letter_content": application.cover_letter_content,
        "ats_score_estimate": result.get("ats_score_estimate"),
    }
