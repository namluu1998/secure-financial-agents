from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    database_url: str = "sqlite+aiosqlite:///./career_agent.db"
    orchestrator_model: str = "claude-opus-4-8"
    max_jobs_for_llm_eval: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
