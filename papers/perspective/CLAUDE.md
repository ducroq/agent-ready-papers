# The Verification Gap: Why AI-Augmented Academic Writing Needs Reporting Guidelines Beyond Citation Checking

This paper argues that the scholarly community lacks verification infrastructure for non-empirical papers written with AI assistance. Citation checkers and grounded generation address factual accuracy, but argument quality — warrant validity, confidence calibration, boundary conditions — has no structured reporting framework. EQUATOR covers empirical papers (~500 guidelines); nothing covers the rest.

**Core Argument:** AI writing tools are proliferating and citation checkers exist, but the scholarly infrastructure for verifying *argument quality* — not just factual accuracy — is missing. We propose typed verification (CLAIM/ARGUMENT/PROPOSITION) with per-type checklists adapted from Toulmin and Whetten.

- **Target:** Learned Publishing (primary), Research Integrity and Peer Review (backup)
- **Deadline:** TBD
- **Status:** Phase 1 — Framing (scaffold created, registry populated, ready to write)

## Core Concept

EQUATOR Network maintains ~500 reporting guidelines for empirical health research (CONSORT, STROBE, PRISMA, etc.). Essentially zero guidelines exist for non-empirical paper types — theoretical, design science, perspective, methodological. Gregor's (2006) five theory types include two (Type I: analytic, Type V: design) that are fundamentally non-empirical. For these papers, *argument quality* — not factual accuracy — is the primary verification challenge.

We propose a typed verification model: CLAIMs (source-verifiable facts), ARGUMENTs (Toulmin-verified reasoning chains), and PROPOSITIONs (Whetten-verified recommendations with boundary conditions). Each type has distinct verification procedures and confidence criteria. This paper uses the framework it describes.

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

| When | Read |
|------|------|
| Writing or editing prose | `writing-guide.md` — claim-to-section mapping with language calibration |
| Adding or verifying citations | `vv/claims/claim_registry.md` — all claims with priority and status |
| Making scope or methodology decisions | Latest `DR-*.md` — decision records |
| Reviewing before submission | `review-prompt.md` — structured peer review simulation |
| Stuck or unsure about a claim | `anti-hallucination.md` — citation verification checklist |
| Understanding the framework repo | `../../README.md` — the framework this paper describes |
| Checking audit data | `../../audits/*.md` — retrofit audits of source projects |

## Hard Constraints

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows") for claims below SUPPORTED tier
- Never claim own unpublished work as established — always note "under review" status
- Never exceed word budget (3,500 words target, 5,000 max) without explicit decision record
- Never skip the anti-hallucination checklist for AI-introduced citations
- **This paper uses the framework it describes** — all claims in this manuscript must be registered and verified using the same infrastructure presented as the contribution

## Key Files

| File | Purpose |
|------|---------|
| `manuscript.md` | Manuscript source (created during writing) |
| `vv/claims/claim_registry.md` | All claims with verification status |
| `writing-guide.md` | Section-to-registry mapping with language calibration |
| `review-prompt.md` | Peer review simulation (Variant B — non-empirical) |
| `anti-hallucination.md` | Citation verification checklist |
| `backlog.md` | Current tasks (created at first writing session) |
| `DR-*.md` | Decision records (created as needed) |

## Directory Structure

```
papers/perspective/
├── CLAUDE.md                    <- This file (READ FIRST)
├── manuscript.md                <- Manuscript (created during writing)
├── writing-guide.md             <- Section-to-registry mapping
├── review-prompt.md             <- Peer review simulation
├── anti-hallucination.md        <- Citation verification checklist
├── backlog.md                   <- Task tracking (created during writing)
├── DR-*.md                      <- Decision records (as needed)
└── vv/
    └── claims/
        └── claim_registry.md    <- All claims with status
```

## Methodology

This project uses the agent-ready-papers verification framework — the same framework this paper describes:
- **Claims** registered and tracked with priority levels (P0/P1/P2)
- **Typed verification:** CLAIMs (source check), ARGUMENTs (Toulmin), PROPOSITIONs (Whetten)
- **Confidence tiers** (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) mapped to language
- **Anti-hallucination checklist** for all AI-introduced citations
- **Decision records** for all scope/methodology choices

This is the framework eating its own dog food. Any friction, gaps, or false failures encountered during writing become additional evaluation evidence for Paper 2 (DSR).

## Academic Context

| Related Work | Relationship |
|-------------|-------------|
| Paper 2 (DSR) | This paper establishes the gap (Swales Move 1-2); Paper 2 occupies it (Move 3) with full artifact + evaluation |
| Technology paper (IEEE TIM) | Source project — retrofit audit provides evidence of language calibration issues (6/22 entries over-confident) |
| Proposition paper (medical education) | Source project — retrofit audit provides evidence of typing benefits (76% coverage, false failures from mistyping) |
| Engineering Fidelity paper (MST) | Source project — retrofit audit provides additional cross-project evidence |
| DR-007 (SE identity upgrade) | Frames the contribution as lightweight SE applied to academic writing, not just SE metaphor |

## Current Status

**Phase:** 1 — Framing

**Next priorities:**
1. Create backlog for first writing session
2. Begin Section 1 draft (The Problem)
3. Verify P0 claims in registry before writing

---

*Last updated: 2026-03-03*
