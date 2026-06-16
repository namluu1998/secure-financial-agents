import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.models.job import Job
from app.agents.orchestrator import CareerOrchestrator

router = APIRouter()


@router.post("/", summary="Thêm job vào database")
async def create_job(data: dict, db: AsyncSession = Depends(get_db)):
    job = Job(
        title=data["title"],
        company=data["company"],
        description=data["description"],
        location=data.get("location"),
        remote_policy=data.get("remote_policy"),
        salary_min=data.get("salary_min"),
        salary_max=data.get("salary_max"),
        currency=data.get("currency", "USD"),
        source=data.get("source"),
        external_id=data.get("external_id"),
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return {"job_id": job.id, "title": job.title, "company": job.company}


@router.post("/match/{candidate_id}", summary="Claude tự tìm và match jobs cho candidate")
async def match_jobs(
    candidate_id: str,
    preferences: dict = {},
    db: AsyncSession = Depends(get_db),
):
    dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = dna_result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA chưa có — hãy upload CV trước")

    career_dna = json.loads(dna.raw_json)
    orchestrator = CareerOrchestrator(db)

    pref_text = ""
    if preferences:
        pref_text = f"\nPreferences: {json.dumps(preferences, ensure_ascii=False)}"

    response = await orchestrator.run(
        task=f"Tìm jobs phù hợp cho candidate {candidate_id} và tính match score cho từng job. "
             f"Dùng tool query_jobs để lấy danh sách, sau đó phân tích và lưu kết quả bằng save_match_result.{pref_text}",
        context={
            "candidate_id": candidate_id,
            "career_dna_summary": {
                "seniority": career_dna.get("seniority_level"),
                "skills": [s["skill"] for s in career_dna.get("hard_skills", [])[:8]],
                "current_title": career_dna.get("current_title"),
                "market_value": career_dna.get("market_value_usd_range"),
            },
        },
    )

    return {
        "candidate_id": candidate_id,
        "agent_response": response.get("result"),
        "matches": response.get("matches", []),
        "mode": response.get("mode"),
    }
