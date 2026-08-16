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

**Position (provisional):** Successor to the split entry in *Resolved*, carrying only the half that survived. **In any third-party audit, coverage of ARGUMENT and PROPOSITION units will be at or near 0%, whatever the CLAIM coverage turns out to be.** The mechanism is Toulmin item 2: an ARGUMENT is verified only when each of its grounds is `[x]`, and its grounds are the audited text's own units. Where those units are closeable by a reader — reproducible arithmetic, checkable references — the CLAIM layer can go high; the interpretive layer still cannot, because the audited author's *inferences* are not reproducible in the way their arithmetic is. Observed twice: 0 of 22 and 0 of 6. The documents share no subject matter — but they share the maintainer, the repo, the instruments, the registry template, the Toulmin criterion and a three-day window, which is everything that governs the measurement. And by the argument below, only the second observation is informative. **Read this as n=1 with a consistent n=2, not as a replication.**

**The stronger claim this deliberately does not make:** that CLAIM coverage is capped. It is not — one audit reached 77% on a document citing no sources at all. The weakest informative form is the interpretive half alone, per the 2026-06-11 discipline.

**Alternative (the falsifier):** A third-party audit in which one or more ARGUMENTs or PROPOSITIONs reaches `[x]` with all grounds verified. Most likely route: a document whose interpretive steps rest entirely on units the auditor could close independently — a purely mathematical argument, say, where each premise is a reproducible calculation. If that happens the pattern is about *inference from uncheckable premises*, not about third-party status, and the right response is guidance on which documents repay auditing rather than any threshold change.

**Method:** On the next third-party audit, before drawing conclusions, record three things: CLAIM coverage, ARGUMENT/PROPOSITION coverage, and — separately — **the count of ARGUMENT + PROPOSITION units with every ground `[x]`**, together with the mean number of grounds per unit.

⚠ **The third is not obtainable from `tools/coverage.py`, and an earlier version of this entry wrongly said it was.** That tool reads the Status checkbox and has no concept of Toulmin grounds; "ARGUMENT coverage 0%" and "0 units with all grounds `[x]`" are different measurements. Count the grounds figure by hand and record that you did, or write a checker for it. The parent entry's Method demanded this be computed mechanically and it was not — the figure below rests on inspection, which is the error that Method existed to prevent.

**Report grounds-per-unit, because without it the headline is unreadable.** 0-of-N is close to forced when CLAIM coverage is low: with k grounds per unit drawn from a pool that is p-verified, the expected count of fully-grounded units falls off as p^k. At 16% CLAIM coverage, 0 of 22 was near-inevitable. At 77%, 0 of 6 is surprising. Only the second observation carries information.

**Revisit trigger:** A third third-party audit completing in this repo; or any change to Toulmin item 2 or to how grounds verification is scored, which would move this directly.

**Review by:** 2027-08-16 — backstop; expected to resolve whenever a third audit runs.

**Origin:** Registered 2026-08-16 on the resolution of the entry now in *Resolved*, whose headline prediction and first mechanism were both refuted by a second audit the same day while this half replicated exactly.

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

**Origin:** Surfaced 2026-06-11 by DR-011 Pass 2 (Opus, intra-family large) reviewing v2.1.0–v2.1.2. Pass 2's finding (quoted): *"the Rebuttal row (README:60) deflects to *When It Is Overkill* (which addresses *who shouldn't use the framework*), not the Warrant's actual challenger"* — i.e., the README's central Warrant had no engaged counter for the dynamic case (capability rises over time). Logged here as a falsifiable bet rather than papered over in the Warrant itself, per the hypothesis-log convention. README's Toulmin block now points at this entry from a *Dynamic counter to the Warrant* note. Logged in `vv/cost-log.md` as the second of two findings from the 2026-06-11 DR-011 battery.

**Domain:** Framework Warrant validity, process-layer-vs-model-layer competition
**Status:** open

## Resolved

### [2026-08-16] The verification ceiling on a third-party audit is structural, not project-specific — SPLIT

