# [Paper Title]

<!-- 3-5 lines: what this paper argues, target journal, deadline -->

**Core Argument:** [One-sentence thesis]

- **Target:** [Journal name — special issue / track if applicable]
- **Deadline:** [Submission date]
- **Status:** [Phase 0-5: Framing / Requirements / Literature Audit / Writing / Validation / Submission]
- **agent-ready-papers:** v3.0.0 <!-- The framework version this project is pinned to. Keep this line: the drift row in the table below has nothing to read without it. Bump it deliberately, after reviewing UPGRADING.md — not automatically. -->

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
| Starting any session (framework drift) | Compare the `- **agent-ready-papers:** vX.Y.Z` line in this file's header against the framework's [`CHANGELOG.md`](https://github.com/ducroq/agent-ready-papers/blob/master/CHANGELOG.md). If this project is behind, surface the drift before starting work and point at [`UPGRADING.md`](https://github.com/ducroq/agent-ready-papers/blob/master/UPGRADING.md) for what each version asks of you. Don't auto-update — bumping the pin is the author's call. |
| Writing or editing prose | `writing-guide.md` — claim-to-section mapping with language calibration |
| Adding or verifying citations | `vv/claims/claim_registry.md` — all claims with priority and status |
| Checking coverage or DOIs for this paper | If your project uses `agent-ready-papers/tools/`: from the framework repo root, run `python -m tools.coverage <path-to-registry>` and `python -m tools.check_dois <path-to-registry>` (or the equivalent `make` targets). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs in `references.bib`. See `tools/README.md` in the framework repo for flags and known limits. |
| Logging token cost of an operation | `vv/cost-log.md` — record `/status` deltas (or subagent `total_tokens`) after named, repeatable operations (review passes, `/curate`, `/audit-context`, batch verification, full Gate sweeps). Don't log incidental tool calls. See `templates/cost-log.md` for the convention. |
| Making scope or methodology decisions | Latest `DR-*.md` — decision records |
| Checking terminology | `glossary.md` — cross-domain term definitions |
| Reviewing before submission | `review-prompt.md` (paper-local copy) or the framework's `agents/review-prompt.md` — peer-review simulator runnable in any agent; pair with the three-pass pattern (DR-011) |
| Verifying equations or derived numerical values | Framework's `agents/equation-checker.md` — mechanical reproduction (substitute → compute → flag), not plausibility review; works in any agent (since agent-ready-papers v2.1.0) |
| Stuck or unsure about a claim | `anti-hallucination.md` — citation verification checklist |
| Placing a bet whose evidence lives in the future | `hypothesis-log.md` (copy from `agent-ready-papers/templates/hypothesis-log.md` <!-- placeholder -->) — provisional positions with `Position` / `Method` / `Revisit trigger` / `Review by`. `/curate` surfaces due items. Write the entry when you make the claim, not at the end of the session. |
| Starting work that will span several sessions | `templates/work-item.md` in the framework repo — a savepoint file in `docs/work-items/`, plus a one-line pointer from wherever this project keeps its in-progress list: the memory index's Current State section if you have one, otherwise the **Active work** section below. |
| Ending a session | `backlog.md` — update progress; `<repo-root>/memory/gotcha-log.md` — review, promote patterns, retire stale entries. (Written as `<repo-root>/` rather than a fixed relative path because the layout varies: from a two-deep `papers/<name>/` project it is `../../memory/gotcha-log.md` <!-- placeholder -->, and in a single-paper repo where the paper *is* the root it is just `memory/gotcha-log.md`. Substitute for your layout.) |

## Active work

<!-- One line per work item that is IN PROGRESS. This is the same list an
     in-repo memory index's "Current State" section carries.

     THE CONDITION IS WHETHER YOU KEEP A MEMORY INDEX, NOT WHICH AGENT YOU USE.
     If you keep one, DELETE this section: keeping both is how the two copies
     start disagreeing, and an audit that finds both reports it as a finding.
     If you do not, this section is where the pointer lives — because without
     it, an adopter who followed every template has work-item files and
     nowhere a pointer could have gone.

     Do not read that as "this file is always loaded". It is not, for every
     agent: `docs/non-claude-setup.md` records that Copilot CLI does not
     auto-read `CLAUDE.md` at session start, and Cursor and Continue read
     their own rules files. Whatever your agent DOES read first has to reach
     this file, or this section is as unreachable as the index would be.

     Work items themselves are agent-independent — `docs/work-items/` is an
     ordinary directory and `templates/work-item.md` is written for any agent.
     Only the location of the POINTER changes.

     Bounded on purpose. A completed item loses its pointer — its Outcome
     section in the work-item file is the durable residue, and that file is
     reached from the pointer while the work is live. Only in-progress items
     belong here, so this section stays two or three lines and does not become
     the session narrative that blows this file's size budget.

     Format — keep the example inside this comment, not below it, or every
     fresh adoption ships a live pointer to a file that does not exist and the
     reference check reports it, correctly, as broken:
       - [Short description] → docs/work-items/slug.md [in progress]

     (agent-ready-projects v1.22.0) -->

## Hard Constraints

<!-- Non-negotiables for this paper project -->

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows", "confirms") for claims below **ESTABLISHED** tier — that is where the DR-002 mapping puts these three words. (Was "below SUPPORTED tier" until 2026-08-13, which permitted "demonstrates" *at* SUPPORTED — the drift a 2026-03 retrofit audit found in 6 of 22 entries — a single-audit figure registered at EMERGING (`S3-3`), not a calibrated rate.)
- Never claim own unpublished work as established — always note "under review" status
- Never exceed page budget without explicit decision record
- Never skip the anti-hallucination checklist for AI-introduced citations
- If this paper describes a framework it also uses, add: **This paper uses the framework it describes** — all claims must be registered and verified using the infrastructure presented as the contribution (self-demonstration constraint)
- **Project state goes in this project's in-repo `memory/` directory (wherever the framework adopter tracks it — typically `<repo-root>/memory/` for a single-paper repo, or `<repo-root>/memory/` shared across papers in a multi-paper repo), not in any agent's user-level auto-memory.** Versions, session narratives, gotchas, priorities, handoffs, and any state tied to *this* paper project belong in the in-repo memory the Before You Start table above routes to. The principle applies most directly to agents with **cross-project user-level memory** — Claude Code (`~/.claude/projects/<slug>/memory/`), ChatGPT memory, Gemini Gems — where this-paper state can leak into other projects without an explicit boundary. Agents with only project-level rules files (Cursor's `.cursorrules`, GitHub Copilot's `.github/copilot-instructions.md` <!-- placeholder -->, Continue's `.continue/config.json` <!-- placeholder -->) inherit the principle vacuously since they have no cross-project store to spill into. Don't write project state into both — drift starts as soon as you do. (Constraint added in agent-ready-papers v1.6.2; generalised to all agents in v2.1.0; narrowed in v2.2.0 to acknowledge which agents have the failure mode the principle prevents.)

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
| `hypothesis-log.md` | Provisional positions awaiting future evidence (since agent-ready-papers v1.7.0) |
| `docs/work-items/` | Savepoints for work spanning several sessions (per the framework's `templates/work-item.md`). Created on demand — absent until the first multi-session task. The pointer to an in-progress item goes in your memory index's Current State section, or in the **Active work** section of this file if you keep no index. |

## Directory Structure

```
[project]/
├── CLAUDE.md                    <- This file (READ FIRST)
├── [paper].tex                  <- LaTeX source
├── references.bib               <- Bibliography
├── backlog.md                   <- Task tracking
├── glossary.md                  <- Terminology reference
├── writing-guide.md             <- Claim-to-section mapping
├── anti-hallucination.md        <- Citation verification
├── hypothesis-log.md            <- Provisional positions awaiting future evidence
├── DR-*.md                      <- Decision records
├── docs/
│   └── work-items/              <- Multi-session savepoints (created on demand)
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
