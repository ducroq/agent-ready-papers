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

### [2026-06-24] The Helberger/Vrijenhoek/Anderson-Bell-Shirky/Simon cluster supports a coherent contribution — not decoration

**Position (provisional):** Reading the three unread cluster papers (Vrijenhoek 2021, Anderson–Bell–Shirky 2012, Simon 2024), on top of Helberger 2024 already read, yields a *concrete* unlock the paper needs — at minimum a normative diversity metric (Vrijenhoek) computable against ovr.news's five-lens distribution, plus a governance frame (Helberger) that makes the open-build move significant. Carried over verbatim from ovr.news `docs/hypothesis-log.md` `[2026-05-27]`; this is its home now that the paper exists.

**Alternative:** The cluster is funder/aesthetic dressing — the contribution stands on the artefact + existence proof alone, and the academic framing adds citations without adding argument. Signal: after reading, no specific metric/frame/compliance-hook changes what the paper claims; the lineage paragraph could be deleted with no loss.

**Method:** After reading all three, classify the take from each as (a) load-bearing (a metric/frame/hook the contribution uses), (b) supporting context, or (c) decorative. If Vrijenhoek yields a computable diversity metric → strongest unlock (promotes the paper from perspective toward design-science-with-evaluation). If only (b)/(c) across all three → narrow the contribution to the evaluation + existence proof and cite the cluster lightly.

**Revisit trigger:** Three cluster papers read (Phase 1), OR a decision to pin the paper type in Phase 0 forces the call earlier.

**Review by:** 2026-09-30 (no pressure; reading-and-citation work, ungated).

**Domain:** contribution framing, literature audit, venue selection
**Status:** open — Phase 0/1. Helberger read 2026-05-27; three pending.

### [2026-06-24] A Vrijenhoek-style diversity score is computable on a real ovr.news daily snapshot

**Position (provisional):** ovr.news's five-lens output distribution + source attribution is rich enough to compute at least one of Vrijenhoek's normative diversity metrics on an actual daily snapshot, turning the paper from a perspective piece into a design-science contribution with an evaluation.

**Alternative:** The metrics require signals ovr.news doesn't capture (e.g. per-article viewpoint/stance labels, reader-personalisation traces) → the evaluation isn't runnable without new instrumentation, and the paper stays a perspective/case piece. Signal: reading Vrijenhoek reveals required inputs ovr.news's DB lacks.

**Method:** After reading Vrijenhoek, list the metric's required inputs; check each against the ovr.news DB schema. If all present → prototype the score on one dated snapshot. If not → record the gap and keep the paper at perspective scope (parking-lot item in backlog).

**Revisit trigger:** Vrijenhoek 2021 read.

**Review by:** 2026-09-30.

**Domain:** evaluation method, own-data, paper type
**Status:** open — blocked on the Vrijenhoek read.

## Resolved

*(none resolved yet)*
