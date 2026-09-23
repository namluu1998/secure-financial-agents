"""
Career Orchestrator — entry point duy nhất cho tất cả tasks.

- Mock mode (không có API key): dùng CareerAgent với mock responses
- Live mode (có API key): dùng MultiAgentCareerOrchestrator
  Orchestrator Opus → gọi sub-agents Haiku chuyên biệt
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings


class CareerOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def run(self, task: str, context: dict | None = None) -> dict:
        if settings.mock_mode:
            from app.agents.career_agent import CareerAgent
            return await CareerAgent(self.db).run(task, context)

        from app.agents.multi_agent import MultiAgentCareerOrchestrator
        return await MultiAgentCareerOrchestrator(self.db).run(task, context)

