# DR-015: Rebutting vs. Undercutting Defeaters in the ARGUMENT Rebuttal Field

---
status: Proposed
date: 2026-06-11
---

## Context

ARGUMENT rows in the claim registry use the Toulmin schema (DR-001; `templates/claim-registry.md` Unit Type Reference; `agents/review-prompt.md`): claim, grounds, warrant, backing, qualifier, rebuttal. Toulmin chose this layout deliberately against the monolithic classical syllogism, and the Rebuttal field is the load-bearing concession to defeasibility — the place where conditions under which the conclusion fails get named.

The Rebuttal field as currently used collapses two structurally distinct ways an argument can fail:

- **The conclusion is wrong.** Counter-evidence directly contradicts the claim. The grounds-warrant link may be intact, but the conclusion does not hold.
- **The reasoning does not carry here.** The warrant's applicability conditions are not met in this case. The conclusion may be true or false; what fails is the inference from these grounds to this conclusion.

A reviewer (or registry editor) writing "*Rebuttal:* X applies in case Y" cannot distinguish whether Y is a counter-conclusion or a warrant-suspension, because the field has no sub-type. This shows up most clearly in DR-011 Pass 2 / Pass 3 outputs: when a reviewer flags a "load-bearing finding," the registry has no field to record whether the finding rebuts the conclusion or undercuts the inference. The distinction has been carried in reviewer prose, not in registry structure.

The vocabulary for this distinction is from Pollock's defeasible-reasoning programme: *rebutting defeaters* attack the conclusion; *undercutting defeaters* attack the reason-for-conclusion link without contesting the conclusion itself. The distinction is over thirty years old in the philosophical-logic literature; the framework has not been borrowing from that body of work, and this is the smallest-surface-change place to start.

This DR was prompted by a 2026-06-11 survey of patterns from philosophical logic against the framework's current apparatus (Toulmin, Whetten, category theory). Pollock's distinction emerged as the highest-fit, lowest-cost candidate; the survey itself is archived as a hypothesis-log entry rather than as committed framework content (see *Evidence Base*).

### Status of related work

- **DR-001** — Accepted. Toulmin schema as the structuring vocabulary for ARGUMENT rows. Not under reconsideration.
- **DR-011** — Proposed. Three-pass review. The structural rationale for splitting reviewer characters is what this DR extends downward — naming what reviewer findings *are*, not just how they were produced.
- **`templates/claim-registry.md` per-type sub-tables** — landed v1.2.0. The ARGUMENT sub-table is where the rebuttal sub-typing would live if adopted.
- **`agents/review-prompt.md`** — already asks reviewers to surface argument-shape critique. It does not currently ask them to type their findings as rebutting vs. undercutting.

## Options Considered

### Option A: Status quo — leave Rebuttal monolithic
- (+) Zero restructure cost.
- (+) Honours Toulmin verbatim.
- (-) Loses a distinction the framework's own review outputs are already making informally.
- (-) Reviewer findings remain harder to slot back into the registry than they need to be.

### Option B: Add `rebuttal-type: rebutting | undercutting` as a required sub-field on ARGUMENT rows
- (+) Forces every ARGUMENT row to name which defeater kind applies.
- (+) Names the distinction in template shape, not just in guidance prose.
- (-) High surface cost: every existing ARGUMENT row across active papers needs back-fill, including Paper 1.
- (-) Required-field discipline may push registry authors to over-fit findings into one of two buckets when the case is genuinely mixed.
- (-) DR-014 precedent: required new fields are a MAJOR-release-shaped change.

### Option C: Add `rebuttal-type: rebutting | undercutting` as an *optional* sub-field on ARGUMENT rows, with explicit "leave blank if unclear" guidance
- (+) Low surface cost: existing ARGUMENT rows remain valid without back-fill.
- (+) Authors who find the distinction useful start using it; authors who don't, don't.
- (+) Reviewer findings (Pass 2 / Pass 3) get a place to land: when a finding has a clear type, the registry now records it.
- (+) MINOR-release-shaped change — additive, not breaking.
- (-) Optional fields are weaker discipline than required; uptake may be uneven.
- (-) Does not solve the registry-editor-laziness failure mode by itself.

### Option D: Add the distinction as guidance prose in `templates/claim-registry.md` and `agents/review-prompt.md` without changing the registry shape
- (+) Lowest cost.
- (+) Vocabulary introduced; usage encouraged.
- (-) The distinction lives in prose only; reviewer findings still cannot be stored in a structurally distinguished form.
- (-) Indistinguishable from the status quo at the registry-data level.

## Proposed Decision (pending field-test)

**Option C: Optional `rebuttal-type: rebutting | undercutting` sub-field on ARGUMENT rows, with "leave blank if unclear" guidance.**

