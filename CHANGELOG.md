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

## v2.0.0 (2026-06-10)

Repository scope-tightening + README reflection pass. This release is a **MAJOR bump** because two public artifacts have been removed entirely:

- `templates/physics-verification/` — nine-file physics-paper verification template family removed. The methodology lives on conceptually but the template files are no longer shipped.
- `docs/METHODOLOGY.md` — methodology-derivation narrative removed.

In addition, all in-text references to specific source projects and audit findings have been replaced with generic phrasing throughout templates, DRs, and Paper 1 supporting files. The framework now stands on its own design rationale rather than enumerating which projects it was derived from.

### Removed
- **`templates/physics-verification/`** — all nine templates (`cross-document-consistency.md`, `dimensional-checker.md`, `estimation-checker.md`, `lean-as-optional-tier.md`, `limiting-case-checker.md`, `scope-domain-registry.md`, `two-paths-consistency.md`, `verification-tier-hierarchy.md`, `README.md`). Adopters who pinned to v1.7.x and depended on this family must either freeze on v1.7.x or replace with their own equivalents.
- **`docs/METHODOLOGY.md`** — derivation narrative. No replacement; the framework is now described entirely by README + templates + DRs.
- **`audits/`** — directory and its contents are gitignored and no longer published. Adopters do not need this directory.

### Changed — README restructure (front-of-file)
- **Order:** Problem → Approach → When-Worth-It → When-Overkill → Common Questions → Quickstart → (divider) → details. The case is made before the action is asked for.
- **Status hedge:** A new line near the top declares the framework as "a working framework we use on our own papers" with broader empirical validation as an open question. The README's previous confident framing is calibrated.
- **Common Questions** section added: overhead, small-paper applicability, vs. reference managers, non-AI use, peer-review status.
- **One row, concretely** worked-example added to the Verification Registry section so adopters see a populated CLAIM entry inline rather than via a click-through.
- **What Doesn't Work** tightened from eight paragraphs to eight one-liners with backlinks to the explanatory sections.
- **Workflow Phases** consolidated with the former Session Continuity and Project File sections; now includes an explicit Phase→Gate mapping table.
- **Tools cost-log** reframed from "empirical operation costs from Paper 1" to "self-applied cost data (N=2, code-tooling scale)" with honest scope caveats.

### Changed — Paper 1
- **`papers/perspective/manuscript.tex`** — Section 4 (Preliminary Evidence) collapsed from a two-audit case-study presentation into a shorter "Related Work and Design Rationale" section. Appendix A's worked examples are rewritten to use generic illustrations. The paper is publishable as a pure proposal/perspective; the empirical anchors from the source-project audits are removed.
- **Supporting files** (`CLAUDE.md`, `backlog.md`, `backlog-paper2.md`, `writing-guide.md`, `vv/claims/claim_registry.md`) — all audit references removed; sources column reset to "own design rationale" or generic phrasing where source-project citations were used.

### Changed — templates
- **`templates/anti-hallucination.md`** — Step Z worked example uses a generic DSM-form imitation rather than naming a specific speculative-design book.
- **`templates/equation-checker.md`** — origin comment removed (referenced source project).
- **`templates/claim-registry.md`** — inverse-hallucination note genericised.
- **`templates/hypothesis-log.md`** — example tags genericised.
- **`templates/vv-framework.md`** — Gate 2.7 source-pattern pointer removed.

### Changed — DRs
All DRs that referenced audits or specific source projects (DR-004, 006, 007, 008, 009, 010, 011, 012, 013, 014) have had their evidence-base sections, triggering-observation blocks, and audit pointers rewritten. The decisions themselves are unchanged; their evidence narratives are genericised.

