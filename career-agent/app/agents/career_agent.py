"""
Career Agent — Claude làm trung tâm, tự quyết định dùng tools nào.
Thay vì gọi Claude như một service, Claude IS the agent.
"""
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.agents.tools import (
    TOOL_DEFINITIONS,
    save_career_dna,
    get_career_dna,
    query_jobs,
    save_match_result,
    save_resume,
    get_salary_benchmarks,
)

SYSTEM_PROMPT = """Bạn là Career Agent — một AI headhunter cá nhân 24/7.

Bạn có quyền truy cập vào các tools sau:
- query_jobs: tìm jobs trong database
- save_career_dna: lưu Career DNA sau khi phân tích xong
- save_match_result: lưu kết quả match
- save_resume: lưu resume và cover letter đã tailored
- get_salary_benchmarks: lấy dữ liệu lương thị trường

## Quy tắc phân tích Career DNA
Khi nhận CV/hồ sơ, hãy:
1. Trích xuất: skills, kinh nghiệm, học vấn, thành tích
2. Tính Career Score (0-100): skills_depth×30% + experience_breadth×25% + career_progression×25% + education×10% + market_demand×10%
3. Ước tính market value (USD/tháng)
4. Xác định điểm mạnh, khoảng trống, job titles phù hợp
5. Lưu vào database bằng save_career_dna

## Quy tắc Job Matching
Match Score = Hard Skills 30% + Experience 20% + Seniority 20% + Salary 10% + Location 10% + Holistic 10%
- strong-match: ≥80 | good-match: 65-79 | stretch: 45-64 | not-recommended: <45
Lưu từng kết quả bằng save_match_result.

## Quy tắc Resume Tailoring
- Dùng keywords từ JD một cách tự nhiên (không keyword stuffing)
- Lượng hóa thành tích (%, $, thời gian)
- Cover letter 3 đoạn: lý do apply → 2-3 thành tích liên quan → call to action
- Lưu bằng save_resume

## Quy tắc Salary Benchmarking
- Lấy benchmark từ get_salary_benchmarks
- So sánh offer với P25/P50/P75/P90
- Đưa ra target ask cụ thể (không phải range)
- Cung cấp opening script và các đòn bẩy ngoài lương

Luôn dùng tools để lưu dữ liệu. Trả lời bằng tiếng Việt khi không có yêu cầu khác."""


