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

## IDOR and Broken Access Control

For object-backed features, explicitly test insecure direct object reference and missing access-control checks:

- URL tampering: change path, query, route, or filename identifiers to another valid-looking object, such as a different contract, report, project, profile, or invoice.
- API object swap: repeat a valid request with another `userId`, `accountId`, `projectId`, `invoiceId`, document id, tenant id, or composite identifier.
- Cross-user and cross-tenant reads: verify that users cannot view another user's profile, salary-like data, private project material, internal report, or uploaded file.
- Unauthorized downloads: verify direct file links and generated document URLs require server-side authorization on every request.
- Unauthorized writes: verify update/delete operations are denied when the actor does not own or administer the target object, including nested routes like `/users/{userId}/invoices/{invoiceId}`.
- Force browsing: request authenticated pages or API routes directly without following the UI flow, with missing roles, downgraded roles, or expired sessions.
- Metadata manipulation: alter client-controlled role, owner, tenant, workflow state, or approval metadata and verify the backend ignores or rejects it.
- Least privilege and deny by default: verify unknown, newly created, disabled, or partially provisioned users receive no access until explicit permissions are assigned.

Expected secure behavior: authorization is enforced on the backend for every object and action, identifiers are not trusted because they came from the client, denial responses do not leak sensitive object details, and suspicious attempts are audit logged.

## SQL Injection

For database-backed features, explicitly test SQL injection paths using authorized environments and non-destructive probes:

- Authentication forms: test username and password fields with quotes, comments, tautology-style probes, malformed encodings, and mixed valid/invalid credentials. Authentication must fail safely and not reveal whether the SQL syntax changed.
- Search boxes and filters: test free-text search, advanced filters, sort fields, pagination, and report parameters. Results must remain scoped to the user's query, role, tenant, and permissions.
- Detail, view, and report URLs: test ids and query parameters used to fetch records, such as news/report ids, project ids, account ids, and document ids. The app must return safe not-found or denied responses without database errors.
- Write and delete endpoints: test ids, filters, and action parameters against disposable data only. The app must not modify or delete unintended rows.
- Permission checks: verify injection probes cannot turn a restricted query into an unrestricted query or bypass row-level security.
- Error handling: confirm SQL errors, stack traces, query fragments, table names, column names, and connection details are not exposed in UI/API responses.
- Logging and monitoring: confirm rejected probes are audit logged at an appropriate level without storing credentials, raw secrets, or excessive personal data.

Prefer parameterized-query and ORM-safe remediation guidance. When documenting evidence, show only minimal sanitized payload summaries and avoid destructive examples unless the test was run in an isolated lab.

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
