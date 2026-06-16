import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"))
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    match_score: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="matched")  # matched | resume_ready | applied | interviewing | offered | rejected
    resume_version: Mapped[str | None] = mapped_column(String(10))
    resume_content: Mapped[str | None] = mapped_column(Text)
    cover_letter_content: Mapped[str | None] = mapped_column(Text)
    match_analysis_json: Mapped[str | None] = mapped_column(Text)
    user_consent_apply: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate: Mapped["Candidate"] = relationship(back_populates="applications")
