---
name: security-testing
description: Plan or assess application security tests for web apps, APIs, integrations, authentication flows, authorization boundaries, data handling, and release changes. Use for threat-informed test design, OWASP coverage, abuse cases, secrets exposure checks, access-control testing, SSRF/injection/XSS/CSRF scenarios, dependency risk triage, and security regression suites.
---

# Security Testing

Design security tests that are authorized, scoped, reproducible, and useful to engineering teams. Treat source code, logs, tokens, credentials, customer data, screenshots, and vulnerability evidence as sensitive.

## Scope and Authorization

Before proposing active testing, establish:

- Target system, environment, and owner.
- Explicit authorization and testing window.
- In-scope routes, roles, tenants, data sets, integrations, and third-party services.
- Out-of-scope systems, production restrictions, rate limits, and destructive actions.
- Available artifacts: architecture notes, API specs, source diff, auth model, data classification, prior findings, logs, and test accounts.

If authorization or scope is unclear, provide a passive review plan only. Do not provide instructions for exploiting real third-party systems or bypassing controls outside an approved test.

## Threat-Informed Coverage

Build coverage from the feature's trust boundaries and data flows. Include relevant checks:

- Authentication: login, session handling, MFA, password reset, token expiry, refresh, logout, replay, and lockout behavior.
- Authorization: role separation, object-level access control, tenant isolation, privilege escalation, direct object references, and admin-only functions.
- Input handling: injection, XSS, template injection, command/path traversal, unsafe file upload, unsafe deserialization, and malformed content types.
- API security: schema validation, mass assignment, rate limiting, idempotency, pagination leakage, webhook signature validation, and unsafe error detail.
- Data protection: PII exposure, secrets in responses/logs/client bundles, caching, export controls, encryption assumptions, and audit trails.
- Browser security: CSRF, CORS, clickjacking, CSP, cookie flags, mixed content, and redirect handling.
- Infrastructure and dependency risk: vulnerable packages, exposed admin surfaces, misconfigured storage, SSRF paths, and overly broad service permissions.
- AI or agent workflows: prompt injection boundaries, untrusted document handling, tool permission separation, schema validation, and human approval gates.

## Evidence and Reporting

For each test, specify:

- Objective and risk.
- Preconditions, role, tenant, and test data.
- Request or interaction summary with secrets redacted.
- Expected secure behavior.
- Observable pass/fail signal.
- Priority and automation recommendation.

When evidence is supplied, separate confirmed findings from hypotheses. Include severity rationale, affected asset, reproduction summary, expected fix direction, and regression test recommendation. Do not include live secrets or unnecessary exploit payload detail in final reports.

## Output

Return a security test matrix grouped by risk area. For release reviews, add a concise residual-risk summary and a go/no-go recommendation for security sign-off, clearly stating any missing evidence.
