# Hypothesis Log — agent-ready-papers framework (self-application)

<!-- Public framework-level provisional positions whose evidence lives in
     the future. Companion to:
     - memory/hypothesis-log.md (maintainer-local, gitignored — intra-session
       bets, working positions)
     - templates/hypothesis-log.md (the template adopters copy for their own
       paper projects)

     What goes here: positions about the framework's own design — its
     boundary conditions, its long-term relevance, its claims about itself.
     Each entry is registered with Position / Method / Revisit trigger /
     Review by per the hypothesis-log convention.

     Why a public framework-level log: positions that load-bearing prose
     in the README depends on need a place to be registered as falsifiable
     bets, not papered over as confident assertions. The Toulmin block's
     central Warrant is one such bet (the dynamic case where model+tool
     capability rises).

     Convention introduced in v2.2.0 alongside vv/cost-log.md as part of
     the framework's self-verification surface. -->

**Repo:** agent-ready-papers
**Started:** 2026-06-11

## Open

### [2026-08-16] The third-party ceiling lives in the interpretive layer, not the factual one

**Position (provisional):** Successor to the split entry now in [`hypothesis-log-resolved.md`](hypothesis-log-resolved.md), carrying only the half that survived. **In any third-party audit, coverage of ARGUMENT and PROPOSITION units will be at or near 0%, whatever the CLAIM coverage turns out to be.** The mechanism is Toulmin item 2: an ARGUMENT is verified only when each of its grounds is `[x]`, and its grounds are the audited text's own units. Where those units are closeable by a reader — reproducible arithmetic, checkable references — the CLAIM layer can go high; the interpretive layer still cannot, because the audited author's *inferences* are not reproducible in the way their arithmetic is. Observed twice: 0 of 22 and 0 of 6. The documents share no subject matter — but they share the maintainer, the repo, the instruments, the registry template, the Toulmin criterion and a three-day window, which is everything that governs the measurement. And by the argument below, only the second observation is informative. **Read this as n=1 with a consistent n=2, not as a replication.**

**The stronger claim this deliberately does not make:** that CLAIM coverage is capped. It is not — one audit reached 77% on a document citing no sources at all. The weakest informative form is the interpretive half alone, per the 2026-06-11 discipline.

**Alternative (the falsifier):** A third-party audit in which one or more ARGUMENTs or PROPOSITIONs reaches `[x]` with all grounds verified. Most likely route: a document whose interpretive steps rest entirely on units the auditor could close independently — a purely mathematical argument, say, where each premise is a reproducible calculation. If that happens the pattern is about *inference from uncheckable premises*, not about third-party status, and the right response is guidance on which documents repay auditing rather than any threshold change.

**Method:** On the next third-party audit, before drawing conclusions, record three things: CLAIM coverage, ARGUMENT/PROPOSITION coverage, and — separately — **the count of ARGUMENT + PROPOSITION units with every ground `[x]`**, together with the mean number of grounds per unit.

⚠ **The third is not obtainable from `tools/coverage.py`, and an earlier version of this entry wrongly said it was.** That tool reads the Status checkbox and has no concept of Toulmin grounds; "ARGUMENT coverage 0%" and "0 units with all grounds `[x]`" are different measurements. Count the grounds figure by hand and record that you did, or write a checker for it. The parent entry's Method demanded this be computed mechanically and it was not — the figure below rests on inspection, which is the error that Method existed to prevent.

**Report grounds-per-unit, because without it the headline is unreadable.** 0-of-N is close to forced when CLAIM coverage is low: with k grounds per unit drawn from a pool that is p-verified, the expected count of fully-grounded units falls off as p^k. At 16% CLAIM coverage, 0 of 22 was near-inevitable. At 77%, 0 of 6 is surprising. Only the second observation carries information.

**Revisit trigger:** A third third-party audit completing in this repo; or any change to Toulmin item 2 or to how grounds verification is scored, which would move this directly.

**Review by:** 2027-08-16 — backstop; expected to resolve whenever a third audit runs.

**Origin:** Registered 2026-08-16 on the resolution of the entry now in [`hypothesis-log-resolved.md`](hypothesis-log-resolved.md), whose headline prediction and first mechanism were both refuted by a second audit the same day while this half replicated exactly.

