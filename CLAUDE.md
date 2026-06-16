# Agent-Ready Papers

Verification infrastructure for AI-augmented academic and structured non-fiction writing. Templates, quality gates, and session continuity that catch the failure modes automated tools miss — hallucinated citations, confidence inflation, argument quality gaps, and calculation errors. Covers academic papers plus speculative-design / voice-driven non-fiction work (DR-010) and decision-support artefacts (DR-012).

- **Type**: Guide + templates + active paper projects
- **Companion**: [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code)
- **agent-ready-projects**: v1.10.3
- **agent-ready-papers** (this repo): v2.2.4 (2026-06-12 — first end-to-end self-application to a non-paper adopter (dsp-workshop teaching site): syllabus pilot bet registered + resolved HELD, whole-repo V&V sweep, 6 basics claim registries (526 claims); fixes a `tools/coverage.py` escaped-pipe bug it exposed (+2 regression tests); literature L48 (Elsevier *Researcher of the Future* 2025 adoption–trust survey); PATCH)

> Live project state (current paper status, recent decisions, deferred items) lives in `memory/MEMORY.md` (maintainer-local — see *What is intentionally not shipped* below). Release notes live in `CHANGELOG.md`.

## Before You Start

| When | Read |
|------|------|
| Starting any session (companion drift) | Compare the `agent-ready-projects: vX.Y.Z` line in this file's header against `C:/local_dev/agent-ready-projects/CHANGELOG.md` (local clone) or https://github.com/ducroq/agent-ready-projects/blob/master/CHANGELOG.md. If the project is behind the latest released version, briefly surface the drift to the user before starting work. Don't auto-update — adopting changes is the engineer's call. |
| Starting any session (self drift) | Compare the `agent-ready-papers: vX.Y.Z` line in this file's header against `CHANGELOG.md`. If a newer version has shipped, surface it before starting. |
| Working on Paper 1 (Perspective) | `papers/perspective/CLAUDE.md` — paper identity, constraints, status, verification state |
| Making scope or methodology decisions | `decisions/` — 15 decision records (DR-001 through DR-015; DR-014 + DR-015 Proposed) |
| Starting template / DR / verification-gate design work | `memory/dead-ends.md` — pattern proposals already concluded as don't-retry |
| Adding or verifying literature sources | `literature/README.md` — indexed sources organized by topic |
| Checking coverage or DOIs in a registry | Run `python -m tools.coverage <registry.md>` or `python -m tools.check_dois <registry.md>` (or `make coverage` / `make check-dois`). See `tools/README.md` for flags, exit codes, and known limits (no HTTP proxy support, sequential HEAD scaling; escaped-pipe support added in v2.2.4). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs. |
| Working with claims, gates, or confidence calibration | `docs/framework-summary.md` — unit types, gates, tier-to-language mapping at a glance (templates remain normative) |
| Asking what a coverage or peer-review threshold means | `docs/THRESHOLDS.md` — rationale for the 100% P0 / 90% P1 / 70% P2 / ≥85% overall coverage and ≥3.5/5.0 simulated-peer-review thresholds (top-of-file SPECULATIVE label per the framework's own tier discipline) |
| Asking what's on the backlog | No single `BACKLOG.md` by design — framework backlog is distributed by velocity: `memory/MEMORY.md` "Next session priorities" for volatile near-term items (maintainer-local); each `decisions/DR-*.md` *Open Questions* section for decision-specific long-burn items. Paper projects have their own `papers/<name>/backlog.md` for paper-scoped tasks. Forcing items at different velocities into one file creates drift; this row is the discoverability fix instead. |
| Stuck or debugging something weird | `memory/gotcha-log.md` — problem-fix archive |
| Placing a bet whose evidence lives in the future | `memory/hypothesis-log.md` — provisional positions with `Position` / `Method` / `Revisit trigger` / `Review by`. `/curate` surfaces due items. Adopted from agent-ready-projects v1.10.0 in this repo's v1.7.0. Paper projects: copy `templates/hypothesis-log.md`. |
| Creating a new paper project | `templates/CLAUDE.md` — paper project template (includes hypothesis-log row since v1.7.0) |
| Running a portable agent-role prompt (equation verifier, peer reviewer) | `agents/` — copy the prompt into any agent's system-prompt slot; works with Claude Code, GitHub Copilot CLI, Cursor, Gemini, ChatGPT, etc. (since v2.1.0) |
| Using the framework with an agent other than Claude Code | `docs/non-claude-setup.md` — universal pattern + tool-specific entry points for Copilot CLI / Cursor / Continue / Aider / web chat; lists the per-tool behaviours adopters should verify (since v2.1.1) |
| Ending a session | Run `/curate` — updates gotcha log, promotes patterns, syncs docs, checks freshness |
| Monthly or after major restructuring | Run `/audit-context` — structural health check for duplication, bloat, broken references |

## Hard Constraints

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows") for claims below SUPPORTED tier
- Never skip the anti-hallucination checklist for AI-introduced citations
- Decision records are binding — check `decisions/` before proposing scope changes
- This repo contains both the framework AND papers that use it — changes to templates may affect active papers
- **Project state goes in `memory/` (in-repo, gitignored — see *What is intentionally not shipped*), not in any agent's user-level auto-memory.** Versions, session narratives, gotchas, priorities, handoffs, and any state tied to *this* repo's work belong in this repo's `memory/` directory. The principle applies most directly to agents with **cross-project user-level memory** — Claude Code (`~/.claude/projects/<slug>/memory/`), ChatGPT memory, Gemini Gems — where state can leak across projects without an explicit boundary. Agents with only project-level rules files (Cursor's `.cursorrules`, GitHub Copilot's `.github/copilot-instructions.md`, Continue's `.continue/config.json`) inherit the principle vacuously since they have no cross-project store to spill into. The Before You Start table above routes to in-repo memory; that's the canonical pickup path. Don't duplicate project state into both — drift starts as soon as you do. (Generalised to all agents in v2.1.0; narrowed in v2.2.0 to acknowledge which agents have the failure mode the principle prevents; original Claude-Code-only form added in v1.6.2.)
- **New state claims in `memory/` may embed a verification command in an HTML comment: `<!-- verify: cmd -->`.** `/curate` Step 0 sub-step 5 runs the command on read and flags drift (PASS / FAIL / ERROR / MANUAL). Convention applies to *new* claims going forward; no retrofit required for existing entries — opportunistic retrofit during routine edits is welcome but not gated. Adopted from agent-ready-projects v1.9.0 (self-verifying memory) + v1.10.0 (/curate audit hook) in this repo's v1.7.0.

