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
- For an **illustrative** registry with P0 ≈ 30%, P1 ≈ 45%, P2 ≈ 25%: weighted average ≈ 88%. This shape is hypothetical — it is not drawn from any registry in this repo, and the "typical" label it used to carry asserted a population that has never been measured.
- **The registries that actually exist are nothing like it**, and both sit far clear of the envelope: Paper 1 (`papers/perspective`, 19 entries) is P0 42.1% / P1 52.6% / P2 5.3% → **93.2%**; a second, maintainer-local paper project (7 entries) is P0 57.1% / P1 42.9% / P2 0% → **95.7%**. Both have a *lower* P2 share than the illustrative case, not higher. **Only the Paper 1 figure is reproducible from a clone** — the second project is gitignored under the same policy as `memory/` (see *What is intentionally not shipped* in `CLAUDE.md`), so an adopter can re-derive one of these two data points and must take the other on trust. N=2, and one of the two is unverifiable by the reader.
- For a heavier P2 distribution (P2 share 40%, holding the illustrative 30:45 P0:P1 ratio for the rest): weighted average ≈ 84%.

The 85% threshold is set just below **the illustrative 88% figure in the first bullet**, so that a project hitting its per-tier targets clears the overall threshold **for registries at or near that shape**, while a project gaming the per-tier targets by under-counting P0s or P1s does not.

⚠ **The "clears automatically" property is false as an unconditional claim.** Meeting every per-tier target bounds overall coverage only into [70%, 100%] — a registry that is entirely P2 and hits its 70% target scores 70% overall. No ratio assumption is needed to see that per-tier compliance does not imply ≥85%.

Where the break point sits depends on the P0:P1 split of the non-P2 remainder. Writing *r* for P0's share of that remainder, overall = 70 + (1 − p)(20 + 10r), and the break point is p\* = 1 − 15/(20 + 10r):

