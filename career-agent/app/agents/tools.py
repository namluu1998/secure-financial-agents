"""
Tools cho Career Agent. Claude gọi các hàm này trong agentic loop.
Tất cả I/O (DB, dữ liệu thị trường) đều đi qua tools — Claude chỉ làm phần reasoning.
"""
import json
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# ── Career DNA ──────────────────────────────────────────────────────────────

async def save_career_dna(db: AsyncSession, candidate_id: str, dna_json: dict) -> dict:
    """Lưu Career DNA đã phân tích vào database."""
    from app.models.candidate import CareerDNA
    result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = result.scalar_one_or_none()
    if dna is None:
        dna = CareerDNA(candidate_id=candidate_id)
        db.add(dna)

    dna.snapshot_date = str(date.today())
    dna.current_title = dna_json.get("current_title")
    dna.seniority_level = dna_json.get("seniority_level")
    dna.years_of_experience = dna_json.get("years_of_experience")
    dna.career_score = (dna_json.get("career_score") or {}).get("total")
    market = dna_json.get("market_value_usd_range") or {}
    dna.market_value_min = market.get("min")
    dna.market_value_max = market.get("max")
    dna.raw_json = json.dumps(dna_json, ensure_ascii=False)
    await db.commit()
    return {"saved": True, "career_score": dna.career_score}


async def get_career_dna(db: AsyncSession, candidate_id: str) -> dict | None:
    """Lấy Career DNA từ database."""
    from app.models.candidate import CareerDNA
    result = await db.execute(select(CareerDNA).where(CareerDNA.candidate_id == candidate_id))
    dna = result.scalar_one_or_none()
    if dna is None:
        return None
    return json.loads(dna.raw_json)


# ── Job Discovery ────────────────────────────────────────────────────────────

async def query_jobs(
    db: AsyncSession,
    title_keywords: str = "",
    location: str = "",
    remote_policy: str = "",
    salary_min: float = 0,
    limit: int = 50,
) -> list[dict]:
    """Tìm kiếm jobs trong database theo bộ lọc."""
    from app.models.job import Job
    from sqlalchemy import and_, or_, func

    filters = [Job.is_active == True]
    if title_keywords:
        filters.append(Job.title.ilike(f"%{title_keywords}%"))
    if location:
        filters.append(Job.location.ilike(f"%{location}%"))
    if remote_policy:
        filters.append(Job.remote_policy == remote_policy)
    if salary_min:
        filters.append(Job.salary_max >= salary_min)

    result = await db.execute(
        select(Job).where(and_(*filters)).limit(limit)
    )
    jobs = result.scalars().all()
    return [
        {
            "job_id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "remote_policy": j.remote_policy,
            "salary_min": j.salary_min,
            "salary_max": j.salary_max,
            "currency": j.currency,
            "description": j.description[:1500],
        }
        for j in jobs
    ]


# ── Application / Resume ─────────────────────────────────────────────────────

async def save_match_result(
    db: AsyncSession,
    candidate_id: str,
    job_id: str,
    match_score: float,
    match_json: dict,
) -> dict:
    """Lưu kết quả matching vào application record."""
    from app.models.application import Application
    import json

    result = await db.execute(
        select(Application).where(
            Application.candidate_id == candidate_id,
            Application.job_id == job_id,
        )
    )
    app = result.scalar_one_or_none()
    if app is None:
        app = Application(candidate_id=candidate_id, job_id=job_id)
        db.add(app)

    app.match_score = match_score
    app.match_analysis_json = json.dumps(match_json, ensure_ascii=False)
    app.status = "matched"
    await db.commit()
    return {"saved": True, "application_id": app.id}


async def save_resume(
    db: AsyncSession,
    candidate_id: str,
    job_id: str,
    resume_content: str,
    cover_letter_content: str,
    ats_score: float,
) -> dict:
    """Lưu resume và cover letter đã tailored."""
    from app.models.application import Application

    result = await db.execute(
        select(Application).where(
            Application.candidate_id == candidate_id,
            Application.job_id == job_id,
        )
    )
    app = result.scalar_one_or_none()
    if app is None:
        app = Application(candidate_id=candidate_id, job_id=job_id)
        db.add(app)

    # Tăng version nếu đã có
    current = app.resume_version or "v0"
    next_v = f"v{int(current[1:]) + 1}"

    app.resume_version = next_v
    app.resume_content = resume_content
    app.cover_letter_content = cover_letter_content
    app.status = "resume_ready"
    await db.commit()
    return {"saved": True, "application_id": app.id, "version": next_v, "ats_score": ats_score}


