import json
from datetime import date
import anthropic
from app.core.prompt_templates import CAREER_DNA_SYSTEM


class CareerDNAAgent:
    def __init__(self, model: str):
        self.client = anthropic.AsyncAnthropic()
        self.model = model

    async def run(self, candidate_id: str, cv_text: str) -> dict:
        response = await self.client.messages.create(
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
        # Extract JSON from response
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