| P0:P1 of the remainder | Identity | Break point |
|---|---|---|
| all P1 (r = 0) | 90 − 20p | **25.0%** |
| 10:65 | 91.3 − 21.3p | 29.7% |
| 30:45 (the illustrative shape above) | 94 − 24p | 37.5% |
| 8:10 (Paper 1's actual) | 94.4 − 24.4p | 38.6% |
| all P0 (r = 1) | 100 − 30p | **50.0%** |

So the break point ranges over **25–50%**, and the frequently-quoted 37.5% is a property of the illustrative 30:45 shape, not of the gate. The second bullet above is an instance: at P2 share 40% under that shape the weighted average is ≈84%, below the gate. Stated here rather than smoothed away, because the earlier wording asserted the property unconditionally and its own adjacent example falsified it. If your registry is P2-heavy, the honest reading is that the overall gate is measuring your tier distribution, not your verification discipline.

**Reasoning:** 85% is an envelope check, not an independent constraint. It catches the failure mode where per-tier targets are met by misclassifying load-bearing claims as P2 — and, on the arithmetic above, it also fires on a legitimately context-heavy registry, which is a false positive it cannot distinguish from that failure mode.

**Note on enforcement:** `tools/coverage.py --strict` gates the **per-tier** targets only; it never computes an overall figure (verified by source read — no code path aggregates across tiers). The ≥85% line is enforced only by a human, and it is stated in at least four shipped places: [Gate 2](../README.md#gate-2-verification-complete) in the README, [`templates/vv-framework.md`](../templates/vv-framework.md) §3, [`templates/claim-registry.md`](../templates/claim-registry.md) *Targets*, and the *Targets* line each paper registry inherits from it. So the tool and the checklist disagree about what Gate 2 requires — worth knowing before treating a green `--strict` run as a passed Gate 2.

**What would change this:** A registry whose P2 share exceeds its break point (25–50% depending on tier mix — see the table above) would settle whether the threshold should track tier distribution rather than be a fixed number. To our knowledge no audited project has yet supplied one: the two that exist sit at 5.3% and 0%. (This bullet previously named ">50%" as the risk point; that figure did not follow from the arithmetic and is corrected. An intermediate revision named 37.5% just as unconditionally, which was the same error with a better number — the break point is a range, not a constant.)

### Why ≥3.5/5.0 for simulated peer review

The 3.5 floor matches the review-prompt rubric's *Minor revision* band:

- ≥4.0 — Accept with minor revisions
- 3.5–<4.0 — Minor revision
- 2.5–<3.5 — Major revision
- <2.5 — Reject

≥3.5 is the threshold below which a real journal reviewer is likely to flag for major revision rather than minor. Setting the simulated-review gate at 3.5 means *"before submission, the paper should be in Minor revision territory at worst by AI peer-review simulation."*

**Reasoning:** The simulated review is a pre-flight check, not a substitute for real peer review. The threshold is calibrated to the rubric's band edge, not to a target acceptance rate.

**What would change this:** Systematic divergence between simulated and real reviews on the same papers. Currently, only Paper 1 has data (3.95 pre-DR-011 simulated; real review pending) — N=1.

## Honest accounting

These thresholds are **SPECULATIVE** per the framework's own confidence-tier discipline:

- The per-tier targets (100% / 90% / 70%) follow from how the priorities are *defined*. They are not empirically calibrated against project outcomes.
- The 85% overall is an envelope check derived arithmetically from the per-tier targets, not from external data.
- The 3.5/5.0 peer-review floor is calibrated to the review-prompt rubric, which is itself a heuristic.

The framework requires SPECULATIVE-tier claims to use hedged language ("warrants investigation", "remains unclear", "we hypothesise"). This document *attempts* to hold itself to the same discipline — the thresholds are presented as **defensible heuristics**, not as derived constants — but the claim that it succeeds is one it should not make on its own behalf, and a 2026-08-13 review found it did not. Two tier violations remain open in the sections above: the flat mechanism claim under "Why 70% for P2" (no measurement exists anywhere in this document), and the transfer of the rubric's band edge onto *real* reviewer behaviour under "Why ≥3.5/5.0" (N=0 real reviews). Both are left standing rather than papered over, because repairing them requires deciding what the actual justification for those two thresholds is — which is content work, not an editing pass. Tracked in [#33](https://github.com/ducroq/agent-ready-papers/issues/33).

### N=1 evidence

Paper 1 ("The Verification Gap") hit 100% on all tiers (19 entries) and scored 3.95/5.0 pre-DR-011 simulated peer review. This is **consistent with** the thresholds but does not validate them — a project would also be consistent with the thresholds if those thresholds were wrong, because Paper 1's coverage was driven by the author's discipline, not by the threshold-induced pressure.

### Scope: these thresholds assume you can close your own claims

*(Added 2026-08-16 on the resolution of a registered bet; see `vv/hypothesis-log.md`. **Tier is per row, not per table** — see the n column below. The document's own SPECULATIVE status is unchanged: this section observes an assumption the thresholds were making, and does not raise the tier of any threshold. Both audits behind it are unpublished and gitignored, so — per the standard `templates/vv-framework.md` §3 sets for exactly this case — **treat the pattern as directional and measure your own registry rather than checking against these numbers**.)*

Every number above presumes a **self-authored** project, where an unverified claim is work the author has not done yet. Applied to a document the project did not write, coverage measures something different, and two audits run in this repo put a usable bound on how different.

The governing variable is not third-party status. It is **whether a claim can be closed without its author.**

| Claim closes by… | Third-party coverage | n | Tier | Why |
|---|---|---|---|---|
| Citation | Low — 16% on the CLAIM axis | 1 | EMERGING | The evidence is in the author's hands; true-but-uncited stays `[ ]` |
| Reproduction (arithmetic, code, derivation) | Higher — **not** demonstrably uncapped: 77% on the CLAIM axis, with the residual 3 of 13 unexplained | 1 | EMERGING | A stranger can compute it. The audit reaching 77% cited **no** sources at all, so the figure is not a function of sourcing quality |
| Inference (ARGUMENT, PROPOSITION) | 0% in both audits | 2, of which 1 informative | EMERGING | Toulmin item 2 requires every ground `[x]`, and the grounds are the audited text's own units. See the caveat below |

Three consequences for reading a coverage number:

1. **Do not compare coverage across projects whose claims close differently.** The same percentage means different things. The two audits here differ by roughly a factor of five on the CLAIM axis (16% and 77%); **claim-closure type is the candidate explanation, not an isolated one** — the two also differ in genre, size, subject and auditor familiarity, and nothing was held constant. This repo retiered `README.md` R-4 from SUPPORTED to EMERGING for exactly this shape of attribution, and the same caveat applies here.

   On the inference row: 0-of-N is **largely forced** where CLAIM coverage is low, because a unit needs *every* ground verified. In the 16% audit, 0 of 22 was close to arithmetically inevitable and carries little information. In the 77% audit, 0 of 6 is genuinely surprising and is the one informative observation. Read the row as n=1, not n=2.
2. **Report the CLAIM and the ARGUMENT/PROPOSITION axes as a pair.** `tools/coverage.py` emits per-unit-type coverage, which gives you both. A single overall figure hides the split that carries the information — which is how a 12% ceiling on one audit was briefly read as a general property of third-party review, and why the numbers in the table above are CLAIM-axis figures rather than overall ones.

   ⚠ **Coverage is not grounds-verification, and no shipped tool measures the latter.** `tools/coverage.py` reads the Status checkbox only; it has no concept of Toulmin grounds. "ARGUMENT coverage 0%" and "0 units with every ground `[x]`" are different measurements — a unit can be `[ ]` for a warrant or rebuttal failure with all grounds verified, and an auditor can tick `[x]` while a ground is `[ ]`. If you need the grounds figure, **count it by hand and say that you did**.
3. **A missed threshold on a third-party audit is not a defect in the audit.** It is a measurement of how much of that document its readers can check. Say which reading you mean.

This does **not** create a threshold exemption, and no number above changes. It states the assumption the thresholds were always making. Registered at EMERGING because n=2, both self-run, with no external replication.

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
