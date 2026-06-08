# Changelog

All notable changes to `agent-ready-papers`. Adopters can check their paper project's framework version against this log to see what has changed.

<!-- Maintainer release process:
     When promoting a `vX.Y.Z (candidate, unreleased)` block to a dated release:

     1. Tag the release commit:

         git tag vX.Y.Z <commit>
         git push --tags

        Tags let adopters `git checkout vX.Y.Z` to inspect a pinned version and
        `git diff vX.Y.Z..vX.Y+1.0 -- templates/` to preview an upgrade.

     2. Cut a GitHub Release from the tag (gh release create vX.Y.Z ...) with a
        short summary + link back to this CHANGELOG entry.

     3. Add a row to UPGRADING.md under the new version section: one table row
        per change that requires pinned-consumer action, paired with the
        from-version it applies from. Adopters read UPGRADING.md sequentially
        from their pin down to latest.

     Versioning convention (mirrors agent-ready-projects):
     - MAJOR — breaking changes to template surfaces or DR semantics
     - MINOR — new templates, patterns, application classes, or behaviours
     - PATCH — docs-only changes, clarifications, cross-reference adds

     Adopter-notes convention:
     - Every release entry below MUST include an "Adopter notes" or
       "Adopter action" subsection listing what action (if any) pinned
       consumers need to take. UPGRADING.md aggregates these per version
       for quick lookup. If an entry has no adopter action, say so explicitly
       ("No adopter action required.") rather than omitting the subsection.
-->

## v1.6.1 (2026-06-08)

README discoverability fix. v1.5.0 shipped `tools/`, v1.6.0 shipped `templates/cost-log.md` — neither was threaded through the public-facing README. v1.5.1 fixed this for the three CLAUDE.md surfaces (agent-orientation); v1.6.1 applies the same discipline to the README (adopter-orientation). The principle from v1.5.1 — *audit each release against "would a fresh README/CLAUDE.md read surface this?"* — now covers both the agent-facing and adopter-facing entry points.

### Documentation
- **`README.md`** — five edits:
  - Current-release line bumped to v1.6.1.
  - *"What's in this repo"* Framework row extended to include `tools/` (since v1.5.0).
  - *"Anti-Hallucination Checklist"* gains an *Automated companion* note pointing at `python -m tools.check_dois` as the batch Step 0 helper.
  - New *## Tools* section between *Templates* and *Paper Projects* — purpose-vs-when-to-run table for `coverage.py` and `check_dois.py`, known-limits pointer to `tools/README.md`, and the empirical cost data from `papers/perspective/vv/cost-log.md` (Pass 1 vs Pass 2 mean tokens + load-bearing-findings ratio).
  - *Templates* index gains a row for `cost-log.md`.

### Adopter notes
- **No template content changes.** README-only edits. Pinned consumers on v1.6.0 require **no migration action**.
- **Discoverability principle continued.** v1.5.1 audited CLAUDE.md; v1.6.1 audits the README. Future releases should check both surfaces against the same question — *would a fresh read of this file surface the new artefact?* — to avoid the v1.5.0 / v1.6.0 gap repeating.

---

## v1.6.0 (2026-06-08)

Operation cost logging. New `templates/cost-log.md` template + per-paper `vv/cost-log.md` convention for tracking token cost of major framework operations (review passes, `/curate`, `/audit-context`, batch verification, full Gate sweeps). Makes the *cost* side of cost-vs-value tradeoffs in decision-record evidence bases empirical rather than qualitative. DR-011 evidence base updated with the first N=2 token-cost replication, logged from this session's own scaffolding-stage and parser-stage review batteries on `tools/`.

### New template
- **`templates/cost-log.md`** — Column structure for per-paper operation cost log: date, operation, total tokens, input/output deltas (when available), cache read, wall clock, notes. Includes an aggregation section for summarizing by operation type after ~10 entries. Top-of-file convention paragraph documents how to use `/status` for the deltas and explicitly notes that subagent (Agent tool) results report `total_tokens` only — input/output/cache breakdown is not surfaced at that granularity.
- **`papers/perspective/vv/cost-log.md`** — Paper 1 bootstrap data: four entries from today's two scaffold + parser DR-011 batteries (Haiku Pass 1 × 2, Opus Pass 2 × 2). Self-application of the convention with caveats and forward-looking gather list.

### DR-011 evidence-base extension
- **`decisions/DR-011_multi-model-review-pattern.md`** — Evidence Base section gains a token-cost replication entry (N=2 within-Claude, code-tooling scale): Pass 1 mean **36,812 tokens** with **0 / 2 rounds load-bearing findings**; Pass 2 mean **52,540 tokens** (~1.4× Pass 1) with **2 / 2 rounds load-bearing design findings** that would have shipped broken. Open Questions section gains a "paper-scale token cost calibration" entry naming the next data point to gather as Paper 1 accrues passes.

