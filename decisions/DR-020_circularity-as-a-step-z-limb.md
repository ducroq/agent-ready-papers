# DR-020: Circular Evidence — a Reuse Check as a Step Z Limb

<!-- Filename, this title and the CLAUDE.md decision row previously gave three different
     names for this document, which is grep-hostile for a DR whose subject is that a
     defect class needs a name. All three now lead with "circular evidence". -->

---
status: Proposed
date: 2026-08-16
superseded_by:
---

**Evidence tier: the gap is EMERGING, the remedy is EMERGING.** Both are weaker than a first draft of this document claimed, and the reasons are recorded rather than quietly repaired — see *Draft history*.

- **The gap** — that a result can be arithmetically correct and evidentially empty, with **no shipped instrument helping an auditor notice it** — rests on **n=2**: one in-repo instance found by the DR-019 backlog sweep (2026-08-13) and one external document audited three days later. One is self-application. Two instances three days apart, surfaced by the same maintainer with the same instruments, is a pattern worth naming and **not** a measured recurrence rate.
- **The remedy** is now a single mechanical test on a derivation graph. It has been run once, retrospectively, where it caught a real defect. It has never been run prospectively.

## Context

Across this repo's **shipped normative surfaces** — `templates/`, `agents/`, and the README's verification registry — circularity is touched in four places. Three are judgment calls; the fourth is a different failure mode entirely.

*(The population is stated because the count is otherwise unfalsifiable. Outside it, `decisions/DR-004` carries the same falsification checkbox, and DRs, CHANGELOG, UPGRADING and paper instances carry further mentions; none is a shipped check.)*

| Surface | Form | Scope |
|---|---|---|
| `templates/claim-registry.md:258`, `templates/vv-framework.md:131` | Checkbox — "Criterion is independent of the proposition (not circular)" | PROPOSITION falsification criteria only |
| `agents/review-prompt.md:85` | Reviewer question — "Do the arguments build on each other without circular reasoning?" | Peer-review simulation |
| `templates/anti-hallucination.md:55` | Step 6 *Human-in-loop anchor* | **A different animal, and not a judgment call** — *procedural* circularity (is the verifying agent the introducing agent?), decidable from provenance. Listed for completeness, excluded from the three |

R-4 in `README.md:522` is deliberately **not** in that table: it is an ad-hoc retiering *after* the fact, and it appears below as Instance 1 of the gap. Counting it as one of the checks and as evidence the checks are inadequate would be the same double-count this DR is about.

`agents/equation-checker.md` has no circularity check. Its nearest category, `ASSUMPTION`, is severity Low and reads "correct only under an assumption that is not stated" — which does not describe a result that is correct under *no* extra assumption and simply carries no evidential weight.

### The narrow, defensible claim

An earlier draft proposed a two-limb "provenance trace" and called it Step Z's first mechanical trigger. **One limb was unsound and is dropped.** What remains is one test:

> **Reuse.** If the equation producing a result is the same equation already used to define one of its inputs, the agreement is an identity.

Where a derivation graph is available, this is decidable by inspecting it rather than by weighing the physics. In the external instance it matched a real defect: an energy comparison reported as confirmation, where the two quantities had been set equal earlier in order to solve for a third. **That is not independent evidence** — the test was constructed from that instance, so it has been run zero times prospectively.

⚠ **Step Z's rule already covers the case; what is missing is the noticing.** `templates/anti-hallucination.md` says *if language > evidence, that is a Step Z finding*, and a circular result offered as confirmation is exactly that. An earlier draft of this DR said three times that *no shipped check names it*, which is false and overstates the gap. The honest claim is narrower and weakens the case against Option A accordingly.

### Why Step Z rather than the equation-checker

Both recorded instances were adjudicated as **tier** problems and repaired by **retiering**, which is Step Z's job. Circular evidence is not a new kind of finding under Step Z's rule; it is a mechanism by which the evidence tier is lower than the prose implies.

⚠ **The counter-precedent, stated because an earlier draft omitted it.** `DR-019`'s F1 adjudication moved a finding *out* of Step Z on the ground that *"Step Z tests language-tier > evidence-tier; F1 is *false*, not under-evidenced, and neither Step Z remediation repairs it. It is an `agents/equation-checker.md` finding (INCONSISTENT/NUMERICAL) — an instrument already shipped."* That is a precedent for routing mechanical findings toward the equation-checker, and this DR proposes the opposite direction. The distinction relied on: F1 was a **false** value, which the equation-checker can adjudicate alone; a reused equation produces a **true** value whose evidential weight is the thing in question, and only Step Z compares weight against prose. This is a real tension and the reader should weigh it, not take it as settled.

