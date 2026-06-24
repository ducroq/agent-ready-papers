# Constructive Lenses: An Open, Diversity-Aware AI Pipeline for Public-Interest News Selection

<!-- WORKING TITLE — the author (an engineering academic, NL) sets the final angle, title,
     and venue in Phase 0. Everything below the line marked (WORKING) is a starting
     position seeded from the ovr.news project, not a fixed commitment. -->

This paper presents **ovr.news** — a live multilingual pipeline that scores news through five constructive "lenses" via distilled classifier models — as a worked case for a specific claim: constructive news selection can be operationalised as a *transparent, diversity-aware, reproducible* AI pipeline, and building it openly fills an infrastructure gap between constructive-journalism content producers and the methodology authorities that hold the classification know-how. The paper situates this in the AI-governance literature (Helberger), the normative news-diversity literature (Vrijenhoek), and the post-industrial-journalism scaffold (Anderson–Bell–Shirky; Simon), and engages Byung-Chul Han's information-vs-narrative critique as a boundary condition rather than a footnote.

**Core Argument (WORKING):** A small newsroom or researcher can implement editorially-meaningful constructive selection as an open, diversity-aware, distillation-based AI pipeline; ovr.news is an existence proof, and evaluating it against a normative diversity framework (Vrijenhoek 2021) shows what such a system can and cannot yet do.

- **Target:** *Digital Journalism* (primary candidate) — alternatives: *Journalism Studies*, *AI & Society*, *Journalism Practice*. **TBD in Phase 0.**
- **Deadline:** TBD (no submission pressure; gated by neither the readiness gate nor outbound rules — this is reading-and-writing work).
- **Status:** **Phase 0 — Framing.** Scaffolded 2026-06-24 from the ovr.news `[2026-05-27]` intellectual-lineage hypothesis-log entry.

## Core Concept

The constructive-journalism field has **content producers** (Reasons to be Cheerful, Squirrel News, Optimist Daily, regional outlets in 20+ languages) and **methodology authorities** (Solutions Journalism Network, Constructive Institute at Aarhus, Bonn Institute) — but **no open infrastructure between the two**. The Constructive Institute's classification algorithm is partner-only. ovr.news's contribution is a working, documentable, releasable example of that missing layer: RSS ingest in 25+ languages → five distilled lens classifiers → transparent per-article rationale on a public reader site. The *selection lives in the lens, not the source list* — the same scoring runs across dedicated constructive feeds and general news.

The intellectual move that makes this a paper rather than a project report: read the artefact through the academic cluster. Helberger 2024 names the provider/deployer asymmetry and the disincentive against in-house AI in small media orgs — ovr.news is precisely the deployer-that-builds. Vrijenhoek 2021 formalises *normative* diversity metrics for news recommenders — ovr.news's five-lens distribution is directly measurable against them. Han supplies the sharpest counter: a feed of short summaries is still *additive information*, not *orienting narrative* — the honest boundary condition the paper must not dodge.

## Session Continuity

### Starting a Session
1. **Read this file** (CLAUDE.md) — you're doing this now
2. **Read the backlog** (`backlog.md`) — current tasks and priorities
3. **Check recent DRs** (`DR-*.md`) — any pending decisions? (none yet)
4. **Resume from last state** — don't restart completed work

### Ending a Session
1. Update `backlog.md` with progress
2. Commit all changes
3. Update this file if a major milestone was reached
4. Session state (narratives, gotchas) goes in the **shared repo `../../memory/`**, not in any agent's user-level auto-memory (see Hard Constraints)

## Before You Start

| When | Read |
|------|------|
| Settling the angle, title, venue, or paper type | This file's Core Argument + `backlog.md` Phase 0 tasks — **this is the author's call**, not an agent default |
| Writing or editing prose | `writing-guide.md` — claim-to-section mapping with language calibration |
| Adding or verifying citations | `vv/claims/claim_registry.md` + `anti-hallucination.md` — **every bib entry here is currently UNVERIFIED** (see `references.bib` header) |
| Reading the literature / taking notes | `../../literature/README.md` → "Constructive & AI-Driven Journalism" section (L49–L55); per-source reading stubs in `../../literature/sources/` carry status + what-to-extract + claim map |
| Checking coverage or DOIs | From the framework repo root: `python -m tools.coverage papers/constructive-lenses/vv/claims/claim_registry.md` and `python -m tools.check_dois papers/constructive-lenses/vv/claims/claim_registry.md` |
| Logging token cost of an operation | `vv/cost-log.md` |
| Making scope or methodology decisions | Create a `DR-*.md` (see `../../templates/decision-record.md`) |
| Checking terminology | `glossary.md` — cross-domain terms (journalism × ML × governance) |
| Reviewing before submission | `review-prompt.md` + the three-pass pattern (DR-011) |
| Stuck or unsure about a claim | `anti-hallucination.md` |
| Placing a bet whose evidence lives in the future | `hypothesis-log.md` |
| Pulling evidence about the ovr.news artefact | The ovr.news repo (`C:/local_dev/ovr.news`): `docs/PROPOSITION.md`, `docs/LANDSCAPE.md` (academic cluster), `docs/hypothesis-log.md` `[2026-05-27]`, the ADR record. **ovr.news is the case; this paper cites it as own-work / own-data.** |

