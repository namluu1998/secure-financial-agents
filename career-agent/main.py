from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.api.routes import profile, jobs, resume, interview, salary, review

app = FastAPI(
    title="Career Agent API",
    description="AI career operating system — personal headhunter powered by Claude",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/profile", tags=["Career DNA"])
app.include_router(jobs.router, prefix="/jobs", tags=["Job Matching"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])
app.include_router(interview.router, prefix="/interview", tags=["Interview"])
app.include_router(salary.router, prefix="/salary", tags=["Salary"])
app.include_router(review.router, prefix="/review", tags=["Human Review"])


@app.on_event("startup")
async def startup():
    await create_tables()
    from app.config import settings
    import sys
    if settings.mock_mode:
        mode = "MOCK (no API key)"
    else:
        mode = "LIVE — Multi-Agent (Opus orchestrator + Haiku sub-agents)"
    print(f"\n{'='*60}\n  Career Agent API — {mode}\n{'='*60}\n", file=sys.stderr)


@app.get("/health")
async def health():
    from app.config import settings
    return {"status": "ok", "mode": "mock" if settings.mock_mode else "multi-agent"}


@app.get("/agent/info", tags=["System"])
async def agent_info():
    from app.config import settings
    if settings.mock_mode:
        return {"mode": "mock", "description": "Không có API key — dùng mock responses"}
    return {
        "mode": "multi-agent",
        "architecture": {
            "orchestrator": {
                "model": settings.orchestrator_model,
                "role": "Điều phối workflow, quyết định gọi sub-agent nào",
            },
            "sub_agents": [
                {"name": "career_dna_agent",   "model": "claude-haiku-4-5-20251001", "task": "Phân tích CV → Career DNA JSON"},
                {"name": "job_matcher_agent",   "model": "claude-haiku-4-5-20251001", "task": "Tính Match Score cho jobs"},
                {"name": "resume_tailor_agent", "model": "claude-haiku-4-5-20251001", "task": "Viết resume + cover letter"},
                {"name": "interview_agent",     "model": "claude-haiku-4-5-20251001", "task": "Tạo briefing pack phỏng vấn"},
                {"name": "salary_agent",        "model": "claude-haiku-4-5-20251001", "task": "Benchmark lương + thương lượng"},
            ],
            "db_tools": ["query_jobs", "save_career_dna", "save_match_result", "save_resume"],
            "routing": "Sub-agents không gọi nhau — mọi điều phối qua Orchestrator",
        },
    }