### Adopter notes
- **Pinned consumers on v1.7.x using `templates/physics-verification/`**: this is a breaking change. Freeze on v1.7.1 (`git checkout v1.7.1 -- templates/physics-verification/`) or replace with your own family.
- **Pinned consumers on v1.7.x using `docs/METHODOLOGY.md`**: same — freeze or write your own.
- **Pinned consumers using only the core templates** (`CLAUDE.md`, `claim-registry.md`, `vv-framework.md`, `writing-guide.md`, `review-prompt.md`, `decision-record.md`, `anti-hallucination.md`, `glossary.md`, `equation-checker.md`, `cost-log.md`, `hypothesis-log.md`, `key-quotes.md`): templates' contracts are unchanged. Migrate by bumping your pin to `agent-ready-papers: v2.0.0`. The minor template edits (Step Z example, etc.) do not affect the surface adopters consume.

### Origin

This release reflects a deliberate scope-tightening decision. The framework's public artifact is now intentionally smaller and self-contained: it does not point at evidence outside its own files, and it does not enumerate source projects. The README reflection pass that produced the restructure is documented in this session's curate output.

---

## v1.7.1 (2026-06-09)

Companion pin bump: `agent-ready-projects` advanced from v1.10.2 → v1.10.3. Upstream v1.10.3 added structural-lint self-tests at `tests/lint/` — maintainer-only infrastructure with no template-surface change.

### Documentation
- **Root `CLAUDE.md`** — Companion pin: `agent-ready-projects: v1.10.2` → `v1.10.3`. Self-pin: `v1.7.0` → `v1.7.1`.
- **`README.md`** — Current release line bumped to v1.7.1.

### Adopter notes

No action required. PATCH release, metadata-only.

---

## v1.7.0 (2026-06-09)

Full adoption of agent-ready-projects v1.10.0 features. Two upstream additions land here: the **hypothesis log** (provisional positions with pre-registered falsification criteria) and the **self-verifying memory posture** (verify-comments embedded in state claims, audited by `/curate` Step 0 sub-step 5). Companion pin advances to v1.10.2.

The two additions answer different questions. Decision records freeze rationale at decision time; the gotcha log captures problems with known root causes. Neither has a home for *bets* — provisional positions whose evidence lives in the future. Self-verifying memory addresses a different failure mode: state claims in `memory/` decay immediately after the session that writes them.

### Templates
- **`templates/hypothesis-log.md`** — new template, adapted from agent-ready-projects v1.10.0. Lifecycle: open → dormant → revisit → resolved (close or promote to DR). Adopters: copy to your paper project's root and populate.
- **`templates/CLAUDE.md`** — three edits to surface hypothesis-log: new Before You Start row, Key Files row, Directory Structure entry.

### Documentation
- **Root `CLAUDE.md`** — companion pin bumped, self-pin bumped, new Before You Start row for the hypothesis-log, new Hard Constraint for self-verifying memory.

### Adopter notes
- **Recommended migration for pinned consumers on v1.6.3:**
  1. Copy `templates/hypothesis-log.md` to your paper project root.
  2. Add the new Before You Start row in your paper project's `CLAUDE.md` — see updated `templates/CLAUDE.md` for the exact phrasing.
  3. Self-verifying memory: optional and incremental. Add `<!-- verify: cmd -->` comments to new state claims going forward.
- **No template-content breaking changes.**

---

## v1.6.3 (2026-06-08)

Backlog discoverability. Framework backlog is distributed by velocity — `memory/MEMORY.md` "Next session priorities" for volatile near-term items, DR *Open Questions* sections for decision-specific long-burn items. No single `BACKLOG.md` file by design.

### Documentation
- **Root `CLAUDE.md`** — new Before You Start row pointing at the backlog locations with their velocity semantics named.

### Adopter notes
- **No template content changes.** PATCH release.

---

## v1.6.2 (2026-06-08)

Framework convention codification: in-repo memory is canonical for project state.

The conflict: a *global* "you have this memory system" instruction (framed as agent capability, loaded early in the system prompt) versus a *project-level* routing instruction (framed as task trigger). The global one wins by default unless the project explicitly tells the agent otherwise.

### Documentation
- **Root `CLAUDE.md`** — new Hard Constraint: project state goes in `memory/` (in-repo, gitignored), not in user-level Claude Code auto-memory.
- **`templates/CLAUDE.md`** — same constraint, phrased for adopters.

### Adopter notes
- **PATCH release.** No template content changes.
- **Recommended for adopters using Claude Code:** mirror the constraint in your own paper project's `CLAUDE.md`.