## Hard Constraints

- Never cite a paper without verifying it exists (DOI check or Google Scholar) — **the seed `references.bib` is unverified; Phase 2 verifies every entry**
- Never use confident language ("demonstrates", "shows") for claims below SUPPORTED tier
- Never claim own unpublished work as established — ovr.news adoption signals are EMERGING at best (HuggingFace downloads are not disaggregable; see PROPOSITION.md)
- Never exceed page budget without an explicit decision record
- Never skip the anti-hallucination checklist for AI-introduced citations
- **This paper describes a working system the author built** — own-data claims about ovr.news (lens distribution, source counts, throughput) follow DR-008: confidence from methodological rigour + reproducibility, not source count. Document the query/measurement that produced each number.
- **Project state goes in this project's in-repo shared `memory/` (`../../memory/`), not in any agent's user-level auto-memory.** This paper's state must not leak into the Claude Code `~/.claude/projects/<slug>/memory/` store. (agent-ready-papers v2.2.0 constraint.)

## Key Files

| File | Purpose |
|------|---------|
| `manuscript.tex` | LaTeX source — **not yet created** (Phase 0 deliverable: outline first) |
| `references.bib` | Bibliography — seeded UNVERIFIED, verify in Phase 2 |
| `vv/claims/claim_registry.md` | All claims with verification status — seeded with the core argument |
| `vv/PAPER_VV_FRAMEWORK.md` | V&V methodology (copied from framework) |
| `writing-guide.md` | Confidence-to-language mapping |
| `glossary.md` | Terminology (journalism × ML × AI-governance) |
| `backlog.md` | Current tasks |
| `hypothesis-log.md` | Provisional positions awaiting future evidence |

## Academic Context

| Related Work | Relationship |
|-------------|-------------|
| Helberger 2024, *FutureNewsCorp* | AI-governance frame: provider/deployer asymmetry, AI Act Art. 52 authenticity, in-house-AI disincentive for small media. **Already read** (notes in ovr.news `LANDSCAPE.md`). |
| Vrijenhoek et al. 2021, *Recommenders with a Mission* (CHIIR) | Normative news-diversity metrics — the evaluation lens for ovr.news's five-lens distribution. **To read (highest payoff).** |
| Anderson, Bell & Shirky 2012, *Post-Industrial Journalism* (Tow) | The post-industrial-journalism scaffold most AI-and-journalism work leans on. **To read.** |
| Simon 2024, *AI in the News* (Tow) | Recent survey placing ovr.news on a contemporary map. **To read.** |
| Karadimitriou 2026 | Synthesis placing constructive + networked + AI journalism in one frame — the trigger for this paper. |
| Byung-Chul Han, *The Crisis of Narration* / *The Reign of Information* | Cited as **tension**: the additive-information critique of any feed. Boundary condition, not endorsement. |
| **ovr.news** (`ducroq/ovr.news`) | **The case/artefact.** This paper is the journalism-studies sibling of `ducroq/augmented-engineering` (which consumes ovr.news as SE-with-AI evidence — different paper, different venue). |

## Current Status

**Phase:** 0 — Framing

**Next priorities:**
1. **Author decision:** pin the angle, paper type (design-science vs perspective vs case study), and target venue. Everything downstream depends on this.
2. Read the three unread cluster papers (Vrijenhoek, Anderson–Bell–Shirky, Simon) → decide if they support the contribution or merely decorate it (the ovr.news `[2026-05-27]` counter-hypothesis).
3. Draft a one-page outline + lock the page budget; then promote claims from the registry into a section structure.

---

*Last updated: 2026-06-24 (scaffolded)*
