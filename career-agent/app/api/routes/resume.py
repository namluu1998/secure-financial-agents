import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.models.job import Job
from app.models.application import Application
from app.agents.orchestrator import CareerOrchestrator

router = APIRouter()


@router.post("/tailor", summary="Claude tự viết resume ATS-optimized và cover letter cho job cụ thể")
async def tailor_resume(data: dict, db: AsyncSession = Depends(get_db)):
    candidate_id = data["candidate_id"]
    job_id = data["job_id"]

    dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = dna_result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA chưa có")

    job_result = await db.execute(select(Job).where(Job.id == job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job không tồn tại")

    orchestrator = CareerOrchestrator(db)
    response = await orchestrator.run(
        task=f"Viết resume ATS-optimized và cover letter cho candidate {candidate_id} ứng tuyển job {job_id}. "
             f"Sau khi xong, lưu bằng tool save_resume với ats_score ước tính.",
        context={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "job": {
                "title": job.title, "company": job.company,
                "location": job.location, "description": job.description,
                "salary_min": job.salary_min, "salary_max": job.salary_max,
            },
            "career_dna": json.loads(dna.raw_json),
        },
    )

    # Đọc lại application từ DB
    app_result = await db.execute(
        select(Application).where(
            Application.candidate_id == candidate_id,
            Application.job_id == job_id,
        )
    )
    application = app_result.scalar_one_or_none()

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "agent_response": response.get("result"),
        "mode": response.get("mode"),
        "resume_version": application.resume_version if application else None,
        "resume_content": application.resume_content if application else response.get("resume_markdown"),
        "cover_letter_content": application.cover_letter_content if application else response.get("cover_letter_markdown"),
    }
