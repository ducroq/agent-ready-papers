# Coverage and Review Thresholds — Rationale

## Status

**SPECULATIVE.** The numerical thresholds in this framework — 85% overall coverage, 100% P0 / 90% P1 / 70% P2 verification, ≥3.5/5.0 simulated peer-review score — are heuristics chosen on internal reasoning and observation of audited projects, **not** derived from a calibration dataset.

This document explains the reasoning behind each threshold and names the data that would harden them.

External feedback flagged this gap: [ducroq/agent-ready-papers#16](https://github.com/ducroq/agent-ready-papers/issues/16) (June 2026 external review, P0).

## The thresholds

The framework declares five numerical thresholds:

| Threshold | Where it appears | Value |
|-----------|------------------|-------|
| P0 coverage | Gate 2 (Verification Complete) | 100% verified |
| P1 coverage | Gate 2 | 90% verified; ≥90% at EMERGING or above |
| P2 coverage | Gate 2 | 70% verified |
| Overall coverage | Gate 2 | ≥85% |
| Simulated peer review | Gate 3 (Review Complete) | ≥3.5/5.0 |

These appear in the README's [Quality Gates](../README.md#quality-gates) section, [`templates/vv-framework.md`](../templates/vv-framework.md) §3 "Claim Priority Classification" → "Coverage Targets", and [`agents/review-prompt.md`](../agents/review-prompt.md) "Recommendation thresholds".

## Why each value

### Why 100% for P0

P0 is defined as *"core argument — paper fails without it."* If the framework allowed even one P0 claim to ship unverified, its discipline would be empty for the cases that matter most. The 100% target is therefore not empirical — it follows from how P0 is defined.

**Reasoning:** If a P0 claim cannot be verified, the right action is not to ship it under-verified. The right action is to find a source, demote the claim to P1 / P2 with hedged language, or restructure the argument so it does not depend on the claim.

**What would change this:** Nothing within the framework's own logic. The threshold is definitional, not empirical.

### Why 90% for P1 (with ≥90% at EMERGING or above)

P1 is defined as *"supporting — strengthens argument."* Some P1 claims will inevitably be SPECULATIVE or weakly-evidenced; requiring 100% would force either deletion of useful supporting material or over-claiming of evidence strength. 90% leaves room for ~1 in 10 P1 claims to remain unverified at submission, on the expectation that those are flagged for the reader rather than dropped.

The *"≥90% at EMERGING or above"* qualifier is the language-calibration discipline applied: even when verified, P1 claims should be evidence-backed enough to carry SUPPORTED or stronger language. Pure-SPECULATIVE P1s should be rare.

**Reasoning:** Allowing some unverified P1s is honest about real publication constraints — sometimes a useful supporting reference exists but can't be located in time. The discipline forces declaration ("this 1 of 10 is flagged unverified"), not absence.

**What would change this:** Empirical data on the distribution of P1 verifiability across multiple paper projects. If 90% is consistently easy to hit (or impossible), the threshold should move.

### Why 70% for P2

P2 is defined as *"context — nice to have."* These claims are background, not load-bearing; SPECULATIVE confidence is acceptable. 70% is chosen low enough that the framework does not punish writers for including useful context they cannot fully verify, but high enough that P2 does not degenerate into a dumping ground for unsupported assertions.

**Reasoning:** Below roughly 70%, the registry-discipline signal weakens — too many entries are unverified to detect a problem-class shift. Above roughly 80%, P2 starts feeling like P1 and the priority distinction loses force.

**What would change this:** A signal that P2 entries below 70% predict downstream reviewer concerns. Currently no such signal exists in the audits.

### Why ≥85% overall

The overall coverage target is a weighted aggregate envelope that the per-tier distribution falls under:

- 100% × (P0 share) + 90% × (P1 share) + 70% × (P2 share)
- For a typical registry where P0 ≈ 30%, P1 ≈ 45%, P2 ≈ 25%: weighted average ≈ 88%.
- For a heavier P2 distribution (P2 share 40%): weighted average ≈ 84%.

The 85% threshold is set just below the typical weighted average so that a project hitting its per-tier targets clears the overall threshold automatically, but a project gaming the per-tier targets by under-counting P0s or P1s does not.

**Reasoning:** 85% is an envelope check, not an independent constraint. It catches the failure mode where per-tier targets are met by misclassifying load-bearing claims as P2.

**What would change this:** Audited projects with P2 share > 50% may push the typical weighted average below 85%, suggesting the threshold should track tier distribution rather than be a fixed number.

### Why ≥3.5/5.0 for simulated peer review

The 3.5 floor matches the review-prompt rubric's *Minor revision* band:

- ≥4.0 — Accept with minor revisions
- 3.5–3.9 — Minor revision
- 2.5–3.4 — Major revision
- <2.5 — Reject

≥3.5 is the threshold below which a real journal reviewer is likely to flag for major revision rather than minor. Setting the simulated-review gate at 3.5 means *"before submission, the paper should be in Minor revision territory at worst by AI peer-review simulation."*

**Reasoning:** The simulated review is a pre-flight check, not a substitute for real peer review. The threshold is calibrated to the rubric's band edge, not to a target acceptance rate.

**What would change this:** Systematic divergence between simulated and real reviews on the same papers. Currently, only Paper 1 has data (3.95 pre-DR-011 simulated; real review pending) — N=1.

## Honest accounting

These thresholds are **SPECULATIVE** per the framework's own confidence-tier discipline:

- The per-tier targets (100% / 90% / 70%) follow from how the priorities are *defined*. They are not empirically calibrated against project outcomes.
- The 85% overall is an envelope check derived arithmetically from the per-tier targets, not from external data.
- The 3.5/5.0 peer-review floor is calibrated to the review-prompt rubric, which is itself a heuristic.

The framework requires SPECULATIVE-tier claims to use hedged language ("warrants investigation", "remains unclear", "we hypothesise"). This document holds itself to the same discipline: the thresholds are presented as **defensible heuristics**, not as derived constants.

### N=1 evidence

Paper 1 ("The Verification Gap") hit 100% on all tiers (19 entries) and scored 3.95/5.0 pre-DR-011 simulated peer review. This is **consistent with** the thresholds but does not validate them — a project would also be consistent with the thresholds if those thresholds were wrong, because Paper 1's coverage was driven by the author's discipline, not by the threshold-induced pressure.

## What would harden these numbers

Promoting any of these thresholds from SPECULATIVE to EMERGING or SUPPORTED requires:

1. **Multi-project coverage benchmark.** Track per-tier coverage across ≥5 paper projects spanning different domains. Establish whether the typical achievable coverage matches the targets, exceeds them comfortably, or strains under them.
2. **Calibrated peer-review correlation.** For papers that hit ≥3.5 in simulated review, track the real-review outcome. If simulated and real reviews diverge systematically, recalibrate.
3. **Failure-mode tracking.** For papers that hit the thresholds and *still* received major-revision-or-worse from real reviewers, identify what the thresholds missed. Currently zero such cases are in the evidence base.

Until at least (1) and (2) accumulate to N≥3, the thresholds remain SPECULATIVE — a defensible heuristic that the framework's own discipline requires to be labelled as such.

## Open question: tooling implication

A coverage calculator (planned per [#17](https://github.com/ducroq/agent-ready-papers/issues/17)) makes it trivial to report per-tier coverage at any moment. That same calculator could, if applied across multiple projects, produce the (1) benchmark above as a byproduct. The thresholds will be hardest to defend until tooling makes the benchmarking cheap.

## Cross-references

- Coverage targets — [`templates/vv-framework.md`](../templates/vv-framework.md) §3 "Coverage Targets"; [Gate 2](../README.md#gate-2-verification-complete) in the README.
- Peer-review threshold — [`agents/review-prompt.md`](../agents/review-prompt.md) "Recommendation thresholds"; [Gate 3](../README.md#gate-3-review-complete) in the README.
- Paper 1 measured values — [`papers/perspective/vv/claims/claim_registry.md`](../papers/perspective/vv/claims/claim_registry.md); [`CHANGELOG.md`](../CHANGELOG.md) v1.0.0.
- External feedback that prompted this doc — [#16](https://github.com/ducroq/agent-ready-papers/issues/16).
