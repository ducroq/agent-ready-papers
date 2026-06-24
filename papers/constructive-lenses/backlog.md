# Constructive Lenses — Backlog

Last updated: 2026-06-24 (scaffolded)

**Phase:** 0 — Framing

## Phase 0 — Framing (author-led; do these before any prose)

- [ ] **Pin the angle + paper type.** Design-science (artefact + evaluation), perspective, or case study? This shapes the registry's unit-type mix and the venue. **Author's call.**
- [ ] **Pin the target venue + read its author guidelines.** Candidates: *Digital Journalism*, *Journalism Studies*, *AI & Society*, *Journalism Practice*. Note word/page budget → record as the first DR.
- [ ] **Decide the contribution sentence.** Is the contribution (a) the existence proof, (b) the Vrijenhoek-style evaluation of ovr.news's diversity, (c) the open-infrastructure-gap argument, or (d) the Han boundary analysis — or a weighted combination? One primary, the rest supporting.
- [ ] Draft a one-page outline; map the seven seed claims onto sections; identify what's missing.

## Phase 1 — Literature audit (the ovr.news [2026-05-27] reading list)

> Reading stubs are seeded at `../../literature/sources/` (L49–L55), each with status + what-to-extract + the claim ID it maps to. Read into the stub, then promote the take into the claim registry.

- [ ] Read **Vrijenhoek et al. 2021** (CHIIR) — highest payoff; extract the diversity metric(s) + their **required inputs**, check inputs against the ovr.news DB schema, decide the computable-score bet. Update S2-2. → `vrijenhoek-2021.md`
- [ ] Read **Anderson, Bell & Shirky 2012** (Tow) — post-industrial scaffold. → `anderson-bell-shirky-2012.md`
- [ ] Read **Simon 2024** (Tow) — contemporary AI-in-newsrooms map placement. → `simon-2024.md`
- [ ] Confirm **Helberger 2024** notes are sufficient or re-read for citable specifics (S2-1). → `helberger-2024.md`
- [ ] Decide the **Han** treatment: weight + placement (boundary condition vs framing); **disambiguate L54 vs L55** (which Han work). Draft paragraph in ovr.news `memory/project_session_2026_06_17_chain_latency_step2.md` (Addendum). → `han-2024-narration.md`, `han-2022-infocracy.md`
- [ ] **Go/no-go on the lineage** (the ovr.news counter-hypothesis): do the three papers surface a *concrete* unlock — a metric, frame, or compliance hook the paper needs — or is this decorative? If decorative, narrow the contribution to the evaluation + existence proof.

## Phase 2 — Verification (before any confident prose)

- [ ] Verify **every** `references.bib` entry (DOI / Scholar). Currently all UNVERIFIED. Run `python -m tools.check_dois`.
- [ ] Reproduce the ovr.news own-data numbers (S3-1) with a dated query against the live DB — not from PROPOSITION.md prose.
- [ ] Confirm the honest adoption framing: HuggingFace downloads are not disaggregable (PROPOSITION.md) → keep EMERGING.

## Parking lot

- [ ] Whether to compute an actual Vrijenhoek-style diversity score on a real ovr.news daily snapshot (turns the paper from perspective → design-science with evaluation; bigger but stronger). Decide after reading Vrijenhoek.
- [ ] Figure: the five-layer pipeline (FluxusSource → distilled scorers → NexusMind → reader site) — reuse PROPOSITION.md table.

## Notes

- **No deadline pressure.** This work is *not* gated by ovr.news's readiness gate or its `feedback_no_outbound_before_audience` rule — reading and citation are allowed; only author *outreach* is gated.
- ovr.news is the **case**; cite it as own-work/own-data. The SE-with-AI angle is a *separate* paper (`ducroq/augmented-engineering`) — do not merge.
- Session narratives + gotchas → shared `../../memory/`, not user-level auto-memory.