**Position (provisional):** The coverage ceiling measured on a third-party audit run in this repo — **11 of 91 units (12%)** — is a property of *auditing text the project did not author*, and any future third-party audit here will land in the same low band (under ~25%) regardless of subject, source quality or effort spent. Two independent mechanisms produce it and both are structural: (1) claims the audited text leaves uncited are permanently `[ ]`, because only the original author can cite them and the framework's own rule is that true-and-uncited is `[ ]`; (2) every ARGUMENT and PROPOSITION fails Toulmin item 2, which requires each ground be `[x]` verified, because their grounds *are* those uncited claims. Measured on the worked case: 0 of 22 had fully verified grounds. If this holds, the project-level ruling that produced it (a DR titled *Coverage thresholds do not apply to a third-party audit*, held in the audit's own untracked project directory) generalises to a framework-level statement, and `docs/THRESHOLDS.md` needs an explicit scope note naming the self-authorship assumption it currently leaves unstated.

**Alternative:** A second third-party audit reaches materially higher coverage — say above 40% — because its subject cites its sources properly, so most CLAIMs close on the author's own citations and the ARGUMENT grounds verify in turn. In that case the ceiling is a function of *how well-sourced the audited text is*, not of third-party auditing as such, and the right fix is guidance about which documents are worth auditing rather than a threshold exemption. The 12% figure would then be evidence about one unusually uncited essay and nothing more.

**Method:** On the next third-party audit in this repo, record before drawing any conclusion: total units; fraction of CLAIMs the audited text cites at all; coverage at the point the audit is declared complete; and the count of ARGUMENTs/PROPOSITIONs with fully verified grounds. The last is the decisive one — if it is again 0, mechanism (2) is structural and the position holds even if mechanism (1) varies with subject. Compute it mechanically rather than by inspection; the worked case first produced a wrong ceiling estimate (~32%) from reasoning about the grounds instead of measuring them.

**Revisit trigger:** A second third-party audit completing in this repo; or any change relaxing Toulmin item 2 or adding an exception for true-but-uncited grounds, which would raise the ceiling substantially and is the single change with the largest effect on it.

**Review by:** 2027-08-16 — backstop. Expected to resolve whenever a second third-party audit runs; there is no reason to force one early.

**Origin:** A third-party audit of a published essay, run to completion in this repo on 2026-08-16. The audit is deliberately not tracked in git (see `.gitignore` — reviews of work this project did not author stay invisible, because the repo is public as a general tool), so this entry records the *structural* result without the subject. The ceiling was reached, not merely approached: after full source verification, cluster sourcing and the Toulmin/Whetten passes, no further unit could be marked `[x]` by the audit at all.

**Domain:** Coverage thresholds, third-party audit scope, Toulmin grounds constraint
**Status:** resolved — **SPLIT: headline prediction REFUTED, mechanism (2) HELD** (2026-08-16, same day as registration)

**Resolution [2026-08-16]:** The revisit trigger fired the same day. A **second third-party audit** completed in this repo — an unpublished quantitative note, subject withheld and directory untracked per the same rule as the first. Measured against the four items this entry's *Method* named, before drawing any conclusion:

| Method item | First audit | Second audit |
|---|---|---|
| Total units | 91 | 19 |
| Fraction of CLAIMs the text cites at all | low | **zero — the document cites nothing at all** |
| Coverage at completion | **12%** | **53%** (P0 36%, P1 83%, P2 50%) |
| ARGUMENTs/PROPOSITIONs with fully verified grounds | **0 of 22** | **0 of 6** |

**The headline prediction is refuted.** It said any future third-party audit here would land under ~25% *regardless of subject*. The second landed at 53%.

**Mechanism (1) is refuted, and in the strongest possible form.** It said claims the audited text leaves uncited are permanently `[ ]` because only the original author can cite them. The second document cites **nothing whatsoever** — no bibliography, no DOIs, not one reference — and 10 of its 13 CLAIMs still verified `[x]`. The mechanism assumed claims close by *citation*. These closed by *reproduction*: they were arithmetic, and arithmetic is fully available to a stranger.

**Mechanism (2) held, and is now the durable half.** 0 of 6 ARGUMENTs and PROPOSITIONs had fully verified grounds, against 0 of 22 in the first audit. Two audits, disjoint subject matter, disjoint evidence types, same result. This entry's *Method* nominated it as the decisive item in advance, and it survived.

**The registered Alternative was not refuted — it was never tested, and saying otherwise was sloppy.** It was a conditional: higher coverage arrives *because the subject cites its sources properly*. The second document cites nothing whatsoever, so the antecedent never obtained, and falsifying an antecedent does not refute a conditional. What the second audit does show is that its *implied mechanism* — sourcing quality as the governing variable — is not the whole story, since high coverage arrived with no sourcing at all. The Alternative remains open and is still the branch that would separate "well-sourced text → high coverage" from the closure-type account below. Neither branch anticipated the variable that actually governs:

