---
name: test-case-design
description: Design manual or automatable QC test scenarios and test cases from requirements, user stories, acceptance criteria, wireframes, or observed behavior. Use when preparing functional, negative, boundary, state-transition, decision-table, regression, or exploratory coverage.
---

# Design Test Cases

## Response Language

Respond in Vietnamese by default. Keep standard technical terms in English when they are clearer, such as `test case`, `API`, `regression`, `severity`, `priority`, `GO/NO-GO`, `XSS`, `SQL Injection`, and `IDOR`. Use another language only when the user explicitly asks for it.

Translate expected behavior and risks into reproducible tests with observable outcomes.

## Workflow

1. Extract requirements, business rules, roles, validation rules, states, integrations, and assumptions from the supplied material.
2. Choose appropriate techniques: boundary values for inputs and limits; decision tables for conditional rules; state transitions for workflows; pairwise coverage for meaningful combinations; exploratory charters for risk hot spots.
3. Include positive, negative, permission, recovery, data integrity, and regression cases where the feature warrants them.
4. Separate cases needing real integration, mock data, special permissions, or destructive operations.

Never use real credentials, production personal data, or irreversible production actions in test instructions.

## Access-Control Case Patterns

When the feature exposes records, files, reports, invoices, projects, user profiles, or other object identifiers, include IDOR and ownership cases:

- Modify URL, route, query, body, or file identifiers to reference another user's object.
- Attempt view, download, update, and delete actions on objects owned by a different user, tenant, account, project, or role.
- Verify that hidden UI controls are not the only protection; direct API calls and deep links must be denied by the backend.
- Check sequential, guessable, or user-controlled identifiers such as `contract_1234`, `projectId=2025`, `userId`, and `invoiceId`.
- Confirm unauthorized access returns a safe denial response without exposing object existence, sensitive fields, internal paths, or stack traces.
- Include least-privilege and deny-by-default cases for unknown roles, missing roles, expired sessions, and users with partial permissions.
- Confirm suspicious denied attempts are recorded in audit logs without logging secrets or personal data unnecessarily.

## SQL Injection Case Patterns

When the feature accepts search terms, login credentials, identifiers, filters, sort fields, report parameters, or action URLs, include SQL injection cases. Use only authorized test environments and non-destructive payloads; do not run destructive statements such as table drops outside a disposable lab database.

- Login bypass attempts: submit SQL metacharacters, tautology-style input, comment markers, and malformed values in username/password fields. Expected result: authentication fails safely with a generic error.
- Client-side validation bypass: repeat validation cases with JavaScript disabled or by sending direct API requests. Expected result: server-side validation rejects unsafe input.
- Search and filter inputs: submit quote characters, boolean conditions, union-like probes, encoded payloads, and long/malformed input. Expected result: results are constrained to legitimate matches, not all rows, and no SQL error detail is exposed.
- URL and route parameters: alter numeric or string ids in detail pages, report URLs, and query parameters with injection probes. Expected result: safe not-found or denied response, with parameterized handling.
- Write/delete actions: test action URLs and request bodies with injection probes in ids or filters using mock data only. Expected result: no unintended records are modified or deleted.
- Permission-sensitive queries: verify injection probes cannot bypass role, tenant, ownership, or row-level constraints.
- Error and logging checks: verify database errors, query text, stack traces, table names, and sensitive fields are not returned to the user or stored in logs with secrets.

## OS Command Injection Case Patterns

When a feature invokes system utilities, diagnostics, file conversion, ping/check endpoints, archive tools, or background jobs, include command injection cases. Use isolated test environments and benign marker commands only; never write cases that delete files, alter permissions, exfiltrate data, or run against production.

- Command separators: submit safe probes containing shell metacharacters such as command chaining, pipes, conditional execution, subshell syntax, background execution, and newline encodings.
- JSON/API inputs: repeat probes through POST bodies, query parameters, headers, and hidden fields, not only the UI.
- Redirection attempts: verify output redirection and append operators cannot create or modify files from user input.
- Delay probes: use short, bounded timing probes only in approved test environments to detect unintended blocking/background execution.
- Windows and Unix variants: cover platform-specific separators and escape characters where the deployment OS is known.
- Expected result: the application performs only the intended function, rejects invalid target values, uses allowlisted arguments, and does not return command output, environment details, filesystem paths, or shell errors.

## Template Injection Case Patterns

When user-controlled content is rendered through email templates, admin notes, notifications, reports, CMS fields, or server-side template engines, include template injection cases:

- Expression handling: submit arithmetic-like, variable-like, and template-delimiter strings and verify they render as literal text or are rejected safely.
- Config and secret references: verify user input cannot access configuration objects, environment variables, request objects, headers, session data, or secret-like values.
- Loop/control syntax: verify template loops, conditionals, filters, and macros in user content are not executed.
- Nested expressions: test nested or encoded template delimiters through both API and UI entry points.
- Allowlist fields: where templates intentionally support variables, verify only documented placeholders are accepted and unknown variables fail safely.
- Expected result: no expression evaluation from untrusted input, no internal class/object names, no stack traces, and no leakage of configuration or user data.

## XSS Case Patterns

When a feature displays user-controlled text in HTML, JavaScript, URLs, attributes, rich text, comments, profiles, search results, or notifications, include XSS cases:

- Reflected input: verify search terms, URL fragments, query parameters, validation errors, and form echoes are encoded for the rendering context.
- Stored input: verify comments, descriptions, bios, messages, uploaded metadata, and notification templates cannot execute script when viewed later by the same or another user.
- Encoded and nested input: test HTML-encoded, URL-encoded, mixed-case, nested tag, and malformed markup variants.
- HTML and rich text: verify allowed tags/attributes are allowlisted and dangerous tags, event handlers, JavaScript URLs, iframes, and inline script are blocked or sanitized.
- Context-specific escaping: verify output encoding is correct for HTML body, attribute, JavaScript string, URL, and JSON contexts.
- Expected result: input is displayed as safe text or sanitized allowed markup, no alert/script execution occurs, and CSP/cookie flags provide defense in depth.

## Test Case Format

Provide a table with:

| ID | Requirement/Risk | Priority | Preconditions/Data | Steps | Expected Result | Type |
|---|---|---|---|---|---|---|

Make each expected result objectively verifiable. Include exact validation messages or API status/schema assertions only when they are defined by the requirement or observable evidence.

## Coverage Review

After the cases, list:

- Requirements not covered or not testable with available information.
- Suggested automation candidates and why.
- Exploratory charters for areas with uncertain behavior.
- Security/privacy cases relevant to authentication, authorization, leakage, untrusted input, uploads, logs, or audit trails.