### Status of related work

- **`DR-009`** — Accepted. CALCULATION is a verification *procedure* running alongside the registry. Untouched here.
- **`DR-017`** — Accepted. Generalised Step Z to all project types. This extends the same instrument along a different axis.
- **`DR-018`** — Proposed. Rejected folding a second lens into the equation-checker (its Option B). Its deeper principle — *one lens per instrument* — cuts against this DR too, and is engaged under Option D.
- **`DR-019`** — Proposed. Also edits Step Z, along the *surface* axis. Orthogonal and composable; see *Consequences*.
- **`memory/dead-ends.md`** — *don't promote a new verification procedure to a registry unit type.* This is a check, and a limb of an existing one. The door stays closed.

## Options Considered

### Option A: Status quo
- (+) Honest at n=2; zero surface.
- (−) Leaves a defect class with no home through two instances, both found by someone happening to look.

### Option B: A `CIRCULAR` category in `agents/equation-checker.md`
- (+) The Reuse test is mechanical, which is that agent's native method.
- (−) A reused equation produces an arithmetically correct result. Mixing an evidential verdict into a correctness instrument means "passed the equation check" stops having one meaning — `DR-018`'s Option-B objection.
- (−) ⚠ An earlier draft also argued B "strands the finding, since the equation-checker has no route into the registry." **That was false**, and is withdrawn: in the triggering instance every registry row carries a `Verified by | CALC-nn` column and the audit file is the registry's stated centre of gravity. The route exists and is in use. Only the first objection survives.

### Option C: A Reuse limb under Step Z *(proposed)*
- (+) Lands where both instances were actually adjudicated and where the repair already happens.
- (+) Reuses a shipped instrument rather than adding one — the move `DR-019` found productive.
- (+) The matching step is mechanical where a derivation graph exists — no physics judgment in the comparison itself.
- (−) That is narrower than "mechanical". Constructing the derivation graph for a third-party document is judgment-laden, deciding whether two written equations are *the same* up to rearrangement is judgment, and the scope gate reads intent. **This is a noticing heuristic, not an adjudicator**; an earlier draft called it Step Z's "first mechanical trigger" and used that to beat Options A, B and D.
- (−) Step Z is already the longest section in `templates/anti-hallucination.md`.
- (−) ⚠ **Its scope line is a judgment call.** The limb applies to "a number offered as confirmation", and deciding whether a number is *offered as confirmation* reads authorial intent. Legitimately re-using a governing equation as an internal consistency check is not circularity, and the gate is what separates the two. The judgment is **relocated, not eliminated** — an earlier draft claimed otherwise and that claim is withdrawn.
- (−) An earlier draft cited this option's lack of a gate obligation as a virtue while condemning Option B for the same property. That asymmetry is removed; neither option obliges anyone.

### Option D: A standalone circularity-checker agent, `DR-018` shape
- (+) Mirrors one-lens-per-instrument, which is `DR-018`'s actual principle and a real argument here: Step Z's object is a prose tier comparison, the Reuse test's object is algebraic dependency structure. Those are at least as disjoint as `DR-018`'s values-versus-symbols.
- (−) `DR-018` earned a standalone agent for a lens *no* instrument touched. Here Step Z already owns the verdict; only detection is missing.
- (−) A whole agent for one test, at n=2.
- Kept live rather than dismissed: if the class recurs, D is the honest destination.

### Option E: Both B and C with a stated split
- (+) The equation-checker reports, Step Z adjudicates — mirroring how CALCULATION already relates to the registry.
- (−) Two surfaces to synchronise on the weakest evidence here. Deferred, see *Revisit If*.

## Decision

**Option C, reduced to one test.**

Proposed text, to sit in `templates/anti-hallucination.md` under Step Z's *General triggers*:

> ### Reuse check (mechanical)
>
> Applies when a number is presented as confirming a model. Trace the result's inputs back through the derivation.
>
> **If the equation producing the result is the same equation already used to define one of its inputs, the agreement is an identity and confirms nothing.**
>
> Deciding whether a number is *offered as confirmation* is a judgment; the matching itself is not. Where it fires, treat the claim's evidence tier as **SPECULATIVE** and apply Step Z's existing remediation unchanged — **both branches remain available**: downshift the prose, or supply the missing apparatus. In the common case a derivation that entails its result cannot be rescued by more measurement, but that is a judgment about the particular derivation, not a rule; an entailment that holds only to leading order leaves an informative residual.
>
> *Related but out of scope:* a result may also be empty because the posited entity drops out of the final expression, or because the construction is a change of units. Neither is decidable by substitution. Judge them by asking how many independent predictions the construction buys per observable it consumes.
>
> **Known limits of the match — check these before acting on a hit.** It fires on some non-circular constructions and stays silent on some circular ones:
>
> | Case | Behaviour |
> |---|---|
> | Iterative / fixed-point solve — equation E defines x, then E computes a residual to certify convergence | **False positive.** The residual is informative |
> | Same equation, *different* observable — E fixes a parameter from O₁, then predicts O₂ | **False positive.** A real prediction |
> | One rearrangement — E₁ defines `x = a·b`, E₂ computes `y = x/b` and reports `y ≈ a` | **False negative.** Syntactically a different equation |
> | Multi-hop — x from y, z from x, then y from z reported as agreeing with the input y | **False negative.** No equation is reused |
>
> The discriminating question in every one of these is the predictions-per-observable question above, which is a judgment. This match is a cheap first filter, not an adjudicator.

