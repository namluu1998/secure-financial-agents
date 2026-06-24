import json
from app.config import settings
from app.core.prompt_templates import RESUME_TAILOR_SYSTEM


class ResumeTailorAgent:
    def __init__(self, model: str):
        self.model = model

    async def run(self, career_dna: dict, job: dict, match_analysis: dict) -> dict:
        if settings.mock_mode:
            from app.agents.mock_responses import resume_tailor_mock
            return resume_tailor_mock(career_dna, job)

        import anthropic
        client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        response = await client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=RESUME_TAILOR_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Career DNA:\n{json.dumps(career_dna, ensure_ascii=False)}\n\n"
                        f"Target job:\n{json.dumps(job, ensure_ascii=False)}\n\n"
                        f"Match analysis:\n{json.dumps(match_analysis, ensure_ascii=False)}"
                    ),
                }
            ],
        )
        text = response.content[0].text
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
