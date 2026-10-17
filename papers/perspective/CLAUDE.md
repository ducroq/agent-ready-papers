# The Verification Gap: Checking the Reasoning in AI-Assisted Academic Writing

This commentary argues that AI-assisted non-empirical papers need their reasoning checked, not only their citations. EQUATOR lists about 700 reporting guidelines for empirical health research; no consensus checklist was found for verifying the reasoning of non-empirical papers.

**Core Argument:** The vocabulary for such a checklist already exists. Toulmin's layout treats every assertion as a claim resting on grounds through a warrant, with a qualifier; Whetten's criteria judge a theoretical contribution as a whole. The paper proposes: register each claim with what it rests on, check each item by its kind, and check the contribution once. It applies the procedure to itself and reports no evaluation.

- **Target:** Learned Publishing, Opinion (1,000–4,000 words; decided 2026-10-16 after four model reviews), Research Integrity and Peer Review Comment (backup)
- **Deadline:** TBD
- **Status:** Phase 3, Writing: draft 2 is tag `paper1-draft-2` (2026-10-16); the registry was revised for draft 3 on 2026-10-17 (DR-029 trial). Plan and gaps: `../../docs/work-items/paper1-draft3.md` (maintainer-local)
- **agent-ready-papers:** v4.3.0 <!-- A number, not a status. Bump deliberately after reading UPGRADING.md. v4.2.0 -> v4.3.0 reconciled 2026-10-12: no required item; the new tools are optional and the wording change alters no rule. Still not taken: the optional readability template and DR-019's Step Z scope line. v4.0.0's P0 floor is the known red gate (#38). Earlier reconciliation notes: git history. -->

<!-- This paper lives inside the framework repo, so the pin above tracks the
     framework's own version by construction. It is stated anyway: this is the
     repo's only shipped worked example, and an exemplar that omits the line
     teaches adopters to omit it too. -->


## Core Concept

The gap (S2-1, S2-2, EMERGING) is stated above. Gregor's (2006) five theory types include two (Type I: analytic, Type V: design) that are largely non-empirical (S2-3a/b). For these papers, *argument quality*, not factual accuracy, may be the primary verification challenge (S2-4, EMERGING).

The proposal is DR-027's model. Every statement the paper puts forward and supports is a claim, recording what it says (descriptive or normative) and its grounds item by item: sources, other claims, declared starting points, own work. The checks follow the items (source check, warrant check), and the contribution is checked once with Whetten's questions (validation). This paper uses the framework it describes.

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
| Writing or editing prose | `glossary.md` (this paper's terms; framework terms in `../../docs/glossary.md`, DR-027/028), then `writing-guide.md` — claim-to-section mapping with language calibration |
| Writing or editing prose for a reader | The maintainer's private house-voice profile (maintainer-local; ask for it), then `make formula-scan` from the repo root (tier language in `writing-guide.md` still wins) |
| Adding or verifying citations | `vv/claims/claim_registry.md` — all claims with priority and status |
| Checking coverage or DOIs for this paper | From repo root: `python -m tools.coverage papers/perspective/vv/claims/claim_registry.md` and `python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md` (or `make coverage` / `make check-dois`). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs in `references.bib`. See `../../tools/README.md` for flags and known limits. |
| Logging token cost of an operation | `vv/cost-log.md` — record `/status` deltas (or subagent `total_tokens`) after named, repeatable operations (review passes, `/curate`, `/audit-context`, batch verification, full Gate sweeps). Bootstrap data from 2026-06-08 already present. See `../../templates/cost-log.md` for the convention. |
| Making scope or methodology decisions | Latest `DR-*.md` — decision records |
| Reviewing before submission | `review-prompt.md` — structured peer review simulation |
| Stuck or unsure about a claim | `anti-hallucination.md` — citation verification checklist |
| Adding or verifying literature sources | `../../literature/README.md` — indexed sources by topic |
| Understanding the framework repo | `../../README.md` — the framework this paper describes |
| Stuck or debugging something weird | `../../memory/gotcha-log.md` — problem-fix archive |
| Ending a session | `backlog.md` — update progress; `../../memory/gotcha-log.md` — review, promote patterns, retire stale entries |

## Hard Constraints

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows", "confirms") for claims below **ESTABLISHED** tier — that is where the DR-002 mapping puts these three words.
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
- **Claims** registered with what they say and their typed grounds, tracked with priority levels (P0/P1/P2); declared starting points D1–D8 and contribution C1 in their own tables
- **Checks by grounds** (DR-027): source check per `src:`, warrant check (Toulmin) for `claim:` grounds, contribution check (Whetten) for C1
- **Confidence tiers** (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) mapped to language
- **Anti-hallucination checklist** for all AI-introduced citations
- **Decision records** for all scope/methodology choices

This is the framework eating its own dog food. Any friction, gaps, or false failures encountered during writing become additional evaluation evidence for Paper 2 (DSR).

## Academic Context

| Related Work | Relationship |
|-------------|-------------|
| Paper 2 (DSR) | This paper establishes the gap (Swales Move 1-2); Paper 2 occupies it (Move 3) with full artifact + evaluation |
| DR-007 (SE identity upgrade) | Frames the contribution as lightweight SE applied to academic writing, not just SE metaphor |

## Current Status

**Phase:** 3, Writing (draft 3 next). Coverage and the P0 floor: `make coverage` from the repo root; the registry header carries the last figure. The history of drafts 1 and 2 (what was completed, and the corrections made during verification up to 2026-10-05) is in this file's git history before 2026-10-17. Gate 2.5 (internal consistency) was introduced after Paper 1 passed Gate 2; Appendix A was cross-checked against the main text by hand on 2026-03-06, which meets its intent.

**Next priorities** (2026-10-17; detail in `../../docs/work-items/paper1-draft3.md`, maintainer-local):
1. Draft 3 from the revised registry: narrower claims, prior work before the proposal, the warrant check in §3, and the four manuscript passages that lost their registry row
2. One outside helper: a second screener for S2-2's search and a migration by another person for S3-4 (task drafted, recipient open)
3. P0 floor 3 of 6 (C1, S2-2, S3-4 EMERGING); DR-029 (Proposed) keeps it at 3 of 6 for evidential reasons, not because they are inferences
4. Gate 3 review before submission: by the maintainer unless a co-author is found

---

*Last updated: 2026-10-17*