### CLAUDE.md updates (continuing the v1.5.1 discoverability discipline)
- **`templates/CLAUDE.md`** — Before You Start row added: *"Logging token cost of an operation"* → `vv/cost-log.md`.
- **`papers/perspective/CLAUDE.md`** — same row added with the path correctly noting that bootstrap data from 2026-06-08 is already present.

### Adopter notes
- **Optional.** The cost-log is a convention, not a required surface. If you don't care about token spend you can ignore the template; nothing in the existing verification workflow depends on it.
- **Recommended** if you want to make decision-record cost-vs-value claims quantitative (e.g., DR-011's Pass 2 prescription becomes empirically priceable), or if you want to budget framework overhead per paper.
- **Discoverability continued.** New artefact routed through the three CLAUDE.md surfaces per the v1.5.1 principle. Fresh agent sessions discover the cost-log without `git log` or `ls`.

---

## v1.5.1 (2026-06-08)

CLAUDE.md discoverability fix. v1.5.0 shipped the `tools/` directory but did not update any of the three CLAUDE.md files (root, Paper 1, paper template) to point future agent sessions at the tools — and a separate gap surfaced in the same audit: `docs/THRESHOLDS.md` (landed v1.4.0) had no direct trigger in the root Before You Start table. A fresh session would have done the manual count or thumbed through `docs/framework-summary.md` instead of running the tool or reading the threshold rationale.

The audit prompt and the principle behind it: *the whole point of this framework is that an agent picks up tools and skills automatically.* If an agent has to discover capabilities by `git log` or `ls`, the framework has failed at its primary job. Each release should be audited against the question "would a fresh session find this without external prompting?" — and the audit recurses into per-paper and template CLAUDE.md files, not just the root.

### Documentation
- **Root `CLAUDE.md`:**
  - Architecture diagram — `tools/`, `tests/`, `Makefile`, `pyproject.toml` rows added.
  - Before You Start — two new rows: *"Checking coverage or DOIs in a registry"* (points at `tools/coverage.py` and `tools/check_dois.py` with both direct and Makefile invocations); *"Asking what a coverage or peer-review threshold means"* (points at `docs/THRESHOLDS.md`).
  - How to Work Here — replaced the *"Manual: open file and check P0/P1/P2 percentages"* comment with the actual `python -m tools.coverage` and `python -m tools.check_dois` commands.
- **`papers/perspective/CLAUDE.md`** — Before You Start gains a row pointing at the tools with the correct registry path for Paper 1. Paper 1 is the first project to use the tools self-applied.
- **`templates/CLAUDE.md`** — Before You Start gains the same row with adopter-facing path placeholders. New paper projects created from this template now discover the tools by default.

### Adopter notes
- **No template content changes.** Only the agent-orientation tables in the three CLAUDE.md files. Pinned consumers on v1.5.0 require **no migration action**.
- **Recommended:** if you maintain your own paper project, copy the new Before You Start row from `papers/perspective/CLAUDE.md` (with paths adjusted for your project) so your own agent sessions discover the tools.
- **Principle adoption:** the *"audit each release against discoverability from a fresh CLAUDE.md read"* discipline is recommended for every release. The framework's value depends on it.

---

## v1.5.0 (2026-06-08)

Registry-verification tooling. The `tools/` directory introduces the first Python footprint in the repo: two zero-dep CLIs that read a `claim_registry.md` and answer two operational questions — *what is my coverage* and *do all my DOIs resolve*. Both tools are deterministic, importable, and CLI-runnable; targeted at CI use against a paper project's registry. Two DR-011 multi-model review batteries (one against the API scaffolding, one against the parser implementation) caught real load-bearing issues — most notably a PROVOCATION column-resolution bug that would have shipped green against the empty-PROVOCATION Paper 1 fixture and bit the first FSD-style adopter. Closes [#17](https://github.com/ducroq/agent-ready-papers/issues/17).

### New tooling
- **`tools/coverage.py`** — Per-type sub-table parser. Walks a claim registry, identifies `**CLAIMs:**` / `**ARGUMENTs**` / `**PROPOSITIONs**` / `**PROVOCATIONs**` sub-tables by marker, finds Priority/Tier and Status columns by name (not position), counts verified entries. Two axes: priority (P0/P1/P2) for the standard unit types, provocation_tier (GROUNDED/EXTRAPOLATED/PROVOCATIVE/CRITICAL) for PROVOCATION sub-tables per [DR-010](decisions/DR-010_provocation-unit-type.md). Markdown and JSON output. Exit codes 0 (success) / 1 (with `--strict`, target missed) / 2 (tooling error).
- **`tools/check_dois.py`** — DOI extractor and resolver. Regex-extracts DOIs (allowing balanced `()` for Lancet-style identifiers like `10.1016/S0140-6736(13)62228-X`), strips prose punctuation, then HEAD against `https://doi.org/` without redirect-following (a 30x from doi.org IS the resolution signal). `--offline` mode verifies parseability only; the `parseable` and `resolved` fields are intentionally distinct so a CI gate over `all_resolved` cannot silently pass if the offline flag is inherited.
- **`tools/README.md`** — Usage, exit codes, design constraints, known limits (no escaped-pipe support in cells, no HTTP proxy support, sequential HEAD scaling, line-anchored marker recognition, heuristic `_clean_doi`).
- **`Makefile`, `pyproject.toml`, `.gitignore`** — First Python footprint in the repo: ruff config (E/W/F/I/B/UP/S), pytest config, py3.10 target, `make test / lint / format / check / coverage / check-dois` targets. Patterns borrowed from `vmodel.eu/reqrev/structure_checker.py` (public API in module docstring, frozen dataclass result types).
- **`tests/`** — Shape-pin tests against the Paper 1 fixture (19 entries, 9 DOIs). 17 tests: dataclass-shape pins, FileNotFoundError pins, end-to-end fixture verification, determinism pins (same input → byte-identical output across runs), focused unit tests for `_clean_doi` and `_find_bucket_and_status_columns` including the PROVOCATION-with-`Source Tier` regression test that the second DR-011 battery surfaced.

### DR-011 evidence base
Two review batteries across the scaffolding stage and the parser stage. Pass 2 (Opus, fresh session) caught **3 load-bearing design issues** across the two rounds that Pass 1 (Haiku) did not surface, including a forward-looking PROVOCATION column-resolution bug that the Paper 1 fixture could not exercise. Pass 1 in the scaffolding round had a documented false positive (regex check). Pass 1 in the parser round was visibly more careful (no false positives) — a single datapoint, not a confirmed pattern. Recorded as one more N within Claude family for the DR-011 evidence base.

### DR-013 *Revisit If* check
`tools/` is ~620 LOC of Python — sub-threshold for the dual CC BY 4.0 + MIT trigger condition named in [DR-013](decisions/DR-013_license-choice.md). No DR-013 amendment in this release. Re-evaluate when `tools/` exceeds ~2000 LOC or grows an importable API surface used by external code.

### Adopter notes
- **No template changes.** All additions are opt-in tooling. Pinned consumers on v1.4.0 require **no migration action**.
- **Optional adoption.** If you maintain a `claim_registry.md` in your own paper project, you can run `python -m tools.coverage <your-registry.md>` and `python -m tools.check_dois <your-registry.md>` from your own clone of this repo. The tools have no dependency on the rest of `agent-ready-papers` — only stdlib.
- **Known limits documented in `tools/README.md`.** If your registry uses escaped pipes in cells (`\|`), if you sit behind a corporate HTTPS proxy, or if your registry has >50 DOIs, read the limits section before adopting.
- **License:** tools inherit CC BY 4.0 per DR-013. Current size is sub-threshold for revisiting that choice.

---

## v1.4.0 (2026-06-08)

External-feedback-driven release. June 2026 external review — three independent reviewers, convergent at [#30](https://github.com/ducroq/agent-ready-papers/issues/30) — produced 14 actionable issues. This release closes 12 of them outright plus DR-014 Proposed (#18) and #17 (registry tooling) deferred to a dedicated session. The framework gains a LICENSE (CC BY 4.0), three new top-level docs (`CONTRIBUTING.md`, `UPGRADING.md`, `docs/THRESHOLDS.md`), two new DRs (DR-013 Accepted, DR-014 Proposed), substantially restructured README front-of-file (Quickstart + three-layer map + adoption scorecard), and the maintainer release process is now codified in this CHANGELOG's header.

### New decisions
- **[DR-013](decisions/DR-013_license-choice.md)** — *License Choice — CC BY 4.0.* Status: Accepted. Five options considered (CC BY 4.0, MIT, Apache 2.0, dual MIT+CC, no licence). CC BY 4.0 chosen as lingua franca for prose-heavy methodology repos. *Revisit If* conditions named for a future `tools/` directory (per [#17](https://github.com/ducroq/agent-ready-papers/issues/17)). Closes [#20](https://github.com/ducroq/agent-ready-papers/issues/20).
- **[DR-014](decisions/DR-014_provocation-layered-as-opt-in-extension.md)** — *PROVOCATION as Explicit Opt-In Extension Over Core Unit Types.* Status: **Proposed**. Four options considered; Option B (separate extension doc referenced from core, mirroring the conditional-gates pattern) proposed. Three pending checks gate promotion to Accepted: (1) Paper 1 reference audit, (2) FSD template-adapter check, (3) v1.4.x-MINOR vs v2.0.0-MAJOR version-impact decision. Templates NOT touched in this release. [#18](https://github.com/ducroq/agent-ready-papers/issues/18) stays open as the implementation tracker.

### New top-level files
- **`LICENSE`** — CC BY 4.0 deed + canonical legal-code URL + citation block. GitHub-detected. Closes [#20](https://github.com/ducroq/agent-ready-papers/issues/20).
- **`CONTRIBUTING.md`** — Three-audience structure (adopters / collaborators / issue filing), in-scope / out-of-scope sections, licence clause referencing DR-013, multi-issue commit-keyword convention codified (use `Closes #A. Closes #B.` not comma-separated multi-line — empirical finding from this session's #19/#27/#28 commit `fac6872` where only the first issue auto-closed). Closes [#22](https://github.com/ducroq/agent-ready-papers/issues/22).
- **`UPGRADING.md`** — Per-version adopter-notes aggregation for pinned consumers. Convention block + sections for v1.4.0 / v1.3.0 / v1.2.0 / v1.1.0 / v1.0.0 baseline. Closes [#29](https://github.com/ducroq/agent-ready-papers/issues/29).

### New docs
- **`docs/THRESHOLDS.md`** — Rationale for the 100% P0 / 90% P1 / 70% P2 / ≥85% overall coverage and ≥3.5/5.0 simulated-peer-review thresholds. Top-of-file **SPECULATIVE** label per the framework's own confidence-tier discipline. Per-threshold reasoning, honest accounting (N=1 Paper 1 evidence is *consistent with* the thresholds but does not validate them), three data gaps named that would harden the thresholds to EMERGING or SUPPORTED (multi-project coverage benchmark, calibrated peer-review correlation, failure-mode tracking). Closes [#16](https://github.com/ducroq/agent-ready-papers/issues/16).

### README restructure (front-of-file)
Additive — nothing removed. The new sections sit between the existing intro callouts and `## The Core Problem`, in the order *orient → act → see data → understand problem*.

- **## What's in this repo** — three-layer Framework / Worked examples / Evidence map with the "If you only want the framework, stop at the Quickstart below" opt-out. Closes [#25](https://github.com/ducroq/agent-ready-papers/issues/25).
- **## Quickstart + Three tiers of adoption** — 5-step ~10-minute path with the minimum-viable-adoption file table (Required for first use / Useful once the paper grows / Reference-only). Closes [#23](https://github.com/ducroq/agent-ready-papers/issues/23).
- **## What it does in practice** — six-row sourced metrics table with the CALCULATION 3/3 vs 0/3 finding led and emphasised; *when worth the overhead* / *when overkill* sections. Closes [#26](https://github.com/ducroq/agent-ready-papers/issues/26).
- **DR-011 expanded in *What Doesn't Work*** — three-bullet pass breakdown + paragraph naming the empirical anchor scales (blog, grant N=2, decision-support). Closes [#19](https://github.com/ducroq/agent-ready-papers/issues/19).
- **METHODOLOGY callout** — sibling to the existing "Want to get started fast?" line, surfacing `docs/METHODOLOGY.md` as provenance. Closes [#27](https://github.com/ducroq/agent-ready-papers/issues/27).
- **## Audits index** — new section between *Paper Projects* and *Further Reading* indexing all 9 audits grouped by kind (retrofits / cross-project / forward-feedback / discovery). Closes [#28](https://github.com/ducroq/agent-ready-papers/issues/28).
- **## Contributing & Support** — pointer into `CONTRIBUTING.md`, licence pointer, `UPGRADING.md` pointer.
- **Quality Gates intro callout** — SPECULATIVE label on the gate thresholds, pointer to `docs/THRESHOLDS.md`. (Part of #16.)

### CLAUDE.md changes
- **`.claude/skills/` and `memory/`** in the architecture diagram now labelled as `(gitignored — not shipped)` / `(gitignored — maintainer-local)`. Closes [#24](https://github.com/ducroq/agent-ready-papers/issues/24).
- **New ## What is intentionally not shipped section** — five-row table covering `/curate`, `/audit-context`, `MEMORY.md`, `gotcha-log.md`, `dead-ends.md` with "For adopters" guidance. Explicit statement that the public framework is fully consumable without these maintainer-local files.

### Release process
- **CHANGELOG header** now numbers the three-step maintainer release process (tag + push, `gh release create`, refresh `UPGRADING.md`) and codifies the *Adopter notes* subsection requirement for every entry — including the explicit "No adopter action required." case to avoid the omit-by-mistake failure mode.
- **4 retroactive GitHub Releases** cut from existing tags v1.0.0–v1.3.0, each with a short summary plus CHANGELOG link, v1.3.0 marked latest at cut time (this release will subsequently overtake it). Closes [#21](https://github.com/ducroq/agent-ready-papers/issues/21).

### External validation
- **Issue [#30](https://github.com/ducroq/agent-ready-papers/issues/30)** — convergent positive signals from three independent reviewers recorded as a tracking issue. SE mental model, decision records, anti-hallucination (Step 0 + Step Z), and equation verification all called out as the framework's strongest assets by all three reviewers. Reviewer 2 (Gemini) verdict: 9/10 *"Gold Standard"*. Reviewer 3 (Copilot): *"framework looks stronger than the packaging"* — all productization concerns addressed in this release.

### Carried forward to a future session
- **[#17](https://github.com/ducroq/agent-ready-papers/issues/17)** — registry tooling (Python coverage calculator + DOI validator + `tools/` directory). Deferred to a dedicated session per maintainer call; the reviewer-asked scope is documented in the issue body.
- **[#18](https://github.com/ducroq/agent-ready-papers/issues/18)** — PROVOCATION layering at DR-014 (Proposed) pending the three checks named in the DR. Implementation deferred.

### Adopter notes
- **No breaking changes.** All adopter-facing changes are additive: LICENSE adds permission that was previously absent; `CONTRIBUTING.md` / `UPGRADING.md` / `docs/THRESHOLDS.md` are new informational docs; README restructure is additive at the top of file; CLAUDE.md changes clarify previously implicit conventions. Pinned consumers on v1.3.0 require **no migration action**.
- **Recommended:** if you maintain your own `UPGRADING.md` in a downstream paper project, copy the format from this repo's `UPGRADING.md` and start aggregating per-version adopter notes.
- **DR-013 licence:** new contributions are CC BY 4.0 from v1.4.0 forward. Older versions inherit by default since no contrary licence was previously declared.

---

## v1.3.0 (2026-06-01)

Seven items landed: DR-012 names decision-support as a third opt-in application class; DR-011 evidence base extended to N=2 within-Claude; anti-hallucination gains WebFetch fallback discipline; claim-registry adds Coverage-by-Type cut; Paper 1 registry migrated to per-type sub-tables; Engineering Fidelity audit files archived outside the repo; Paper 1 §4 rewritten from "three audits" to "two audits" to reflect the reduced evidence base (Gate 2 invalidation acknowledged — Gate 2.5 re-check is co-author's call at Gate 3).

### New decisions
- **[DR-012](decisions/DR-012_decision-support-artefacts.md)** — *Decision-Support Artefacts as Third Non-Paper Application Class.* Status: Proposed. N=1 worked example (`new_hardware/vv/`, 2026-05-30). Five sufficient conditions for the class named; what is paper-specific and does not apply (page budgets, LaTeX, journal style, author guidelines, co-author signoff, submission gates) explicitly listed. Self-critique applied before commit — see commit message.

### New templates / pattern additions
- **`templates/claim-registry.md`** — Coverage Summary now cuts both by Priority (existing) and by Type (new). Type-level Gate 2 expectation: every registered ARGUMENT and PROPOSITION should be `[x]` before gating, since each is load-bearing for the contribution. Closes #10.
- **`templates/anti-hallucination.md`** — Adds "Verifying Web Sources: WebFetch Fallback Discipline" between *Verifying Negative Claims* and Step Z. Names two failure modes (subpage blindspot; transport failure) and prescribes a fallback ladder (specific URL → homepage → `site:` search → sitemap). Two worked examples from the 2026-05-22 NLnet v3 application. Closes #8 (Proposal 2; Proposal 4 closed via the DR-011 evidence-base extension below).

### Decision extensions
- **[DR-011](decisions/DR-011_multi-model-review-pattern.md)** Evidence Base + Open Questions extended with grant-scale N=2 replication (NLnet NGI Zero Commons Fund v3, 2026-05-22). Within-Claude disjoint-coverage pattern replicated; cross-family generality still untested. (Addresses #8 Proposal 4.)

### New audits
- **`audits/feedback-from-decision-support.md`** — Worked example for DR-012. Captures the 2026-05-30 session, what confirmed unchanged, what did not apply, three patterns surfaced at decision-support scale (each marked *incubate* pending a second sighting), and open questions (sub-class differentiation, calibration to stakes, time-pressured application).

### Paper 1
- **`papers/perspective/vv/claims/claim_registry.md`** — Migrated from legacy single-mixed-type table per section to per-type sub-tables (CLAIMs / ARGUMENTs / PROPOSITIONs). Prose verification blocks (S3-4 warrant, S4-4 warrant, S5-1 premises/reasoning/boundaries) folded into checklist-aligned columns. List delimiter normalised to `;`. Coverage Summary gains by-type cut. Closes #11. Self-eating-dog-food restored between template and first instance.

### Removals
- **Engineering Fidelity audits archived externally.** `audits/engineering-fidelity-retrofit.md` and `audits/engineering-fidelity-audit-2.md` moved to `OneDrive/.../Johan/EngineeringFidelity/framework-audits/` on 2026-06-01. The Engineering Fidelity content belongs with its own project, not as evidence carried by this framework repo.
  - **Adopter action:** none required for new adopters. Existing adopters who linked to either file in their own work need to re-link to the external archive or replace with their own audit.
- **Paper 1 manuscript §4** rewritten from "three audits" to "two audits" (proposition + technology). The third-audit paragraph (lines 457-464 previously) describing the engineering-characterisation audit is removed. Limitations updated from "all three audits" / "all three projects" to "both audits" / "both projects." Domain cluster updated from "medical simulation and measurement science" to "medical simulation and instrumentation." Abstract reflects the count change. **Gate 2 invalidation:** this is a content change to a registry that previously held a verification freeze. Gate 2.5 (Internal Consistency) re-check is the co-author's call at Gate 3.
- **Paper 1 supporting files** (`papers/perspective/CLAUDE.md`, `backlog.md`, `backlog-paper2.md`, `writing-guide.md`, `vv/claims/claim_registry.md`): EF references removed or repathed. S4-4 ARGUMENT in the registry rewritten to cite two audits with N=2 caveat explicit.
- **`docs/METHODOLOGY.md`**: removed the EngineeringFidelity (MST Paper) source-project subsection; updated opening from "Three" to "Two paper projects"; removed broken `engineering-fidelity-retrofit.md` link; updated remaining "all three" / "original three" mentions to source-project-agnostic phrasing; "What Survived" table's *Where it came from* column updated to refer to "earlier source-project work" rather than naming EF.
- **README**: dropped "across two journals (IEEE TIM, MST)" parenthetical and the "three real paper projects" count from the tagline and Further Reading. The framework's tagline is now journal-agnostic and count-agnostic.
- **`decisions/DR-006_publication-roadmap.md`**: updated "three real paper projects (IEEE TIM, MST, medical education)" to "two real paper projects (IEEE TIM, medical education)"; Paper 2 evaluation-evidence list updated to drop EngineeringFidelity; Paper 2 timeline annotation acknowledges that a prospective case study is likely needed.
- **`decisions/DR-008_empirical-paper-support.md`**: top-of-file note added pointing to the external archive. Findings table preserved as historical record of the audits that motivated this DR.
- **`audits/driven-pendulum-retrofit.md`**: top-of-file note added pointing to the external archive. Cross-project comparison data (Appendix) preserved as historical record reflecting framework state at audit time.
- **`audits/equation-verification-journey.md`** and **`audits/proposition-retrofit.md`**: "three paper projects" / "three source projects" mentions softened to project-count-agnostic phrasing.

### Versioning
This is the framework's first explicitly-versioned release. Prior versions (v1.0.0 through v1.2.0 below) are reconstructed retroactively from the git history. Going forward, releases follow the maintainer-release-process block at the top of this file.

---

## v1.2.0 (2026-05-29)

Multi-pass review pattern + structural rationale + per-type registry surface. The framework's most consequential mid-2026 expansion — DR-011 made *bias-escape* a first-class verification dimension; the subsequent rationale work named the structural principles already implicit across the framework.

### New decisions
- **[DR-011](decisions/DR-011_multi-model-review-pattern.md)** (2026-05-12) — *Multi-Model Review Pattern.* Three-pass review with explicit bias-escape semantics: Pass 1 (intra-family small) escapes sunk-cost from the drafting session; Pass 2 (intra-family large) does the same with argument-shape critique character; Pass 3 (cross-vendor) escapes training-data and stylistic priors and requires a mandatory style/voice filter. Naming convention chosen ("Pass", not "Tier") to avoid collision with existing tier semantics. Status: Proposed; evidence N=1 at blog scale.
  - **Design Rationale: Functorial Composition** added 2026-05-29 (commit `74d7976`, closes #13). Each pass is a different functorial view; their combined verification is the limit. Makes adding/skipping/retiring a pass decidable on invariant-coverage grounds, not empirical hand-waving. Background: `docs/category-theory-as-design-lens.md`.
- **[DR-005](decisions/DR-005_nanoarguments-as-argument-layer-peer.md)** addition — Nanoarguments (NLnet NGI Zero) added as an argument-layer peer + revisit trigger (commit `299a521`).

### Template / pattern additions
- **`templates/claim-registry.md`** (commit `97f3c3b`, closes #9) — Per-type sub-tables (one each for CLAIMs / ARGUMENTs / PROPOSITIONs / PROVOCATIONs) with checklist-aligned columns. Required verification fields (Grounds, Warrant, Rebuttal for ARGUMENT; Constructs, Relationship, Premises, Reasoning, Boundary conditions, Alternatives engaged for PROPOSITION; Plausibility evidence, Generative move, Reflexive marker, Ethics commitment for PROVOCATION) now have structural homes in columns rather than orbiting prose blocks below the table. `;` list-delimiter convention named explicitly. Replaces the legacy single-mixed-type table.
- **`templates/writing-guide.md`** (commit `a294361`, closes #12) — Tier-monotonicity principle added: manuscript language must sit at or below the registered confidence tier. Citation drift is named as a tier-monotonicity failure, not a separate rule of thumb.
- **`templates/review-prompt.md`** — "Style/voice rules to filter against" added as a required-with-default field per DR-011 Pass 3 requirement.
- **`templates/anti-hallucination.md`** — Step 7 (Multi-Pass Review Across Model Families) added per DR-011.

### Docs / structural rationale
- **`docs/category-theory-as-design-lens.md`** (commit `f79b6f0`) — New note. Names the structural lens implicit across DR-004 (typed registry), DR-011 (multi-pass functors), and the layered memory system. Vocabulary stays in the rationale doc; templates and slash commands remain free of category-theory terminology.
- **Grounding disambiguation** (commit `ff44246`) — "Grounding" in the AI sense (RAG, retrieval-augmented generation) explicitly distinguished from PROVOCATION-tier GROUNDED in the writing-guide and framework-summary.

### Audits added
- **`audits/feedback-from-blog-application.md`** — DR-011 triggering observation, three-reviewer comparison on a LinkedIn cross-post.
- **`audits/feedback-from-grant-application.md`** — NLnet NGI Zero Commons Fund v3 (2026-05-22) application: surfaces WebFetch subpage-blindspot, WebFetch 403 fallback, cross-document inheritance patterns (each captured as Proposals in #8).
- **`audits/feedback-from-template-revision.md`** — Multi-model review log for #9 (claim-registry per-type sub-tables).

### Adopter notes
- Pre-existing registries with the legacy single-mixed-type table still work; migration to per-type sub-tables is mechanical and recommended at next major revision. Paper 1's registry migrates in v1.3.0 (closes #11).
- Pass 1 + Pass 2 default applicability ("every publish" / "every major revision") is provisional at blog and grant scale; full-paper scale untested as of v1.2.0.

---

## v1.1.0 (2026-05-10)

Speculative-design extension. DR-010 activates DR-004's reserved non-empirical slot with PROVOCATION as a fifth opt-in unit type. The framework now formally supports speculative-design / design-fiction / diegetic-prototype work.

### New decisions
- **[DR-010](decisions/DR-010_provocation-unit-type.md)** — *PROVOCATION as Fifth Unit Type for Speculative-Design Work.* Status: Accepted. PROVOCATION is a designed artefact that makes no truth claim. Verification: Auger 2013 four criteria (plausible / generative / reflexive / ethically held). Separate confidence axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL), each tier carrying a required prose marker. Opt-in: default registry type remains CLAIM. Activated by the FSD speculative-design book.

### Template / pattern additions
- **`templates/claim-registry.md`** — PROVOCATION row in the Unit Type Reference; PROVOCATION-tier confidence row in the Confidence Tiers table; reflexive-marker required field. Detecting-mistyped-entries decision tree extended (questions 6 and 7).
- **`templates/anti-hallucination.md`** — Step Z (Inverse Hallucination Check, PROVOCATION-specific) added. Catches the failure mode where speculation is presented as if sourced — the opposite of standard citation hallucination.
- **`templates/vv-framework.md` / quality gates** — Three project-conditional gates added:
  - **Gate 2.6 — Reflexivity.** Every PROVOCATION carries a reflexive marker visible in the prose.
  - **Gate 2.7 — Ethical Review.** For projects engaging contested topics (multi-case treatment, paired-mirror rule, no real-world group pathologised).
  - **Gate 2.8 — Voice Consistency.** For voice-driven work (defined voice manifest binding for every chapter).

### Audits added
- **`audits/feedback-from-fsd.md`** — *Fascism Spectrum Disorder* speculative-design book scaffolded against the framework. Tier 1 / Tier 2 / Tier 3 adoption-readiness discipline introduced. Tier 1 (PROVOCATION + tiers + gates + Step Z) lands as v1.1.0; Tier 2 items (multi-reviewer round template; cross-model verification; DR amendment pattern) carried as incubation; Tier 3 patterns (per-chapter obviousness test; compositional discipline; genre-mismatch reception risk; calibration vs awareness) noted but not promoted.

### Framework scope extension
- **`README.md`** — Scope note added: framework now covers non-fiction beyond academic papers. Speculative-design / design-fiction work supported via PROVOCATION opt-in.
- **`docs/METHODOLOGY.md`** — FSD documented as a forward extension; forward-extension pattern itself documented as part of the methodology.

### Adopter notes
- PROVOCATION is opt-in. Projects without speculative-design content can ignore the new unit type, gates 2.6/2.7/2.8, and Step Z entirely. The standard CLAIM / ARGUMENT / PROPOSITION trio remains unchanged.
- Tier 2 / Tier 3 patterns from the FSD audit are deferred until corroborating evidence accumulates (battle-tested-once is not enough for full promotion).

---

## v1.0.0 (2026-05-09)

Baseline release of the framework as developed through 2026-04. Captures the state reached through three retrospective paper-project audits, ten decision records (DR-001 through DR-009 plus DR-010 reserved), 47 indexed literature sources, and active development of Paper 1 (Verification Gap).

### Decisions in scope at v1.0.0
- **DR-001** through **DR-009** as documented in [`decisions/`](decisions/).
- Notable highlights:
  - **DR-002** — Confidence tiers (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) and the language-calibration mapping.
  - **DR-004** — Typed verification model (CLAIM / ARGUMENT / PROPOSITION); reserved slots for DESIGN PRINCIPLE / PROCEDURE / SYNTHESIS for future non-empirical work (DR-010 activates one such slot in v1.1.0).
  - **DR-005** — Nanoarguments / argument-layer peer concept (extended in v1.2.0).
  - **DR-006** — Publication roadmap (Papers 1 / 2 / 3).
  - **DR-007** — SE-inspired verification identity.
  - **DR-008** — Methodological-facts exception for own-data claims.
  - **DR-009** — Calculation verification as distinct procedure (prompt-matters-more-than-model finding).

### Templates in scope at v1.0.0
- `templates/CLAUDE.md` — Paper project identity template.
- `templates/claim-registry.md` — Registry structure with P0/P1/P2 priority, typed verification (legacy single-mixed-type table format; migrated to per-type sub-tables in v1.2.0).
- `templates/vv-framework.md` — Verification & validation framework, quality gates.
- `templates/writing-guide.md` — Confidence-tier to language mapping.
- `templates/review-prompt.md` — Structured peer review simulation (single-shot pre-DR-011).
- `templates/anti-hallucination.md` — Step 0 + 6-step citation verification (pre-Step-Z, pre-Step-7).
- `templates/equation-checker.md` — Mechanical equation verification (DR-009).
- `templates/decision-record.md` — DR template.
- `templates/glossary.md` — Cross-domain terminology.
- `templates/key-quotes.md` — Reference quotes.
- `templates/physics-verification/` — Physics-verification template family (cross-document consistency, scope-domain registry, estimation/limiting-case/dimensional/two-paths checkers, lean-as-optional-tier).

### Audits in scope at v1.0.0
- Three retrospective paper-project audits: proposition (CPR manikin feedback accuracy), technology (IEEE TIM sensor integration), and engineering fidelity (MST manikin characterisation). The engineering-fidelity audits are archived externally as of v1.3.0; the audit findings remain in the framework's history but are no longer carried in the repo.
- `audits/equation-verification-journey.md` — DR-009 discovery log.
- `audits/driven-pendulum-retrofit.md` — Cross-project comparison with the driven-pendulum design project.

### Paper 1 state at v1.0.0
- First draft of `papers/perspective/manuscript.tex` (~3,450 words, 5 sections + Appendix A).
- 19-entry claim registry at 100% coverage (P0 / P1 / P2 all 100%).
- 14 references in `references.bib`, all DOI-verified.
- Anti-hallucination checklist: 14/14 references pass.
- Peer-review simulation: 3.95/5.0 (upper "Minor revision").

### Adopter notes
- v1.0.0 is the baseline pin for adopters who started with this framework before the speculative-design extension. Upgrading to v1.1.0 is opt-in (PROVOCATION is opt-in); upgrading to v1.2.0 brings the multi-pass review pattern as a recommended-but-not-required workflow improvement.

---

*The framework's pre-v1.0.0 history (template extraction from three real paper projects, DR-001 through DR-009 evolution) is documented in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) rather than enumerated as separate version blocks here.*
