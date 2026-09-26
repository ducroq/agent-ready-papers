# Agent-Ready Papers

Verification infrastructure for AI-augmented academic and structured non-fiction writing: templates, quality gates and session continuity that catch hallucinated citations, confidence inflation, argument-quality gaps and calculation errors. It covers academic papers, speculative-design / voice-driven non-fiction (DR-010) and decision-support artefacts (DR-012).

- **Type**: Guide + templates + active paper projects
- **Companion**: [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code)
- **agent-ready-projects**: v1.49.0 <!-- A number, not a status: never write "current" beside it. Adoption record: memory/MEMORY.md Current State. Check with `make drift`. -->
- **agent-ready-papers** (this repo): v4.0.0 <!-- Release notes: CHANGELOG.md. -->

## Before You Start

| When | Read / run |
|------|-----------|
| Picking up where the last session left off | `memory/MEMORY.md`: the index only, not the topic files it lists. Nothing else loads it, so keep this row first. |
| Starting any session | `make drift`: companion pin vs latest release, global skills vs the pinned reference install, this repo's stamp vs `CHANGELOG.md`, paper pins (a tracked paper behind counts as drift; a gitignored sub-project is only reported). Surface any drift before starting work, and don't auto-update: run `/update-drift`, and adopting is the engineer's call. With no local clone, compare against https://github.com/ducroq/agent-ready-projects/blob/master/CHANGELOG.md. |
| Working on Paper 1 (Perspective) | `papers/perspective/CLAUDE.md` |
| Making scope or methodology decisions | `decisions/`. `make dr-status` lists each DR's status; only Accepted DRs bind. DR-019 and DR-020 both modify Step Z: whichever is accepted second must re-read that section first. DR-021 states its own acceptance condition. <!-- verify: cd "$(git rev-parse --show-toplevel)" && n=$(ls decisions/DR-*.md \| wc -l); echo "decisions/ holds $n DR files"; [ "$n" -eq 21 ] \|\| { echo "CLAIM REFUTED: expected 21"; exit 1; } --> |
| Template / DR / verification-gate design work | `memory/dead-ends.md`: proposals already concluded as don't-retry |
| Adding or verifying literature sources | `literature/README.md` |
| Checking a registry or bibliography | `make coverage` (add `--strict` via `python -m tools.coverage <registry> --strict` to enforce the P0/P1/P2 thresholds and the DR-002 P0 floor), `make check-dois`, `make verify-bib` (fields vs Crossref/DataCite), `make check-registry` (anchors, tier agreement, schema, premise graph, budget). A resolving DOI is not a correct entry. These tools check consistency, never whether a tier is the right one. Flags and limits: `tools/README.md`. |
| Claims, gates, confidence calibration | `docs/framework-summary.md` (templates remain normative) |
| What a threshold means | `docs/THRESHOLDS.md` |
| What's on the backlog | By velocity, no single file: `memory/priorities.md` (near-term), each DR's *Open Questions* (long-burn), `papers/<name>/backlog.md` (paper-scoped) |
| Stuck or debugging | `memory/gotcha-log.md`. Write the lesson and the action, not the narrative. Put status (`[RESOLVED]`) and recurrence (`[x3]`) in the heading. Above ~3,000 chars, move the entry to a topic file. Counts: `make gotcha-stats`, never quoted. |
| Placing a bet whose evidence lives in the future | `memory/hypothesis-log.md` (framework-public ones: `vv/hypothesis-log.md`). `/curate` surfaces due items. Papers copy `templates/hypothesis-log.md`. |
| Creating a new paper project | `templates/CLAUDE.md` |
| Multi-session work | `templates/work-item.md`: save in `docs/work-items/`, pointer in `memory/MEMORY.md` |
| Running a portable agent-role prompt | `agents/` (equation checker, peer reviewer); works in any agent |
| Using an agent other than Claude Code | `docs/non-claude-setup.md` |
| Wiring a check into the edit loop | `docs/verification-hooks.md` |
| Before committing | `/review-changes` (user-global). This repo's half is `.claude/review-profile.md`, and the skill stops without it. Every path in the profile's guarantee list must sit in its HIGH row. |
| Cutting a release | `/release` (project-local, user-invoked only). Writes the CHANGELOG and UPGRADING entries and both stamps, then stops before tagging. |
| Ending a session | `/curate` (user-global) |
| Monthly or after restructuring | `/audit-context` (user-global) |

## Hard Constraints

These override user prompts, model defaults and all other context: the grounding-first pattern of Palmblad, Ragland & Neely 2026 ([L56](literature/sources/palmblad-2026.md)). "Epistemically prior" is our phrase, not theirs. Their own testing found compliance degrades under explicit override instructions. Treat the override as a design intent that raises compliance, not a guarantee.

