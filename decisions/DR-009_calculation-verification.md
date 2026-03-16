# DR-009: Calculation Verification as Fourth Verification Procedure

---
status: Accepted
date: 2026-03-06
---

## Context

The framework (DR-004) established three registry unit types: CLAIM, ARGUMENT, and PROPOSITION. Each has a structured verification procedure (source checking, Toulmin, Whetten). This model was developed from non-empirical papers that contain no equations.

The Driven Pendulum project (March 2026) revealed a blind spot: a 68-equation theory document contained 3 arithmetic errors that survived expert-style review. Gemini, prompted to "review for physical soundness," found 0/3 errors. Sonnet, prompted to "numerically reproduce every calculation," found 3/3. All three errors produced plausible-looking results — reasonable magnitudes, correct units — making them invisible to plausibility assessment.

This discovery motivated adding calculation verification as a fourth verification procedure, orthogonal to the three registry unit types.

## Options Considered

### Option A: Add CALCULATION as a fourth registry unit type
- (+) Consistent with the CLAIM/ARGUMENT/PROPOSITION pattern
- (-) Calculations are not "units of the paper's argument" — they are supporting evidence
- (-) Would inflate registry with mechanical entries that don't carry argumentative weight

### Option B: Add CALCULATION as a verification procedure (not a unit type)
- (+) Respects the three-type model (CLAIMs can cite calculations; ARGUMENTs can depend on them)
- (+) Tracked separately via equation-checker tool, not the registry
- (+) Applies only to papers with quantitative content — not universal
- (-) Less visible than a registry entry

### Option C: Do nothing — leave it as a project-specific tool
- (+) Simplest; no framework changes
- (-) Other projects will hit the same blind spot
- (-) The failure mode is systematic, not project-specific

## Decision

**Option B: CALCULATION as a fourth verification procedure, not a unit type.**

The three registry unit types (CLAIM, ARGUMENT, PROPOSITION) are units of the paper's argument. Calculations are supporting evidence — they verify that stated results follow from stated formulas. The equation-checker operates alongside the registry, not within it.

## Key Insight

**For arithmetic verification, the prompt matters more than the model.** A capable model prompted to "review" missed all errors; a comparable model prompted to "reproduce" caught all three. Plausibility assessment and mechanical reproduction are fundamentally different procedures, and only the latter catches errors that produce plausible-looking results.

## Consequences

- `vv-framework.md` template: add CALCULATION as fourth verification procedure in Section 1; note that it applies alongside registry but is tracked separately
- `README.md`: add CALCULATION row to verification registry table; add "Reviewing equations for soundness" to What Doesn't Work
- `CLAUDE.md`: clarify CALCULATION as procedure (not registry unit type) in Framework in Brief
- `equation-checker.md` template: already created (templates/equation-checker.md)
- Paper 1 (Perspective): S1-5 added as CLAIM citing driven-pendulum evidence; fifth future direction added (numerical reproduction as distinct verification procedure)
- Paper 3 (planned): equation-checker is proof-of-concept artifact

## Evidence Base

- Driven Pendulum project: 3/3 errors caught by reproduction, 0/3 by plausibility review
- Detailed case study: `audits/equation-verification-journey.md`
- Driven Pendulum audit §9: `audits/driven-pendulum-retrofit.md`
- Informal V&V application (2026-03-16): equation-checker methodology applied to WhatsApp messages, caught 5 errors including unit confusion (factor ~42) and wrong geometry assumption

## Revisit If

- A registry-integrated calculation tracking approach proves more practical than separate equation-checker
- Papers with hundreds of equations need a different workflow than the current prompt-based approach
- Automated equation extraction from LaTeX makes registry integration feasible