The optional-field shape matches the framework's standing preference for minimum surface change at first adoption. Required-field discipline (Option B) is the harder commitment and warrants evidence that the distinction earns its keep before it becomes mandatory. The blank default ("leave blank if unclear") protects against forcing a binary choice on genuinely mixed cases — a finding can be both a rebuttal and an undercutter, and registry editors should be permitted to mark that ambiguity rather than guess.

This DR is **Proposed**, not Accepted. The decision is contingent on the pending checks documented in *Pending Assessment* below.

### Scope of the proposed change

If accepted, the following changes land together as a single coordinated commit batch:

- **`templates/claim-registry.md`**: ARGUMENT sub-table gains an optional `rebuttal-type` column with values `rebutting | undercutting | (blank)`; Unit Type Reference adds a one-paragraph definition pairing the two types with examples.
- **`agents/review-prompt.md`**: instruction to reviewers to name finding-type when reporting rebuttal-shaped issues — "*If your finding contests the conclusion, mark it `rebutting`. If your finding contests the inference without contesting the conclusion, mark it `undercutting`. If both or neither, say so.*"
- **`docs/framework-summary.md`**: ARGUMENT row in the Registry Unit Types table gains a short note pointing at the sub-typing; Toulmin descriptor extended with "(rebutting / undercutting per DR-015)".
- **No back-fill of existing ARGUMENT rows** in `papers/perspective/` or any other active project. The field is optional; absence means *unclassified*, not *neither*.

### What stays unchanged

- **Toulmin schema** as the ARGUMENT structuring vocabulary. DR-001 is not revisited.
- **PROPOSITION / CLAIM / PROVOCATION** row shapes. The defeater distinction is ARGUMENT-specific; whether it generalises is an open question (below).
- **`templates/anti-hallucination.md` Step 6**. The distinction does not change the citation-verification checklist.
- **Quality gates 1–4 and conditional gates 2.6–2.8.** No gate criterion change.

## Consequences

If Accepted:

- ARGUMENT rows in newly-authored claim registries gain a typed rebuttal field. Reviewer findings (DR-011 Pass 2 / Pass 3) get a place to land that preserves the distinction reviewer prose is already making informally.
- Future work may extend the distinction to PROPOSITION's boundary conditions or to PROVOCATION's required prose markers, but only after observed uptake on ARGUMENT establishes the basic vocabulary.
- Adopters with existing claim registries are not forced to back-fill — the optional field shape means existing rows remain valid as-is. New rows may or may not use the sub-typing; the framework's default is *unclassified* rather than *required*.
- CHANGELOG version bump: MINOR. The change is additive and template-shape-extending, not breaking.

If Rejected:

- DR-015 is closed with the rationale (e.g., field-test shows the distinction is unused, or reveals overlap with an unanticipated third defeater type that the binary sub-typing would foreclose). The vocabulary may still be incorporated into `agents/review-prompt.md` guidance prose without committing the registry shape (Option D as fallback).

## Pending Assessment

Before this DR can be promoted from Proposed to Accepted, three checks are needed:

1. **Field-test on Paper 1's existing ARGUMENT rows.** Walk the eight ARGUMENT entries in `papers/perspective/vv/claims/claim_registry.md` and ask, for each Rebuttal field: would `rebutting` or `undercutting` apply, or neither? If five-plus entries split cleanly, the distinction earns its keep. If most are mixed or unclear, Option D (guidance-only) is the safer commitment.
2. **DR-011 review-output classification.** Walk the load-bearing findings logged in DR-011's Evidence Base (Pass 2 / Pass 3 cross-vendor) and classify each as rebutting, undercutting, or mixed. If the classification is informative — i.e., the *kind* of finding correlates with which Pass produced it — the sub-typing has cross-DR value beyond its local effect on ARGUMENT rows.
3. **Adopter check.** If any external adopter is reachable, ask whether an optional `rebuttal-type` column would be used or ignored. If the answer is *ignored*, the field is overhead without payoff; defer to Option D.

The DR ships as Proposed so the layering decision is visible and discussable without forcing template changes in this session.

## Key Insight

**Toulmin's Rebuttal field is doing two structurally different jobs.** The framework has been getting away with this because reviewer prose carries the distinction informally; but reviewer prose is exactly the surface the registry exists to formalise. The Pollock distinction is not a new concept — it is the vocabulary for a distinction the framework is already making, currently without a place to write it down.

A second-order insight, parallel to DR-011's functorial framing: **Rebutting and undercutting defeaters preserve different invariants of the argument.** A rebuttal that survives is evidence the conclusion does not hold, *regardless* of whether the inference would have carried in a different case. An undercutting defeater that survives is evidence the inference does not carry here, *regardless* of whether the conclusion happens to be true. Collapsing the two loses information about which invariant the defeater attacks — which matters when a downstream entry depends on either the conclusion or the inference (but not both).

## Evidence Base