---

## v1.6.1 (2026-06-08)

README discoverability fix. v1.5.0 shipped `tools/`, v1.6.0 shipped `templates/cost-log.md` — neither was threaded through the public-facing README.

### Documentation
- **`README.md`** — current-release line bumped; *Anti-Hallucination Checklist* gains an automated-companion note pointing at `python -m tools.check_dois`; new *## Tools* section between *Templates* and *Paper Projects*; *Templates* index gains a row for `cost-log.md`.

### Adopter notes
- **No template content changes.** README-only edits.

---

## v1.6.0 (2026-06-08)

Operation cost logging. New `templates/cost-log.md` template + per-paper `vv/cost-log.md` convention for tracking token cost of major framework operations (review passes, `/curate`, `/audit-context`, batch verification, full Gate sweeps).

### New template
- **`templates/cost-log.md`** — column structure for per-paper operation cost log: date, operation, total tokens, input/output deltas, cache read, wall clock, notes. Top-of-file convention paragraph documents how to use `/status` for the deltas.
- **`papers/perspective/vv/cost-log.md`** — Paper 1 bootstrap data.

### CLAUDE.md updates
- **`templates/CLAUDE.md`** — Before You Start row added: *"Logging token cost of an operation"* → `vv/cost-log.md`.
- **`papers/perspective/CLAUDE.md`** — same row added.

### Adopter notes
- **Optional.** The cost-log is a convention, not a required surface.
- **Recommended** if you want to make decision-record cost-vs-value claims quantitative or if you want to budget framework overhead per paper.

---

## v1.5.1 (2026-06-08)

CLAUDE.md discoverability fix. v1.5.0 shipped the `tools/` directory but did not update any of the three CLAUDE.md files (root, Paper 1, paper template) to point future agent sessions at the tools.

### Documentation
- **Root `CLAUDE.md`:**
  - Architecture diagram — `tools/`, `tests/`, `Makefile`, `pyproject.toml` rows added.
  - Before You Start — two new rows: *"Checking coverage or DOIs in a registry"* and *"Asking what a coverage or peer-review threshold means"*.
  - How to Work Here — replaced the manual percentages comment with `python -m tools.coverage` and `python -m tools.check_dois` commands.
- **`papers/perspective/CLAUDE.md`** — Before You Start gains a row pointing at the tools with the correct registry path.
- **`templates/CLAUDE.md`** — Before You Start gains the same row with adopter-facing path placeholders.

### Adopter notes
- **No template content changes.** Only the agent-orientation tables.

---

## v1.5.0 (2026-06-08)

Registry-verification tooling. The `tools/` directory introduces the first Python footprint in the repo: two zero-dep CLIs that read a `claim_registry.md` and answer two operational questions — *what is my coverage* and *do all my DOIs resolve*.

### New tooling
- **`tools/coverage.py`** — per-type sub-table parser. Walks a claim registry, identifies `**CLAIMs:**` / `**ARGUMENTs**` / `**PROPOSITIONs**` / `**PROVOCATIONs**` sub-tables by marker, counts verified entries. Markdown and JSON output. Exit codes 0 (success) / 1 (with `--strict`, target missed) / 2 (tooling error).
- **`tools/check_dois.py`** — DOI extractor and resolver. Regex-extracts DOIs, HEAD against `https://doi.org/` without redirect-following. `--offline` mode verifies parseability only.
- **`tools/README.md`** — usage, exit codes, design constraints, known limits.
- **`Makefile`, `pyproject.toml`, `.gitignore`** — first Python footprint in the repo: ruff config, pytest config, py3.10 target.
- **`tests/`** — shape-pin tests against the Paper 1 fixture.

### Adopter notes
- **No template changes.** All additions are opt-in tooling.
- **Optional adoption.** If you maintain a `claim_registry.md`, you can run `python -m tools.coverage <your-registry.md>` and `python -m tools.check_dois <your-registry.md>`.
- **Known limits documented in `tools/README.md`.**

---

## v1.4.0 (2026-06-08)