**Rationale.** The Reuse test is the part that survives scrutiny, and it is worth having. The rest of what a first draft proposed was either unsound or a judgment call wearing a procedure's clothes, and is demoted to the closing note above — present as guidance, absent as a check.

## Consequences

- `templates/anti-hallucination.md` **would gain** the sub-section above. Adopter-facing → MINOR bump plus an `UPGRADING.md` row **if accepted**. Only Accepted DRs bind.
- **MINOR is correct only because the limb obliges nothing.** An earlier draft's text foreclosed Step Z remediation (b) — *supplying more apparatus* — which `templates/anti-hallucination.md` currently permits. Removing a permitted remediation **is** an obligation change, and by this repo's own v3.0.0 precedent (*"three adopter-installed templates now oblige action … rule 1 fires"*) that would make the bump **MAJOR**, not MINOR. The foreclosure has been removed rather than the classification raised, because the narrowest version is what the evidence supports. If a future revision reinstates it, the bump must be reclassified in the same edit.
- **A named sub-check, not a gate obligation.** No Gate in `templates/vv-framework.md` changes. Deliberate: obliging action on this evidence is what `DR-019` withheld.
- `agents/equation-checker.md` is **not modified**, and the `CIRCULAR` category in the triggering audit stays a project-local extension.
- **Vocabulary.** The limb says "at the floor" (SPECULATIVE), not "null". ⚠ An earlier draft invented a null tier; `templates/writing-guide.md` maps four tiers with SPECULATIVE as the floor, no shipped surface can consume a fifth, and the triggering audit's own Step Z table recorded the affected entry as SPECULATIVE — its own instance never used the tier the draft proposed.
- **Sequencing with `DR-019`:** both edit Step Z; whichever lands second should re-read the section rather than patching blind.
- `agent-ready-research` vendors this layer under `DR-017` and should be offered it if accepted, with the n=2 caveat.

## Evidence Base

**Instance 1 — in-repo, 2026-08-13.** `README.md:522`, row R-4, retiered SUPPORTED → EMERGING: *"the earlier SUPPORTED rested on one source plus the artifact the claim recommends, which is circular."* Surfaced by the `DR-019` sweep, whose adjudicator listed *"a registry row at SUPPORTED on one circular source"* among four upheld findings.

> **These are one finding, not two.** Same date, same row, same description. A first draft counted them separately and reported n=3.

**Instance 2 — external, 2026-08-16.** An unpublished third-party quantitative note audited under the framework; the project directory is gitignored and the author is not named here, per the standing rule that a critique of work this project did not author is never version-controlled. What generalises:

- One check was a clean Reuse case: an energy reported as agreeing with a quantity it had been *set equal to* in order to solve for a third. No shipped instrument names this, and the proposed limb catches it by inspection.
- ⚠ **The four checks that audit labelled `CIRCULAR` are not four instances of one defect.** On review: two are genuine circularity, one is an *idle wheel* (the posited entity drops out — a different failure), and one turned out to be the first result multiplied by a geometric constant. A first draft of this DR reported "4 of 14 mechanical checks were circular"; that line is withdrawn. The conservative n=2 framing was right and the inflated figure inside it was not.
- ⚠ **The audit's own mechanical reproducer could not encode the finding.** `verify_claims.py` emits `ASSUMPTION` on those checks and prints that all checks agree with the audit — certifying the arithmetic, not the adjudication. That is direct evidence *against* any strong mechanicality claim, and it is why this DR now proposes one narrow test rather than a general procedure.

**What this does not establish.** Two instances, three days apart, one maintainer, one model family. No cross-vendor pass. No prospective run. No adopter evidence.

## Revisit If

