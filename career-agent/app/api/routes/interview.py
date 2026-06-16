import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.models.job import Job
from app.agents.orchestrator import CareerOrchestrator

router = APIRouter()


@router.post("/prepare", summary="Claude chuẩn bị bộ câu hỏi phỏng vấn và briefing pack")
async def prepare_interview(data: dict, db: AsyncSession = Depends(get_db)):
    candidate_id = data["candidate_id"]
    job_id = data["job_id"]
    interview_type = data.get("interview_type", "behavioural")

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
        task=f"Chuẩn bị interview briefing pack cho candidate {candidate_id} phỏng vấn tại {job.company}. "
             f"Loại phỏng vấn: {interview_type}. "
             f"Tạo 15-20 câu hỏi dự đoán với model answers dựa trên Career DNA của candidate.",
        context={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_type": interview_type,
            "job": {
                "title": job.title, "company": job.company,
                "location": job.location, "description": job.description,
            },
            "career_dna_summary": {
                "current_title": json.loads(dna.raw_json).get("current_title"),
                "skills": [s["skill"] for s in json.loads(dna.raw_json).get("hard_skills", [])[:6]],
                "work_history": json.loads(dna.raw_json).get("work_history", [])[:2],
                "strengths": json.loads(dna.raw_json).get("strengths", []),
                "gaps": json.loads(dna.raw_json).get("gaps", []),
            },
        },
    )

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "agent_response": response.get("result"),
        "briefing": response.get("briefing"),
        "mode": response.get("mode"),
    }
