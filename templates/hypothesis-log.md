# Hypothesis Log

<!-- SAVE AS: <paper-or-project-root>/hypothesis-log.md
              (or memory/hypothesis-log.md if you keep maintainer-local positions separate)

     Adapted from agent-ready-projects v1.10.0 templates/hypothesis-log.md.

     Flavored for paper-writing and structured non-fiction work: bets
     about review outcomes, verification predictions, calibration of
     speculative claims (PROVOCATION tier), pre-registered forecasts
     about the next round of evidence.

     The hypothesis log captures provisional positions whose evidence
     lives in the future. It complements the gotcha log (problems
     encountered & solved) and decision records (positions accepted,
     with rationale frozen) by giving a home to bets you've placed
     but haven't yet resolved.

     Why this matters for verification work: the falsification criterion
     is pinned BEFORE the data lands, which protects against post-hoc
     rationalization — the same failure mode the framework guards against
     in tier-monotonicity and anti-hallucination. -->

Provisional design and verification positions under observation. Each entry is a bet taken where the evidence to confirm or revise it lives in the future. Different from:

- **TODO / GitHub Issues** — tasks with an owner, ready to execute
- **`decisions/DR-*.md`** — positions accepted, with rationale frozen
- **`memory/gotcha-log.md`** — problems encountered & solved
- **`memory/dead-ends.md`** — pattern proposals concluded as don't-retry

Lifecycle: **open** → dormant → revisit (with evidence) → resolved (close or promote to DR).

**How to use this file:**

- Add an entry when you take a provisional position you want to revisit later — especially for predictions about verification outcomes, review findings, or model-behavior bets.
- Each entry has a `Review by:` date and a `Revisit trigger:` so the agent can surface due items at session start and in `/curate`.
- The **Method** field pins the falsification criterion *before* the data lands — that's the whole point. Don't loosen Method when the answer arrives; if you want to redefine the bet, open a new entry.
- When an entry resolves, move it to `## Resolved` with a one-line outcome. If the resolution justifies a decision record, promote to `decisions/DR-XXX.md` and link it.
- Keep entries tight. If an entry grows a plan, it becomes a TODO; if it grows a rationale, it becomes a DR.

## Entry template

```markdown
### [YYYY-MM-DD] One-sentence position

**Position (provisional):** What you're betting on, with concrete forecasts (numbers, ranges, dates). Cite the evidence that motivates the bet.

**Alternative:** The failure mode you'd see if the position is wrong, with a *signal* — not just "it could fail." A useful Alternative tells future-you exactly what observation would refute the Position.

**Method:** How you'll test it later. Pre-commit the falsification criterion. Often a checklist of observations to compare against the forecasts in Position. For verification work, name the specific procedure: which review pass, which audit, which DOI check, which calculation step.

**Revisit trigger:** What event causes the entry to become reviewable. Prefer evidence triggers ("once Pass 3 lands on Paper 1") over calendar triggers when the data drives the decision.

**Review by:** YYYY-MM-DD — backstop date. The agent flags entries past this in `/curate`.

**Domain:** Tags for filtering (e.g. "DR-011 review patterns", "PROVOCATION layering", "Paper 1 verification")
**Status:** open | open (low priority) | open (blocked on X) | dormant
```

## Open

*(populate with project-specific entries)*

## Resolved

### [YYYY-MM-DD] Example: position one-liner

**Outcome:** One-line result. Confirmed / refuted / nuanced (with a brief why). Link to the DR or commit if the resolution produced one.

---

## Worked examples — paper-writing flavor

These illustrate what a useful entry looks like in this domain. Delete this section when you populate your own log.

### [2026-06-01] DR-011 cross-family generality holds at paper scale

**Position (provisional):** The disjoint-coverage prediction between Pass 1 (intra-family small) and Pass 2 (intra-family large) replicates at paper scale (Paper 1) and *also* cross-family (Pass 3 cross-vendor finds ≥1 load-bearing item that neither intra-family pass found). N=2 within-Claude at code-tooling scale (2026-06-08); cross-family untested.

**Alternative:** Pass 3 finds zero load-bearing items beyond what Pass 1+2 caught, OR cross-family finds duplicates of intra-family findings rather than independent ones. Either would suggest cross-family pass is ceremony, not bias-escape.

**Method:** When Paper 1 reaches a Pass-3 trigger, run Pass 3 with the documented cross-vendor style/voice filter. Classify each finding as: (a) duplicate of Pass 1/2 finding, (b) load-bearing new, (c) noise. Compare *load-bearing new* count to the in-DR forecast.

**Revisit trigger:** Paper 1 Gate 3 produces a Pass-3 trigger AND user picks up the Paper 1 paper-writing track (currently deferred — see MEMORY.md *Direction 2026-06-09*).

**Review by:** 2027-01-01 — backstop only; expected to resolve before.

**Domain:** DR-011 evidence base, multi-model review pattern
**Status:** open (blocked on Paper 1 paper-writing track resumption)

### [2026-06-08] PROVOCATION-as-extension can ship without parser changes

**Position (provisional):** DR-014's "PROVOCATION layered as opt-in extension" can land as a templates-only restructure without changes to `tools/coverage.py`. The Pass 2 regression test from v1.6.0 (PROVOCATION column substring-match catch) demonstrates the parser already handles per-type sub-tables correctly.

**Alternative:** Restructuring templates surfaces a parser path that wasn't exercised by Paper 1's registry, requiring a tools/ update. Signal: `make coverage` against Paper 1's registry returns different numbers after the restructure than before.

**Method:** Run `make coverage` against Paper 1 BEFORE the restructure. Apply restructure. Run `make coverage` AFTER. If output is byte-identical, position confirmed. If different, examine the delta and decide whether to patch the parser or revise the restructure.

**Revisit trigger:** User picks up #18 / DR-014 promotion thread.

**Review by:** 2026-12-31

**Domain:** DR-014, PROVOCATION layering, tools/
**Status:** open (blocked on #18 pickup)