The framework gains a LICENSE (CC BY 4.0), three new top-level docs (`CONTRIBUTING.md`, `UPGRADING.md`, `docs/THRESHOLDS.md`), two new DRs (DR-013 Accepted, DR-014 Proposed), substantially restructured README front-of-file (Quickstart + adoption tiers), and the maintainer release process is codified in this CHANGELOG's header.

### New decisions
- **[DR-013](decisions/DR-013_license-choice.md)** — *License Choice — CC BY 4.0.* Status: Accepted.
- **[DR-014](decisions/DR-014_provocation-layered-as-opt-in-extension.md)** — *PROVOCATION as Explicit Opt-In Extension Over Core Unit Types.* Status: Proposed.

### New top-level files
- **`LICENSE`** — CC BY 4.0 deed + canonical legal-code URL + citation block.
- **`CONTRIBUTING.md`** — contribution guide.
- **`UPGRADING.md`** — per-version adopter-notes aggregation for pinned consumers.

### New docs
- **`docs/THRESHOLDS.md`** — rationale for the 100% P0 / 90% P1 / 70% P2 / ≥85% overall coverage and ≥3.5/5.0 simulated-peer-review thresholds. Top-of-file **SPECULATIVE** label per the framework's own confidence-tier discipline.

### README restructure (front-of-file)
- **## Quickstart + Three tiers of adoption** — 5-step ~10-minute path with the minimum-viable-adoption file table.

### CLAUDE.md changes
- **`.claude/skills/` and `memory/`** in the architecture diagram now labelled as gitignored.
- **New ## What is intentionally not shipped section** — table covering `/curate`, `/audit-context`, `MEMORY.md`, `gotcha-log.md`, `dead-ends.md`.

### Adopter notes
- **No breaking changes.** All adopter-facing changes are additive.
- **DR-013 licence:** new contributions are CC BY 4.0 from v1.4.0 forward.

---

## v1.3.0 (2026-06-01)

DR-012 names decision-support as a third opt-in application class; DR-011 evidence base extended; anti-hallucination gains WebFetch fallback discipline; claim-registry adds Coverage-by-Type cut; Paper 1 registry migrated to per-type sub-tables.

### New decisions
- **[DR-012](decisions/DR-012_decision-support-artefacts.md)** — *Decision-Support Artefacts as Third Non-Paper Application Class.* Status: Proposed.

### New templates / pattern additions
- **`templates/claim-registry.md`** — Coverage Summary now cuts both by Priority and by Type. Type-level Gate 2 expectation: every registered ARGUMENT and PROPOSITION should be `[x]` before gating.
- **`templates/anti-hallucination.md`** — adds *Verifying Web Sources: WebFetch Fallback Discipline* between *Verifying Negative Claims* and Step Z. Names two failure modes (subpage blindspot; transport failure) and prescribes a fallback ladder.

### Paper 1
- **`papers/perspective/vv/claims/claim_registry.md`** — migrated from legacy single-mixed-type table per section to per-type sub-tables (CLAIMs / ARGUMENTs / PROPOSITIONs). List delimiter normalised to `;`. Coverage Summary gains by-type cut.

### Versioning
This is the framework's first explicitly-versioned release. Prior versions (v1.0.0 through v1.2.0 below) are reconstructed retroactively from the git history.

---

## v1.2.0 (2026-05-29)

Multi-pass review pattern + structural rationale + per-type registry surface.

### New decisions
- **[DR-011](decisions/DR-011_multi-model-review-pattern.md)** — *Multi-Model Review Pattern.* Three-pass review with explicit bias-escape semantics: Pass 1 (intra-family small), Pass 2 (intra-family large), Pass 3 (cross-vendor) requires a mandatory style/voice filter. Status: Proposed.

### Template / pattern additions
- **`templates/claim-registry.md`** — per-type sub-tables (one each for CLAIMs / ARGUMENTs / PROPOSITIONs / PROVOCATIONs) with checklist-aligned columns.
- **`templates/writing-guide.md`** — tier-monotonicity principle added: manuscript language must sit at or below the registered confidence tier.
- **`templates/review-prompt.md`** — *Style/voice rules to filter against* added as a required-with-default field per DR-011 Pass 3 requirement.
- **`templates/anti-hallucination.md`** — Step 7 (Multi-Pass Review Across Model Families) added per DR-011.

