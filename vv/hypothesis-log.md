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

**Origin:** Surfaced 2026-06-11 by DR-011 Pass 2 (Opus, intra-family large) reviewing v2.1.0–v2.1.2. Pass 2's finding (quoted): *"the Rebuttal row (README:60) deflects to *When It Is Overkill* (which addresses *who shouldn't use the framework*), not the Warrant's actual challenger"* — i.e., the README's central Warrant had no engaged counter for the dynamic case (capability rises over time). Logged here as a falsifiable bet rather than papered over in the Warrant itself, per the hypothesis-log convention. README's Toulmin block now points at this entry from a *Dynamic counter to the Warrant* note. Logged in `vv/cost-log.md` as the second of two findings from the 2026-06-11 DR-011 battery.

**Domain:** Framework Warrant validity, process-layer-vs-model-layer competition
**Status:** open

## Resolved

*(none yet)*
