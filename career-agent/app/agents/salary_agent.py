import json
from app.config import settings
from app.core.prompt_templates import SALARY_BENCHMARK_SYSTEM


class SalaryAgent:
    def __init__(self, model: str):
        self.model = model

    async def run(self, career_dna: dict, offer: dict) -> dict:
        if settings.mock_mode:
            from app.agents.mock_responses import salary_benchmark_mock
            return salary_benchmark_mock(offer)

        import anthropic
        client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        response = await client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=SALARY_BENCHMARK_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Candidate profile summary:\n"
                        f"- Title: {career_dna.get('current_title')}\n"
                        f"- Seniority: {career_dna.get('seniority_level')}\n"
                        f"- Years experience: {career_dna.get('years_of_experience')}\n"
                        f"- Industries: {career_dna.get('industries', [])}\n\n"
                        f"Offer details:\n{json.dumps(offer, ensure_ascii=False)}"
                    ),
                }
            ],
        )
        text = response.content[0].text
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
