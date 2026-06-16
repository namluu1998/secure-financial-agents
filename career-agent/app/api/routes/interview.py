import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.models.job import Job
from app.agents.orchestrator import CareerOrchestrator
from app.schemas.application import InterviewRequest

router = APIRouter()
orchestrator = CareerOrchestrator()


@router.post("/prepare", summary="Generate interview briefing pack")
async def prepare_interview(data: InterviewRequest, db: AsyncSession = Depends(get_db)):
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
    }

    briefing = await orchestrator.run_interview_prep(
        json.loads(dna.raw_json), job_data, data.interview_type
    )
    return {"candidate_id": data.candidate_id, "job_id": data.job_id, "briefing": briefing}
