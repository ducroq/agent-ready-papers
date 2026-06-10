# DR-009: Calculation Verification as Fourth Verification Procedure

---
status: Accepted
date: 2026-03-06
---

## Context

The framework (DR-004) established three registry unit types: CLAIM, ARGUMENT, and PROPOSITION. Each has a structured verification procedure (source checking, Toulmin, Whetten). This model was developed from non-empirical papers that contain no equations.

Papers containing derived numerical values have a verification blind spot the three unit types do not catch: arithmetic errors that produce plausible-looking results (reasonable magnitudes, correct units, coherent surrounding prose) survive plausibility review. They are caught only by mechanical reproduction — substituting the stated inputs into the stated formula and computing.

This motivates adding calculation verification as a fourth verification procedure, orthogonal to the three registry unit types.

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

**For arithmetic verification, the prompt matters more than the model.** A capable model prompted to "review" can miss arithmetic errors; the same model prompted to "reproduce" can catch them. Plausibility assessment and mechanical reproduction are fundamentally different procedures, and only the latter catches errors that produce plausible-looking results.

## Consequences

- `vv-framework.md` template: add CALCULATION as fourth verification procedure in Section 1; note that it applies alongside registry but is tracked separately
- `README.md`: add CALCULATION row to verification registry table; add "Reviewing equations for soundness" to What Doesn't Work
- `CLAUDE.md`: clarify CALCULATION as procedure (not registry unit type) in Framework in Brief
- `equation-checker.md` template: already created (templates/equation-checker.md)
- Paper 3 (planned): equation-checker is proof-of-concept artifact

## Revisit If

- A registry-integrated calculation tracking approach proves more practical than separate equation-checker
- Papers with hundreds of equations need a different workflow than the current prompt-based approach
- Automated equation extraction from LaTeX makes registry integration feasible
