from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    email: str
    full_name: str | None = None


class CareerDNAResponse(BaseModel):
    candidate_id: str
    snapshot_date: str
    current_title: str | None
    seniority_level: str | None
    years_of_experience: float | None
    career_score: float | None
    market_value_min: float | None
    market_value_max: float | None
    raw_json: dict

    class Config:
        from_attributes = True
