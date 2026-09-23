"""
Human-in-the-loop review flow.
User xem kết quả match, quyết định approve/reject trước khi tạo resume và nộp.
"""
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.candidate import CareerDNA
from app.agents.orchestrator import CareerOrchestrator

router = APIRouter()


@router.get("/{candidate_id}", summary="Xem tất cả matches đang chờ user duyệt")
async def list_pending_reviews(candidate_id: str, db: AsyncSession = Depends(get_db)):
    """Trả danh sách matches chưa được user duyệt, kèm thông tin đủ để quyết định."""
    result = await db.execute(
        select(Application, Job)
        .join(Job, Application.job_id == Job.id)
        .where(
            Application.candidate_id == candidate_id,
            Application.status == "pending_review",
        )
        .order_by(Application.match_score.desc())
    )
    rows = result.all()

    items = []
    for app, job in rows:
        analysis = json.loads(app.match_analysis_json) if app.match_analysis_json else {}
        items.append({
            "application_id": app.id,
            "job": {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "remote_policy": job.remote_policy,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "currency": job.currency,
            },
            "match_score": app.match_score,
            "recommendation": analysis.get("recommendation"),
            "rationale": analysis.get("rationale"),
            "missing_skills": analysis.get("missing_skills", []),
            "career_growth_potential": analysis.get("career_growth_potential"),
            "status": app.status,
            "created_at": app.created_at.isoformat(),
        })

    return {
        "candidate_id": candidate_id,
        "pending_count": len(items),
        "matches": items,
    }


@router.get("/{candidate_id}/all", summary="Xem tất cả applications theo trạng thái")
async def list_all_applications(candidate_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Application, Job)
        .join(Job, Application.job_id == Job.id)
        .where(Application.candidate_id == candidate_id)
        .order_by(Application.match_score.desc())
    )
    rows = result.all()

    by_status: dict[str, list] = {}
    for app, job in rows:
        entry = {
            "application_id": app.id,
            "title": job.title,
            "company": job.company,
            "match_score": app.match_score,
            "user_decision": app.user_decision,
            "user_notes": app.user_notes,
            "resume_version": app.resume_version,
            "decided_at": app.decided_at.isoformat() if app.decided_at else None,
        }
        by_status.setdefault(app.status, []).append(entry)

    return {"candidate_id": candidate_id, "applications": by_status}


@router.post("/{application_id}/decide", summary="User quyết định approve hoặc reject job")
async def decide_application(
    application_id: str,
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    """
    data = {
      "decision": "approved" | "rejected" | "skipped",
      "notes": "lý do (tuỳ chọn)"
    }

    Nếu approved → tự động trigger tạo resume.
    Nếu rejected → đánh dấu và bỏ qua.
    """
    decision = data.get("decision")
    if decision not in ("approved", "rejected", "skipped"):
        raise HTTPException(400, "decision phải là: approved | rejected | skipped")

    result = await db.execute(select(Application).where(Application.id == application_id))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "Application không tồn tại")
    if app.status != "pending_review":
        raise HTTPException(400, f"Application đang ở trạng thái '{app.status}', không thể duyệt lại")

    app.user_decision = decision
    app.user_notes = data.get("notes")
    app.decided_at = datetime.utcnow()

    if decision == "approved":
        app.status = "approved"
        app.user_consent_apply = True
        await db.commit()

        # Tự động tạo resume sau khi approved
        job_result = await db.execute(select(Job).where(Job.id == app.job_id))
        job = job_result.scalar_one()
        dna_result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == app.candidate_id))
        dna = dna_result.scalar_one_or_none()

        orchestrator = CareerOrchestrator(db)
        resume_response = await orchestrator.run(
            task=f"Viết resume ATS-optimized và cover letter cho candidate {app.candidate_id} "
                 f"ứng tuyển job {app.job_id} tại {job.company}. "
                 f"Lưu bằng tool save_resume.",
            context={
                "candidate_id": app.candidate_id,
                "job_id": app.job_id,
                "job": {
                    "title": job.title, "company": job.company,
                    "location": job.location, "description": job.description,
                    "salary_min": job.salary_min, "salary_max": job.salary_max,
                },
                "career_dna": json.loads(dna.raw_json) if dna else {},
            },
        )

        # Reload application sau khi resume được lưu
        await db.refresh(app)
        return {
            "application_id": application_id,
            "decision": decision,
            "status": app.status,
            "message": f"✅ Approved! Resume đã được tạo cho {job.title} @ {job.company}.",
            "resume_version": app.resume_version,
            "resume_preview": (app.resume_content or "")[:300] + "..." if app.resume_content else None,
            "agent_response": resume_response.get("result"),
        }

    else:
        app.status = "rejected" if decision == "rejected" else "skipped"
        await db.commit()
        return {
            "application_id": application_id,
            "decision": decision,
            "status": app.status,
            "message": f"{'❌ Đã reject.' if decision == 'rejected' else '⏭️ Đã bỏ qua.'} Lý do: {data.get('notes', 'không có')}",
        }


@router.post("/{application_id}/approve-submit", summary="User xác nhận nộp đơn (sau khi đã review resume)")
async def approve_submit(application_id: str, db: AsyncSession = Depends(get_db)):
    """
    Bước cuối: user xác nhận nộp sau khi đã đọc resume.
    Thực tế sẽ gọi Apply Agent — hiện tại chỉ cập nhật status.
    """
    result = await db.execute(select(Application).where(Application.id == application_id))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "Application không tồn tại")
    if not app.resume_content:
        raise HTTPException(400, "Resume chưa được tạo — approve job trước")
    if not app.user_consent_apply:
        raise HTTPException(403, "Cần user consent trước khi nộp")

    app.status = "applied"
    app.updated_at = datetime.utcnow()
    await db.commit()

    job_result = await db.execute(select(Job).where(Job.id == app.job_id))
    job = job_result.scalar_one()

    return {
        "application_id": application_id,
        "status": "applied",
        "message": f"🚀 Đã nộp đơn cho {job.title} @ {job.company}!",
        "note": "Apply Agent sẽ điền form và submit — tính năng đang phát triển.",
    }
