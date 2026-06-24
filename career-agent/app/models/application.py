import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"))
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id"))
    match_score: Mapped[float | None] = mapped_column(Float)

    # Workflow status
    # pending_review → approved | rejected → resume_ready → pending_submit → applied | interviewing | offered | declined
    status: Mapped[str] = mapped_column(String(50), default="pending_review")

    # Human-in-the-loop decision
    user_decision: Mapped[str | None] = mapped_column(String(20))   # approved | rejected | skipped
    user_notes: Mapped[str | None] = mapped_column(Text)            # lý do user reject hoặc ghi chú
    decided_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Resume
    resume_version: Mapped[str | None] = mapped_column(String(10))
    resume_content: Mapped[str | None] = mapped_column(Text)
    cover_letter_content: Mapped[str | None] = mapped_column(Text)

    # Analysis
    match_analysis_json: Mapped[str | None] = mapped_column(Text)

    # Apply consent — bắt buộc có trước khi nộp
    user_consent_apply: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate: Mapped["Candidate"] = relationship(back_populates="applications")