**Domain:** Coverage thresholds, third-party audit scope, Toulmin grounds constraint
**Status:** open

### [2026-08-16] Circular evidence is a recurring defect class with no shipped check

**Position (provisional):** A result can be arithmetically correct, dimensionally sound and fully reproducible while carrying **no evidential weight**, because the derivation entails it. This is a distinct defect class, it recurs, and no shipped instrument names it — `agents/equation-checker.md` has no category for it (its nearest, `ASSUMPTION`, is severity Low and describes something else), and the framework's five existing circularity touchpoints are all judgment calls. The bet: **it will keep appearing, and the ad-hoc retiering that has handled it twice will keep being the only response until something names it.** `DR-020` (Proposed) proposes the narrowest defensible check — a single mechanical *Reuse* test.

**Alternative (the falsifier):** No third instance appears within a year of ordinary use, in which case two instances three days apart were a coincidence of one session's attention rather than a rate, and `DR-020` should be declined rather than accepted. Or: instances keep appearing but the *Reuse* test catches none of them, because they take the idle-wheel or change-of-units form instead — both of which `DR-020` explicitly declines to make mechanical. That outcome argues for Option D (a standalone lens) over the proposed limb.

**Method:** Count instances, and for each record which form it took — reuse of a defining equation, an idle wheel (the posited entity drops out), or a change of units. Record whether the *Reuse* test would have caught it by inspection. Three forms were distinguished on the worked case only after adversarial review collapsed a four-instance count to two, so classify before counting.

**Revisit trigger:** A third instance in any surface; or `DR-020` reaching Accepted or Declined; or an adopter reporting a false positive from the *Reuse* test on a legitimate internal consistency check, which is its known weak point.

**Review by:** 2027-08-16.

**Origin:** n=2 — one in-repo registry row retiered 2026-08-13 by the `DR-019` sweep, and one external quantitative note audited 2026-08-16 (untracked, subject withheld). A first draft of `DR-020` claimed three instances and a general mechanical procedure; a DR-011 Pass 1 / Pass 2 battery established that two of the three were the same finding and that the proposed diagnostic was unsound — every defined constant vanishes under reduction to primitives, so "what cancels" would flag most of derived physics. Both corrections are recorded in that DR's *Draft history*.

**Domain:** Step Z, equation-checker categories, evidential weight vs arithmetic correctness
**Status:** open

### [2026-08-16] Sentence-level calibration and whole-argument impression come apart, and only structural registration catches it

**Position (provisional):** There is a failure mode in careful AI-assisted writing that **no amount of close reading detects and registry-based verification does**: every individual sentence is correctly hedged relative to its evidence, while the piece as a whole leaves the reader with an impression stronger than any of its sentences licenses. It arises when a recurring motif keeps its persuasive force after the text has itself explained why the motif should not extend to the case at hand. If this holds, it is an argument-*structure* defect with no sentence-level signature, it will recur across AI-assisted work, and the framework should name it explicitly — as a Step Z sibling operating at whole-argument scale rather than at the level of a single claim's language tier.

**Alternative:** The pattern is an artefact of one document, or it is reliably caught by an ordinary careful reader or a simulated peer-review pass without any registry. Evidence for the alternative: a DR-011 review pass on the same document independently surfaces it, or two further registered documents show fully calibrated sentence-level tiers with no whole-argument inflation. In that case the observation is a good critical note about one essay and not a framework-worthy pattern, and Step Z stays where it is.

**Method:** Two tests, both cheap. (1) **Reader test** — run a DR-011 peer-review pass on a document where the registry has found this pattern, *without* showing the reviewer the registry, and see whether the reviewer names it unaided. If reviewers reliably catch it, no new machinery is warranted. (2) **Recurrence test** — on the next two registered documents, record whether all entries pass the tier-language check individually while the document's overall thesis outruns them. The pattern needs the conjunction; either half alone is an ordinary finding already covered.

**Revisit trigger:** A DR-011 review pass run on a document with this pattern already registered; or the second registered document showing the same conjunction.

**Review by:** 2027-02-16 — sooner than the other open entries, because test (1) is a single review pass and can be run against work already in hand.

