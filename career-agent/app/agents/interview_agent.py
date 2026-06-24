import json
from app.config import settings
from app.core.prompt_templates import INTERVIEW_PREP_SYSTEM


class InterviewAgent:
    def __init__(self, model: str):
        self.model = model

    async def run(self, career_dna: dict, job: dict, interview_type: str) -> dict:
        if settings.mock_mode:
            from app.agents.mock_responses import interview_prep_mock
            return interview_prep_mock(job, interview_type)

        import anthropic
        client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        response = await client.messages.create(
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
