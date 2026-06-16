import anthropic
from app.config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)


class CareerOrchestrator:
    """Routes tasks to specialized career agents. No agent calls another directly."""

    def __init__(self):
        self.model = settings.orchestrator_model

    async def run_career_dna(self, candidate_id: str, cv_text: str) -> dict:
        from app.agents.career_dna import CareerDNAAgent
        return await CareerDNAAgent(self.model).run(candidate_id, cv_text)

    async def run_job_matching(self, career_dna: dict, jobs: list[dict], preferences: dict) -> list[dict]:
        from app.agents.job_matcher import JobMatcherAgent
        return await JobMatcherAgent(self.model).run(career_dna, jobs, preferences)

    async def run_resume_tailor(self, career_dna: dict, job: dict, match_analysis: dict) -> dict:
        from app.agents.resume_tailor import ResumeTailorAgent
        return await ResumeTailorAgent(self.model).run(career_dna, job, match_analysis)

    async def run_interview_prep(self, career_dna: dict, job: dict, interview_type: str) -> dict:
        from app.agents.interview_agent import InterviewAgent
        return await InterviewAgent(self.model).run(career_dna, job, interview_type)

    async def run_salary_benchmark(self, career_dna: dict, offer: dict) -> dict:
        from app.agents.salary_agent import SalaryAgent
        return await SalaryAgent(self.model).run(career_dna, offer)
