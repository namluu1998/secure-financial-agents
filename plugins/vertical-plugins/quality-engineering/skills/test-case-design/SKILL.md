---
name: test-case-design
description: Design manual or automatable QC test scenarios and test cases from requirements, user stories, acceptance criteria, wireframes, or observed behavior. Use when preparing functional, negative, boundary, state-transition, decision-table, regression, or exploratory coverage.
---

# Design Test Cases

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
