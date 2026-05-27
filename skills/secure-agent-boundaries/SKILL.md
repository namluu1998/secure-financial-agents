---
name: secure-agent-boundaries
description: Review or design financial workflow agents that read untrusted documents, pass work between agents, access firm data connectors, or configure Office add-ins. Use when assessing prompt-injection boundaries, handoff safety, credential handling, deployment manifests, or approval controls.
---

# Secure Agent Boundaries

Use this skill for financial-services agent workflows where incorrect output,
prompt injection, or leaked credentials can create operational or compliance
risk.

## Required Checks

1. Identify every input that can contain content supplied by a client,
   counterparty, applicant, external data source, email, PDF, spreadsheet, or
   upstream system outside the trust boundary.
2. Keep the reader for each untrusted input read-only: no write tool, shell,
   external connector, posting action, or privileged handoff.
3. Require executable schema validation between reader output and any trusted
   processor. A prompt instruction saying "return JSON" is not validation.
4. Validate cross-agent handoffs as structured data and allowlist target
   agents. Do not parse nested JSON with regular expressions.
5. Keep credentials out of manifests, URLs, logs, transcripts, and generated
   documents. Deliver secrets only through an authenticated runtime mechanism
   or secret manager.
6. Require human approval before trades, onboarding decisions, ledger posts,
   external distributions, or client-facing investment recommendations.

## Implementation Pattern

When editing a codebase, implement the boundary in code and add regression
tests that prove:

- Unexpected fields or instruction-like text from an untrusted reader are
  rejected before privileged processing occurs.
- A valid nested handoff parses correctly and an unapproved target fails.
- Manifest/config generation rejects secret-bearing keys without logging their
  values.

This repository includes a dependency-free reference implementation under
`src/secure_financial_agents/` and tests under `tests/`.

## Review Output

For security reviews, list findings first with severity, affected path/line,
impact, and the smallest concrete remediation. Distinguish exploitable
boundaries from documentation mismatches or general hardening opportunities.

