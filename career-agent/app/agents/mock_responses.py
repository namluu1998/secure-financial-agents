"""Mock responses dùng khi không có ANTHROPIC_API_KEY (MOCK_MODE=true)."""
from datetime import date


def career_dna_mock(candidate_id: str) -> dict:
    return {
        "candidate_id": candidate_id,
        "snapshot_date": str(date.today()),
        "full_name": "Nguyễn Văn A",
        "current_title": "Senior Software Engineer",
        "seniority_level": "senior",
        "years_of_experience": 6.5,
        "hard_skills": [
            {"skill": "Python", "proficiency": "expert", "years": 6},
            {"skill": "FastAPI", "proficiency": "expert", "years": 3},
            {"skill": "PostgreSQL", "proficiency": "practitioner", "years": 4},
            {"skill": "Docker", "proficiency": "practitioner", "years": 3},
            {"skill": "React", "proficiency": "beginner", "years": 1},
        ],
        "soft_skills": ["Problem solving", "Communication", "Teamwork"],
        "industries": ["Fintech", "E-commerce"],
        "domains": ["Backend", "API Design", "Data Engineering"],
        "education": [
            {"degree": "Bachelor", "field": "Computer Science", "institution": "Đại học Bách Khoa HCM", "year": 2018}
        ],
        "certifications": [],
        "work_history": [
            {
                "title": "Senior Software Engineer",
                "company": "VNG Corporation",
                "start": "2021-03",
                "end": "present",
                "achievements": ["Tăng throughput API lên 3x", "Giảm latency trung bình 40%"],
            },
            {
                "title": "Software Engineer",
                "company": "Tiki",
                "start": "2018-07",
                "end": "2021-02",
                "achievements": ["Xây dựng payment service xử lý 50k req/s", "Tích hợp 5 cổng thanh toán"],
            },
        ],
        "market_value_usd_range": {"min": 2500, "max": 4500, "currency": "USD"},
        "career_score": {
            "total": 72,
            "breakdown": {
                "skills_depth": 80,
                "experience_breadth": 70,
                "career_progression": 75,
                "education": 60,
                "market_demand": 85,
            },
        },
        "strengths": ["Python backend mạnh", "Kinh nghiệm fintech", "Hiệu năng hệ thống"],
        "gaps": ["Thiếu kinh nghiệm cloud (AWS/GCP)", "Frontend còn yếu", "Chưa có leadership experience"],
        "recommended_titles": [
            "Senior Backend Engineer",
            "Lead Software Engineer",
            "Staff Engineer",
        ],
    }


def job_matching_mock(jobs: list[dict]) -> list[dict]:
    results = []
    scores = [88, 74, 61, 45]
    recommendations = ["strong-match", "good-match", "stretch", "not-recommended"]
    growths = ["high", "medium", "medium", "low"]
    for i, job in enumerate(jobs):
        score = scores[i % 4]
        results.append({
            "job_id": job.get("job_id", f"job-{i}"),
            "match_score": score,
            "score_breakdown": {
                "hard_skills": score + 5,
                "experience": score - 3,
                "seniority": score,
                "salary": score - 10,
                "location": 90,
                "llm_holistic": score - 5,
            },
            "missing_skills": [
                {"skill": "AWS", "importance": "preferred", "estimated_learning_weeks": 8}
            ] if score < 80 else [],
            "recommendation": recommendations[i % 4],
            "rationale": f"[MOCK] Candidate's Python/FastAPI skills match {job.get('title','this role')} well. "
                         f"Main gap is cloud experience.",
            "career_growth_potential": growths[i % 4],
        })
    return sorted(results, key=lambda x: x["match_score"], reverse=True)


def resume_tailor_mock(career_dna: dict, job: dict) -> dict:
    name = career_dna.get("full_name", "Candidate")
    title = job.get("title", "Software Engineer")
    company = job.get("company", "Company")
    return {
        "resume_markdown": f"""# {name}
**{title}** | Ho Chi Minh City | email@example.com

## Summary
Senior Software Engineer with 6+ years building high-performance backend systems in fintech and e-commerce.
Targeting the {title} role at {company}.

## Experience
**Senior Software Engineer — VNG Corporation** (2021–present)
- Increased API throughput 3x through async refactoring and connection pooling
- Reduced average latency by 40% via Redis caching layer

**Software Engineer — Tiki** (2018–2021)
- Built payment service handling 50k req/s with 99.99% uptime
- Integrated 5 payment gateways including MoMo and ZaloPay

## Skills
Python · FastAPI · PostgreSQL · Docker · Redis · SQL

## Education
B.Sc. Computer Science — Đại học Bách Khoa HCM (2018)
""",
        "cover_letter_markdown": f"""Dear Hiring Manager,

I am excited to apply for the {title} position at {company}. With 6+ years of backend engineering experience
in high-scale fintech systems, I am confident I can make an immediate impact on your team.

At VNG, I redesigned the core API layer achieving 3x throughput improvement and 40% latency reduction.
At Tiki, I built the payment service processing 50k requests per second with 99.99% uptime.

I would love the opportunity to discuss how my experience aligns with {company}'s engineering challenges.

Best regards,
{name}
""",
        "ats_keywords_integrated": ["Python", "FastAPI", "PostgreSQL", "Docker", "microservices"],
        "ats_score_estimate": 82.0,
        "version": "v1",
    }