**Origin:** Surfaced 2026-08-16 by a completed registry pass on a third-party document, where all 16 ARGUMENTs passed qualifier calibration (item 4) with none overclaiming, and four counter-argument gaps were nevertheless found — one of which was that a motif kept doing rhetorical work after the text had explicitly stated the constraint that should have stopped it. Neither the framework's tier-language mapping nor Step Z, both of which operate per-entry, has a place to record a defect that only exists between entries.

**Domain:** Step Z, tier-monotonicity, argument-structure verification, AI-assisted writing failure modes
**Status:** open

### [2026-06-11] Named structural distinctions from defeasible-reasoning literature earn their place in the registry shape

**Position (provisional):** Pollock's rebutting/undercutting distinction (and the broader family of defeater typologies from the defeasible-reasoning literature) will, when introduced as an optional sub-field on ARGUMENT rows per [DR-015](../decisions/DR-015_rebutting-undercutting-defeater-distinction.md), see non-trivial uptake — at least 40% of newly-authored ARGUMENT entries across active projects use the sub-typing, and DR-011 Pass 2 / Pass 3 review outputs benefit from the classification (reviewer-finding-type correlates with which Pass produced it). If this holds, the framework should pursue further low-cost vocabulary borrowings from philosophical logic (dialogical-logic Underlying Form for DR-011; Dung-graph-style attack typology when inter-entry conflicts accumulate). If it fails, the borrowing was vocabulary-without-payoff and Option D in DR-015 (guidance prose only) is the lesson.

**Alternative:** The optional sub-field is left blank in >60% of new ARGUMENT entries, AND reviewer findings do not classify cleanly as rebutting vs. undercutting (most are mixed or unclear), AND no downstream registry consumer (Gate 2.5 internal-consistency check, hypothesis-log defeater link, attack-graph extension) is built that uses the field. In that case the borrowing *pattern* — "import distinctions from philosophical logic as low-cost registry extensions" — is wrong; the framework should retreat to Toulmin + Whetten + category theory as the closed set and stop adding vocabulary from adjacent traditions.

**Method:** Track three signals across the next two-to-three adoptions of DR-015 (if Accepted):

- *Uptake rate* — fraction of new ARGUMENT entries with non-blank `rebutting | undercutting` sub-type across active projects.
- *Reviewer classification yield* — when prompted via `agents/review-prompt.md`, can DR-011 Pass 2 / Pass 3 reviewers classify their load-bearing findings as rebutting / undercutting / mixed? What fraction are mixed vs. one-of-two?
- *Downstream use* — does any later DR or template change reference the sub-typing? Candidates: Gate 2.5 consistency-check criterion, Dung attack-graph proposal, PROPOSITION boundary-condition sub-typing per the Open Question in DR-015.

Position holds if uptake ≥40% AND reviewer classification yield ≥60% non-mixed AND at least one downstream artefact references the sub-typing. Position fails on any one of the three.

**Revisit trigger:** DR-015 promoted from Proposed to Accepted (which requires the three Pending Assessment checks pass — Paper 1 ARGUMENT-row field-test, DR-011 review-output classification, adopter check) AND at least one new claim registry is authored under the accepted shape. Earliest realistic: Paper 1 paper-writing-track resumption with Gate 3 re-pass, OR a new paper project's claim-registry bootstrap.

**Review by:** 2027-06-30 — backstop. Expected to resolve as adoption signal accumulates over the next one-to-two paper projects.

**Origin:** Surfaced 2026-06-11 by an in-session literature survey of philosophical-logic patterns against the framework's current apparatus (Toulmin, Whetten, category theory). Six candidates assessed: Pollock's defeasible reasoning (HIGH FIT, LOW COST — became DR-015); dialogical logic / Lorenzen-Hintikka (HIGH FIT, MODERATE COST — deferred to a follow-up DR proposing an *Underlying Form* subsection for DR-011); Dung abstract argumentation frameworks (MID-HIGH FIT, cost scales with registry size — deferred until inter-entry conflicts accumulate past ~50 entries); Reiter default logic + epistemic logic (vocabulary-only relabeling — low payoff at current scale, noted but not pursued); classical proof theory + adaptive logic (over-formalisation — skipped). The bet here is the broader pattern that this kind of low-cost borrowing earns its keep; DR-015 is the concrete first instance.

