import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.candidate import Candidate, CareerDNA
from app.agents.orchestrator import CareerOrchestrator

router = APIRouter()


@router.post("/", summary="Tạo hồ sơ candidate")
async def create_candidate(data: dict, db: AsyncSession = Depends(get_db)):
    candidate = Candidate(email=data["email"], full_name=data.get("full_name"))
    db.add(candidate)
    await db.commit()
    await db.refresh(candidate)
    return {"candidate_id": candidate.id, "email": candidate.email}


@router.post("/{candidate_id}/upload-cv", summary="Upload CV — Claude tự phân tích và xây dựng Career DNA")
async def upload_cv(
    candidate_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    if not result.scalar_one_or_none():
        raise HTTPException(404, "Candidate không tồn tại")

    content = await file.read()
    if file.filename and file.filename.endswith(".pdf"):
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(content))
        cv_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        cv_text = content.decode("utf-8", errors="ignore")

    orchestrator = CareerOrchestrator(db)
    response = await orchestrator.run(
        task=f"Phân tích CV sau và xây dựng Career DNA cho candidate {candidate_id}. "
             f"Sau khi phân tích xong, lưu vào database bằng tool save_career_dna.",
        context={"candidate_id": candidate_id, "cv_text": cv_text},
    )

    # Đọc lại từ DB để trả về
    dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = dna_result.scalar_one_or_none()
    career_dna = json.loads(dna.raw_json) if dna else {}

    return {
        "candidate_id": candidate_id,
        "career_score": dna.career_score if dna else None,
        "agent_response": response.get("result"),
        "mode": response.get("mode"),
        "career_dna": career_dna,
    }


@router.get("/{candidate_id}/career-dna", summary="Xem Career DNA")
async def get_career_dna(candidate_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = result.scalar_one_or_none()
    if not dna:
        raise HTTPException(404, "Career DNA chưa có — hãy upload CV trước")
    return json.loads(dna.raw_json)