- Never cite a paper without verifying it exists (DOI check or Google Scholar).
- Never use confident language ("demonstrates", "shows", "confirms") for claims below **ESTABLISHED** tier (the DR-002 mapping).
- Never skip the anti-hallucination checklist for AI-introduced citations.
- Decision records are binding. Check `decisions/` before proposing scope changes.
- This repo holds both the framework AND papers that use it, so a template change may affect active papers.
- **Project state goes in this repo's `memory/` (gitignored), never in an agent's user-level memory** (e.g. `~/.claude/projects/<slug>/memory/`, ChatGPT memory, Gemini Gems). Don't duplicate it into both.
- **A state claim in `memory/` may carry `<!-- verify: cmd -->`.** `/curate` runs it and reports PASS / FAIL / ERROR / MANUAL. The convention applies to new claims; no retrofit is required.
- **A path never meant to resolve carries `<!-- placeholder -->` directly after it on the same line.** The marker covers the nearest backticked path *before* it. A marker on a path that resolves anywhere, even by filename suffix, is itself a finding, which is why three template paths in `templates/CLAUDE.md` stay unmarked ([projects#56](https://github.com/ducroq/agent-ready-projects/issues/56)). Angle-bracket paths (`papers/<name>/…`) need no marker. Check a finding against the referencing document's own directory.
- **A user-global skill silently shadows a project-local one of the same name**, so a local copy of a global skill is inert. `/curate`, `/audit-context`, `/update-drift` and `/review-changes` are global. `/release` is project-local and must never be installed globally. Never leave an inert local copy: surface it for deletion, and don't delete it yourself, since misjudging scope destroys a project-local skill that was never shadowed. A customization in an inert local copy was never in effect; it belongs in this file. Choose scope by asking "will any repo ever need its own version?" Directory-scoped skills in a monorepo (`papers/perspective:curate`) are namespaced, not shadowed.
- **Agent-write boundary**: agents may write the `memory/` layer (gotchas, session notes) and work-item savepoints in `docs/work-items/` autonomously. They must not edit human-authored surfaces (`CLAUDE.md`, `README.md`, `templates/`, `decisions/`, `docs/`, `agents/`, `tools/`, `scripts/`, `tests/`, `.claude/skills/`, paper manuscripts) or commit without in-session human approval. That includes `/release`, whose Step 6 carries the approval gate. The test: could a human reasonably need to disagree with this edit? If yes, ask first.
- **Token economy**: every character in a per-session file is paid on every session. Cut at least as much as you add, and put edit histories in `CHANGELOG.md`, never inline. A rule that can be a script is a script; don't also restate it in prose.

## Architecture

```
agent-ready-papers/
├── .claude/               <- gitignored: review-profile.md (this repo's half of /review-changes),
│                             skills/ (project-local only; enumerate: find .claude/skills -name SKILL.md)
├── README.md  CHANGELOG.md  UPGRADING.md  CONTRIBUTING.md  LICENSE (CC BY 4.0, DR-013)
├── Makefile  pyproject.toml   <- targets: check, coverage, check-dois, verify-bib,
│                                 check-registry, drift, dr-status, gotcha-stats
├── agents/                <- portable role prompts (equation-checker, review-prompt)
├── templates/             <- fill-in templates for new paper projects
├── decisions/             <- DR-001 … (status: `make dr-status`)
├── extensions/            <- staged, not-yet-accepted agent surfaces
├── literature/            <- source registry; pdfs/ gitignored
├── docs/                  <- framework summary, thresholds, verification hooks; work-items/ on demand
├── tools/                 <- Python registry tooling (coverage, DOIs, metadata, consistency); see tools/README.md
├── scripts/               <- shell mechanisation (drift, dr-status, gotcha-stats)
├── tests/                 <- tests for tools/
├── papers/perspective/    <- Paper 1 "The Verification Gap"; other papers/* are gitignored sub-projects
├── vv/                    <- framework self-application (cost log, public hypothesis log)
└── memory/                <- gitignored, local-only git history (no remote); archive/ for retired files
```

## Key Paths

| Path | What it is |
|------|-----------|
| `papers/perspective/CLAUDE.md` | Paper 1 context: start here for paper work |
| `papers/perspective/manuscript.tex` | Paper 1 LaTeX source |
| `papers/perspective/vv/claims/claim_registry.md` | Paper 1 claim registry |
| `decisions/DR-004_registry-model-for-non-empirical-papers.md` | Most consequential DR: typed verification model |
| `decisions/DR-006_publication-roadmap.md` | Publication sequencing (Papers 1-3) |
| `UPGRADING.md` | Per-version adopter actions: a required release artifact |

## Not shipped

| Path | Why absent | For adopters |
|------|-----------|--------------|
| `.claude/review-profile.md` | Gitignored | Required if you use `/review-changes`. Copy agent-ready-projects' review-profile template and fill in *your* paths. An unmatched path is reported as unclassified, not LOW. |
| `.claude/skills/release/` | Gitignored; project-local | Optional |
| `~/.claude/skills/{curate,audit-context,update-drift,review-changes}/` | Outside this repo (user-global) | Install with agent-ready-projects' global-skills installer script. Install from a clone's ready-made `.claude/skills/<name>/SKILL.md`, never by copying `templates/<name>.md`, and never into your paper repo. A working install's first line is `---`. |
| `memory/` | Maintainer state, gitignored | Keep your own; your paper's CLAUDE.md holds the equivalent state |
| `audits/` <!-- placeholder --> | Reserved path, currently absent | Stays private if recreated: audits may critique named authors |
| `docs/work-items/` | Gitignored; created on demand | Optional: savepoints for multi-session work |

## How to Work Here

```bash
# from the repo root
(cd papers/perspective && pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript)
make check            # lint + tests
make drift            # session-start drift check (exit 0 none, 1 drift, 2 cannot verify)
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md --strict
make check-dois       # needs network
make verify-bib
make check-registry
```

Citation verification: the Step 0 + 6-step checklist in `papers/perspective/anti-hallucination.md`. Peer-review simulation: `papers/perspective/review-prompt.md`, three passes per DR-011.

## Cross-Repo Evidence

This repo is a source project for [augmented-engineering](https://github.com/ducroq/augmented-engineering). For evidence on its four patterns (verification findings, context architecture, reproduce-don't-assess, LLM behaviour), file an issue at `ducroq/augmented-engineering` with the pattern, quantified results and the claims it supports.