- **Survey of patterns from philosophical logic (2026-06-11).** Conducted in-session against the framework's current logical apparatus (Toulmin, Whetten, category theory). Six candidates assessed: Pollock's defeasible reasoning (HIGH FIT, LOW COST — this DR); dialogical logic (HIGH FIT, MODERATE COST — deferred to a separate DR if/when DR-011 receives an Underlying Form subsection); Dung argumentation frameworks (MID-HIGH FIT, COST DEPENDS ON SCOPE — deferred until inter-entry conflicts accumulate); Reiter default logic (vocabulary-only relabeling of Whetten boundary conditions); epistemic logic (vocabulary-only sharpening of Step 6 anti-hallucination); classical proof theory / adaptive logic (over-formalisation at current scale — skip). Survey archived in `memory/hypothesis-log.md` as the framework-level bet that *named structural distinctions from defeasible-reasoning literature will earn their place in the registry shape*. Pass 3 (DR-011) cross-vendor review of this DR has not yet been run.
- **Pollock's distinction.** Originally introduced in Pollock 1987 ("Defeasible Reasoning," *Cognitive Science* 11) and developed in *Cognitive Carpentry* (1995); standard vocabulary in the contemporary defeasible-reasoning and computational-argumentation literature (Prakken & Vreeswijk, Modgil & Prakken on ASPIC+, etc.). **Citation specifics require Step 6 anti-hallucination verification before any consumer template embeds them as named references.** This DR's body uses the distinction as a structural concept; consumer templates (`templates/claim-registry.md`, `agents/review-prompt.md`) on acceptance would either (a) embed verified citations or (b) describe the distinction without citing, following the framework's standing preference for verifiability over name-dropping.
- **N=0 field-test evidence for this DR specifically.** No claim registry has yet been authored using the rebuttal-type sub-typing. The proposed-shape risk is structurally similar to the per-type sub-tables migration (v1.2.0) and the cost-log convention (v1.6.0) — additive surface, optional uptake.

## Open Questions Carried Forward

- **Generalisation to PROPOSITION boundary conditions.** Whetten's boundary conditions could be sub-typed similarly: a boundary condition that *invalidates* the proposition (analogous to rebutting) versus a boundary condition that *suspends* the proposition's applicability without invalidating it (analogous to undercutting). Whether this distinction is useful at PROPOSITION-shape is unsettled; defer until ARGUMENT uptake establishes the basic vocabulary.
- **Generalisation to PROVOCATION's required prose markers.** PROVOCATION (DR-010) has its own confidence axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL). The rebuttal-type distinction is orthogonal — a PROVOCATION can be rebutted by counter-evidence or undercut by domain-non-applicability — but the surface cost of layering it in is higher because PROVOCATION already has more required fields than the other types. DR-014 is currently restructuring PROVOCATION's surface; this question should wait until that restructure lands.
- **Cross-link to `vv/hypothesis-log.md` and `memory/hypothesis-log.md`.** Hypothesis-log entries record provisional positions whose evidence lives in the future. A defeater that emerges against a hypothesis-log entry could be typed using the same vocabulary — *rebutting* the position vs. *undercutting* the method by which the position was registered. The hypothesis-log shape does not currently have a defeater field; whether to add one is a downstream question.
- **Reviewer-side uptake.** Whether DR-011 Pass 2 / Pass 3 reviewers consistently name finding-type when prompted (`agents/review-prompt.md` instruction) is the test of whether the vocabulary travels from registry shape back into reviewer output. If reviewers ignore the prompt, the registry-side field is a one-way write that won't replenish from review.
- **Third defeater type.** Pollock's literature also distinguishes *reliability defeaters* (the source of the grounds is not reliable here) from rebutting and undercutting, and later work has added further refinements. The optional-field shape of this DR is permissive — it does not foreclose a third value — but the binary `rebutting | undercutting` vocabulary may need to extend to `rebutting | undercutting | reliability` if a third class proves load-bearing.

## Revisit If

- The Paper 1 field-test (Pending Assessment #1) reveals that most existing ARGUMENT Rebuttal fields do not split cleanly — Option D (guidance prose only) becomes the fallback.
- The DR-011 finding-classification check (Pending Assessment #2) reveals that finding-type does not correlate with Pass — the cross-DR value diminishes, and the DR's scope narrows back to ARGUMENT row shape alone.
- A future reviewer (or external adopter) reports that the binary `rebutting | undercutting` vocabulary forces a choice their case genuinely resists — extend the field's permitted values rather than retract the sub-typing.
- A future DR proposes a Dung-style attack graph for the registry (deferred candidate from the 2026-06-11 survey). The rebuttal-type sub-typing should be reconciled with the attack-edge typology that proposal would introduce; the optional-field shape is forward-compatible because *unclassified* is a permitted value.
- An adopter check reveals that the sub-typing is ignored across multiple projects — close DR-015 with the rationale and keep the vocabulary as guidance prose only.
