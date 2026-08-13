# DR-019: Step Z Surface Scope — Naming Framework Prose, Not Sweeping It

---
status: Proposed
date: 2026-08-13
superseded_by:
---

**Evidence tier: EMERGING.** The evidence arrived in two stages and this document was written across both, so read them separately:

- **Stage 1 — the deciding run** (the *Context* section below): one off-protocol sweep of one document, self-run and self-adjudicated, no cross-vendor pass, no control arm. This is what the *Options Considered* section was written against, and on it Option A is **not supported**.
- **Stage 2 — the backlog sweep** (the *Sweep result* section, added later): ten reviewers plus an independent adjudicator, rubric pre-registered before reading, denominators reported. On this, Option A becomes **proposable** — see that section for why, and for what it still does not establish.

Both remain EMERGING: everything is self-application, and neither stage had a cross-vendor pass or a generic-prompt control. The gap this DR names is well-evidenced; the remedy is not. Language throughout is hedged deliberately — an earlier draft of this DR was written in ESTABLISHED register on this same evidence and was failed by its own Step Z check.

## Context

`templates/anti-hallucination.md` scopes Step Z as *"Applies to all project types"* — a **project-type** scope with no **surface** scope, and its remediation steps target "the manuscript" and registry entries throughout. The sibling repo `agent-ready-research` has the same gap in mirror image: its Step Z enumerates surfaces exhaustively (three `every`s), all of them world-claim surfaces, with methodology prose never entering the enumeration.

The generalisation worth keeping:

> **A scope statement complete along the axis it names reads as complete along the axes it doesn't.**

