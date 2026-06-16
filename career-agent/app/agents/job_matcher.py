import json
import anthropic
from app.core.prompt_templates import JOB_MATCHER_SYSTEM


class JobMatcherAgent:
    def __init__(self, model: str):
        self.client = anthropic.AsyncAnthropic()
        self.model = model

    async def run(self, career_dna: dict, jobs: list[dict], preferences: dict) -> list[dict]:
        jobs_text = json.dumps(jobs, ensure_ascii=False)
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=JOB_MATCHER_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Career DNA:\n{json.dumps(career_dna, ensure_ascii=False)}\n\n"
                        f"Candidate preferences: {json.dumps(preferences, ensure_ascii=False)}\n\n"
                        f"Jobs to evaluate (max {len(jobs)}):\n{jobs_text}\n\n"
                        "Return a JSON array of match results, one per job."
                    ),
                }
            ],
        )
        text = response.content[0].text
        start = text.find("[")
        end = text.rfind("]") + 1
        return json.loads(text[start:end])
