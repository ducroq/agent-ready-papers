# Hypothesis Log — resolved entries

Resolved entries moved here from `vv/hypothesis-log.md` on 2026-09-30, word for word, so the open log stays short. New resolutions go here too, newest first. Where the moved text points to *Open* or to "successor entries", those are the open entries in [`hypothesis-log.md`](hypothesis-log.md).

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
