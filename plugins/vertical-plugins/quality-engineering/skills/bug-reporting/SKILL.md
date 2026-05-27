---
name: bug-reporting
description: Produce evidence-based defect reports and triage notes from failed tests, screenshots, logs, user reports, or observed behavior. Use when documenting a bug, improving reproduction steps, selecting severity, identifying regression impact, or preparing developer-ready handoff.
---

# Report and Triage a Defect

A useful defect is reproducible, scoped, and supported by evidence. Do not label undocumented behavior as a bug without stating the assumed expectation.

## Workflow

1. Capture the affected feature, build/version, environment, account role, data/setup, frequency, and first observed date if known.
2. State the expected result and its source: requirement, acceptance criterion, design, API contract, or prior verified behavior.
3. Write minimal numbered reproduction steps and the actual result.
4. Attach or summarize evidence: sanitized logs, request/response details, screenshot references, console output, video, query/result, or failing automated test.
5. Assess scope and impact, then assign proposed severity separately from scheduling priority.

Redact credentials, session tokens, personal data, account numbers, keys, and sensitive document content from every artifact and log excerpt.

## Severity Guidance

| Severity | Meaning |
|---|---|
| Critical | Exploitable security/privacy breach, material data loss/corruption, or total production outage without workaround |
| High | Core flow blocked, authorization failure, major integration broken, or serious incorrect result |
| Medium | Feature degradation with workaround or limited-user impact |
| Low | Minor usability, cosmetic, or low-impact inconsistency |

## Defect Template

Return:

- Title: concise symptom, context, and impact.
- Environment/build and prerequisites.
- Steps to reproduce.
- Expected result and source of expectation.
- Actual result and evidence.
- Reproducibility and affected scope.
- Proposed severity, priority suggestion, and rationale.
- Security/privacy impact and redaction confirmation.
- Regression candidates and open questions.

## Vietnamese Bug Task Template

When the user asks for a Vietnamese bug task, defect ticket, or "mẫu tạo task", use the structure in `assets/bug-task-template-vi.md`. Preserve the requested core headings:

- `Mô tả Bug`
- `Tiêu đề`
- `Môi trường` with `Hệ thống`, `Trang`, and `Trình duyệt`
- `Mức độ`
- `Mô tả vấn đề`
- `Các bước tái hiện`
- `Kết quả thực tế vs Mong đợi`
- `Nguyên nhân nghi ngờ`
- `Bằng chứng`

Fill only facts supported by supplied evidence. Leave explicit placeholders for missing facts and add impact, reproducibility, redaction, and regression fields needed for triage.
