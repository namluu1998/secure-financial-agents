import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    career_dna: Mapped["CareerDNA | None"] = relationship(back_populates="candidate", uselist=False)
    applications: Mapped[list["Application"]] = relationship(back_populates="candidate")


class CareerDNA(Base):
    __tablename__ = "career_dna"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), unique=True)
    snapshot_date: Mapped[str] = mapped_column(String(10))
    current_title: Mapped[str | None] = mapped_column(String(255))
    seniority_level: Mapped[str | None] = mapped_column(String(50))
    years_of_experience: Mapped[float | None] = mapped_column(Float)
    career_score: Mapped[float | None] = mapped_column(Float)
    market_value_min: Mapped[float | None] = mapped_column(Float)
    market_value_max: Mapped[float | None] = mapped_column(Float)
    raw_json: Mapped[str] = mapped_column(Text)  # full Career DNA JSON
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate: Mapped["Candidate"] = relationship(back_populates="career_dna")
