# DR-016: The Framework Is an Authoring Discipline; Its Evaluative Components Are Secondary

---
status: Proposed
date: 2026-06-16
---

## Context

The framework presents two kinds of surface to a user:

- **Preventive / authoring-time machinery** — register a claim as you write it, verify each citation as you add it (`templates/anti-hallucination.md`), calibrate language to evidence while drafting (`templates/writing-guide.md`), gate before you ship (`vv-framework.md`).
- **Evaluative machinery** — the peer-review simulation (`agents/review-prompt.md`, Rubric A/B) and the coverage gates (`docs/THRESHOLDS.md`: 100% P0 / 90% P1 / 70% P2 / ≥85% overall, plus the ≥3.5/5.0 simulated-review band), which *judge* a body of work and emit a score or pass/fail.

The repo already self-describes as "verification infrastructure for AI-augmented **writing**" — i.e., authoring. But the evaluative components are framed and used as if the framework were also a *reviewer*, and the README's standing pitch leans on catching "the failure modes automated tools miss." A 2026-06-16 control experiment tested that pitch directly and found it does not hold in *review* mode.

### What triggered this

A pre-registered control comparison was run on an external **published** document (a maintainer-local audit, 2026-06-16 — genericised here because the audited document is a named third party; see *Evidence Base*). Three fresh agents in clean contexts: (a) the full framework run, (b) a single generic-prompt reviewer ("review rigorously, verify citations, flag problems"), (c) an independent primary-source verifier. The success criterion for "the framework adds review value" was committed **before** the control output was seen.

**Result, against the pre-registration:**
- The generic one-prompt reviewer **matched the framework on findings** and **beat it on one load-bearing argument-quality point** the framework run missed.
- The framework's *only* finding-level edge was **citation exhaustiveness** (verify-all vs the control's sampling caught two metadata errors the control skipped).
- A deep primary-source read (verifier) caught a defect *both* the framework and the control missed.

The framework's wins were all **preventive-shaped** disciplines applied evaluatively (verify-everything coverage). Its losses were all **evaluative** acts (judge a finished argument; find the unflagged seam). A plausible mechanism: the framework's checklists *channel* attention and crowd out open-ended reading — structure buys coverage and pays in attentional tunneling.

### The distinction this DR turns on

Two claims hide in "is the framework an authoring discipline rather than a reviewer?", with different evidence levels:

1. **Design fact (not a hypothesis):** every component is authoring-time machinery; the framework is *built* for writing. Readable off the artifact; not contingent on data.
2. **Comparative claim (N=1):** in *review* mode its marginal value over a generic prompt is coverage/exhaustiveness, not insight.

The honest position softens the "rather than": it is **primarily an authoring / preventive discipline; review is a real but weaker secondary mode whose only demonstrated edge is completeness, not perception.**

### Status of related work

- **README self-description** — "verification infrastructure for AI-augmented writing." Consistent with the design-fact half; the "catches what automated tools miss" pitch is the part this DR qualifies (it holds for *authoring*, not for *review-vs-generic-prompt*).
- **`docs/THRESHOLDS.md`** — already carries a top-of-file SPECULATIVE label on the simulated-review threshold. The coverage gates are defined there *for pre-submission drafts*.
- **DR-011 (multi-model review)** — Proposed. Orthogonal but adjacent: DR-011 is about escaping *shared-model bias* via different models/families. This DR is about whether the framework's review *apparatus* beats a *generic prompt* at all. The control used one generic LLM prompt, not a cross-family battery, so DR-011's disjoint-coverage claim is not directly tested or contradicted here — but if the evaluative apparatus is weak, DR-011's value rests entirely on the cross-family axis, not on the framework scaffolding around it. Flagged, not resolved.
- **The control experiment (2026-06-16)** — `control-comparison.md` in the maintainer-local audit folder (gitignored). The N=1 evidence for the comparative claim.

## Options Considered

