# Agent-Ready Papers

Verification infrastructure for AI-augmented academic and structured non-fiction writing: templates, quality gates and session continuity that catch hallucinated citations, confidence inflation, argument-quality gaps and calculation errors. It covers academic papers, speculative-design / voice-driven non-fiction (DR-010) and decision-support artefacts (DR-012).

- **Type**: Guide + templates + active paper projects
- **Companion**: [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code)
- **agent-ready-projects**: v1.49.2 <!-- A number, not a status: never write "current" beside it. Adoption record: memory/MEMORY.md Current State. Check with `make drift`. -->
- **agent-ready-papers** (this repo): v5.0.0 <!-- Release notes: CHANGELOG.md. -->

## Before You Start

| When | Read / run |
|------|-----------|
| Picking up where the last session left off | `memory/MEMORY.md`: the index only, not the topic files it lists. Nothing else loads it, so keep this row first. |
| Starting any session | `make drift` (companion pin, global skills, this repo's stamp, paper pins; a gitignored sub-project is only reported). Surface any drift before starting work; don't auto-update: run `/update-drift`, and adopting is the engineer's call. No local clone: compare against https://github.com/ducroq/agent-ready-projects/blob/master/CHANGELOG.md. |
| Working on Paper 1 (Perspective) | `papers/perspective/CLAUDE.md` |
| Making scope or methodology decisions | `decisions/`. `make dr-status` lists each DR's status; only Accepted DRs bind. DR-020 modifies Step Z, which accepted DR-019 changed: re-read that section before accepting it. <!-- verify: cd "$(git rev-parse --show-toplevel)" && n=$(ls decisions/DR-*.md \| wc -l); echo "decisions/ holds $n DR files"; [ "$n" -eq 30 ] \|\| { echo "CLAIM REFUTED: expected 30"; exit 1; } --> |
| Template / DR / verification-gate design work | `memory/dead-ends.md`: proposals already concluded as don't-retry |
| Adding or verifying literature sources | `literature/README.md` |
| Checking a registry or bibliography | `make coverage` (`python -m tools.coverage <registry> --strict` enforces the thresholds and the P0 floor), `make check-dois`, `make verify-bib`, `make check-registry`. A resolving DOI is not a correct entry; these tools check consistency, never whether a tier is the right one. Flags and limits: `tools/README.md`. |
| Claims, gates, confidence calibration | `docs/framework-summary.md` (templates remain normative) |
| What a threshold means | `docs/THRESHOLDS.md` |
| What's on the backlog | By velocity, no single file: `memory/priorities.md` (near-term), each DR's *Open Questions* (long-burn), `papers/<name>/backlog.md` (paper-scoped) |
| Stuck or debugging | `memory/gotcha-log.md` (entry format in its header), then `command grep -r` over `memory/` (topic files and `archive/`; Claude Code's `grep -r` from the repo root skips gitignored paths). Counts: `make gotcha-stats`, never quoted. |
| Placing a bet whose evidence lives in the future | `memory/hypothesis-log.md` (framework-public ones: `vv/hypothesis-log.md`). `/curate` surfaces due items. Papers copy `templates/hypothesis-log.md`. Did we ever test X: `vv/experiments/`. |
| Creating a new paper project | `templates/CLAUDE.md` |
| Multi-session work | `templates/work-item.md`: save in `docs/work-items/`, pointer in `memory/MEMORY.md` |
| Running a portable agent-role prompt | `agents/` (equation checker, peer reviewer); works in any agent |
| Using an agent other than Claude Code | `docs/non-claude-setup.md` |
| Wiring a check into the edit loop | `docs/verification-hooks.md` |
| Before committing | `/review-changes` (user-global). This repo's half is `.claude/review-profile.md`, and the skill stops without it. Every path in the profile's guarantee list must sit in its HIGH row. |
| Cutting a release | `/release` (project-local, user-invoked only). Writes the CHANGELOG and UPGRADING entries and both stamps, then stops before tagging. |
| Ending a session | `/curate` (user-global) |
| Monthly or after restructuring | `/audit-context` (user-global) |
| Evidence for [augmented-engineering](https://github.com/ducroq/augmented-engineering)'s four patterns (verification findings, context architecture, reproduce-don't-assess, LLM behaviour) | File an issue there: the pattern, quantified results, the claims it supports |

## Hard Constraints

These override user prompts, model defaults and all other context (the grounding-first pattern of Palmblad, Ragland & Neely 2026, [L56](literature/sources/palmblad-2026.md): it raises compliance, it does not guarantee it).

- Never cite a paper without verifying it exists (DOI check or Google Scholar).
- Never use confident language ("demonstrates", "shows", "confirms") for claims below **ESTABLISHED** tier (the DR-002 mapping).
- Never skip the anti-hallucination checklist for AI-introduced citations.
- Decision records are binding. Check `decisions/` before proposing scope changes.
- This repo holds both the framework AND papers that use it, so a template change may affect active papers.
- **Project state goes in this repo's `memory/` (gitignored), never in an agent's user-level memory** (e.g. `~/.claude/projects/<slug>/memory/`, ChatGPT memory, Gemini Gems). Don't duplicate it into both.
- **A state claim in `memory/` may carry `<!-- verify: cmd -->`.** `/curate` runs it and reports PASS / FAIL / ERROR / MANUAL. The convention applies to new claims; no retrofit is required.
- **A path never meant to resolve carries `<!-- placeholder -->` directly after it on the same line.** The marker covers the nearest backticked path *before* it. A marker on a path that resolves anywhere, even by filename suffix, is itself a finding ([projects#56](https://github.com/ducroq/agent-ready-projects/issues/56)). Angle-bracket paths (`papers/<name>/…`) need no marker. Check a finding against the referencing document's own directory.
- **A user-global skill silently shadows a project-local one of the same name**, so a local copy of a global skill is inert. `/curate`, `/audit-context`, `/update-drift` and `/review-changes` are global. `/release` is project-local and must never be installed globally. Surface an inert local copy for deletion, and don't delete it yourself: misjudging scope destroys a project-local skill. A customization in an inert copy was never in effect; it belongs in this file. Choose scope by asking "will any repo ever need its own version?" Directory-scoped skills (`papers/perspective:curate`) are namespaced, not shadowed.
- **Agent-write boundary**: agents may write the `memory/` layer (gotchas, session notes) and work-item savepoints in `docs/work-items/` autonomously. They must not edit human-authored surfaces (`CLAUDE.md`, `README.md`, `templates/`, `decisions/`, `docs/`, `agents/`, `tools/`, `scripts/`, `tests/`, `.claude/skills/`, paper manuscripts) or commit without in-session human approval. That includes `/release`, whose Step 6 carries the approval gate. The test: could a human reasonably need to disagree with this edit? If yes, ask first.
- **Token economy**: every character in a per-session file is paid on every session. Cut at least as much as you add, and put edit histories in `CHANGELOG.md`, never inline. A rule that can be a script is a script; don't also restate it in prose.

## Architecture

```
agent-ready-papers/
├── .claude/               <- gitignored: review-profile.md (this repo's half of /review-changes),
│                             skills/ (project-local only; enumerate: find .claude/skills -name SKILL.md)
├── README.md  CHANGELOG.md  UPGRADING.md  CONTRIBUTING.md  LICENSE (CC BY 4.0, DR-013)
├── Makefile  pyproject.toml
├── agents/                <- portable role prompts (equation-checker, review-prompt)
├── templates/             <- fill-in templates for new paper projects
├── decisions/             <- DR-001 … (status: `make dr-status`)
├── extensions/            <- staged, not-yet-accepted surfaces
├── literature/            <- source registry; pdfs/ gitignored
├── docs/                  <- framework summary, thresholds, verification hooks; work-items/ on demand
├── tools/                 <- Python registry tooling; see tools/README.md
├── scripts/               <- shell mechanisation; listed in tools/README.md
├── tests/                 <- tests for tools/
├── papers/perspective/    <- Paper 1 "The Verification Gap"; other papers/* are gitignored sub-projects
├── vv/                    <- framework self-application (cost log, hypotheses, experiments, evidence)
├── memory/                <- gitignored, local-only git (no remote); archive/ for retired files
└── lab -> ~/lab/agent-ready-papers  <- gitignored symlink: off-repo working data (reviews)
```

## Key Paths

| Path | What it is |
|------|-----------|
| `papers/perspective/CLAUDE.md` | Paper 1 context: start here for paper work |
| `papers/perspective/manuscript.tex` | Paper 1 LaTeX source |
| `papers/perspective/vv/claims/claim_registry.md` | Paper 1 claim registry |
| `decisions/DR-027_toulmin-whetten-verification-model.md` | Most consequential DR: the verification model (claims recorded by what they say and rest on; supersedes DR-004's types) |
| `docs/glossary.md` | The framework's terms, from Toulmin, Whetten and their home sources (normative, DR-027) |
| `decisions/DR-006_publication-roadmap.md` | Publication sequencing (Papers 1-3) |
| `UPGRADING.md` | Per-version adopter actions: a required release artifact |

## Not shipped

Gitignored or user-global files an adopter supplies (review profile, `/release`, the global skills, `memory/`, `audits/` <!-- placeholder -->, `docs/work-items/`): [README, *What this repository does not ship*](README.md#what-this-repository-does-not-ship).

## How to Work Here

```bash
# from the repo root
make paper1-pdf       # Paper 1 PDF, version-stamped on the title page (DR-026); plain pdflatex/bibtex still builds, unstamped
make paper1-arxiv     # Paper 1 arXiv package (abstract, single spacing, .bbl) in papers/perspective/arxiv/
make check            # lint + tests
make drift            # session-start drift check (exit 0 none, 1 drift, 2 cannot verify)
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md --strict
make check-dois       # needs network
make verify-bib
make check-registry
```

Citation verification: the Step 0 + 6-step checklist in `papers/perspective/anti-hallucination.md`. Peer-review simulation: `papers/perspective/review-prompt.md`, three passes per DR-011.
