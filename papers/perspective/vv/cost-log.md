# Operation Cost Log

**Paper:** The Verification Gap (Paper 1)
**Started logging:** 2026-06-08

Convention: see [`templates/cost-log.md`](../../../templates/cost-log.md) for column semantics and what's worth logging.

## Log

| Date | Operation | Total tokens | Input Δ | Output Δ | Cache read | Wall clock | Notes |
|------|-----------|--------------|---------|----------|------------|------------|-------|
| 2026-06-08 | DR-011 Pass 1 (Haiku) on `tools/` scaffolding stage | 31,821 | — | — | — | 41s | 0 concrete bugs surfaced. False positive on the Lancet DOI regex (claimed `10.1016/S0140-6736(13)62228-X` would match — regex actually excluded `)` and stopped at `S0140-6736(13`). Caught by pytest 0.04s after parser landed. |
| 2026-06-08 | DR-011 Pass 2 (Opus) on `tools/` scaffolding stage | 60,799 | — | — | — | 74s | Caught 5 medium+ design issues including the load-bearing `bucket: str` axis conflation (priority vs PROVOCATION tier) that would have silently mis-modelled PROVOCATION when DR-014 lands. Also surfaced `types=` filter omission, offline-mode silent-pass, asymmetric exit-code policy, missing `tests/` skeleton. |
| 2026-06-08 | DR-011 Pass 1 (Haiku) on `tools/` parser implementation | 41,803 | — | — | — | 62s | 0 concrete bugs after a careful character-by-character regex trace of all 4 marker forms + all 9 fixture DOIs + `_clean_doi` paren-balancing + HTTP client semantics. Visibly more careful than the scaffold-stage Pass 1 (the prior false positive may have prompted caution — N=1 datapoint). |
| 2026-06-08 | DR-011 Pass 2 (Opus) on `tools/` parser implementation | 44,281 | — | — | — | 54s | Caught 1 load-bearing forward-looking bug (PROVOCATION column substring-match `"tier" in name.lower()` would silently false-match `Source Tier`). 7 follow-up items (escaped pipes, no proxy support, retry policy, audit trail, helper test seam, determinism pin, DR-013 size check — confirmed sub-threshold). |

## Aggregation (N=2 per pass-type)

| Operation type | N | Mean total tokens | Load-bearing findings (would have shipped broken) | Other findings | Notes |
|----------------|---|-------------------|---------------------------------------------------|----------------|-------|
| DR-011 Pass 1 (Haiku) | 2 | 36,812 | 0 / 2 rounds | 0 (1 false positive round 1, 0 round 2) | At code-tooling scale, value approaching zero. Pass 1 caught only what tests / smoke runs would also catch. |
| DR-011 Pass 2 (Opus) | 2 | 52,540 | 2 / 2 rounds (1 per round) | 13 medium/low across both rounds (mostly structural improvements + documentation gaps) | ~1.4× Pass 1 cost. Both rounds surfaced design issues that the fixture-based test suite could not exercise. Strong cost-vs-value at code-tooling scale. |

## Caveats

- **Subagent tool results report `total_tokens` only.** Input / output / cache breakdown is not surfaced at the Agent-tool granularity, so the Δ columns are intentionally blank. If a future Pass is run via direct API or interactive `/status`, populate the Δ columns.
- **Code-tooling scope, not prose.** Both data points are reviews of `tools/coverage.py` + `tools/check_dois.py` (~620 LOC of Python). Paper-prose-scale Pass 2 cost is still unmeasured. The DR-011 "every major revision" default may need recalibration when an ~8,000-word manuscript revision produces data.
- **"Would have shipped broken" definition.** Counts an issue as load-bearing only if the test suite at HEAD did not catch it and the fix changed behaviour (not just docs). Discounts soft findings like documentation gaps and follow-up improvements.

## Forward-looking entries to gather

- DR-011 Pass 2 on a manuscript revision (paper-prose scale, not code).
- DR-011 Pass 3 (cross-vendor) on any artefact — no Paper 1 data point exists yet; the DR's "high-stakes only" prescription remains untested at paper scale.
- `/curate` and `/audit-context` skill invocations — both are routine but uncosted.
- Full Gate 2 sweep (manual run through registry + writing-guide + anti-hallucination + review prompt).