> **The ceiling is set by whether a claim can be closed without the author — not by third-party status, and not by how well-sourced the text is.** Citation-bound claims put the evidence in the author's hands and cap out. Calculation-bound claims can be reproduced by anyone and do not. Interpretive units (ARGUMENT, PROPOSITION) rest on the other units and inherit whatever ceiling those have, which is why their coverage was 0% in both audits even though the CLAIM halves differed by a factor of four.

**What this means for `docs/THRESHOLDS.md`.** This entry proposed a scope note naming the self-authorship assumption. That is still warranted but must say something different from what was drafted: the exemption is not "third-party audits get a lower bar" but "**coverage is only comparable between projects whose claims close the same way**". A scope note to that effect has been added; it is registered at EMERGING (n=2) and points here.

**Superseded by** the successor entry registered in *Open* the same day, which carries the surviving half as a falsifiable claim in its own right.

⚠ **Registration and resolution happened in the same session, and this is now the pattern rather than the exception.** The bet was committed at 14:05:07 and the second audit's earliest artefact is timestamped 14:14:33, so the Method genuinely predates the evidence — but by nine minutes, not by a period in which anything could have been forgotten. **Both** resolved entries in this log resolved on the day they were registered. A log in which registration and resolution are never separated is recording reasoning, not testing prediction; the two successor entries below are the first with a real interval ahead of them, and that is the property to protect.

**Do not cite the 12% figure as a general third-party ceiling.** It is one measurement on one citation-bound essay, and the contrast case is now on record.


### [2026-06-12] A lightweight profile of the framework earns its cost on a technical syllabus (dsp-workshop pilot) — HELD

**Position (provisional):** Applying a lightweight profile of the framework — `agents/equation-checker.md` pass, per-page claim-registry draft, anti-hallucination citation verification — to one full-stack page of a technical teaching syllabus surfaces **≥1 load-bearing finding that the project's existing QA did not catch**, at a total measured cost not exceeding one paper-scale DR-011 intra-family battery (~170K tokens, the 2026-06-11 Pass 1 + Pass 2 sum from `vv/cost-log.md`). Pilot target: `dsp-workshop/topics/adaptive-filtering` (Quarto DSP teaching site, agent-ready-projects v1.10.0 adopter) — a 201-line theory page with ~4 display equations and 3 citations, plus `adaptive.py` with 14 pytest tests and an `embedded.qmd` companion. Existing QA there = the pytest suite + the project's persona-review skill (student / self-learner / practitioner / instructor perspectives). Per the registered-hypothesis discipline (weakest informative form, promoted 2026-06-11), this does **not** claim the full apparatus applies to teaching content — only that the framework's portable verification surface pays for itself on one page.

**Alternative:** The pilot yields zero load-bearing findings beyond what pytest and persona-review already cover (findings are stylistic-only or empty), OR total cost exceeds the ~170K-token bound. In that case the framework's correct relationship to teaching knowledge bases is **borrowing without adoption** — the portable prompts as standalone artefacts, no registry, no gates — and the README's *When It Is Overkill* boundary gains its first empirical content-type data point ("technical syllabi whose claims are verified by executable code"). No content-type DR is warranted on that outcome.

**Method:** Run on `C:/local_dev/dsp-workshop/topics/adaptive-filtering`, bracketed with `/status` snapshots, logged in `vv/cost-log.md`:

1. *Equation-checker pass* — `agents/equation-checker.md` on `index.qmd` + `embedded.qmd` (mechanical reproduction, not plausibility assessment, per the 2026-03-06 promoted rule).
2. *Per-page claim-registry draft* — type each load-bearing statement (CLAIM / ARGUMENT / candidate-PROCEDURE); record what fraction the current registry shape expresses without extension.
3. *Citation verification* — the page's 3 bib entries (`haykin2002adaptive`, `widrow1960adaptive`, `heiligenberg1991neural`) per the 6-step checklist.

Primary criterion: ≥1 load-bearing finding missed by existing QA AND cost ≤ bound. Position fails on either.

Secondary signals tracked but **not** falsifying: (a) ≥3 PROCEDURE-shaped registry rows → case for activating DR-004's reserved PROCEDURE slot via a new DR (DR-010 is the activation precedent); (b) whether "verification = named test file passes" fits the typed-verification model without shape extension — the syllabus's dominant verification mode, untested by any paper project; (c) tier-language register fit across the site's pedagogical (basics) vs. research-flavoured (topics) registers. These inform the DR-or-not decision after the pilot; the bet resolves on the primary criterion alone.

