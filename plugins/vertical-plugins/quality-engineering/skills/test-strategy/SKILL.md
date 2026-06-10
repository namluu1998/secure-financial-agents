---
name: test-strategy
description: Build a risk-based QA test strategy or test plan for a feature, integration, migration, or release. Use when defining test scope, test levels, coverage priorities, environments, data needs, entry/exit criteria, traceability, or regression approach.
---

# Build a Risk-Based Test Strategy

## Response Language

Respond in Vietnamese by default. Keep standard technical terms in English when they are clearer, such as `test case`, `API`, `regression`, `severity`, `priority`, `GO/NO-GO`, `XSS`, `SQL Injection`, and `IDOR`. Use another language only when the user explicitly asks for it.

Create a practical plan that tells the delivery team what must be proved before release and why.

## Workflow

1. Establish scope: feature/change, users, platforms, integrations, out-of-scope areas, timeline, and available test environments.
2. Identify quality risks: business impact, likelihood, affected data, authorization boundaries, external dependencies, and rollback difficulty.
3. Map requirements and risks to coverage: functional, integration, API, UI, accessibility, compatibility, performance, security, recovery, and regression tests as applicable.
4. Define execution: environment, sanitized test data, mocks/stubs, automation candidates, ownership, defect workflow, and evidence to retain.
5. Set quality gates: entry criteria, exit criteria, blocker rules, accepted residual risks, and release recommendation owner.

Do not invent requirements. Mark unresolved assumptions and questions explicitly.

## Prioritization

Use `P0` for paths whose failure could create unauthorized access, data corruption, material financial/compliance impact, or total service outage. Use `P1` for core user journeys and integrations. Use `P2` for secondary workflows and presentation issues.

Include abuse and failure scenarios for authentication, authorization, secrets, personally identifiable information, input validation, prompt/document injection where AI workflows read external input, and audit logging when relevant.

## Deliverable

Produce:

- Objectives and scope.
- Risk matrix with `risk`, `impact`, `likelihood`, `priority`, and `mitigation/coverage`.
- Coverage matrix mapping requirements or user journeys to test types and priority.
- Environment and test-data plan, stating how secrets and personal data are protected.
- Execution schedule and ownership.
- Entry criteria, exit criteria, defect thresholds, and residual-risk section.

End with missing information that blocks confident sign-off.
