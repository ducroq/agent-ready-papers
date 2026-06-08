# [Paper Title]

<!-- 3-5 lines: what this paper argues, target journal, deadline -->

**Core Argument:** [One-sentence thesis]

- **Target:** [Journal name — special issue / track if applicable]
- **Deadline:** [Submission date]
- **Status:** [Phase 0-5: Framing / Requirements / Literature Audit / Writing / Validation / Submission]

## Core Concept

<!-- The key insight in 2-3 sentences. This orients the agent every session. -->

[Key distinction or finding that the paper is built around.]

## Session Continuity

### Starting a Session
1. **Read this file** (CLAUDE.md) — you're doing this now
2. **Read the backlog** (`backlog.md`) — current tasks and priorities
3. **Check recent DRs** (`DR-*.md`) — any pending decisions?
4. **Resume from last state** — don't restart completed work

### Ending a Session
1. Update `backlog.md` with progress
2. Commit all changes
3. Update this file if a major milestone was reached

## Before You Start

<!-- Task-triggered pointers — "when doing X, read Y" -->

| When | Read |
|------|------|
| Writing or editing prose | `writing-guide.md` — claim-to-section mapping with language calibration |
| Adding or verifying citations | `vv/claims/claim_registry.md` — all claims with priority and status |
| Checking coverage or DOIs for this paper | If your project uses `agent-ready-papers/tools/`: from the framework repo root, run `python -m tools.coverage <path-to-registry>` and `python -m tools.check_dois <path-to-registry>` (or the equivalent `make` targets). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs in `references.bib`. See `tools/README.md` in the framework repo for flags and known limits. |
| Making scope or methodology decisions | Latest `DR-*.md` — decision records |
| Checking terminology | `glossary.md` — cross-domain term definitions |
| Reviewing before submission | `review-prompt.md` — structured peer review simulation |
| Stuck or unsure about a claim | `anti-hallucination.md` — citation verification checklist |
| Ending a session | `backlog.md` — update progress; `../../memory/gotcha-log.md` — review, promote patterns, retire stale entries |

## Hard Constraints

<!-- Non-negotiables for this paper project -->

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows") for claims below SUPPORTED tier
- Never claim own unpublished work as established — always note "under review" status
- Never exceed page budget without explicit decision record
- Never skip the anti-hallucination checklist for AI-introduced citations
- If this paper describes a framework it also uses, add: **This paper uses the framework it describes** — all claims must be registered and verified using the infrastructure presented as the contribution (self-demonstration constraint)

## Key Files

| File | Purpose |
|------|---------|
| `[paper].tex` | LaTeX source |
| `references.bib` | Bibliography |
| `vv/claims/claim_registry.md` | All claims with verification status |
| `vv/PAPER_VV_FRAMEWORK.md` | V&V methodology |
| `writing-guide.md` | Confidence-to-language mapping |
| `glossary.md` | Terminology reference |
| `backlog.md` | Current tasks |
| `DR-*.md` | Decision records |

## Directory Structure

```
[project]/
├── CLAUDE.md                    <- This file (READ FIRST)
├── [paper].tex                  <- LaTeX source
├── references.bib               <- Bibliography
├── backlog.md                   <- Task tracking
├── glossary.md                  <- Terminology reference
├── writing-guide.md             <- Claim-to-section mapping
├── review-prompt.md             <- Peer review simulation
├── anti-hallucination.md        <- Citation verification
├── DR-*.md                      <- Decision records
├── vv/                          <- Verification & Validation
│   ├── PAPER_VV_FRAMEWORK.md    <- V&V methodology
│   ├── claims/
│   │   └── claim_registry.md    <- All claims with status
│   ├── audits/                  <- Per-section audits
│   ├── oracles/                 <- Author guidelines, exemplars
│   └── validation/              <- Co-author review, reviewer checklist
├── data/                        <- Experimental data (if applicable)
└── figures/                     <- Figures
```

## Supported Paper Formats

| Format | Build command | Citation management | Typical use |
|--------|-------------|---------------------|-------------|
| LaTeX + BibTeX | `pdflatex` + `biber` | `.bib` file | Academic journals |
| Markdown + pandoc | `pandoc` with citeproc | `.bib` or inline | Internal reports, technical docs |
| Word / docx | Manual or pandoc export | Zotero / Mendeley / inline | Institutional reports, policy briefs |

The verification framework (claim registry, writing guide, quality gates) applies identically regardless of format. Adapt build commands and static checks per format.

## Build Commands

```bash
# LaTeX compilation
pdflatex [paper].tex
biber [paper]
pdflatex [paper].tex
pdflatex [paper].tex

# Markdown compilation (alternative)
# pandoc [paper].md --citeproc --bibliography=references.bib -o [paper].pdf
```

## Methodology

This project uses a verification framework adapted from systems engineering:
- **Claims** registered and tracked with priority levels (P0/P1/P2)
- **Confidence tiers** (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) mapped to language
- **Anti-hallucination checklist** for all AI-introduced citations
- **Quality gates** before each phase transition
- **Decision records** for all scope/methodology choices

See `vv/PAPER_VV_FRAMEWORK.md` for full details.

## Academic Context

<!-- Situate the paper relative to prior work and related projects -->

| Related Work | Relationship |
|-------------|-------------|
| [Related paper/project 1] | [How it connects] |
| [Related paper/project 2] | [How it connects] |

## Current Status

**Phase:** [Current phase]

**Next priorities:**
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

---

*Last updated: [date]*
