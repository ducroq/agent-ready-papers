# Upgrading

If your paper project pins a specific version of `agent-ready-papers` (e.g. `agent-ready-papers: v1.2.0` in your project's `CLAUDE.md`), this document tells you what changed in each subsequent release and what action — if any — is required when you bump your pin.

The full release notes are in [`CHANGELOG.md`](CHANGELOG.md). This file is the quick-lookup adopter view. **Pinned before v4.0.0?** Start in [`UPGRADING-archive.md`](UPGRADING-archive.md) with the release after your pin and continue through v3.0.0, then read v4.0.0 onward here. Both files list the newest release first, so work through the sections bottom to top: oldest unread release first, newest last.

## Convention

- **MAJOR** version bumps signal breaking changes to template surfaces or DR semantics. Adopters should expect to review.
- **MINOR** version bumps add templates, patterns, application classes, or behaviours. Adoption of the new additions is typically opt-in.
- **PATCH** version bumps are docs-only / clarifications, or backward-compatible bug fixes (e.g. a tooling fix that changes no public interface). Usually no action required; a bug fix may be worth adopting if you hit the bug.
- Every release entry in `CHANGELOG.md` includes an "Adopter notes" / "Adopter action" subsection. This file aggregates them per version for quick lookup.

## v4.2.0 (2026-10-02)

**From v4.1.0 — what to review when you bump your pin to v4.2.0:**

| Change | Adopter action |
|--------|-----------------|
| **`templates/anti-hallucination.md` — Step Z's scope names surfaces** (DR-019, now Accepted) | **Optional.** Step Z now also covers a project's own methodology prose (docs, decision records, `CLAUDE.md`, changelog rationale). It sets no cadence and no standing sweep. To take it in a paper-local copy, replace the italic scope line under *Step Z* with the template's; don't re-copy over an adapted file. A current copy contains `and to every surface that states claims`. |
| `decisions/DR-019` Accepted; DR-020 stays Proposed | None beyond the row above. Proposed DRs do not bind. |
| `scripts/` (`make check-counts`, `make read-surface`, `make check-profile`) | None. They read this repo's own layout, not yours. |
| Release history split: v3.0.0 and earlier in `CHANGELOG-archive.md` and `UPGRADING-archive.md` | None. If you were pinned before v4.0.0, start in the archive. |

**Breaking changes:** none.

## v4.1.0 (2026-09-30)

**From v4.0.0 — what to review when you bump your pin to v4.1.0:**

| Change | Adopter action |
|--------|-----------------|
| **New: `templates/readability.md`** | **Optional.** Two prompts against hard-to-read AI prose, *Explain like I'm 18* and *Write for a reader*. Copy it into your paper project if your prose or your reports read as compressed. Its tier guard keeps each claim at its registry tier. |
| `templates/CLAUDE.md` — one tree line for `readability.md` | None. Add the line only if you copy the template. |
| `templates/hypothesis-log.md` — resolved entries may move to a separate file | None. Optional; the `## Resolved` section still works as before. Your log is a journal: never re-copy the template over it. |
| `decisions/DR-022`, `DR-023` (both **Proposed**) | None — Proposed DRs do not bind. DR-022 records the decision to keep AI-text detectors out of every gate. |
| `extensions/` — `formula_scan.py`, `formula-review.md`, `effect-profiles.md` (DR-022); `preservation_check.py`, `translation-prompts.md` (DR-023) | None. Staged, not accepted. Try them if you like; they report and never gate. |
| README — *Will an AI-text detector flag my paper?* | None. Reference only. |
| `scripts/` (`make drift`, `make dr-status`, `make gotcha-stats`) | None. They read this repo's own layout, not yours. |

**Breaking changes:** none.

## v4.0.0 (2026-09-26)

**From v3.0.0 — what to review when you bump your pin to v4.0.0:**

| Change | Adopter action |
|--------|-----------------|
| `tools/coverage.py` — **`--strict` enforces the DR-002 P0 tier floor** | **Required if you run `coverage --strict` in CI — it can now go red with no change on your side.** Every P0 entry must be SUPPORTED or ESTABLISHED; DR-002 always said so, and nothing checked it. Run `python -m tools.coverage <registry.md>` and read the `P0 tier floor` line under the table: it names every failing ID. Remedies are stronger sources, re-prioritisation, or an explicit decision record. A P0 row with an empty or missing Confidence cell **fails** the floor. |
| `tools/coverage.py` — **fails closed on a registry it cannot read (exit 2, with or without `--strict`)** | **Required if yours hits one — the error names the line.** Now errors: a row with more cells than its header (escape `\|`, including inside backticks); a sub-table marker followed by prose, end of file, or a table with no Priority/Status column; a file with no recognised sub-table marker; a row with content but a blank Priority. Every one of these was previously a silent miscount. A one-cell section divider (`\| **PART TWO** \|`) still passes, but a divider with a second cell, or a totals row inside a marked sub-table, now exits 2 — move totals outside the marked table. A freshly started registry (recognised markers over empty tables) reports zero rows cleanly, in `check_registry` too. |
| `tools/coverage.py` — blank Status counts as unverified; unknown Priority values fail | **Check your numbers.** A blank Status cell used to remove the row from the denominator, so your coverage may drop. A Priority that is not P0/P1/P2 (`-`, `TBD`) now fails `meets_targets` (`NO — not a priority`); `p0` and `**P0**` now count as P0. Custom `priority_targets` passed through the API are unaffected. |
| **New: `tools/check_metadata.py`** (`make verify-bib`) | **Optional, recommended.** Compares citation fields — title, authors, year, venue — against Crossref/DataCite. A DOI that resolves can still carry the wrong metadata; `check_dois.py` cannot see that. |
| **New: `tools/check_registry.py`** (`make check-registry`) | **Optional.** Registry/manuscript consistency: anchors, tier agreement across copies, type-conditional schema, premise graph, word budget. To use the `tiers` check, write anchors as `% S1-1: label (TYPE, P0, TIER)`; an anchor without the tier is a note, not a failure. Checks consistency, never whether a tier is right. |
| `agents/equation-checker.md` — derived op-counts reproduced from the procedure ([#32](https://github.com/ducroq/agent-ready-papers/issues/32)) | **Optional.** For an adapted copy, add the Rule beginning `Reproduce op-counts, complexity and budgets from the procedure`, the Step 3 bullet beginning `For a derived operation-count`, and the `FORMULA` row's clause `or counts work the described procedure does not perform`. |
| `templates/CLAUDE.md` — pin is "a number, not a status"; *Before committing* row | None required. If you copy the new row, it points at `/review-changes` or its paste-in prompt. |
| `templates/vv-framework.md`, `templates/claim-registry.md` — comment and note wording | None. They now describe the tools accurately (coverage reads Confidence for the P0 floor only; prose after a marker is an error). |
| `decisions/DR-020`, `DR-021` (both **Proposed**) | None — Proposed DRs do not bind. |

**Breaking changes:** two, both in `tools/coverage.py` and both listed above as *Required* — the P0 tier floor under `--strict`, and exit 2 on an unreadable registry. Neither removes an artifact or changes a template's required structure; each makes a check that used to pass over a non-compliant or miscounted registry report it.

## When new versions land

This file is updated as part of each release. The maintainer release process (the header comment of [`CHANGELOG.md`](CHANGELOG.md)) includes refreshing this file alongside the CHANGELOG entry. If you find this file out of date relative to `CHANGELOG.md`, that is a bug — please open an issue.

Convention for new releases: each `CHANGELOG.md` entry's "Adopter notes" or "Adopter action" content gets distilled into a table row here, paired with the *from-version* it applies from. Pinned consumers read every release after their pin, oldest first, to know exactly what to review. To preview an upgrade: `git checkout vX.Y.Z` inspects a pinned version, and `git diff vX.Y.Z..vA.B.C -- templates/` shows what changed in the templates.