def interview_prep_mock(job: dict, interview_type: str) -> dict:
    company = job.get("company", "Company")
    return {
        "company_summary": f"[MOCK] {company} là công ty công nghệ hàng đầu trong lĩnh vực fintech, "
                           f"thành lập năm 2015, hiện có 500+ nhân viên.",
        "culture_signals": [
            "Engineering-first culture",
            "Remote-friendly",
            "Fast-paced startup environment",
        ],
        "interview_readiness_score": 75,
        "questions": [
            {
                "question": "Hãy kể về một lần bạn cải thiện hiệu năng hệ thống đáng kể.",
                "type": "behavioural",
                "model_answer_outline": "STAR: Situation — API chậm tại VNG. Task — giảm latency 40%. "
                                        "Action — Redis caching + async refactor. Result — 40% latency giảm, 3x throughput.",
                "candidate_experience_to_cite": "VNG API optimization 2022",
                "gap_flag": False,
            },
            {
                "question": "Thiết kế một hệ thống xử lý 100k requests/second.",
                "type": "technical",
                "model_answer_outline": "Load balancer → API Gateway → async workers → queue (Kafka) → DB với read replicas.",
                "candidate_experience_to_cite": "Tiki payment service",
                "gap_flag": False,
            },
            {
                "question": "Kinh nghiệm của bạn với AWS/cloud infrastructure?",
                "type": "technical",
                "model_answer_outline": "Thành thật về gap, nhấn mạnh Docker/container experience và khả năng học nhanh.",
                "candidate_experience_to_cite": "Docker at VNG",
                "gap_flag": True,
            },
        ],
        "suggested_questions_to_ask": [
            f"Team engineering tại {company} đang dùng tech stack gì?",
            "Roadmap sản phẩm 6 tháng tới là gì?",
            "Quy trình onboarding cho engineer mới như thế nào?",
        ],
        "red_flags_to_probe": [
            "Turnover rate trong team engineering",
            "Technical debt hiện tại",
        ],
    }


def salary_benchmark_mock(offer: dict) -> dict:
    base = offer.get("base_salary", 3000)
    bonus_pct = offer.get("bonus_target_pct", 10)
    equity = offer.get("equity_value_usd", 0)
    total_y1 = base * 12 * (1 + bonus_pct / 100) + equity / 4
    p50 = base * 12 * 1.1
    return {
        "offer_summary": {
            "base_salary": base,
            "bonus_target_pct": bonus_pct,
            "equity_value_usd": equity,
            "total_comp_year_1": round(total_y1),
        },
        "market_benchmarks": {
            "p25": round(p50 * 0.85),
            "p50": round(p50),
            "p75": round(p50 * 1.15),
            "p90": round(p50 * 1.30),
            "data_sources": ["Glassdoor", "ITviec", "LinkedIn Salary"],
        },
        "offer_percentile": 55,
        "assessment": "at-market",
        "negotiation_strategy": {
            "target_ask": round(base * 1.12),
            "opening_script": f"Cảm ơn offer hấp dẫn. Dựa trên kinh nghiệm 6 năm và benchmark thị trường, "
                              f"tôi muốn đề xuất mức base ${round(base * 1.12):,}/tháng. "
                              f"Tôi rất hào hứng với cơ hội này và tin rằng mức này phản ánh đúng giá trị tôi mang lại.",
            "non_salary_levers": [
                "Signing bonus $2,000–5,000",
                "Remote 3 ngày/tuần",
                "Review lương sau 6 tháng thay vì 12",
                "Thêm ngày phép",
            ],
            "counter_responses": [
                {
                    "likely_counter": "Budget bị giới hạn ở mức này",
                    "response": "Nếu base không thể tăng, có thể xem xét signing bonus hoặc review sớm hơn không?",
                },
                {
                    "likely_counter": "Mức này đã cao hơn band của vị trí",
                    "response": "Tôi hiểu. Vậy có thể điều chỉnh title sang Senior II hoặc Lead để phù hợp band cao hơn không?",
                },
            ],
        },
    }
