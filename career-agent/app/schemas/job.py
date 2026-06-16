from pydantic import BaseModel
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    location: str | None = None
    remote_policy: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    currency: str | None = "USD"
    source: str | None = None
    external_id: str | None = None


class JobMatchResult(BaseModel):
    job_id: str
    title: str
    company: str
    match_score: float
    recommendation: str
    rationale: str
    missing_skills: list[dict]
    career_growth_potential: str


class JobMatchResponse(BaseModel):
    candidate_id: str
    matches: list[JobMatchResult]
