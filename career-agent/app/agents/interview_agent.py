import json
import anthropic
from app.core.prompt_templates import INTERVIEW_PREP_SYSTEM


class InterviewAgent:
    def __init__(self, model: str):
        self.client = anthropic.AsyncAnthropic()
        self.model = model

    async def run(self, career_dna: dict, job: dict, interview_type: str) -> dict:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=INTERVIEW_PREP_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Interview type: {interview_type}\n\n"
                        f"Job:\n{json.dumps(job, ensure_ascii=False)}\n\n"
                        f"Candidate Career DNA:\n{json.dumps(career_dna, ensure_ascii=False)}"
                    ),
                }
            ],
        )
        text = response.content[0].text
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
