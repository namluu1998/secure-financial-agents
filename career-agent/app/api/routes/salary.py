import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import CareerDNA
from app.agents.orchestrator import CareerOrchestrator
from app.schemas.application import SalaryRequest

router = APIRouter()
orchestrator = CareerOrchestrator()


@router.post("/benchmark", summary="Benchmark offer and produce negotiation strategy")
async def benchmark_salary(data: SalaryRequest, db: AsyncSession = Depends(get_db)):
    dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == data.candidate_id))
    dna = dna_result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA not found")

    offer = data.model_dump(exclude={"candidate_id"})
    analysis = await orchestrator.run_salary_benchmark(json.loads(dna.raw_json), offer)
    return {"candidate_id": data.candidate_id, "analysis": analysis}