- **A third instance appears in prose rather than a derivation** — the limb's derivation-graph framing would then be too narrow.
- **The Reuse match fires on legitimate internal consistency checks** — the iterative-solve and same-equation/different-observable rows of the Known limits table. Those are the most likely false-positive routes and the sharpest known weakness. Equally: if the two false-negative rows turn out to be the common shape in practice, the match is catching the easy case only and Option D should be revisited.
- **The class recurs enough to justify Option E**, or **Option D** if the lens keeps needing to run where Step Z does not.
- **An adopter reports the limb is unusable without a worked example.** None is included; the only available instance cannot be published, and the framework's own v3.0.0 worked-example defects argue against inventing one.
- **`DR-016` is promoted to Accepted** — its authoring-versus-reviewer position bears on whether a check aimed mostly at other people's finished work belongs in an authoring discipline.

## Draft history

The first draft of this DR (2026-08-16, superseded the same day) proposed a **two-limb provenance trace** and claimed it gave Step Z its **first mechanical trigger** — the argument used to beat Options A, B and D. A DR-011 Pass 1 / Pass 2 battery refuted it. Kept visible rather than rewritten away, because the failure is the most useful evidence in this document:

1. **The Cancellation limb was unsound.** "Substitute every definition back and see which symbols survive" flags ordinary derived constants: the three checked — Rydberg, Bohr radius, Chandrasekhar mass — all vanish under reduction to primitives, which is enough to make cancellation unreliable as a test. (The unhedged form, *every* defined constant vanishes, shipped in the first draft and is withdrawn: it is either trivially true of any constant defined in the chosen basis, or false of one taken as primitive. Three examples of one kind do not license a universal, and this sentence is the sole argument that killed the limb.) A determinate-but-invalid test is worse than an acknowledged judgment call, because it manufactures confident false positives with procedural authority. **Dropped.**
2. **The mechanicality claim was overstated** for the surviving limb too: its scope gate reads intent.
3. **Two supporting arguments were false** — that Option B "strands the finding", and that the equation-checker would return `OK` (it returns `ASSUMPTION`, as the DR's own Context conceded two sections earlier).
4. **A tier was invented** that no shipped surface can consume, and that the DR's own instance had not used.
5. **`DR-019`'s F1 counter-precedent was omitted** while `DR-019` was cited four times in support.

This document is the response. Its scope is roughly a quarter of the first draft's.

## Implementation status

**Nothing in the Decision section has been implemented.** `templates/anti-hallucination.md` carries no reuse check, `agents/equation-checker.md` still has seven categories, and no CHANGELOG or `UPGRADING.md` entry exists. `status: Proposed`.

<!-- verify: cd "$(git rev-parse --show-toplevel)" && grep -qi 'reuse check' templates/anti-hallucination.md && { echo 'CLAIM REFUTED: DR-020 has been implemented — update this section and the Status field'; exit 1; } || echo 'DR-020 correctly unimplemented: Step Z has no reuse check' -->

<!-- verify: cd "$(git rev-parse --show-toplevel)" && n=$(grep -cE '^\|[^|]*\| `[A-Z]+` ' agents/equation-checker.md); echo "equation-checker categories: $n"; [ "$n" -eq 7 ] || { echo 'CLAIM REFUTED: the category table is no longer the seven this DR was written against'; exit 1; } -->

<!-- The probe above matches ANY backticked all-caps code in column 2, not a whitelist
     of the seven. Written as a whitelist first, it was blind to the change it exists to
     detect: adding an eighth `CIRCULAR` row — i.e. implementing the Option B this DR
     rejects — still counted 7 and PASSED. Demonstrated on a seeded input 2026-08-16.
     A whitelist detects removal and renaming only. Probe 1 is case-insensitive for the
     same reason: an implementation titled "Reuse Check" would otherwise leave this DR
     claiming unimplemented forever. -->

<!-- verify: cd "$(git rev-parse --show-toplevel)" && grep -q 'Retiered SUPPORTED→EMERGING 2026-08-13' README.md && echo 'Evidence Base instance 1 still present in README R-4' || { echo 'CLAIM REFUTED: the R-4 retier note this DR cites is gone'; exit 1; } -->

## Provenance

Triggered by an external third-party audit on 2026-08-16; the in-repo instance it matched was surfaced by the `DR-019` sweep on 2026-08-13. First draft and this revision both written in one session by one model family. Tracked publicly as [#35](https://github.com/ducroq/agent-ready-papers/issues/35). **Review coverage: DR-011 Pass 1 (Haiku-class, checklist) and Pass 2 (Opus-class, adversarial) have run on the triggering audit, and Pass 2 additionally on the first draft of this DR — every substantive objection above came from it. No cross-vendor Pass 3** (no cross-vendor CLI installed), so this document has had no training-prior escape. **This revision has not itself been reviewed.**
