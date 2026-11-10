# The Verification Gap: Checking the Reasoning in AI-Assisted Academic Writing

This paper argues that AI-assisted non-empirical papers need their reasoning checked, not only their citations. EQUATOR lists about 700 reporting guidelines for empirical health research; no consensus checklist was found for verifying the reasoning of non-empirical papers.

**Core Argument:** The vocabulary for such a checklist already exists. Toulmin's layout treats every assertion as a claim resting on grounds through a warrant, with a qualifier; Whetten's criteria judge a theoretical contribution as a whole. The paper proposes: register each claim with what it rests on, check each item by its kind, and check the contribution once. It applies the procedure to itself and reports no evaluation.

- **Target:** Learned Publishing, Opinion (1,000–4,000 words, no abstract, no footnotes: rules at source in `../../memory/reference-learned-publishing-opinion.md`); arXiv preprint first, category undecided because of arXiv's CS position-paper rule (`arxiv-submission.md`). Backup: Research Integrity and Peer Review, Comment
- **Deadline:** TBD
- **Status:** Phase 3, Writing: draft 4 (`paper1-draft-4`, 2026-10-30) plus the reader-feedback pass (2026-11-10, 3,998 words). Plan and next steps: `../../docs/work-items/paper1-draft3.md` (maintainer-local)
- **agent-ready-papers:** v5.0.0 <!-- A number, not a status. Bump deliberately after reading UPGRADING.md; reconciliation notes: git history. -->

<!-- Stated though it tracks the framework by construction: an exemplar that omits the pin teaches adopters to omit it. -->

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
| Checking coverage or DOIs for this paper | `make coverage` / `make check-dois` from the repo root, never a hand count; flags and limits: `../../tools/README.md` |
| Logging token cost of an operation | `vv/cost-log.md`; convention in `../../templates/cost-log.md` |
| Making scope or methodology decisions | `../../decisions/` (`make dr-status`); DR-029 and DR-030 are Proposed and bear on this paper |
| Reviewing before submission | `review-prompt.md` — structured peer review simulation |
| Stuck or unsure about a claim | `anti-hallucination.md` — citation verification checklist |
| Adding or verifying literature sources | `../../literature/README.md` — indexed sources by topic |
| Understanding the framework repo | `../../README.md` — the framework this paper describes |
| Stuck, or ending a session | The root `CLAUDE.md` rows (gotcha log, `/curate`); update `backlog.md` |

## Hard Constraints

- Never cite a paper without verifying it exists (DOI check or Google Scholar)
- Never use confident language ("demonstrates", "shows", "confirms") for claims below **ESTABLISHED** tier — that is where the DR-002 mapping puts these three words.
- Never claim own unpublished work as established — always note "under review" status
- Never exceed the 4,000-word venue limit without a decision record (`test_paper1_v5` fails above it; `make check-registry` counts, the preamble included, the abstract and tables not)
- Never skip the anti-hallucination checklist for AI-introduced citations
- **Reader feedback is private.** Responses stay in `feedback/` (gitignored) or `../../memory/`. Tracked files and commit messages say "a reader" or "a reviewer": no names, no quotes from private correspondence. Named thanks only with the person's consent.
- **This paper uses the framework it describes** — all claims in this manuscript must be registered and verified using the same infrastructure presented as the contribution

## Key Files

| File | Purpose |
|------|---------|
| `manuscript.tex` | LaTeX source: journal build `make paper1-pdf`, preprint build `make paper1-arxiv` (`\preprintmode` adds the abstract) |
| `abstract.tex` | The abstract, used by the preprint build only |
| `supplement.tex` | How to read a claim register (Toulmin primer): Appendix A in the preprint build; `supplement-standalone.tex` builds LP's separate supporting-information file. Outside the word count; its claims still need register rows |
| `references.bib` | BibTeX references |
| `figures/fig-register.tex` | Figure 1 source. Nothing rebuilds `fig-register.pdf`: run `pdflatex` in `figures/` after any edit. LP takes the PDF as a separate file |
| `vv/claims/claim_registry.md` | All claims with verification status |
| `glossary.md` | This paper's terms (DR-028) |
| `cover-letter.md`, `arxiv-submission.md` | Submission drafts: the LP cover letter, and the arXiv steps and form fields |
| `writing-guide.md`, `review-prompt.md`, `anti-hallucination.md` | Writing calibration, peer-review simulation, citation checklist |
| `backlog.md` | Paper-scoped tasks |

## Methodology

The framework this paper describes (Core Concept above): claims P0/P1/P2, declared starting points D1–D8 and contribution C1 in their own tables, confidence tiers mapped to language. Friction, gaps and false failures met while writing become evaluation evidence for Paper 2 (DSR).

## Academic Context

| Related Work | Relationship |
|-------------|-------------|
| Paper 2 (DSR) | This paper establishes the gap (Swales Move 1-2); Paper 2 occupies it (Move 3) with full artifact + evaluation |
| DR-007 (SE identity upgrade) | Frames the contribution as lightweight SE applied to academic writing, not just SE metaphor |

## Current Status

**Phase:** 3, Writing (draft 4, 2026-10-30). Coverage and the P0 floor: `make coverage` from the repo root; the registry header carries the last figure (3 of 6). History of drafts 1 and 2: this file's git history before 2026-10-17.

**Next:** the work item's NEXT list (friends' read, blind re-rating, scope follow-ups, preprint).

---

*Last updated: 2026-11-10*