Registered as a bet in `memory/hypothesis-log.md` (2026-08-08), filed publicly as [#33](https://github.com/ducroq/agent-ready-papers/issues/33). *Provenance caveat:* this sentence is **n=2 but not independent** — near-identical wording was authored first in `agent-ready-research`, same maintainer and same drafting agent. It is a hypothesis that survived restatement, not a replicated finding.

### What the measurement actually showed

A two-arm run on 2026-08-13, then a five-reviewer battery on the run itself. Reporting both, because the second changed the conclusion.

**The original premise was too strong and is now corrected.** The claim was that *no* shipped check runs over framework prose. That is false. `agents/review-prompt.md` is shipped, and `memory/hypothesis-log.md` records it run over framework prose on 2026-06-11 — README, `docs/non-claude-setup.md`, `agents/README.md`, CHANGELOG — returning **3–4 novel load-bearing findings**. The surface is not unreachable by shipped instruments; it has already been reached successfully.

The defensible residual claim is narrower: **no shipped check *names* framework prose in its scope.** Coverage there is incidental — it happens when someone points a general reviewer at the surface, not because any procedure says to.

**The run did not meet its own criterion on-protocol.** The registered Method reads: *"on the next release that … substantially edits `docs/`, run Step Z over the **changed** methodology prose."* Only Arm A (the v2.6.0..v2.6.1 diff) satisfies that, and Arm A returned **1 lite, 0 load-bearing**. Arm B ran on `docs/THRESHOLDS.md`, a document not in the release at all — an unregistered extension of the protocol, not a satisfaction of it.

**Arm B's three findings did not survive review**, and the surviving one belongs elsewhere:

| ID | Claimed | After review |
|----|---------|--------------|
| F1 | 85% envelope's "clears automatically" property is arithmetically false | **Real defect, wrong instrument.** Step Z tests language-tier > evidence-tier; F1 is *false*, not under-evidenced, and neither Step Z remediation repairs it. It is an `agents/equation-checker.md` finding (INCONSISTENT/NUMERICAL) — an instrument already shipped. Severity also downgraded: latent, not live. No registry is near the failure regime (5.3% and 0% against a break point of 25–50%). |
| F2 | flat mechanism claim contradicted two lines later | **Refuted.** Equivocation on "signal": one referent is the registry-discipline signal, the other an empirical predictive correlation named in its own sentence. All four `What would change this:` blocks name external validating evidence, never a retraction — four for four. The weaker residual (flat mechanism, no measurement anywhere) stands. |
| F3 | rubric band edge transferred to real reviewer behaviour | **Cosmetic.** Only the token "real" is unsupported, and the document disclaims it two lines later. Deleting the sentence changes nothing shipped. |

**Net: the criterion was met once at most, on a document the pre-registration excluded, by an instrument other than the one under discussion.**

**Two further limits, both conceded.** The design confounds staleness with claim-density — `docs/THRESHOLDS.md` carries 36 of the 38 numeric-evidence markers in all of `docs/` — 3 of the 5 files there have zero (an earlier draft added "~33× the directory mean"; no reading of these counts yields 33, and the raw 36-of-38 is the evidence), and it is *also* the stalest. Those are precisely the two candidate causes, so the run cannot attribute the gap to either. And the sweep's own remediation introduced four fresh defects of the class it exists to catch, caught only by the battery — which bears directly on the cost of any recurring sweep.

## Options Considered

### Option A: Standing periodic sweep of framework prose

- (+) Would find accumulated defects; the backlog is real.
- (−) **Not supported by the stage-1 evidence** (one off-protocol document, self-adjudicated, no control). ⚠ The stage-2 backlog sweep partially answers this — see *Sweep result*. The Options analysis below was written against stage 1 and is deliberately left unrewritten, so the two stages can be told apart.
- (−) Prices a recurring obligation against a one-time backlog: the first sweep drains two months of accumulation, every later sweep sees only the increment.
- (−) Exit condition is asymmetric — one finding to enter, three null sweeps to leave, against a corpus that only grows.
- (−) DR-016 (Proposed) holds the framework is an authoring discipline, not a reviewer; a standing sweep over finished prose is the evaluative posture that DR warns about.

### Option B: State the surface axis in Step Z's scope

- (+) Directly repairs the mechanism named in Context — an unnamed axis reads as covered.
- (+) Costs nothing recurring, imposes nothing on adopters, and is honest at the current evidence tier.
- (−) A scope line alone changes no behaviour unless something acts on it.

### Option C: Diff-triggered check

- (+) Cheap, automatic, and it did yield a finding on the most-reviewed prose in the repo, after `/review-changes` and the release gates had already passed over it.
- (−) Structurally cannot see unchanged prose.
- Note: an earlier draft rejected this as *"measured not to work."* That was wrong — C was never run, and the counterfactual is release-specific. A diff trigger in force when `docs/THRESHOLDS.md` was authored would have swept it at creation.

### Option D: Name the axis, sweep the backlog once, then re-evaluate

- (+) Matches what the evidence actually supports: a real backlog, an unproven recurrence rate.
- (+) A and C cover disjoint populations (new prose vs stale prose), which under DR-011's own rule is a reason to keep both rather than eliminate one.
- (−) "Re-evaluate later" decays into "never" without a trigger.

## Decision

**Option D**, with the recurring obligation explicitly withheld.

1. **Step Z gains a surface axis.** *(NOT IMPLEMENTED — see Status below.)* Its scope line names both axes — project types *and* surfaces — and states that where a repo ships framework or methodology prose, that prose is in scope. Stating the axis is the fix for the mechanism this DR is about.
2. **Point at the instruments that already work**, rather than creating one. `agents/review-prompt.md` has demonstrated 3–4 load-bearing findings on this surface; `agents/equation-checker.md` owns the numerical-inconsistency class that F1 actually belongs to. Both ship.
3. **One backlog sweep**, not a cadence. Sampled rather than cherry-picked: include at least one stale *claim-sparse* document (3 of 5 files in `docs/` have zero evidence markers) so the yield estimate is not drawn from the densest case again.
4. **Pre-register before that sweep**: the load-bearing rubric, and an adjudicator who did not write the prose. Both were missing this time and both changed the result when supplied.
5. **Re-evaluate after the backlog sweep** against a named trigger — the next `/audit-context` run — not "later".

**No standing obligation is created by this DR.** If the backlog sweep yields load-bearing findings in claim-sparse prose, that is the evidence a cadence would need, and it can be proposed then.

## Consequences

- `templates/anti-hallucination.md` Step Z **would gain** a surface-scope statement. **Adopter-facing** — MINOR bump plus an `UPGRADING.md` row *when this DR is accepted*. **None of this has been done**: `templates/anti-hallucination.md` still scopes Step Z as "Applies to all project types", and no CHANGELOG or UPGRADING entry exists. This DR is `status: Proposed`, and per `CLAUDE.md` only Accepted DRs bind — shipping a template change on an unaccepted decision would be the defect, not the fix.
- **The F1 defect is fixed in `docs/THRESHOLDS.md` independently of this DR** (arithmetic correction, break point stated as the 25–50% range it actually is, enforcement asymmetry documented). **The normative surfaces still carry the bare ≥85%** — README Gate 2, `templates/vv-framework.md` §3, `templates/claim-registry.md`, and each paper registry inheriting from it. Documenting a defect in the rationale file while leaving it in the four places adopters read is not a fix, and this DR does not pretend otherwise. Repairing them is a separate change.
- F2's residual and F3 remain open in `docs/THRESHOLDS.md`, flagged in-place. Both need a decision about what the actual justification for the 70% and 3.5 thresholds is — content work, not an editing pass.
- `/audit-context` is **user-global**, so a papers-specific sweep step cannot be added to the skill without affecting every repo. The sweep is a documented local procedure, or an upstream proposal.
- Sibling repo `agent-ready-research` queued the same finding as METH-001; whatever lands here should be offered there, including the premise correction.

## Sweep result (2026-08-13) — the backlog sweep in decision item 3 has run

Ten reviewers over the shipped surface (`templates/`, `agents/`, README normative sections) and `literature/`, plus one independent adjudicator over the judgement calls. Rubric pre-registered before any file was read; every reviewer required to report words scanned.

**Yield by surface, findings per 1,000 words:**

| Surface | Yield |
|---|---|
| `anti-hallucination` + `writing-guide` | 2.46 |
| literature content (4 slices) | 0.48 – 2.95 |
| `claim-registry` + `vv-framework` | 1.68 |
| README normative | 1.50 |
| small templates + `agents/` | 0.43 |
| cross-surface invariants | **12 of 68 comparable disagreed — 17.6%** |

**The discriminating question is answered: yes.** Load-bearing findings appeared in claim-**sparse** prose — the two most severe literature findings (a phrase attributed to Hevner that belongs to Venable; a paper's own degradation caveat omitted from the entry the Hard Constraints rest on) carry no numbers at all. The pre-registered prediction that risk would concentrate in numeric-dense entries **failed in all four literature slices**: the densest entry in the repo verified to the page number, while prose characterisations leaked. **Option A is therefore proposable** on this evidence — that call is the maintainer's, and this DR does not make it.

**What the sweep found, in one sentence:** the framework's machinery is consistent (unit types, tiers, gates and source weights verified identical across 6–8 surfaces each; zero fabricated sources, zero invented authors, zero invented numbers across 25 literature entries; 41/41 DOIs resolve), and its defects cluster in **worked examples**, **cross-surface propagation**, and **quote fidelity**.

**The adjudicator's cross-cutting diagnosis is the finding this DR should carry forward:** four separate upheld findings were one failure mode — *the framework's normative surfaces stated its own findings at a higher tier than its own Step Z would allow.* A checklist that certified the violation DR-002 exists to prevent; a registry row at SUPPORTED on one circular source; two unverifiable ranges shipped as calibration bands; and a confound concealed inside a binding Accepted DR. That is the strongest evidence yet for this DR's premise — and it was produced by pointing existing instruments at framework prose, not by inventing a new one, which supports Decision item 2 over Option A.

**Cost:** ~1.1M tokens, 11 agents. Logged in `vv/cost-log.md`.

## Revisit If

- ~~**The backlog sweep yields load-bearing findings in claim-sparse prose**~~ — **fired 2026-08-13, see above.** A cadence is now proposable; whether the recurrence rate justifies one is still unmeasured, since this sweep drained an accumulated backlog and says nothing about the increment.
- ~~**It yields nothing outside claim-dense documents**~~ — **falsified.** The narrower "numerically dense methodology prose" scope suggested during the run is wrong and should not be adopted.
- An adopter reports the check produces mostly false positives on prose written outside this repo's house style. All evidence here is self-application, which is this framework's weakest external-validity position.
- DR-016 is promoted to Accepted — the authoring-vs-reviewer tension stops being a caveat and starts being binding.

## Implementation status

**Nothing in the Decision section has been implemented.** Recorded explicitly because a 2026-08-13 review found this document reading as though it had. What exists today: the Context, the two-stage evidence, and the sweep result. What does not: the Step Z surface axis, the CHANGELOG entry, the `UPGRADING.md` row.

<!-- verify: cd "$(git rev-parse --show-toplevel)" && grep -q 'Applies to all project types' templates/anti-hallucination.md && ! grep -q 'DR-019' CHANGELOG.md && echo 'DR-019 correctly unimplemented' || { echo 'CLAIM REFUTED: DR-019 has been partly implemented — update this section and the Status field'; exit 1; } -->

<!-- The `||` above is deliberately UNescaped. The `\|` form is correct only
     inside a markdown table cell, where a bare pipe would split the row and
     the /curate runner unescapes it back before executing. This probe sits in
     prose, so `\|\|` reaches bash literally and is a syntax error — which is
     exactly what it did on first write, caught by the runner reporting ERROR
     with "(no output — it proved nothing)" rather than a false PASS. -->

<!-- verify: cd "$(git rev-parse --show-toplevel)" && grep -rn '\\|\\|' decisions/ docs/ templates/ 2>/dev/null | grep -q 'verify:' && { echo 'CLAIM REFUTED: an escaped-pipe probe exists outside a table cell'; exit 1; } || echo 'no escaped-pipe probes outside table cells' -->

## Provenance

Measurement and five-reviewer battery both 2026-08-13; full record in `memory/hypothesis-log.md` under the 2026-08-08 entry, including the superseded first write-up kept visible. Battery: DR-011 Pass 1 (Haiku) and Pass 2 (Opus), `agents/equation-checker.md` (Sonnet), a Step Z self-application, and an adversarial refuter. **Pass 3 cross-vendor did not run** — no cross-vendor CLI is installed, so every reviewer was one draw from one training prior and this DR has had no training-prior escape. Rubric B on the first draft: 3.3 and 3.35, both below this framework's own ≥3.5 threshold; the Step Z self-application failed it outright. This draft is the response to that battery. Issue [#33](https://github.com/ducroq/agent-ready-papers/issues/33).
