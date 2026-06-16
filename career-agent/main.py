from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.api.routes import profile, jobs, resume, interview, salary

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


@app.on_event("startup")
async def startup():
    await create_tables()


@app.get("/health")
async def health():
    return {"status": "ok"}
