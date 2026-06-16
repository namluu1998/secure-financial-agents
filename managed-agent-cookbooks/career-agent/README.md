# Career Agent — managed-agent template

## Overview

An AI career operating system that acts as a personal headhunter. Analyses a candidate's Career DNA, discovers and ranks matching jobs, tailors resumes, prepares interview briefing packs, and supports salary negotiation. Same source as the [`career-agent`](../../plugins/agent-plugins/career-agent) Cowork plugin — this directory is the Managed Agent cookbook for `POST /v1/agents`.

## Deploy

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export JOBS_MCP_URL=...
export SALARY_MCP_URL=...
../../scripts/deploy-managed-agent.sh career-agent
```

## Steering events

See [`steering-examples.json`](./steering-examples.json).

## Security & handoffs

Candidate documents are untrusted. Five-tier worker isolation:

| Worker | Touches untrusted docs? | Tools | Connectors |
|---|---|---|---|
| **`career-dna`** | **Yes** | `Read`, `Grep` only | None |
| `job-matcher` | No | `Read`, `Grep` | jobs (read-only) |
| `interview-agent` | No | `Read`, `Grep` | None |
| `salary-agent` | No | `Read` | salary (read-only) |
| **`resume-tailor`** (Write-holder) | No | `Read`, `Write`, `Edit` | None |

The orchestrator validates `career-dna` output against its `output_schema` before any downstream worker receives it. `resume-tailor` produces files in `./out/resume-<candidate>-<job>-v<n>.md` and `./out/cover-<candidate>-<job>-v<n>.md`.

**Auto-apply is not implemented** in this cookbook. Any application submission requires explicit per-job user consent captured and stored before `apply` is invoked.

**Not guaranteed:** Career Score and Match Score are model estimates — surface confidence ranges; always give the candidate the rationale so they can decide.
