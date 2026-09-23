---
name: salary-benchmarking
description: Benchmark an offer against market data, evaluate total compensation, and produce a negotiation strategy. Use when an offer is received or to set a salary target before applying.
---

# Benchmark the compensation

Inputs: offer details (or target role details), candidate Career DNA, and target location.

## Step 1: Establish market range

For the role, seniority, location, and industry, determine:
- P25 / P50 / P75 / P90 market salary
- Typical equity and bonus ranges
- Total compensation range

Data sources to cite: Levels.fyi (tech), Glassdoor, Payscale, Salary.com, industry surveys.

## Step 2: Evaluate the offer

```json
{
  "offer": {
    "base_salary": 0,
    "bonus_target_pct": 0,
    "equity_value_usd": 0,
    "equity_vesting_years": 4,
    "benefits_value_estimate_usd": 0,
    "total_comp_year_1": 0
  },
  "market_benchmarks": {
    "p25": 0, "p50": 0, "p75": 0, "p90": 0,
    "data_sources": ["..."]
  },
  "offer_percentile": 0,
  "assessment": "below-market | at-market | above-market | exceptional"
}
```

## Step 3: Negotiation strategy

If offer is below P50, produce:
1. Target ask (specific number, not a range)
2. BATNA (best alternative to negotiated agreement)
3. Opening script — one paragraph
4. Likely counter-responses and how to handle each
5. Non-salary levers to negotiate if salary is fixed (signing bonus, equity cliff, remote days, title, review date)

## Step 4: Offer comparison (if multiple offers)

Side-by-side table: role, company, base, bonus, equity, total comp year 1, total comp year 4, career growth score.
