# The Verification Gap: Checking the Reasoning in AI-Assisted Academic Writing

This paper argues that AI-assisted non-empirical papers need their reasoning checked, not only their citations. EQUATOR lists about 700 reporting guidelines for empirical health research; no consensus checklist was found for verifying the reasoning of non-empirical papers.

**Core Argument:** The vocabulary for such a checklist already exists. Toulmin's layout treats every assertion as a claim resting on grounds through a warrant, with a qualifier; Whetten's criteria judge a theoretical contribution as a whole. The paper proposes: register each claim with what it rests on, check each item by its kind, and check the contribution once. It applies the procedure to itself and reports no evaluation.

- **Target:** Learned Publishing, Opinion (1,000–4,000 words, no abstract, no footnotes: rules at source in `../../memory/reference-learned-publishing-opinion.md`); arXiv cs.DL preprint first (`arxiv-submission.md`). Backup: Research Integrity and Peer Review, Comment
- **Deadline:** TBD
- **Status:** Phase 3, Writing: draft 3 plus the maintainer's feedback round (2026-10-19). Plan and next steps: `../../docs/work-items/paper1-draft3.md` (maintainer-local)
- **agent-ready-papers:** v5.0.0 <!-- A number, not a status. Bump deliberately after reading UPGRADING.md. v4.3.0 -> v5.0.0 reconciled 2026-10-17: the registry is on the DR-027 schema and the paper has a glossary (DR-028), so both required items are met; DR-026 and DR-029 are Proposed. The P0 floor is the known red gate (#38). Earlier reconciliation notes: git history. -->

<!-- This paper lives inside the framework repo, so the pin above tracks the
     framework's own version by construction. It is stated anyway: this is the
     repo's only shipped worked example, and an exemplar that omits the line
     teaches adopters to omit it too. -->


## Core Concept

The gap (S2-1, S2-2, EMERGING) is stated above. Gregor's (2006) five theory types include two (Type I: analytic, Type V: design) that are largely non-empirical (S2-3a/b). For these papers, *argument quality*, not factual accuracy, may be the primary verification challenge (S2-4, EMERGING).

The proposal is DR-027's model. Every statement the paper puts forward and supports is a claim, recording what it says (descriptive or normative) and its grounds item by item: sources, other claims, declared starting points, own work. The checks follow the items (source check, warrant check), and the contribution is checked once with Whetten's questions (validation). This paper uses the framework it describes.

## Session Continuity

Start: this file, then the work item (its NEXT list is what "continue" means), then `backlog.md`. End: update both; `/curate` from the repo root.

## Before You Start

| When | Read |
|------|------|
| Writing or editing prose | `glossary.md` (this paper's terms; framework terms in `../../docs/glossary.md`, DR-027/028), then `writing-guide.md` — claim-to-section mapping with language calibration |
| Writing or editing prose for a reader | The maintainer's private house-voice profile (maintainer-local; ask for it), then `make formula-scan` from the repo root (tier language in `writing-guide.md` still wins) |
| Adding or verifying citations | `vv/claims/claim_registry.md` — all claims with priority and status |
| Checking coverage or DOIs for this paper | From repo root: `python -m tools.coverage papers/perspective/vv/claims/claim_registry.md` and `python -m tools.check_dois papers/perspective/vv/claims/claim_registry.md` (or `make coverage` / `make check-dois`). Prefer the tool to manually counting P0/P1/P2 percentages or eyeballing DOIs in `references.bib`. See `../../tools/README.md` for flags and known limits. |
| Logging token cost of an operation | `vv/cost-log.md` — record `/status` deltas (or subagent `total_tokens`) after named, repeatable operations (review passes, `/curate`, `/audit-context`, batch verification, full Gate sweeps). Bootstrap data from 2026-06-08 already present. See `../../templates/cost-log.md` for the convention. |
| Making scope or methodology decisions | `../../decisions/` (`make dr-status`); DR-029 and DR-030 are Proposed and bear on this paper |
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
- Never exceed the word budget without a decision record: 4,000 is the venue limit, and `test_paper1_v5` fails above 3,800 (`make check-registry` counts; the abstract and tables don't count)
- Never skip the anti-hallucination checklist for AI-introduced citations
- **This paper uses the framework it describes** — all claims in this manuscript must be registered and verified using the same infrastructure presented as the contribution

## Key Files

| File | Purpose |
|------|---------|
| `manuscript.tex` | LaTeX source: journal build `make paper1-pdf`, preprint build `make paper1-arxiv` (`\preprintmode` adds the abstract) |
| `abstract.tex` | The abstract, used by the preprint build only |
| `references.bib` | BibTeX references |
| `vv/claims/claim_registry.md` | All claims with verification status |
| `glossary.md` | This paper's terms (DR-028) |
| `cover-letter.md`, `arxiv-submission.md` | Submission drafts: the LP cover letter, and the arXiv steps and form fields |
| `writing-guide.md`, `review-prompt.md`, `anti-hallucination.md` | Writing calibration, peer-review simulation, citation checklist |
| `backlog.md` | Paper-scoped tasks |

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

**Phase:** 3, Writing (draft 3, 2026-10-19). Coverage and the P0 floor: `make coverage` from the repo root; the registry header carries the last figure (3 of 6). History of drafts 1 and 2: this file's git history before 2026-10-17.

**Next:** the work item's NEXT list (friends' read, blind re-rating, scope follow-ups, preprint).

---

*Last updated: 2026-10-19*
