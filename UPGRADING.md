# Upgrading

If your paper project pins a specific version of `agent-ready-papers` (e.g. `agent-ready-papers: v1.2.0` in your project's `CLAUDE.md`), this document tells you what changed in each subsequent release and what action — if any — is required when you bump your pin.

The full release notes are in [`CHANGELOG.md`](CHANGELOG.md). This file is the quick-lookup adopter view.

## Convention

- **MAJOR** version bumps signal breaking changes to template surfaces or DR semantics. Adopters should expect to review.
- **MINOR** version bumps add templates, patterns, application classes, or behaviours. Adoption of the new additions is typically opt-in.
- **PATCH** version bumps are docs-only / clarifications. No action required.
- Every release entry in `CHANGELOG.md` includes an "Adopter notes" / "Adopter action" subsection. This file aggregates them per version for quick lookup.

## v1.6.0 (2026-06-08)

**From v1.5.1 — what to review when you bump your pin to v1.6.0:**

| Change | Adopter action |
|--------|-----------------|
| New template `templates/cost-log.md` for operation token-cost logging | **Optional** — adopt if you want empirical cost data for framework operations. Copy to `vv/cost-log.md` in your paper project; log `/status` deltas after named operations (review passes, `/curate`, etc.). |
| `decisions/DR-011_multi-model-review-pattern.md` Evidence Base extended with N=2 token-cost replication (Pass 1 mean 36.8k tokens / 0 load-bearing findings; Pass 2 mean 52.5k tokens / 2 load-bearing findings) | Reference only — quantitative cost-per-Pass data added; Open Questions now names paper-scale cost-tier calibration as the next data point. If you've been applying DR-011, your own Pass 1/2 costs are now a meaningful contribution to N. |
| `templates/CLAUDE.md` + `papers/perspective/CLAUDE.md` — Before You Start row added pointing at `vv/cost-log.md` | Reference only — agent-orientation; mirror in your own paper project's CLAUDE.md if you adopt the cost-log convention. |

**No breaking changes.** MINOR release per SemVer: new opt-in template and convention, no existing template-surface changes.

## v1.5.1 (2026-06-08)

**From v1.5.0 — what to review when you bump your pin to v1.5.1:**

| Change | Adopter action |
|--------|-----------------|
| Root `CLAUDE.md` — architecture diagram + two new Before You Start rows (`tools/` for coverage/DOI checks, `docs/THRESHOLDS.md` for threshold rationale); How to Work Here now uses `python -m tools.coverage` instead of the stale "manual P0/P1/P2 count" comment | Reference only — agent-orientation fix in this repo. If you maintain your own paper project's `CLAUDE.md`, copy the pattern. |
| `papers/perspective/CLAUDE.md` — Before You Start row added pointing at tools with the correct registry path for Paper 1 | Reference only — Paper 1 self-application. |
| `templates/CLAUDE.md` — Before You Start row added with adopter-facing path placeholders | **Recommended** — new paper projects created from this template now point at the tools by default. Existing paper projects: add the equivalent row to your own CLAUDE.md. |

**No breaking changes.** PATCH release: discoverability only, no functional change.

## v1.5.0 (2026-06-08)

**From v1.4.0 — what to review when you bump your pin to v1.5.0:**

| Change | Adopter action |
|--------|-----------------|
| `tools/` directory added — two stdlib-only CLIs: `coverage.py` (registry coverage reporter) and `check_dois.py` (DOI resolver) | Optional — if you maintain a `claim_registry.md`, run `python -m tools.coverage <registry.md>` and `python -m tools.check_dois <registry.md>` from your own clone. No template changes. |
| `Makefile`, `pyproject.toml`, `.gitignore` Python patterns added | Reference only — first Python footprint in the repo. The `.gitignore` Python patterns may be useful if your paper project also runs Python tooling. |
| `tests/` directory added — shape-pin and edge-case tests against the Paper 1 fixture | Reference only — pattern source if you want to add tests against your own registry. |
| `tools/README.md` documents known limits (escaped pipes in cells, no HTTP proxy support, sequential HEAD scaling, line-anchored marker recognition) | **Read before adopting** if your registry uses escaped pipes, you sit behind a corporate HTTPS proxy, or your registry has >50 DOIs. |

**No breaking changes.** This is a MINOR release per the SemVer convention: new opt-in tooling, no template-surface changes.

## v1.4.0 (2026-06-08)

**From v1.3.0 — what to review when you bump your pin to v1.4.0:**

| Change | Adopter action |
|--------|-----------------|
| `LICENSE` file added (CC BY 4.0 per [DR-013](decisions/DR-013_license-choice.md)) | Reference only — formalises licence terms that were previously implicit. New contributions to this repo are CC BY 4.0 from v1.4.0 forward. |
| `CONTRIBUTING.md` added | Reference only — formalises the contribution process. If you contribute upstream, read it. The multi-issue commit-keyword convention (`Closes #A. Closes #B.`) is documented there. |
| `UPGRADING.md` added (this file) | Reference only — adopter convenience. If you maintain your own per-project `UPGRADING.md`, this is the template format. |
| `docs/THRESHOLDS.md` added — rationale for the 100/90/70/85 coverage and 3.5/5.0 peer-review thresholds, tagged SPECULATIVE | Reference only — explains thresholds you already use. Quality gates unchanged. |
| **DR-014 (Proposed)** — PROVOCATION layering as opt-in extension | **No action.** Template files NOT changed in v1.4.0. Promotion to Accepted requires Paper 1 audit + FSD adapter check + version-impact decision. |
| README front-of-file restructured (Quickstart + 3-layer map + adoption scorecard near top, expanded DR-011 in *What Doesn't Work*, new Audits index, Contributing & Support pointer) | Reference only — additive; nothing removed. |
| CLAUDE.md: gitignored maintainer-local paths now explicitly labelled (`.claude/skills/`, `memory/`); new *What is intentionally not shipped* section | Reference only — clarifies what is and isn't shipped publicly. No template changes. |
| CHANGELOG header: maintainer release process numbered + *Adopter notes* convention codified | Reference only — formalises an existing pattern. If you use this repo as a reference for your own release process, adopt the same convention. |
| 4 GitHub Releases cut retroactively from v1.0.0–v1.3.0 tags | Reference only — `git checkout vX.Y.Z` and `git diff vX.Y.Z..vX.Y+1.0 -- templates/` work the same. The Releases page now makes pinned versions easier to discover. |

**No breaking changes.** This is a MINOR release per the SemVer convention: new docs and new DRs (DR-013 Accepted, DR-014 Proposed), no template-surface changes.

## v1.3.0 (2026-06-01)

**From v1.2.0 — what to review when you bump your pin to v1.3.0:**

| Change | Adopter action |
|--------|-----------------|
| Engineering Fidelity audits archived externally (`audits/engineering-fidelity-retrofit.md`, `audits/engineering-fidelity-audit-2.md` removed from this repo) | If you linked to either file in your own work, re-link to the external archive or replace with your own audit. New adopters: none required. |
| Anti-hallucination "WebFetch Fallback Discipline" added | Optional — adopt if you use WebFetch for source verification. Names subpage-blindspot and transport-failure modes. |
| Claim registry adds Coverage-by-Type cut | Recommended — update your registry's Coverage Summary to include the by-type cut at next major revision. Type-level Gate 2 expectation: every registered ARGUMENT and PROPOSITION should be `[x]` before gating. |
| DR-012 names decision-support as a third opt-in application class | Optional — relevant only if your project is decision-support work. Inherits unchanged from paper-application class except for paper-specific scaffolding (page budgets, LaTeX, journal style, etc.). |
| Paper 1 manuscript §4 rewritten from "three audits" to "two audits" (engineering-fidelity dropped) | Reference only — affects Paper 1's narrative, not the templates. |

**From v1.0.0 or v1.1.0 → v1.3.0:** review the v1.2.0 entry below as well.

## v1.2.0 (2026-05-29)

**From v1.1.0 — what to review when you bump your pin to v1.2.0:**

| Change | Adopter action |
|--------|-----------------|
| Claim registry migrated from legacy single-mixed-type table to **per-type sub-tables** (CLAIMs / ARGUMENTs / PROPOSITIONs / PROVOCATIONs) | Pre-existing registries with the legacy table still work; migration is mechanical and recommended at next major revision. Per-type sub-tables align verification fields with the unit type they apply to. |
| **DR-011** Multi-Pass Review Pattern + Step 7 in `anti-hallucination.md` | Pass 1 + Pass 2 are recommended-but-not-required workflow improvements; Pass 3 high-stakes only with mandatory style filter. |
| Writing-guide **tier-monotonicity** principle added | Optional — review your writing guide for explicit tier-monotonicity check (manuscript language must sit at or below the registered confidence tier). |
| Review-prompt requires "Style/voice rules to filter against" field | Adopt if you use the three-pass pattern (mandatory for Pass 3, optional for Pass 1 / Pass 2). |
| DR-005 — Nanoarguments added as argument-layer peer | Reference only — affects argument modelling for grant-style work. |
| `docs/category-theory-as-design-lens.md` added | Reference only. Names the structural lens implicit across DR-004, DR-011, and the layered memory system. Templates remain free of category-theory terminology. |

## v1.1.0 (2026-05-10)

**From v1.0.0 — what to review when you bump your pin to v1.1.0:**

| Change | Adopter action |
|--------|-----------------|
| **DR-010** + PROVOCATION as fifth opt-in unit type | **Opt-in.** Projects without speculative-design content can ignore the new unit type entirely. The standard CLAIM / ARGUMENT / PROPOSITION trio remains unchanged. |
| **Step Z** in `anti-hallucination.md` (Inverse Hallucination Check) | Opt-in — applies only to projects with PROVOCATION entries. Catches the failure mode where speculation is presented as if sourced. |
| Three project-conditional gates added | Opt-in. Each gate activates only when its condition is met: |
| → Gate 2.6 — Reflexivity | When PROVOCATION entries exist |
| → Gate 2.7 — Ethical Review | When the project engages contested topics |
| → Gate 2.8 — Voice Consistency | When voice-driven work where register is part of the contribution |
| Tier 1 / Tier 2 / Tier 3 adoption-readiness discipline introduced (via `audits/feedback-from-fsd.md`) | Reference only. Tier 2 / Tier 3 patterns from the FSD audit are deferred for the framework; adopter is free to reuse the same discipline locally. |

## v1.0.0 (2026-05-09)

Baseline. No prior version to upgrade from.

## When new versions land

This file is updated as part of each release. The maintainer release process (top of [`CHANGELOG.md`](CHANGELOG.md)) includes refreshing this file alongside the CHANGELOG entry. If you find this file out of date relative to `CHANGELOG.md`, that is a bug — please open an issue.

Convention for new releases: each `CHANGELOG.md` entry's "Adopter notes" or "Adopter action" content gets distilled into a table row here, paired with the *from-version* it applies from. Pinned consumers can read the table from their pinned version down to the latest, sequentially, to know exactly what to review.