class CareerAgent:
    """
    Một agent duy nhất. Claude tự chọn tools, tự lặp cho đến khi xong.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = settings.orchestrator_model

    async def run(self, task: str, context: dict | None = None) -> dict:
        if settings.mock_mode:
            return await self._run_mock(task, context or {})
        return await self._run_live(task, context or {})

    async def _run_live(self, task: str, context: dict) -> dict:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

        user_message = task
        if context:
            user_message += f"\n\nContext:\n{json.dumps(context, ensure_ascii=False, indent=2)}"

        messages = [{"role": "user", "content": user_message}]

        # Agentic loop — Claude tự quyết định khi nào dừng
        for _ in range(10):  # max 10 vòng để tránh vòng lặp vô hạn
            response = await client.messages.create(
                model=self.model,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            # Claude dừng — trả về kết quả cuối
            if response.stop_reason == "end_turn":
                text = "".join(
                    block.text for block in response.content if hasattr(block, "text")
                )
                return {"result": text, "mode": "live"}

            # Claude muốn dùng tools
            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []

                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    result = await self._execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    })

                messages.append({"role": "user", "content": tool_results})

        return {"result": "Agent đã đạt giới hạn vòng lặp.", "mode": "live"}

    async def _execute_tool(self, name: str, inputs: dict) -> dict:
        """Thực thi tool mà Claude yêu cầu."""
        if name == "query_jobs":
            return await query_jobs(self.db, **inputs)
        if name == "save_career_dna":
            return await save_career_dna(self.db, **inputs)
        if name == "save_match_result":
            return await save_match_result(self.db, **inputs)
        if name == "save_resume":
            return await save_resume(self.db, **inputs)
        if name == "get_salary_benchmarks":
            return get_salary_benchmarks(**inputs)
        return {"error": f"Tool không tồn tại: {name}"}

    async def _run_mock(self, task: str, context: dict) -> dict:
        """Mock mode: mô phỏng agentic loop, không gọi Claude."""
        task_lower = task.lower()

        # Thứ tự kiểm tra: cụ thể nhất trước
        if "save_resume" in task_lower or "viết resume" in task_lower or "cover letter" in task_lower:
            candidate_id = context.get("candidate_id", "mock-001")
            job_id = context.get("job_id", "mock-job")
            dna = await get_career_dna(self.db, candidate_id) or {}
            from app.agents.mock_responses import resume_tailor_mock
            result = resume_tailor_mock(dna, context.get("job", {}))
            await save_resume(
                self.db, candidate_id, job_id,
                result["resume_markdown"], result["cover_letter_markdown"],
                result.get("ats_score_estimate", 80),
            )
            return {
                "result": f"[MOCK] Đã viết resume và cover letter (ATS score: {result.get('ats_score_estimate', 80)}/100).",
                "resume_markdown": result["resume_markdown"],
                "cover_letter_markdown": result["cover_letter_markdown"],
                "ats_score_estimate": result.get("ats_score_estimate", 80),
                "mode": "mock",
            }

        if "phỏng vấn" in task_lower or "interview" in task_lower:
            from app.agents.mock_responses import interview_prep_mock
            briefing = interview_prep_mock(context.get("job", {}), context.get("interview_type", "behavioural"))
            return {
                "result": f"[MOCK] Interview Readiness Score: {briefing['interview_readiness_score']}/100\n"
                          f"Đã tạo {len(briefing['questions'])} câu hỏi dự đoán.",
                "briefing": briefing,
                "mode": "mock",
            }

        if "lương" in task_lower or "salary" in task_lower or "offer" in task_lower or "thương lượng" in task_lower:
            from app.agents.mock_responses import salary_benchmark_mock
            offer = context.get("offer", {})
            analysis = salary_benchmark_mock(offer)
            benchmarks = get_salary_benchmarks(
                context.get("title", "Software Engineer"),
                context.get("seniority", "senior"),
                context.get("location", context.get("candidate_profile", {}).get("location", "Ho Chi Minh City")),
            )
            return {
                "result": f"[MOCK] Offer ở mức P{analysis['offer_percentile']} — {analysis['assessment']}\n"
                          f"Target ask: ${analysis['negotiation_strategy']['target_ask']:,}/tháng",
                "analysis": analysis,
                "market_benchmarks": benchmarks,
                "mode": "mock",
            }

        if "career dna" in task_lower or "cv" in task_lower or "hồ sơ" in task_lower or "phân tích cv" in task_lower:
            from app.agents.mock_responses import career_dna_mock
            candidate_id = context.get("candidate_id", "mock-001")
            dna = career_dna_mock(candidate_id)
            await save_career_dna(self.db, candidate_id, dna)
            return {
                "result": f"[MOCK] Đã phân tích CV và xây dựng Career DNA.\n"
                          f"- Career Score: {dna['career_score']['total']}/100\n"
                          f"- Seniority: {dna['seniority_level']}\n"
                          f"- Market value: ${dna['market_value_usd_range']['min']}–${dna['market_value_usd_range']['max']}/tháng\n"
                          f"- Điểm mạnh: {', '.join(dna['strengths'][:2])}\n"
                          f"- Khoảng trống: {', '.join(dna['gaps'][:2])}",
                "career_dna": dna,
                "mode": "mock",
            }

        if "match" in task_lower or "tìm jobs" in task_lower or "việc" in task_lower:
            jobs = await query_jobs(self.db)
            if not jobs:
                return {"result": "[MOCK] Chưa có job trong database. Hãy thêm jobs trước.", "mode": "mock"}
            from app.agents.mock_responses import job_matching_mock
            candidate_id = context.get("candidate_id", "mock-001")
            matches = job_matching_mock(jobs)
            for m in matches:
                await save_match_result(self.db, candidate_id, m["job_id"], m["match_score"], m)
            top = matches[0]
            return {
                "result": f"[MOCK] Đã phân tích {len(jobs)} jobs.\n"
                          f"Top match: {top.get('job_id')} — Score {top['match_score']}/100 ({top['recommendation']})\n"
                          f"Lý do: {top['rationale']}",
                "matches": matches,
                "mode": "mock",
            }


        return {"result": f"[MOCK] Đã nhận task: {task}", "mode": "mock"}
