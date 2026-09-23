import pytest


def test_prompt_templates_exist():
    from app.core.prompt_templates import (
        CAREER_DNA_SYSTEM,
        JOB_MATCHER_SYSTEM,
        RESUME_TAILOR_SYSTEM,
        INTERVIEW_PREP_SYSTEM,
        SALARY_BENCHMARK_SYSTEM,
    )
    assert "Career DNA" in CAREER_DNA_SYSTEM
    assert "Match Score" in JOB_MATCHER_SYSTEM
    assert "ATS" in RESUME_TAILOR_SYSTEM
    assert "briefing" in INTERVIEW_PREP_SYSTEM
    assert "negotiation" in SALARY_BENCHMARK_SYSTEM


def test_orchestrator_imports():
    from app.agents.orchestrator import CareerOrchestrator
    assert CareerOrchestrator is not None
