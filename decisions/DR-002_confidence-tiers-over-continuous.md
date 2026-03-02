# DR-002: Use Named Confidence Tiers Instead of Continuous 0.0–1.0 Scale

---
status: Accepted
date: 2026-03-02
---

## Context

The claim registry template uses a continuous 0.0–1.0 confidence scale mapped to language hedging tiers. During reflection, we identified that the decimal precision implies a measurement accuracy that doesn't exist — assigning 0.73 vs 0.68 to a claim is false precision. Meanwhile, the language mapping already uses four discrete bands. The numbers add a step without adding information.

## Options Considered

### Option A: Keep the continuous 0.0–1.0 scale
- (+) Granular; allows nuanced ordering of claims
- (+) Already implemented in templates
- (-) False precision — nobody can meaningfully distinguish 0.7 from 0.75
- (-) Invites bike-shedding over exact numbers
- (-) The actual decision ("what language do I use?") collapses to four tiers anyway

### Option B: Switch to 4 named tiers with decision criteria
- (+) Honest about the actual precision of the judgment
- (+) Directly maps to language hedging without a lookup step
- (+) Faster to assign — less cognitive overhead during writing
- (+) Tiers already exist implicitly; this makes them primary
- (-) Loses the ability to rank-order within a tier (rarely needed in practice)

## Decision

**Option B: Named tiers with explicit decision criteria**

Four tiers, each defined by what you'd need to see to assign it:

| Tier | Assign when... | Language |
|------|---------------|----------|
| ESTABLISHED | Multiple independent sources confirm; no credible dispute; textbook-level | "demonstrates", "shows", "confirms" |
| SUPPORTED | At least 2–3 peer-reviewed sources agree; some open questions remain | "indicates", "supports", "evidence suggests" |
| EMERGING | 1–2 sources, or preliminary/pilot data; plausible but not yet replicated | "may", "preliminary evidence", "initial findings suggest" |
| SPECULATIVE | Logical inference, hypothesis, single non-peer-reviewed source, or extrapolation | "warrants investigation", "remains unclear", "we hypothesize" |

**Decision criteria, not descriptions** — the "assign when" column tells you what to look for, not what the tier means in the abstract.

## Consequences

- Update `claim-registry.md` template: replace `Confidence (0.0–1.0)` column with `Tier`
- Update `writing-guide.md` template: simplify to a single tier→language table
- Update `vv-framework.md`: quality gate thresholds become tier-based:
  - P0 claims: all SUPPORTED or ESTABLISHED (no EMERGING/SPECULATIVE)
  - P1 claims: ≥90% at EMERGING or above
  - P2 claims: SPECULATIVE is acceptable, but flag for reader
  - Coverage metric remains: "% of claims with assigned tier and verified source"
- README examples: replace decimal scores with tier names

## Revisit If

- A paper project requires finer granularity (e.g., systematic reviews with quantitative evidence grading like GRADE)
- Users report that the boundary between SUPPORTED and EMERGING is unclear in practice
- A domain has an established confidence framework that should be used instead (e.g., Cochrane evidence levels)
