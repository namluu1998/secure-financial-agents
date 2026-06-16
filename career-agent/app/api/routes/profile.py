import json
from datetime import date
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import Candidate, CareerDNA
from app.agents.orchestrator import CareerOrchestrator
from app.schemas.candidate import CandidateCreate, CareerDNAResponse

router = APIRouter()
orchestrator = CareerOrchestrator()


@router.post("/", summary="Create candidate profile")
async def create_candidate(data: CandidateCreate, db: AsyncSession = Depends(get_db)):
    candidate = Candidate(email=data.email, full_name=data.full_name)
    db.add(candidate)
    await db.commit()
    await db.refresh(candidate)
    return {"candidate_id": candidate.id, "email": candidate.email}


@router.post("/{candidate_id}/upload-cv", summary="Upload CV and build Career DNA")
async def upload_cv(
    candidate_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(404, "Candidate not found")

    content = await file.read()
    # Basic text extraction — for PDFs use pypdf, for txt read directly
    if file.filename.endswith(".pdf"):
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(content))
        cv_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        cv_text = content.decode("utf-8", errors="ignore")

    dna_data = await orchestrator.run_career_dna(candidate_id, cv_text)

    # Upsert Career DNA
    result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = result.scalar_one_or_none()
    if dna is None:
        dna = CareerDNA(candidate_id=candidate_id)
        db.add(dna)

    dna.snapshot_date = str(date.today())
    dna.current_title = dna_data.get("current_title")
    dna.seniority_level = dna_data.get("seniority_level")
    dna.years_of_experience = dna_data.get("years_of_experience")
    dna.career_score = dna_data.get("career_score", {}).get("total")
    market = dna_data.get("market_value_usd_range", {})
    dna.market_value_min = market.get("min")
    dna.market_value_max = market.get("max")
    dna.raw_json = json.dumps(dna_data, ensure_ascii=False)

    await db.commit()
    return {"candidate_id": candidate_id, "career_score": dna.career_score, "career_dna": dna_data}


@router.get("/{candidate_id}/career-dna", summary="Get Career DNA")
async def get_career_dna(candidate_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA not found — upload a CV first")
    return json.loads(dna.raw_json)
