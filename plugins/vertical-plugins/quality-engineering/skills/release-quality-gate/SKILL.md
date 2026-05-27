---
name: release-quality-gate
description: Assess release readiness from test execution, defects, risk acceptance, security checks, and operational evidence. Use for go/no-go reviews, regression summaries, UAT sign-off support, release quality reports, or production deployment recommendations.
---

# Evaluate a Release Quality Gate

Produce an auditable recommendation from available evidence. This skill supports accountable owners; it does not grant approval on their behalf.

## Evidence Required

Collect the release scope and build, test strategy or acceptance criteria, executed test results, coverage gaps, open defects, security/privacy testing status, performance/reliability status when relevant, rollback plan, monitoring plan, and named risk acceptances.

Mark evidence as `provided`, `missing`, or `not applicable`; do not convert missing evidence into a pass.

## Gate Logic

Recommend `NO-GO` when any unresolved issue creates unauthorized access, exposed secrets or personal data, material data corruption, unmitigated critical/high business risk, failed mandatory test, or no credible rollback for a high-impact change.

Recommend `CONDITIONAL GO` only when residual risks have mitigations, owners, deadlines, monitoring, and authorized acceptance. Recommend `GO` only when required gates pass and remaining risk is documented as acceptable.

## Deliverable

Provide:

| Gate | Evidence | Status (`pass/fail/missing/n-a`) | Notes/Risk |
|---|---|---|---|

Then include:

- Test execution summary by priority and type.
- Open defect list with severity and release disposition.
- Security/privacy, data integrity, performance, rollback, and monitoring status.
- Residual risks and required approvers.
- Recommendation: `GO`, `CONDITIONAL GO`, or `NO-GO`, with explicit rationale and blocking actions.
