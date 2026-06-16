import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.models.job import Job
from app.agents.orchestrator import CareerOrchestrator
from app.schemas.job import JobCreate, JobMatchResponse

router = APIRouter()
orchestrator = CareerOrchestrator()


@router.post("/", summary="Add a job to the database")
async def create_job(data: JobCreate, db: AsyncSession = Depends(get_db)):
    job = Job(**data.model_dump())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return {"job_id": job.id, "title": job.title, "company": job.company}


@router.post("/match/{candidate_id}", summary="Match jobs to candidate Career DNA")
async def match_jobs(
    candidate_id: str,
    preferences: dict = {},
    db: AsyncSession = Depends(get_db),
):
    dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = dna_result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA not found — upload a CV first")

    jobs_result = await db.execute(select(Job).where(Job.is_active == True).limit(100))
    jobs = jobs_result.scalars().all()
    if not jobs:
        raise HTTPException(404, "No jobs in database — add jobs first")

    jobs_data = [
        {
            "job_id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "remote_policy": j.remote_policy,
            "salary_min": j.salary_min,
            "salary_max": j.salary_max,
            "description": j.description[:2000],  # cap to manage token cost
        }
        for j in jobs
    ]

    matches = await orchestrator.run_job_matching(json.loads(dna.raw_json), jobs_data, preferences)
    matches.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return {"candidate_id": candidate_id, "matches": matches}
