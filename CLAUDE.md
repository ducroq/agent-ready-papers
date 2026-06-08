# Agent-Ready Papers

Verification infrastructure for AI-augmented academic and structured non-fiction writing. Templates, quality gates, and session continuity that catch the failure modes automated tools miss — hallucinated citations, confidence inflation, argument quality gaps, and calculation errors. Originally developed for academic papers; extended in 2026-05 to cover speculative-design and voice-driven non-fiction work (DR-010).

- **Type**: Guide + templates + active paper projects (non-fiction projects supported via DR-010 but currently external — e.g., FSD; decision-support work supported via DR-012)
- **Companion**: [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code)
- **agent-ready-projects**: v1.7.0
- **agent-ready-papers** (this repo): v1.4.0 (external-feedback-driven release, 2026-06-08)

> Live project state (current paper status, recent decisions, deferred items) lives in `memory/MEMORY.md` (maintainer-local — see *What is intentionally not shipped* below). Repo-name caveat and FSD-rename deferral are tracked in `audits/feedback-from-fsd.md`. Release notes live in `CHANGELOG.md`.

## Before You Start

| When | Read |
|------|------|
| Starting any session (companion drift) | Compare the `agent-ready-projects: vX.Y.Z` line in this file's header against `C:/local_dev/agent-ready-projects/CHANGELOG.md` (local clone) or https://github.com/ducroq/agent-ready-projects/blob/master/CHANGELOG.md. If the project is behind the latest released version, briefly surface the drift to the user before starting work. Don't auto-update — adopting changes is the engineer's call. |
| Starting any session (self drift) | Compare the `agent-ready-papers: vX.Y.Z` line in this file's header against `CHANGELOG.md`. If a newer version has shipped, surface it before starting. |
| Working on Paper 1 (Perspective) | `papers/perspective/CLAUDE.md` — paper identity, constraints, status, verification state |
| Making scope or methodology decisions | `decisions/` — 14 decision records (DR-001 through DR-014; DR-014 Proposed, gated on Paper 1 / FSD / version-impact checks per #18) |
| Starting template / DR / verification-gate design work | `memory/dead-ends.md` — pattern proposals already concluded as don't-retry (#15) |
| Adding or verifying literature sources | `literature/README.md` — 47 indexed sources organized by topic |
| Understanding how the framework was built | `docs/METHODOLOGY.md` — derived from two source paper projects (third source-project audit archived externally in v1.3.0) |
| Reviewing audit evidence | `audits/` — 9 audits: retrofits of source projects (proposition, technology) + cross-project comparisons (driven-pendulum) + forward-feedback applications (FSD, blog, template-revision, decision-support). Grant-application feedback lives in [ducroq/agent-ready-papers#8](https://github.com/ducroq/agent-ready-papers/issues/8). |
| Working with claims, gates, or confidence calibration | `docs/framework-summary.md` — unit types, gates, tier-to-language mapping at a glance (templates remain normative) |
| Stuck or debugging something weird | `memory/gotcha-log.md` — problem-fix archive |
| Creating a new paper project | `templates/CLAUDE.md` — paper project template |
| Ending a session | Run `/curate` — updates gotcha log, promotes patterns, syncs docs, checks freshness |
| Monthly or after major restructuring | Run `/audit-context` — structural health check for duplication, bloat, broken references |

## Hard Constraints

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows") for claims below SUPPORTED tier
- Never skip the anti-hallucination checklist for AI-introduced citations
- Decision records are binding — check `decisions/` before proposing scope changes
- This repo contains both the framework AND papers that use it — changes to templates may affect active papers

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
├── templates/                 <- Reusable templates for new paper projects
│   ├── CLAUDE.md              <- Paper project identity template
│   ├── claim-registry.md      <- Registry structure (P0/P1/P2, typed verification)
│   ├── vv-framework.md        <- Verification & validation framework
│   ├── writing-guide.md       <- Confidence tier to language mapping
│   ├── review-prompt.md       <- Structured peer review simulation
│   ├── anti-hallucination.md  <- Step 0 + 6-step citation verification checklist
│   ├── equation-checker.md    <- Mechanical equation verification prompt
│   ├── glossary.md            <- Cross-domain terminology
│   ├── decision-record.md     <- DR template
│   └── key-quotes.md          <- Reference quotes
├── decisions/                 <- Architecture decision records (DR-001 to DR-014)
├── literature/                <- Source registry (47 sources, 17 detailed summaries)
├── audits/                    <- Retrofit audits + cross-project comparisons + forward-feedback applications (FSD, blog, template-revision, decision-support)
├── docs/                      <- Methodology, framework summary, threshold rationale, category-theory lens
├── papers/
│   └── perspective/           <- Paper 1: "The Verification Gap" (active)
│       ├── CLAUDE.md          <- Paper-specific context (READ THIS for paper work)
│       ├── manuscript.tex     <- LaTeX source (~3,450 words)
│       ├── references.bib     <- 14 entries, all DOI-verified
│       ├── vv/claims/         <- Claim registry (19 entries, 100% verified)
│       └── ...
└── memory/                    <- Session memory (gitignored — maintainer-local)
    ├── gotcha-log.md          <- Problem-fix archive
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

The public framework — templates, DRs, audits, README, CHANGELOG — is fully consumable without any of the above. Adopters maintain their own session state per the patterns in `templates/CLAUDE.md`, not by depending on the maintainer's `memory/`.

Listed here so the architecture diagram above is honest about what an adopter sees on `git clone` versus what the maintainer has on disk. External-review observation that prompted this section: ducroq/agent-ready-papers#24.

## Key Paths

| Path | What it is |
|------|-----------|
| `papers/perspective/CLAUDE.md` | Paper 1 project context — start here for paper work |
| `papers/perspective/manuscript.tex` | Paper 1 LaTeX source |
| `papers/perspective/vv/claims/claim_registry.md` | Paper 1 claim registry (19 entries) |
| `papers/perspective/backlog.md` | Paper 1 current tasks and priorities |
| `decisions/DR-004_registry-model-for-non-empirical-papers.md` | Most consequential DR — typed verification model |
| `decisions/DR-006_publication-roadmap.md` | Publication sequencing (Papers 1-3) |
| `literature/README.md` | Master source index (47 entries) |
| `templates/CLAUDE.md` | Template for new paper projects |
| `audits/equation-verification-journey.md` | Discovery of calculation verification blind spot |

## How to Work Here

```bash
# Compile Paper 1 (LaTeX)
cd papers/perspective && pdflatex manuscript && bibtex manuscript && pdflatex manuscript && pdflatex manuscript

# Check claim registry coverage
# Manual: open papers/perspective/vv/claims/claim_registry.md and check P0/P1/P2 percentages

# Verify a citation (anti-hallucination)
# Follow the Step 0 + 6-step checklist in papers/perspective/anti-hallucination.md

# Run peer review simulation
# Use papers/perspective/review-prompt.md with the three-pass pattern (DR-011): Pass 1 intra-family small, Pass 2 intra-family large, Pass 3 cross-vendor (high-stakes only, with style filter)
```

## Cross-Repo Evidence

This project is a source project for [agentic-engineering](https://github.com/ducroq/agentic-engineering) — a proposition about what's new when engineers work with AI agents. When you discover evidence relevant to the four patterns (verification findings, context architecture lessons, reproduce-don't-assess examples, LLM behavioral properties), file an issue at `ducroq/agentic-engineering` with the pattern name, quantified results, and which claims it supports.