### Docs / structural rationale
- **`docs/category-theory-as-design-lens.md`** — names the structural lens implicit across DR-004 (typed registry), DR-011 (multi-pass functors), and the layered memory system.

### Adopter notes
- Pre-existing registries with the legacy single-mixed-type table still work; migration to per-type sub-tables is mechanical and recommended at next major revision.

---

## v1.1.0 (2026-05-10)

Speculative-design extension. DR-010 activates DR-004's reserved non-empirical slot with PROVOCATION as a fifth opt-in unit type.

### New decisions
- **[DR-010](decisions/DR-010_provocation-unit-type.md)** — *PROVOCATION as Fifth Unit Type for Speculative-Design Work.* Status: Accepted. Separate confidence axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL), each tier carrying a required prose marker. Opt-in: default registry type remains CLAIM.

### Template / pattern additions
- **`templates/claim-registry.md`** — PROVOCATION row in the Unit Type Reference; PROVOCATION-tier confidence row in the Confidence Tiers table; reflexive-marker required field.
- **`templates/anti-hallucination.md`** — Step Z (Inverse Hallucination Check, PROVOCATION-specific) added. Catches the failure mode where speculation is presented as if sourced.
- **`templates/vv-framework.md` / quality gates** — three project-conditional gates added:
  - **Gate 2.6 — Reflexivity.** Every PROVOCATION carries a reflexive marker visible in the prose.
  - **Gate 2.7 — Ethical Review.** For projects engaging contested topics.
  - **Gate 2.8 — Voice Consistency.** For voice-driven work.

### Adopter notes
- PROVOCATION is opt-in. Projects without speculative-design content can ignore the new unit type, gates 2.6/2.7/2.8, and Step Z entirely.

---

## v1.0.0 (2026-05-09)

Baseline release of the framework. Captures the state reached through DR-001 through DR-009 plus DR-010 reserved, 47 indexed literature sources, and active development of Paper 1 (Verification Gap).

### Decisions in scope at v1.0.0
- **DR-001** through **DR-009** as documented in [`decisions/`](decisions/).
- Notable highlights:
  - **DR-002** — confidence tiers (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) and the language-calibration mapping.
  - **DR-004** — typed verification model (CLAIM / ARGUMENT / PROPOSITION); reserved slots for future non-empirical work (DR-010 activates one such slot in v1.1.0).
  - **DR-005** — nanoarguments / argument-layer peer concept (extended in v1.2.0).
  - **DR-006** — publication roadmap (Papers 1 / 2 / 3).
  - **DR-007** — SE-inspired verification identity.
  - **DR-008** — methodological-facts exception for own-data claims.
  - **DR-009** — calculation verification as distinct procedure.

### Templates in scope at v1.0.0
- `templates/CLAUDE.md` — paper project identity template.
- `templates/claim-registry.md` — registry structure with P0/P1/P2 priority, typed verification (legacy single-mixed-type table format; migrated to per-type sub-tables in v1.2.0).
- `templates/vv-framework.md` — verification & validation framework, quality gates.
- `templates/writing-guide.md` — confidence-tier to language mapping.
- `templates/review-prompt.md` — structured peer review simulation (single-shot pre-DR-011).
- `templates/anti-hallucination.md` — Step 0 + 6-step citation verification (pre-Step-Z, pre-Step-7).
- `templates/equation-checker.md` — mechanical equation verification (DR-009).
- `templates/decision-record.md` — DR template.
- `templates/glossary.md` — cross-domain terminology.
- `templates/key-quotes.md` — reference quotes.
- `templates/physics-verification/` — physics-verification template family.

### Adopter notes
- v1.0.0 is the baseline pin for adopters who started with this framework before the speculative-design extension. Upgrading to v1.1.0 is opt-in (PROVOCATION is opt-in); upgrading to v1.2.0 brings the multi-pass review pattern as a recommended-but-not-required workflow improvement.
</content>
</invoke>