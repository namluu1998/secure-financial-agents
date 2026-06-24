import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.agents.orchestrator import CareerOrchestrator

router = APIRouter()


@router.post("/benchmark", summary="Claude phân tích offer và đưa ra chiến lược thương lượng lương")
async def benchmark_salary(data: dict, db: AsyncSession = Depends(get_db)):
    candidate_id = data["candidate_id"]

    dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = dna_result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA chưa có")

    career_dna = json.loads(dna.raw_json)
    offer = {k: v for k, v in data.items() if k != "candidate_id"}

    orchestrator = CareerOrchestrator(db)
    response = await orchestrator.run(
        task=f"Phân tích offer lương cho candidate {candidate_id}. "
             f"Dùng tool get_salary_benchmarks để lấy dữ liệu thị trường, "
             f"sau đó đánh giá offer và đưa ra chiến lược thương lượng cụ thể.",
        context={
            "candidate_id": candidate_id,
            "offer": offer,
            "candidate_profile": {
                "title": career_dna.get("current_title"),
                "seniority": career_dna.get("seniority_level"),
                "years_experience": career_dna.get("years_of_experience"),
                "location": offer.get("location", "Ho Chi Minh City"),
            },
        },
    )

    return {
        "candidate_id": candidate_id,
        "agent_response": response.get("result"),
        "analysis": response.get("analysis"),
        "market_benchmarks": response.get("market_benchmarks"),
        "mode": response.get("mode"),
    }