### Option A: Status quo — present peer-review-sim + coverage gates as general evaluation tools
- (+) Zero change.
- (-) Overstates the review-mode value the control experiment did not find.
- (-) Lets the coverage gates keep being read as *grades* on finished external work (a category error — see Decision).

### Option B: Reposition now — demote/rewrite the peer-review-sim and coverage gates as authoring-only
- (+) Aligns framing with the finding.
- (-) Acts irreversibly on **N=1**. This is the exact goalpost-move (in reverse) the control experiment's own discipline forbids.
- (-) Conflates the *design fact* (safe) with the *empirical claim* (one data point).

### Option C (Proposed): Record the positioning as a Proposed DR; make only the design-fact clarification now; gate the rest on replication
- (+) Stops the insight from evaporating without committing template changes on N=1.
- (+) Lets the one *non-contingent* clarification (coverage gates are authoring gates, not external-work grades) land independently of the empirical checks.
- (+) Minimum surface change — matches the framework's standing preference (cf. DR-015 Option C).
- (-) Leaves the peer-review-sim framing unchanged until replication; uneven in the interim.

### Option D: Keep the insight in `memory/` only; change nothing public
- (+) Lowest cost.
- (-) The decision trail loses a load-bearing positioning question; future sessions re-litigate it.

## Proposed Decision (pending replication)

**Option C.** Record the position — *the framework is primarily an authoring/preventive discipline; its evaluative components (peer-review simulation, coverage gates) are secondary and, on current evidence, under-justified versus a generic prompt* — as a Proposed DR. Do **not** rewrite or demote the components yet; that waits on the Pending Assessment below.

### The one change that can land independently (design fact, not contingent)

The coverage gates (100/90/70/85, and the ≥3.5/5.0 review band) are **authoring / pre-submission gates** — `THRESHOLDS.md` defines them for a draft heading to submission. Applying them as **pass/fail grades on a finished external document** is a category error, true by construction (not contingent on N). On acceptance — or independently, since this half needs no replication — `docs/THRESHOLDS.md` gains a scope note:

> *These thresholds gate an author's own work before submission. They are not a grading rubric for finished or third-party documents; applied to a published work, coverage is a diagnostic lens, not a score (see DR-016).*

### Scope of the proposed change (on acceptance)

- **`docs/THRESHOLDS.md`** — the scope note above (can land now).
- **`README.md`** — qualify the "catches what automated tools miss" pitch toward authoring/preventive use; note that for one-off review of finished work a generic prompt is competitive.
- **`agents/review-prompt.md`** — add a front-matter note that the simulation is a *convenience wrapper*, not demonstrated to beat a generic rigorous-review prompt; recommend pairing any framework review with a **naive open-read pass** (the control was that missing step).
- **`docs/framework-summary.md`** — one line locating the framework as preventive/authoring, with review as a secondary mode.
- **No removal** of the peer-review-sim or the gates. Repositioning is framing, not deletion.

### What stays unchanged

- The preventive core (registry, anti-hallucination, calibration, gates-as-authoring-gates).
- DR-011's multi-model review pattern (orthogonal; see *Status of related work*).
- All unit types and quality-gate criteria.

## Consequences

If Accepted:
- The framework is honestly positioned as an authoring discipline; the coverage gates stop being mis-read as grades; the peer-review-sim is framed as convenience, not edge.
- CHANGELOG bump: MINOR (framing + a docs scope note; additive). The THRESHOLDS scope note alone, if landed independently, is PATCH.

If Rejected (replication overturns the comparative claim):
- The position is closed with rationale; the coverage-gate scope note may still stand (it is a design fact independent of the comparative claim).

## Pending Assessment

Before promotion from Proposed to Accepted:

1. **Replicate the control comparison on ≥2 more external documents.** Framework run vs single generic-prompt reviewer, pre-registered, blinded adjudication where feasible. Tally findings unique to each, **separating *insight* from *coverage***. Position holds if the generic prompt keeps matching/beating on insight while the framework keeps winning only on coverage.
2. **Preventive test (the load-bearing one).** Have an agent draft a claim-bearing passage twice — once under the framework's register-and-verify discipline, once under a generic "be rigorous, cite real sources" prompt — and compare fabricated/overclaimed citations that *survive to output*. The position ("authoring discipline") is only vindicated if the **preventive** arm shows a clear edge here, even though the **evaluative** arm did not. If the preventive arm *also* shows no edge, the framework is mostly process overhead — a much bigger finding.
3. **Peer-review-sim specific.** Across the replications, does Rubric A/B surface findings a generic prompt misses? Consistent *no* → demote it to a documented convenience wrapper. Consistent *yes* → the evaluative half earns its place after all and this DR narrows.

These mirror the Open bet registered in `memory/hypothesis-log.md` (2026-06-16).

## Key Insight

**The framework's wins are preventive; its losses are evaluative.** The clean axis is not authoring-vs-reviewer (a dichotomy the evidence doesn't support) but **preventive-vs-evaluative**. It shapes output *as it is made*; it does not reliably *judge* output once it exists better than a sharp generic prompt does. A corollary the control surfaced: a verification framework should ship an explicit **naive open-read pass**, precisely because its own checklists induce the blind spots that lost it the one argument-quality point.

## Evidence Base

- **N=1 pre-registered control experiment (2026-06-16).** External published document; framework run vs generic-prompt reviewer vs independent verifier. Pre-registration committed before the control output. Result: generic prompt matched on findings, beat on one argument-quality point; framework won only on citation exhaustiveness. **Maintainer-local** (the audited document is a named third party); genericised here to keep this public DR free of a citation a public reader cannot follow (cf. the v2.0.2 fix that removed maintainer-local pointers from public artifacts). The comparative claim is therefore **N=1 with an operator confound** (the comparison was adjudicated by the framework's maintainer; blinding was infeasible because framework output is stylistically self-identifying).
- **Design-fact half — not contingent.** That every component is authoring-time machinery is readable off the artifact and off the repo's own self-description; it needs no replication.
- **N=0 for the preventive claim specifically.** The "authoring discipline earns its keep preventively" half has *not* been tested against a generic prompt (Pending Assessment #2). The DR's honest status is: the *negative* (weak as a reviewer) has one data point; the *positive* (strong as an authoring discipline) has none yet beyond the design-fact reading.

## Open Questions Carried Forward

- **Does the preventive value survive its own control?** If a generic "cite real sources, don't overclaim" prompt prevents as many surviving fabrications as the registry+calibration discipline, the framework's value collapses to legibility/auditability/coverage — process, not perception. This is the highest-stakes open question.
- **Peer-review-sim: reframe or remove?** Reframe (convenience wrapper) is the conservative move; removal waits on consistent Pending-Assessment-#3 evidence.
- **Relationship to DR-011.** If the evaluative apparatus is weak, does DR-011's value rest entirely on the cross-family axis (different models) rather than on the framework scaffolding? Worth a dedicated check when DR-011 next gets a data point.
- **Generalisation.** Is anti-hallucination's value also concentrated authoring-side (catching an agent's own fabrications mid-draft) rather than review-side? Plausible, untested.

## Revisit If

- Replication (Pending Assessment #1) shows the framework consistently surfaces *load-bearing* findings a generic prompt misses (not just more citations) → it is a competitive reviewer after all; narrow or close this DR.
- The preventive test (#2) shows **no** authoring edge over a generic rigor prompt → escalate: the framework is largely process overhead, a finding bigger than this DR's scope.
- A future external adopter reports the coverage gates being used as grades on finished work → the THRESHOLDS scope note is load-bearing; prioritise landing it independently.
- DR-011 receives evidence that isolates framework-scaffolding value from cross-family-model value → reconcile the two positions.
