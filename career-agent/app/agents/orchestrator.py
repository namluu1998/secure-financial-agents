"""
Career Orchestrator — entry point duy nhất cho tất cả tasks.
Khởi tạo CareerAgent với DB session và route task tới đó.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.career_agent import CareerAgent


class CareerOrchestrator:
    def __init__(self, db: AsyncSession):
        self.agent = CareerAgent(db)

    async def run(self, task: str, context: dict | None = None) -> dict:
        return await self.agent.run(task, context)