**Domain:** Registry-shape extension, ARGUMENT defeater typology, philosophical-logic borrowing pattern
**Status:** open

### [2026-06-11] Process-level verification infrastructure remains the locus of value as model-layer capability improves

**Position (provisional):** The Toulmin Warrant in [README → The Argument, Structurally](../README.md#the-argument-structurally) — *"tool-level checkers verify already-written citations; model-level techniques (RAG, grounded generation) constrain what gets generated; neither reaches the process layer where the failure modes originate"* — is **structural** (process layer is the locus of failure modes) rather than **static** (today's tools don't reach it). The structural reading predicts that even as RAG with citation-grounded generation, reasoning-step verification, and step-by-step planning mature at the model layer, the process layer remains the load-bearing site for: registry discipline, confidence-tier calibration, decision-record continuity, gate thresholds, and multi-pass review.

**Alternative:** A frontier-model RAG pipeline with citation grounding + reasoning-step verification + multi-step planning closes ≥75% of the gap the framework currently addresses. At that point the framework's process layer becomes redundant ceremony rather than load-bearing infrastructure, and the remaining residual scope (perhaps confidence-calibration and boundary-condition discipline that require human judgement) is too narrow to justify the apparatus.

**Method:** Apply the framework's own anti-hallucination checklist + claim-registry coverage discipline + Gate 3 multi-pass review to a manuscript written end-to-end by a frontier-model RAG pipeline (no human-mediated framework process during drafting). Compare:

- *Process-level load-bearing findings* the framework's apparatus catches that the RAG pipeline missed (e.g., a SUPPORTED claim phrased as ESTABLISHED that survived to draft; a PROPOSITION missing its boundary condition; an ARGUMENT whose Warrant is hidden)
- *Process-level findings the RAG pipeline catches on its own* (citation existence, factual accuracy, basic logical consistency)

Position holds if ≥3 load-bearing process-level findings remain that the RAG pipeline missed, on a manuscript ≥5,000 words with ≥10 citations. Position fails if the residual count drops below 3 or the residual findings are stylistic rather than load-bearing.

**Revisit trigger:** A frontier-model RAG pipeline with the named capabilities (citation grounding, reasoning-step verification, step-by-step planning) becomes available *and* is applied to a non-trivial academic manuscript. Initial test could be on Paper 1 once paper-writing-track resumes, or on a fresh prospective case study. Either way the test requires a manuscript drafted *without* the framework's process intervention, so the comparison is process-vs-no-process not framework-vs-framework.

**Review by:** 2027-06-30 — backstop. Expected to resolve naturally as frontier-model capability progresses through 2026-2027 and end-to-end RAG pipelines become operationally common.

**Evidence 2026-09-26 (for, weak).** Four independent groups now build *process-level* verification for AI-assisted writing, rather than relying on better models: Chen et al. 2026 (L60), Zhou & Yu 2026 (L61), sciwrite-lint (L66), and the VANRA checklist registered at EQUATOR. That is convergence on the locus, but not yet evidence that process beats model capability. None compares against a frontier RAG pipeline, which is what the revisit trigger requires. Status unchanged: open.

**Origin:** Surfaced 2026-06-11 by DR-011 Pass 2 (Opus, intra-family large) reviewing v2.1.0–v2.1.2. Pass 2's finding (quoted): *"the Rebuttal row (README:60) deflects to *When It Is Overkill* (which addresses *who shouldn't use the framework*), not the Warrant's actual challenger"* — i.e., the README's central Warrant had no engaged counter for the dynamic case (capability rises over time). Logged here as a falsifiable bet rather than papered over in the Warrant itself, per the hypothesis-log convention. README's Toulmin block now points at this entry from a *Dynamic counter to the Warrant* note. Logged in `vv/cost-log.md` as the second of two findings from the 2026-06-11 DR-011 battery.

**Domain:** Framework Warrant validity, process-layer-vs-model-layer competition
**Status:** open

## Resolved

Resolved entries: [`hypothesis-log-resolved.md`](hypothesis-log-resolved.md). The third-party verification ceiling (2026-08-16, SPLIT) and the dsp-workshop pilot (2026-06-12, HELD) are there.
