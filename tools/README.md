# tools/

Registry-verification tooling for agent-ready-papers. Closes [#17](https://github.com/ducroq/agent-ready-papers/issues/17).

Two tools, both stdlib-only, both deterministic, both designed to run in CI:

| Tool | Purpose |
|------|---------|
| `coverage.py` | Parse per-type sub-tables in a claim registry; report P0/P1/P2 coverage. |
| `check_dois.py` | Extract DOI patterns from a registry; verify each resolves via `https://doi.org/`. |

## Status

**Implemented and tested.** Both parsers landed and verified against the Paper 1 fixture (19 entries, 9 DOIs); pytest suite is green; live HEAD-against-`doi.org` confirms all 9 DOIs resolve. Two DR-011 review batteries applied (one for the scaffold, one for the parser). Closes [#17](https://github.com/ducroq/agent-ready-papers/issues/17).

## Usage (once parsing lands)

```bash
# Markdown report to stdout
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md

# JSON for CI consumption
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md --json
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md --json

# CI-friendly: exit 1 if a configured target is missed
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md --strict

# Offline DOI parse-check (no network)
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md --offline
```

Or via the project Makefile:

```bash
make coverage      # report against Paper 1
make check-dois    # DOI verification against Paper 1
make check         # lint + tests
```

## Exit codes

The two tools share a code-space (0 / 1 / 2 = success / failure / tooling error) but **default behavior differs**: `coverage.py` only fails the build under `--strict`; `check_dois.py` fails by default whenever a DOI does not resolve. The asymmetry is intentional — coverage targets are policy-configurable and may legitimately be missed mid-draft, while a DOI that fails to resolve is unambiguous.

| Code | `coverage.py` | `check_dois.py` |
|------|---------------|-----------------|
| 0 | Report emitted (always, unless `--strict` and a target was missed) | All DOIs resolved (or, with `--offline`, all DOIs parseable) |
| 1 | `--strict` and at least one target missed | At least one DOI failed to resolve (or, with `--offline`, failed to parse) |
| 2 | Tooling error (file missing, parse failure) | Tooling error (file missing, parse failure) |

**`--offline` note (check_dois only).** Offline mode does *not* mark DOIs as resolved. It checks parseability only and gates exit on `all_parseable` instead of `all_resolved`. A stderr banner makes the mode explicit so a CI gate over `all_resolved` cannot silently pass if the flag is inherited unintentionally.

## Known limits

Documented here so adopters hit informed surfaces rather than silent miscounts. None are blockers for the current Paper 1 fixture or the canonical templates; each is captured for the next adopter.

- ~~**Escaped pipes in cells (`\|`) are not supported.**~~ **Fixed 2026-06-12.** `_split_row` in `coverage.py` now honors backslash-escaped pipes (`\|`) — common in magnitude notation like `|H(z)|` — restoring them as literal `|` in the cell value instead of splitting the row into spurious columns. Regression tests in `tests/test_coverage.py` (`test_split_row_honors_escaped_pipes`, `test_parse_registry_counts_correctly_with_escaped_pipes`). Surfaced by dog-fooding the tool on the math-heavy dsp-workshop z-domain registry, where the old behavior silently miscounted coverage (read 5/7 where the data was 8/8).
- **No HTTP proxy support.** `check_dois.py` uses `http.client.HTTPSConnection` directly and does not honor `https_proxy` / `HTTPS_PROXY`. This is fine for CI runners and most direct connections; fails opaquely for adopters behind a corporate proxy. If this matters, switch the HEAD path to `urllib.request` (which respects proxy env vars).
- **Sequential, single-retry HTTP.** No concurrency, no backoff. ≤20 DOIs runs in single-digit seconds; ~50 DOIs takes ~30s; 200+ DOIs becomes minute-scale. Concurrency is a follow-up, not a current need.
- **Marker recognition is line-anchored.** `_MARKER_REGEX` requires the sub-table marker on its own line. A heading-form marker like `### **CLAIMs:**` is silently skipped. Keep markers on their own line per the templates.
- **`_clean_doi` is heuristic.** For DOIs whose authoritative form ends with unbalanced punctuation (vanishingly rare in real Crossref data), the cleaner may strip too much. Run a spot-check against the publisher's canonical citation if a DOI fails to resolve unexpectedly.

## Design constraints

- **Stdlib only.** No `requests`, no third-party YAML / Markdown libs. Keeps the toolchain trivial to install and free to vendor.
- **Deterministic.** Same registry input → byte-identical report. Result types use `frozen=True` dataclasses; ordering is stable.
- **No LLM step.** Registry format is author-controlled markdown; a regex parser suffices. (Pattern borrowed from `vmodel.eu` ADR-016 floor-check discipline.)
- **Importable and runnable.** Both modules expose a `check_*` function in addition to the CLI, so tests can call them directly.

## File-naming note

The issue title uses `check-dois.py` (hyphenated). The actual file is `check_dois.py` (underscored) so Python can import it as `tools.check_dois`. The CLI is invoked via `python -m tools.check_dois` either way.

## Licensing

Tools live inside the agent-ready-papers repo and inherit its licence (CC BY 4.0). If `tools/` grows substantially, [DR-013](../decisions/DR-013_licensing.md) carries a "Revisit If" condition for re-examining a dual CC BY 4.0 + MIT split.

## Roadmap (post-scaffold)

1. Implement `coverage.py` sub-table parser. Tests against `papers/perspective/vv/claims/claim_registry.md` (19 entries, 100% verified — known-good fixture).
2. Implement `check_dois.py` extractor + resolver. Tests against the same fixture; offline mode verified against a hand-curated DOI/non-DOI fixture file.
3. PROVOCATION axis support in `coverage.py` (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL — see [DR-010](../decisions/DR-010_provocation-unit-type.md) and [DR-014](../decisions/DR-014_provocation-layered-as-opt-in-extension.md)).
4. Add `tools/` to repo CI once a real fixture suite exists.
