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
