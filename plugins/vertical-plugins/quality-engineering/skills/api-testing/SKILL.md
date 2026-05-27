---
name: api-testing
description: Plan or execute quality checks for REST, GraphQL, webhook, or service APIs using specifications, requests, responses, or code. Use for contract testing, authentication and authorization checks, validation, pagination, idempotency, error handling, security cases, or API regression suites.
---

# Test an API

Evaluate API behavior from its documented contract and observed results. Treat tokens, customer data, logs, and response payloads as sensitive.

## Establish the Contract

Gather the API specification or route definition, base URL/environment, auth mechanism, roles/scopes, operation, schema, error model, rate limits, and side effects. If no contract is available, distinguish observed behavior from expected behavior.

## Coverage

For each operation, cover relevant checks:

- Success responses: status, required fields, data types, headers, filtering, pagination, and side effects.
- Input validation: required fields, formats, size limits, boundaries, malformed JSON, unknown fields, and content types.
- Identity and access: missing/invalid/expired credentials, role separation, object-level authorization, tenant isolation, and secret leakage.
- Reliability: retries, idempotency keys, timeout behavior, duplicate webhook events, concurrency, and partial failures.
- Security and privacy: injection payloads, unsafe error detail, sensitive fields in responses/logs, untrusted uploaded or retrieved content, and audit records.

Do not probe a production endpoint or mutate live data unless the user has explicitly authorized that environment and operation.

## Output

Return an endpoint matrix with method/operation, scenario, setup/request summary, expected status/schema/side effect, priority, and automation recommendation.

When execution evidence is provided, report the observed request/response with tokens and personal data redacted, then state pass/fail against the defined expectation. Record uncertain or undocumented behavior as a question, not a defect.
