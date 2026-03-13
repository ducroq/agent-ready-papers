# Agent-Ready Papers

Verification infrastructure for AI-augmented academic writing. Templates, quality gates, and session continuity that catch the failure modes automated tools miss — hallucinated citations, confidence inflation, argument quality gaps, and calculation errors.

- **Type**: Guide + templates + active paper projects
- **Companion**: [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) (for code)
- **Status**: Paper 1 (Perspective) at Gate 3 (co-author review). Paper 2 (DSR) not yet started.
- **agent-ready-projects**: v1.0.0

## Before You Start

| When | Read |
|------|------|
| Working on Paper 1 (Perspective) | `papers/perspective/CLAUDE.md` — paper identity, constraints, status, verification state |
| Making scope or methodology decisions | `decisions/` — 8 decision records (DR-001 through DR-008) |
| Adding or verifying literature sources | `literature/README.md` — 47 indexed sources organized by topic |
| Understanding how the framework was built | `docs/METHODOLOGY.md` — derived from 3 real paper projects |
| Reviewing audit evidence from source projects | `audits/` — 8 retrofit audits with worked examples |
| Stuck or debugging something weird | `memory/gotcha-log.md` — problem-fix archive |
| Creating a new paper project | `templates/CLAUDE.md` — paper project template |

## Hard Constraints

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows") for claims below SUPPORTED tier
- Never skip the anti-hallucination checklist for AI-introduced citations
- Decision records are binding — check `decisions/` before proposing scope changes
- This repo contains both the framework AND papers that use it — changes to templates may affect active papers

## Architecture

```
agent-ready-papers/
├── README.md                  <- The guide (public-facing)
├── CLAUDE.md                  <- This file (agent orientation)
├── templates/                 <- Reusable templates for new paper projects
│   ├── CLAUDE.md              <- Paper project identity template
│   ├── claim-registry.md      <- Registry structure (P0/P1/P2, typed verification)
│   ├── vv-framework.md        <- Verification & validation framework
│   ├── writing-guide.md       <- Confidence tier to language mapping
│   ├── review-prompt.md       <- Structured peer review simulation
│   ├── anti-hallucination.md  <- 6-step citation verification checklist
│   ├── equation-checker.md    <- Mechanical equation verification prompt
│   ├── glossary.md            <- Cross-domain terminology
│   ├── decision-record.md     <- DR template
│   └── key-quotes.md          <- Reference quotes
├── decisions/                 <- Architecture decision records (DR-001 to DR-008)
├── literature/                <- Source registry (47 sources, 17 detailed summaries)
├── audits/                    <- Retrofit audits of 3 source projects + equation verification
├── docs/                      <- Methodology and development history
├── papers/
│   └── perspective/           <- Paper 1: "The Verification Gap" (active)
│       ├── CLAUDE.md          <- Paper-specific context (READ THIS for paper work)
│       ├── manuscript.tex     <- LaTeX source (~3,450 words)
│       ├── references.bib     <- 14 entries, all DOI-verified
│       ├── vv/claims/         <- Claim registry (19 entries, 100% verified)
│       └── ...
└── memory/                    <- Session memory (not committed)
    ├── gotcha-log.md          <- Problem-fix archive
    └── ...
```

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
# Follow the 6-step checklist in papers/perspective/anti-hallucination.md

# Run peer review simulation
# Use papers/perspective/review-prompt.md with a different model than the one that wrote the paper
```

## The Framework in Brief

Four verification types, each with a structured procedure:

| Type | Question | Framework |
|------|----------|-----------|
| CLAIM | Does the source say this? | Citation checking + anti-hallucination |
| ARGUMENT | Is the reasoning valid? | Toulmin (claim, grounds, warrant, backing, qualifier, rebuttal) |
| PROPOSITION | Are conditions specified? | Whetten (What/How/Why/Who-Where-When, boundary conditions) |
| CALCULATION | Does the result follow from the formula? | Numerical reproduction (equation-checker) |

Four confidence tiers mapped to language:

| Tier | Language examples |
|------|-----------------|
| ESTABLISHED | "demonstrates", "shows", "confirms" |
| SUPPORTED | "indicates", "supports", "evidence suggests" |
| EMERGING | "may", "preliminary evidence", "initial findings suggest" |
| SPECULATIVE | "warrants investigation", "remains unclear", "we hypothesize" |