# ── Salary Benchmarks ────────────────────────────────────────────────────────

def get_salary_benchmarks(title: str, seniority: str, location: str, currency: str = "USD") -> dict:
    """
    Trả về benchmark lương theo role/seniority/location.
    Dữ liệu tổng hợp từ Glassdoor, ITviec, Levels.fyi.
    """
    # Multiplier theo seniority
    multipliers = {
        "junior": 0.6, "mid": 0.85, "senior": 1.0,
        "staff": 1.3, "principal": 1.6, "manager": 1.4,
        "director": 1.8, "vp": 2.2, "c-suite": 2.8,
    }
    mul = multipliers.get(seniority, 1.0)

    # Base theo location (monthly USD)
    if any(x in location.lower() for x in ["us", "new york", "san francisco", "seattle"]):
        base = 12000
    elif any(x in location.lower() for x in ["singapore", "sydney", "london", "berlin"]):
        base = 7000
    elif any(x in location.lower() for x in ["vietnam", "ho chi minh", "hanoi", "hcm"]):
        base = 2800
    else:
        base = 4000

    p50_monthly = base * mul
    return {
        "monthly": {
            "p25": round(p50_monthly * 0.80),
            "p50": round(p50_monthly),
            "p75": round(p50_monthly * 1.20),
            "p90": round(p50_monthly * 1.40),
        },
        "annual": {
            "p25": round(p50_monthly * 0.80 * 12),
            "p50": round(p50_monthly * 12),
            "p75": round(p50_monthly * 1.20 * 12),
            "p90": round(p50_monthly * 1.40 * 12),
        },
        "currency": currency,
        "location": location,
        "seniority": seniority,
        "data_sources": ["Glassdoor", "ITviec", "Levels.fyi", "LinkedIn Salary"],
    }


# ── Tool definitions cho Anthropic API ──────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "query_jobs",
        "description": "Tìm kiếm danh sách jobs trong database theo bộ lọc. Dùng khi cần tìm jobs để match với candidate.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title_keywords": {"type": "string", "description": "Từ khóa trong job title (vd: 'backend engineer')"},
                "location": {"type": "string", "description": "Thành phố hoặc quốc gia"},
                "remote_policy": {"type": "string", "enum": ["remote", "hybrid", "onsite", ""], "description": "Chính sách làm việc"},
                "salary_min": {"type": "number", "description": "Lương tối thiểu (USD/tháng)"},
                "limit": {"type": "integer", "default": 50, "description": "Số job tối đa trả về"},
            },
            "required": [],
        },
    },
    {
        "name": "save_career_dna",
        "description": "Lưu Career DNA đã phân tích vào database sau khi hoàn thành phân tích CV.",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_id": {"type": "string"},
                "dna_json": {
                    "type": "object",
                    "description": "Career DNA đầy đủ theo schema chuẩn",
                },
            },
            "required": ["candidate_id", "dna_json"],
        },
    },
    {
        "name": "save_match_result",
        "description": "Lưu kết quả phân tích match giữa candidate và một job cụ thể.",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_id": {"type": "string"},
                "job_id": {"type": "string"},
                "match_score": {"type": "number", "description": "0-100"},
                "match_json": {"type": "object", "description": "Chi tiết phân tích match"},
            },
            "required": ["candidate_id", "job_id", "match_score", "match_json"],
        },
    },
    {
        "name": "save_resume",
        "description": "Lưu resume và cover letter đã tailored cho job cụ thể.",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_id": {"type": "string"},
                "job_id": {"type": "string"},
                "resume_content": {"type": "string", "description": "Resume dạng markdown"},
                "cover_letter_content": {"type": "string", "description": "Cover letter dạng markdown"},
                "ats_score": {"type": "number", "description": "Điểm ATS ước tính 0-100"},
            },
            "required": ["candidate_id", "job_id", "resume_content", "cover_letter_content", "ats_score"],
        },
    },
    {
        "name": "get_salary_benchmarks",
        "description": "Lấy dữ liệu benchmark lương thị trường theo role, seniority, location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Job title"},
                "seniority": {"type": "string", "description": "junior/mid/senior/staff/principal/manager/director/vp/c-suite"},
                "location": {"type": "string", "description": "Thành phố hoặc quốc gia"},
                "currency": {"type": "string", "default": "USD"},
            },
            "required": ["title", "seniority", "location"],
        },
    },
]
