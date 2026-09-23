from pydantic import BaseModel


class ResumeRequest(BaseModel):
    candidate_id: str
    job_id: str


class ResumeResponse(BaseModel):
    application_id: str
    candidate_id: str
    job_id: str
    resume_version: str
    resume_content: str
    cover_letter_content: str
    ats_score_estimate: float | None


class InterviewRequest(BaseModel):
    candidate_id: str
    job_id: str
    interview_type: str = "behavioural"


class SalaryRequest(BaseModel):
    candidate_id: str
    job_id: str | None = None
    base_salary: float
    bonus_target_pct: float = 0
    equity_value_usd: float = 0
    equity_vesting_years: int = 4
    currency: str = "USD"
    location: str
