# Upgrading

If your paper project pins a specific version of `agent-ready-papers` (e.g. `agent-ready-papers: v1.2.0` in your project's `CLAUDE.md`), this document tells you what changed in each subsequent release and what action — if any — is required when you bump your pin.

The full release notes are in [`CHANGELOG.md`](CHANGELOG.md). This file is the quick-lookup adopter view.

## Convention

- **MAJOR** version bumps signal breaking changes to template surfaces or DR semantics. Adopters should expect to review.
- **MINOR** version bumps add templates, patterns, application classes, or behaviours. Adoption of the new additions is typically opt-in.
- **PATCH** version bumps are docs-only / clarifications. No action required.
- Every release entry in `CHANGELOG.md` includes an "Adopter notes" / "Adopter action" subsection. This file aggregates them per version for quick lookup.

## v2.1.0 (2026-06-11)

**From v2.0.2 — what to review when you bump your pin to v2.1.0:**

| Change | Adopter action |
|--------|-----------------|
| New top-level `agents/` directory; `templates/equation-checker.md` → `agents/equation-checker.md` (`git mv`, history preserved) | **Path update required** if your project's docs, scripts, or CLAUDE.md reference `templates/equation-checker.md` — change to `agents/equation-checker.md`. File contents unchanged. |
| `templates/review-prompt.md` → `agents/review-prompt.md` (`git mv`) | **Path update required** if your project references `templates/review-prompt.md` — change to `agents/review-prompt.md`. File contents unchanged. Paper-local copies in adopter projects are unaffected — those stay where they are; the rename is in the framework only. |
| New `agents/README.md` documenting the agents/ vs templates/ distinction | Reference only — read once to understand the convention. The line: templates are fill-in (copy + populate over project lifetime); agent-role prompts are single-shot (paste into agent system-prompt slot). |
| Root `CLAUDE.md` + `templates/CLAUDE.md` — Hard Constraint about in-repo `memory/` generalised. Now reads "any agent's user-level auto-memory" rather than naming only Claude Code | **Recommended** — if you mirrored the v1.6.2 / v1.7.0 Hard Constraint into your own paper project's CLAUDE.md, update the wording to match (Claude Code retained as the named instance; Cursor / GitHub Copilot CLI / etc. named as parallel cases). |
| Root `CLAUDE.md` Before You Start — new row for `agents/` directory | Reference only — pattern source if you maintain your own paper CLAUDE.md. |
| `templates/CLAUDE.md` (adopter template) Before You Start — *Reviewing before submission* row now mentions both paper-local copy and framework's `agents/review-prompt.md`; new row for `agents/equation-checker.md` | **Optional but recommended** — if you start a new paper project from the v2.1.0 template, you inherit these rows. Existing paper projects: copy the rows if you want to make the agent-role-prompt path discoverable to future sessions. |
| `templates/CLAUDE.md` Directory Structure — `review-prompt.md` removed from the paper-local listing | Reference only — adopters can now reference the framework's `agents/review-prompt.md` rather than keeping a paper-local copy, but the paper-local option remains valid (Paper 1 still uses it). |
| DR-009, DR-011, DR-013 inline references updated to `agents/` paths; DR-013 *Markdown templates* list split into *Markdown templates* + *Agent-role prompts* sub-bullets | Reference only — license scope unchanged (CC BY 4.0 applies to both groups). |
| Root `CLAUDE.md` + `README.md` self-pin bumped v2.0.2 → v2.1.0 | None — metadata only. |

**No breaking changes to template contracts.** Path-level break only for the two moved files, and only for adopters who reference them by path. MINOR release per the SemVer convention used by this repo (path moves are not MAJOR when the file contracts are unchanged and the rename is a single mechanical step documented in UPGRADING).

## v2.0.2 (2026-06-11)

**From v2.0.1 — what to review when you bump your pin to v2.0.2:**

| Change | Adopter action |
|--------|-----------------|
| `README.md` — `## The Argument, Structurally` closing sentence now clarifies type discipline (Toulmin block = ARGUMENT view; R-1 in registered section = PROPOSITION view; two views of the same case, each verified by its own checklist) | Reference only — surfaces the framework's argument/proposition distinction explicitly where the v2.0.1 wording had let them blur. |
| `README.md` — R-3 source narrowed to "Hallucination literature as cited in `templates/anti-hallucination.md`" (removes maintainer-local "replicated in own audits" pointer, since `audits/` was scrubbed from the public repo in v2.0.0) | Reference only — public readers can now follow every source pointer in the registered section. If you copied the v2.0.1 R-3 phrasing into your own README, mirror the tightening. |
| `README.md` — R-4 source narrowed to DR-009 + `templates/equation-checker.md` (removes maintainer-local Gemini-vs-Sonnet comparison pointer that lives in gitignored `memory/gotcha-log.md`) | Reference only — same as R-3: source pointers are now all publicly verifiable. |
| `README.md` — new format-note paragraph above the registered table acknowledging the CLAIM-style single-table layout is a README-brevity compression, not the framework's normative per-type sub-tables; points adopters at `templates/claim-registry.md` for actual paper registries | Reference only — preempts a likely adopter question and prevents the README single-table from being mistaken for the canonical layout. |
| Root `CLAUDE.md` + `README.md` self-pin bumped v2.0.1 → v2.0.2 | None — metadata only. |

**No breaking changes.** PATCH release: README-only self-audit fixes following the v2.0.1 logic-application pass.

## v2.0.1 (2026-06-10)

**From v2.0.0 — what to review when you bump your pin to v2.0.1:**

| Change | Adopter action |
|--------|-----------------|
| `README.md` — new `## The Argument, Structurally` section (Toulmin block) between *The Approach* and *When-Worth-It* | Reference only — makes the README's central argument inspectable. No template, DR, or tool surface changed. |
| `README.md` — confidence-language calibration sweep across seven spots ("catches" → "designed to catch", "prevents" → "constrains" / "guards against", "for everything" → "regardless of tier", "will re-propose" → "repeatedly re-propose across sessions", and similar) | Reference only — README's own language now sits at or below the tier of the underlying claim. If you've copied any of these specific phrasings into your own README or supporting docs, consider mirroring the downshift. |
| `README.md` — `## When This Framework Is Worth The Overhead` and `## When It Is Overkill` rewritten as yes/no-answerable testable boundary conditions | Reference only — you can now answer each bullet for your specific project, not just match it as a vibe. Useful when explaining to a collaborator whether the framework fits their work. |
| `README.md` — new `## This README, registered` section (seven entries R-1…R-7 with priority, type, confidence tier, source, and section anchors) | **Recommended pattern** — applying the framework to its own home document is a low-cost credibility move. Mirror in your own paper project's README (or top of `CLAUDE.md`) with your project's load-bearing claims registered. |
| Root `CLAUDE.md` + `README.md` self-pin bumped v2.0.0 → v2.0.1 | None — metadata only. |

**No breaking changes.** PATCH release: README-only logic-application pass, no functional change to templates, DRs, or tooling.

## v2.0.0 (2026-06-10)

**From v1.7.x — what to review when you bump your pin to v2.0.0:**

| Change | Adopter action |
|--------|-----------------|
| `templates/physics-verification/` removed (nine files) | **BREAKING.** If your project depended on this template family, either freeze on v1.7.1 (`git checkout v1.7.1 -- templates/physics-verification/`) and copy the files into your own project, or replace with your own equivalents. The conceptual methodology (mechanical reproduction, dimensional checking, limiting-case analysis, two-paths consistency) is portable; what's gone is this repo's hosting of the templates. |
| `docs/METHODOLOGY.md` removed | **BREAKING** if you linked to it. The framework is now described entirely by README + templates + DRs. Adopter docs that pointed at METHODOLOGY should re-target the README. |
| `audits/` directory no longer published | Reference only — adopters did not need this directory in the first place. The framework's public artifact is now smaller and self-contained. |
| README restructured (Problem → Approach → When-worth → When-overkill → Common Questions → Quickstart → details) | Reference only — front-of-file orientation changes; no template or DR contracts changed. |
| Paper 1 manuscript Section 4 (Preliminary Evidence) rewritten to "Related Work and Design Rationale"; specific source-project audit findings removed | Reference only — affects Paper 1's content, not the templates. |
| Templates' source-project examples genericised (Step Z worked example, equation-checker origin comment, claim-registry inverse-hallucination note, hypothesis-log example tags, vv-framework Gate 2.7 pointer) | Reference only — template contracts (fields, structure, gate semantics) are unchanged. The minor textual edits don't affect adopter projects that have already copied these templates. |
| DRs (004, 006–014) had audit references and source-project names removed from their evidence sections | Reference only — the decisions themselves stand; only the evidence narratives were genericised. |

**Breaking** flagged on the two removed surfaces (`templates/physics-verification/` and `docs/METHODOLOGY.md`). Everything else is content-level scrubbing that does not change template contracts.

## v1.7.1 (2026-06-09)

**From v1.7.0 — what to review when you bump your pin to v1.7.1:**

| Change | Adopter action |
|--------|-----------------|
| Root `CLAUDE.md` — companion pin advanced `agent-ready-projects: v1.10.2 → v1.10.3` | Reference only — upstream v1.10.3 added maintainer-only structural-lint self-tests. No template surface change; nothing to adopt unless you separately decide the lint pattern would help your own repo. |
| `README.md` + `CLAUDE.md` self-pin bumped v1.7.0 → v1.7.1 | None — metadata only. |

**No breaking changes.** PATCH release: companion-pin acknowledgment, no functional change.

---

## v1.7.0 (2026-06-09)

**From v1.6.3 — what to review when you bump your pin to v1.7.0:**

| Change | Adopter action |
|--------|-----------------|
| New template `templates/hypothesis-log.md` — provisional positions with `Position` / `Method` / `Revisit trigger` / `Review by`. Adopted from agent-ready-projects v1.10.0. | **Optional** — copy `templates/hypothesis-log.md` to your paper project root (or wherever you keep `gotcha-log.md` / `dead-ends.md`). Add the new Before You Start row from updated `templates/CLAUDE.md`: *"Placing a bet whose evidence lives in the future"* → routes to your local `hypothesis-log.md`. Best fit: pre-registered forecasts about Pass-3 outcomes, S1-5 calculation predictions, PROVOCATION calibration bets — anywhere a position needs future evidence to resolve. |
| Root `CLAUDE.md` — new Hard Constraint: self-verifying memory posture. New state claims in `memory/` may embed `<!-- verify: cmd -->` comments; `/curate` runs them on read. | **Optional, incremental.** Adopt for new state claims going forward. No retrofit required. The posture is documented; the discipline scales as you find it useful. Companion to agent-ready-projects v1.9.0 (self-verifying memory) and v1.10.0 (/curate Step 0 sub-step 5). |
| `templates/CLAUDE.md` (paper-project template) — three edits to surface hypothesis-log: new Before You Start row, Key Files row, Directory Structure entry | **Recommended for projects spawned from this template after v1.7.0** — these are inherited automatically. Projects predating v1.7.0 should copy the three edits manually if they adopt the hypothesis-log. |
| Root `CLAUDE.md` — companion pin advanced `agent-ready-projects: v1.7.0` → `v1.10.2` (your own pin can advance if it tracked this repo's) | Reference only — drift-check row will continue to surface upstream drift naturally. Adopting upstream v1.10.2 changes in your code projects is your call independent of this framework's pin. |

**No breaking changes.** MINOR release per SemVer: new opt-in template + new Hard Constraint posture (documents new-write convention, doesn't require retrofit).

## v1.6.3 (2026-06-08)

**From v1.6.2 — what to review when you bump your pin to v1.6.3:**

| Change | Adopter action |
|--------|-----------------|
| Root `CLAUDE.md` — new Before You Start row pointing at the three existing backlog locations (`memory/MEMORY.md` priorities + DR *Open Questions* + GitHub Issues) | Reference only — if you've ever asked yourself *"where's the backlog?"* in your own framework adoption, mirror the row in your project's `CLAUDE.md` with paths adjusted for your project's three locations (e.g., your paper's `backlog.md` + your DRs + your issue tracker). |

**No breaking changes.** PATCH release: discoverability row only, no functional change.

## v1.6.2 (2026-06-08)

**From v1.6.1 — what to review when you bump your pin to v1.6.2:**

| Change | Adopter action |
|--------|-----------------|
| Root `CLAUDE.md` + `templates/CLAUDE.md` — new Hard Constraint: project state goes in `memory/` (in-repo), not in user-level Claude Code auto-memory | **Recommended** — if you use Claude Code: mirror the constraint in your own paper project's `CLAUDE.md` so future agent sessions inherit the rule. The constraint is per-repo enforced; there's no global way to ship it from this framework. If your project predates v1.6.2 the Hard Constraint bullet must be copied manually; projects spawned from `templates/CLAUDE.md` after v1.6.2 inherit it. |

**No breaking changes.** PATCH release: framework convention codification.

## v1.6.1 (2026-06-08)

**From v1.6.0 — what to review when you bump your pin to v1.6.1:**

| Change | Adopter action |
|--------|-----------------|
| `README.md` — *"What's in this repo"* Framework row now lists `tools/`; new *## Tools* section threads `coverage.py` / `check_dois.py` / cost data into the adopter-facing entry point; *Templates* index gains a `cost-log.md` row; Anti-Hallucination section gains an automated-companion note pointing at `tools/check_dois.py` | Reference only — README discoverability fix; same principle as v1.5.1's CLAUDE.md fix. |

**No breaking changes.** PATCH release: README docs-only, no functional change.

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
| **DR-014 (Proposed)** — PROVOCATION layering as opt-in extension | **No action.** Template files NOT changed in v1.4.0. Promotion to Accepted requires Paper 1 audit + speculative-design adopter check + version-impact decision. |
| README front-of-file restructured (Quickstart + 3-layer map + adoption scorecard near top, expanded DR-011 in *What Doesn't Work*, new Audits index, Contributing & Support pointer) | Reference only — additive; nothing removed. |
| CLAUDE.md: gitignored maintainer-local paths now explicitly labelled (`.claude/skills/`, `memory/`); new *What is intentionally not shipped* section | Reference only — clarifies what is and isn't shipped publicly. No template changes. |
| CHANGELOG header: maintainer release process numbered + *Adopter notes* convention codified | Reference only — formalises an existing pattern. If you use this repo as a reference for your own release process, adopt the same convention. |
| 4 GitHub Releases cut retroactively from v1.0.0–v1.3.0 tags | Reference only — `git checkout vX.Y.Z` and `git diff vX.Y.Z..vX.Y+1.0 -- templates/` work the same. The Releases page now makes pinned versions easier to discover. |

**No breaking changes.** This is a MINOR release per the SemVer convention: new docs and new DRs (DR-013 Accepted, DR-014 Proposed), no template-surface changes.

## v1.3.0 (2026-06-01)

**From v1.2.0 — what to review when you bump your pin to v1.3.0:**

| Change | Adopter action |
|--------|-----------------|
| Anti-hallucination "WebFetch Fallback Discipline" added | Optional — adopt if you use WebFetch for source verification. Names subpage-blindspot and transport-failure modes. |
| Claim registry adds Coverage-by-Type cut | Recommended — update your registry's Coverage Summary to include the by-type cut at next major revision. Type-level Gate 2 expectation: every registered ARGUMENT and PROPOSITION should be `[x]` before gating. |
| DR-012 names decision-support as a third opt-in application class | Optional — relevant only if your project is decision-support work. Inherits unchanged from paper-application class except for paper-specific scaffolding (page budgets, LaTeX, journal style, etc.). |

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
| Tier 1 / Tier 2 / Tier 3 adoption-readiness discipline introduced | Reference only. The discipline is a convention adopters may reuse locally for staged feature promotion. |

## v1.0.0 (2026-05-09)

Baseline. No prior version to upgrade from.

## When new versions land

This file is updated as part of each release. The maintainer release process (top of [`CHANGELOG.md`](CHANGELOG.md)) includes refreshing this file alongside the CHANGELOG entry. If you find this file out of date relative to `CHANGELOG.md`, that is a bug — please open an issue.

Convention for new releases: each `CHANGELOG.md` entry's "Adopter notes" or "Adopter action" content gets distilled into a table row here, paired with the *from-version* it applies from. Pinned consumers can read the table from their pinned version down to the latest, sequentially, to know exactly what to review.
