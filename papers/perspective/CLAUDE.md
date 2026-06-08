# The Verification Gap: Why AI-Augmented Academic Writing Needs Reporting Guidelines for Reasoning

This paper argues that the scholarly community lacks verification infrastructure for non-empirical papers written with AI assistance. Citation checkers and grounded generation address factual accuracy, but argument quality — warrant validity, confidence calibration, boundary conditions — has no structured reporting framework. EQUATOR covers empirical papers (~700 guidelines); nothing covers the rest.

**Core Argument:** AI writing tools are proliferating and citation checkers exist, but the scholarly infrastructure for verifying *argument quality* — not just factual accuracy — is missing. We propose typed verification (CLAIM/ARGUMENT/PROPOSITION) with per-type checklists adapted from Toulmin and Whetten.

- **Target:** Learned Publishing (primary), Research Integrity and Peer Review (backup)
- **Deadline:** TBD
- **Status:** Phase 3 — Writing (first draft complete)

## Core Concept

EQUATOR Network maintains ~700 reporting guidelines for empirical health research (CONSORT, STROBE, PRISMA, etc.). Essentially zero guidelines exist for non-empirical paper types — theoretical, design science, perspective, methodological. Gregor's (2006) five theory types include two (Type I: analytic, Type V: design) that are fundamentally non-empirical. For these papers, *argument quality* — not factual accuracy — is the primary verification challenge.

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
| Checking coverage or DOIs for this paper | From repo root: `python -m tools.coverage papers/perspective/vv/claims/claim_registry.md` and `python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md` (or `make coverage` / `make check-dois`). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs in `references.bib`. See `../../tools/README.md` for flags and known limits. |
| Making scope or methodology decisions | Latest `DR-*.md` — decision records |
| Reviewing before submission | `review-prompt.md` — structured peer review simulation |
| Stuck or unsure about a claim | `anti-hallucination.md` — citation verification checklist |
| Adding or verifying literature sources | `../../literature/README.md` — 47 indexed sources by topic |
| Understanding the framework repo | `../../README.md` — the framework this paper describes |
| Checking audit data | `../../audits/*.md` — retrofit audits of source projects |
| Stuck or debugging something weird | `../../memory/gotcha-log.md` — problem-fix archive |
| Ending a session | `backlog.md` — update progress; `../../memory/gotcha-log.md` — review, promote patterns, retire stale entries |

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
| `manuscript.tex` | LaTeX manuscript source |
| `references.bib` | BibTeX references |
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
├── manuscript.tex               <- LaTeX manuscript source
├── references.bib               <- BibTeX references
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
| DR-007 (SE identity upgrade) | Frames the contribution as lightweight SE applied to academic writing, not just SE metaphor |

## Current Status

**Phase:** 3 — Writing (revised draft, verification complete)

**Completed:**
- Scaffold (CLAUDE.md, claim registry, writing guide, review prompt, anti-hallucination checklist)
- First draft of manuscript.tex (~3,450 words incl. abstract, 5 sections)
- references.bib (14 entries, all DOIs verified)
- P0 verification: 8/8 verified (100%)
- P1 verification: 10/10 verified (100%)
- P2 verification: 1/1 verified (100%)
- Overall: 19/19 (100% coverage — all targets exceeded)
- Anti-hallucination checklist: 14/14 references pass
- Peer review simulation: scored 3.95/5.0 (upper "Minor revision")
- Manuscript revisions based on review findings
- DOI verification for all references
- Abstract trimmed to <200 words (Learned Publishing limit)
- Key Points section added (LP requirement: 2-6 bullets)
- Added 4 references: Liang 2025 (Nat Hum Behav), Turner 2012 (Cochrane), Glasziou 2014 (Lancet), Peffers 2007 (JMIS)

**Corrections applied during verification:**
- EQUATOR count updated from ~500 to ~700 (699 verified from equator-network.org, 2026-03-03)
- Added Mugaanyi et al. 2024 (JMIR) for citation hallucination evidence (S1-1 had no source)
- Fixed retyping count from 15/2/4 to 16/2/3 (matched audit table)
- Labelled "confidence inflation" as own term
- Added RAG explanation for Learned Publishing audience
- Acknowledged Gregor Type V empirical evaluation nuance
- Acknowledged Toulmin 6→5 operationalization
- Added counter-argument for the three-type model
- Removed RefChecker/scite.ai names (uncitable tools)
- Added DOIs for gregor2006 and peerarg2024
- Title broadened: "Reporting Guidelines for Reasoning" (was "Beyond Citation Checking")
- Added Appendix A: self-demonstrating typed verification (registry table, 3 worked examples, corrections)
- Added forward reference to Appendix A in Section 4 limitations paragraph
- Added Discussion-section bridging sentence in Section 2 (reasoning gap applies to empirical papers too)
- Added fourth future direction in Section 5 (Discussion sections of empirical papers)
- Added S1-5: calculation verification as failure mode (driven-pendulum Gemini-vs-Sonnet evidence)
- Added fifth future direction in Section 5 (numerical reproduction as distinct verification procedure)
- Created audits/equation-verification-journey.md (discovery log)
- Updated driven-pendulum audit with §9 (equation verification blind spot)
- Integrated calculation verification into framework README
- Registry updated: 19/19 entries, 16 CLAIMs, 2 ARGUMENTs, 1 PROPOSITION

**Note:** Gate 2.5 (Internal Consistency) was introduced after Paper 1 passed Gate 2. Appendix A values were manually cross-checked against main text during the Appendix A addition (2026-03-06), which satisfies the Gate 2.5 intent retroactively.

**Next priorities:**
1. Co-author review (Gate 3) — title change + Appendix A + S1-5 + §4 evidence-base reduction (two audits, not three) are significant additions to discuss
2. Decide submission article type: "Original Article" or "Opinion" (LP uses "Opinion" for perspective-type pieces)
3. Pre-submission enquiry to LP editor (optional)

**Reference corrections found during writing:**
- equator-gap.md attributes GoodReports to "Butcher et al. 2021" — actual first author is Struthers (DOI verified: 10.1186/s12874-021-01402-x)
- peerarg-2024.md lists venue as "LREC-COLING 2024" — actual venue is NeLaMKRR@KR 2024 (verified via arXiv:2409.16813)

---

*Last updated: 2026-03-16*