**Origin:** Surfaced 2026-06-12 in conversation: user proposed dsp-workshop as a worked example of the method on a technical syllabus, with explicit necessary-not-sufficient framing — self-adoption cannot evidence external adoptability (same limitation as Paper 1; the external-adopter gap is tracked separately in the recruitment open question), but a maintainer who does not adopt his own framework cannot ask others to. Pilot-before-DR shape chosen per DR-010 precedent. Candidate pages assessed against the full-stack requirement (equations + module + tests + embedded page + citations): biquad (no tests, 1 citation), ppg (no Python module), adaptive-filtering (complete) — selected. `memory/dead-ends.md` checked: no prior teaching-content conclusion exists.

**Domain:** Content-type boundary, teaching-KB generalisation, verification-by-execution, reserved PROCEDURE slot
**Status:** resolved — HELD (2026-06-12, same session as registration)

**Resolution [2026-06-12]:** Position **HOLDS** on the primary criterion (both legs).

- *≥1 load-bearing finding missed by existing QA* — YES. The equation-checker (run as an independent subagent with `agents/equation-checker.md` as its full instruction set) surfaced a hard arithmetic error in `embedded.qmd`: the STM32F4 performance-budget table claimed "21 000 cycles" available per sample at 180 MHz / 8 kHz, where 180e6 ÷ 8000 = **22 500**. The row was internally self-contradictory — 21 000 cycles at 180 MHz = 116.7 µs, but the same row stated 125 µs (the 22 500 / 125 µs pair is the consistent one). Independently reproduced before trusting the agent, per the 2026-03-06 "reproduce, don't assess" rule. This is a genuine correctness defect in a student-facing table, and **structurally invisible to the project's existing QA**: pytest exercises `adaptive.py`, not the hand-authored numbers in `.qmd` prose tables; the persona-review skill is qualitative, not arithmetic. Three further findings: an `$O(N)$ → $O(\log N)$ per tap` complexity mislabel (correct normaliser is per-sample; per tap LMS is O(1)); a `BFDAF`/`FDBAF` acronym transposition; and a soft `hundreds of taps` vs `400–2400 taps` internal tension. 23/28 checks passed — the page is overwhelmingly correct, which is the honest framing, not "riddled with errors."
- *Cost ≤ ~170K-token bound* — YES, with wide margin. Equation-check subagent: **35,364 tokens** (~21% of the bound). Logged in `vv/cost-log.md`.

**Honesty caveat on "load-bearing":** the headline cycle-count error's *conclusion* survives (utilisation is ~0.9% either way, so "~1%, ample headroom" still holds) — its blast radius is one wrong number a student might copy, not a wrong takeaway. The `per tap` complexity mislabel is arguably the more pedagogically load-bearing finding (it misstates an algorithmic order a student is meant to learn). Either clears the "not stylistic" bar; together they clear it comfortably. The three correctness defects (cycle count, per-tap label, FDBAF typo) were fixed in dsp-workshop the same session; the `hundreds of taps` tension was surfaced to the maintainer as a framing judgement, not auto-edited.

**Secondary signals observed (non-falsifying, inform the DR-or-not call):** (a) **positive** — the page yields ≥2 PROCEDURE-shaped units (two numbered hardware-setup recipes + a bill-of-materials in `embedded.qmd`), a real case for activating DR-004's reserved PROCEDURE slot; across the full site (114 exercises, embedded setup recipes) the threshold of ≥3 is comfortably met. (b) **Verification-by-execution** — the dominant mode for the Python claims is "the named pytest file passes," which the typed-verification model accommodates as a source/verification entry without shape change; no extension needed at N=1. (c) **Tier-language register** — not exercised this pilot (single research-flavoured Topics page; the basics/topics two-register test needs a basics chapter in scope).

**Consequence:** Borrowing route is justified now — `agents/equation-checker.md` + the anti-hallucination citation checklist earn their place in dsp-workshop. The reserved-PROCEDURE-slot activation case (secondary signal a) is the candidate for a follow-up DR (DR-016-shaped, DR-010 as precedent) **if** the maintainer wants dsp-workshop to be a formal content-type adopter rather than a borrower — that decision is open and not forced by this pilot. The bet was deliberately the weak form (one page pays for itself); that is what was tested and that is what held. It does **not** evidence external adoptability — same necessary-not-sufficient limitation stated at registration.