## Architecture

```
agent-ready-papers/
├── .claude/skills/            <- Maintainer slash commands (gitignored — not shipped)
├── README.md                  <- The guide (public-facing)
├── CHANGELOG.md               <- Versioned release notes (v1.0.0 onwards)
├── CLAUDE.md                  <- This file (agent orientation)
├── LICENSE                    <- CC BY 4.0 (see DR-013)
├── CONTRIBUTING.md            <- Three-audience contribution guide
├── UPGRADING.md               <- Per-version adopter notes (pinned consumers)
├── Makefile                   <- Tooling targets: test / lint / format / coverage / check-dois (since v1.5.0)
├── pyproject.toml             <- Python tooling config: ruff + pytest, py3.10 target (since v1.5.0)
├── agents/                    <- Portable agent-role prompts (since v2.1.0; mirrors agent-ready-assessment)
│   ├── README.md              <- Directory purpose; line between role prompts and fill-in templates
│   ├── equation-checker.md    <- Mechanical equation & numerical verifier (was templates/equation-checker.md)
│   └── review-prompt.md       <- Peer-review simulator with multi-pass bias-escape (was templates/review-prompt.md)
├── templates/                 <- Fill-in templates for new paper projects
│   ├── CLAUDE.md              <- Paper project identity template
│   ├── claim-registry.md      <- Registry structure (P0/P1/P2, typed verification)
│   ├── vv-framework.md        <- Verification & validation framework
│   ├── writing-guide.md       <- Confidence tier to language mapping
│   ├── anti-hallucination.md  <- Step 0 + 6-step citation verification checklist
│   ├── glossary.md            <- Cross-domain terminology
│   ├── decision-record.md     <- DR template
│   ├── hypothesis-log.md      <- Provisional positions with future evidence (since v1.7.0)
│   └── key-quotes.md          <- Reference quotes
├── decisions/                 <- Architecture decision records (DR-001 to DR-015)
├── literature/                <- Source registry
├── docs/                      <- Framework summary, threshold rationale, category-theory lens
├── tools/                     <- Registry tooling: coverage + DOI verification CLIs (since v1.5.0)
│   ├── coverage.py            <- Per-type sub-table parser; P0/P1/P2 + PROVOCATION tier coverage
│   ├── check_dois.py          <- DOI extractor + resolver (HEAD against doi.org, --offline mode)
│   └── README.md              <- Usage, exit codes, design constraints, known limits
├── tests/                     <- Shape-pin + edge-case tests for tools/ (since v1.5.0)
├── papers/
│   └── perspective/           <- Paper 1: "The Verification Gap" (active)
│       ├── CLAUDE.md          <- Paper-specific context (READ THIS for paper work)
│       ├── manuscript.tex     <- LaTeX source (~3,450 words)
│       ├── references.bib     <- 14 entries, all DOI-verified
│       ├── vv/claims/         <- Claim registry (19 entries, 100% verified)
│       └── ...
├── vv/                        <- Framework self-application (since v2.2.0; public)
│   ├── cost-log.md            <- Operation cost log — framework operations on the framework
│   └── hypothesis-log.md      <- Public framework-level provisional positions (where load-bearing README prose depends on a falsifiable bet)
├── audits/                    <- Audits of external/published docs (gitignored — maintainer-local; may critique named authors)
└── memory/                    <- Session memory (gitignored — maintainer-local)
    ├── gotcha-log.md          <- Problem-fix archive
    ├── hypothesis-log.md      <- Maintainer-local intra-session bets (since v1.7.0; complement to vv/hypothesis-log.md which is public)
    └── ...
```

