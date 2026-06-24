import json
from datetime import date
from app.config import settings
from app.core.prompt_templates import CAREER_DNA_SYSTEM


class CareerDNAAgent:
    def __init__(self, model: str):
        self.model = model

    async def run(self, candidate_id: str, cv_text: str) -> dict:
        if settings.mock_mode:
            from app.agents.mock_responses import career_dna_mock
            return career_dna_mock(candidate_id)

        import anthropic
        client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        response = await client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=CAREER_DNA_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": f"candidate_id: {candidate_id}\ntoday: {date.today()}\n\n<cv_text>\n{cv_text}\n</cv_text>",
                }
            ],
        )
        text = response.content[0].text
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