## What is intentionally not shipped

These paths exist in the maintainer's local clone but are gitignored — they are *not* in the public repo:

| Path | What it holds | For adopters |
|------|---------------|--------------|
| `.claude/skills/curate/` | `/curate` slash command (session-end maintenance) | Optional — the README and templates already document what the skill does |
| `.claude/skills/audit-context/` | `/audit-context` slash command (structural health check) | Optional — same |
| `memory/MEMORY.md` | Maintainer's index of current project state and deferred items | Not needed — equivalent state for your paper lives in your paper's CLAUDE.md |
| `memory/gotcha-log.md` | Maintainer's problem-fix archive | Build your own per-project |
| `memory/dead-ends.md` | Maintainer's "don't retry" log | Build your own per-project |
| `memory/hypothesis-log.md` | Maintainer's intra-session framework bets (working positions) | Adopters maintain their own per `templates/hypothesis-log.md`; the *public* framework-level positions are at `vv/hypothesis-log.md`, which IS shipped |
| `audits/` | Maintainer-local audits applying the framework to *external / published* documents (dogfooding on third-party material). May critique named authors, so kept private by default | Not needed — run your own audits locally; un-ignore per-folder only with the author's awareness if you intend to publish |

The public framework — templates, DRs, README, CHANGELOG — is fully consumable without any of the above. Adopters maintain their own session state per the patterns in `templates/CLAUDE.md`, not by depending on the maintainer's `memory/`.

Listed here so the architecture diagram above is honest about what an adopter sees on `git clone` versus what the maintainer has on disk.

## Key Paths

| Path | What it is |
|------|-----------|
| `papers/perspective/CLAUDE.md` | Paper 1 project context — start here for paper work |
| `papers/perspective/manuscript.tex` | Paper 1 LaTeX source |
| `papers/perspective/vv/claims/claim_registry.md` | Paper 1 claim registry (19 entries) |
| `papers/perspective/backlog.md` | Paper 1 current tasks and priorities |
| `decisions/DR-004_registry-model-for-non-empirical-papers.md` | Most consequential DR — typed verification model |
| `decisions/DR-006_publication-roadmap.md` | Publication sequencing (Papers 1-3) |
| `literature/README.md` | Master source index (48 entries) |
| `templates/CLAUDE.md` | Template for new paper projects |

## How to Work Here

```bash
# Compile Paper 1 (LaTeX)
cd papers/perspective && pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript

# Check claim registry coverage (since v1.5.0)
python -m tools.coverage papers/perspective/vv/claims/claim_registry.md
# or: make coverage
# --strict makes the call fail if P0=100% / P1=90% / P2=70% thresholds are missed

# Verify DOIs in a registry resolve at doi.org (since v1.5.0)
python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md
# or: make check-dois  (use --offline to skip network)

# Verify a citation (anti-hallucination)
# Follow the Step 0 + 6-step checklist in papers/perspective/anti-hallucination.md

# Run peer review simulation
# Use papers/perspective/review-prompt.md with the three-pass pattern (DR-011): Pass 1 intra-family small, Pass 2 intra-family large, Pass 3 cross-vendor (high-stakes only, with style filter)
```

## Cross-Repo Evidence

This project is a source project for [agentic-engineering](https://github.com/ducroq/agentic-engineering) — a proposition about what's new when engineers work with AI agents. When you discover evidence relevant to the four patterns (verification findings, context architecture lessons, reproduce-don't-assess examples, LLM behavioral properties), file an issue at `ducroq/agentic-engineering` with the pattern name, quantified results, and which claims it supports.
