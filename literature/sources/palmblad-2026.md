# Palmblad, Ragland & Neely 2026 — GROUNDING.md (L56)

## Bibliographic Info
- **Authors:** Magnus Palmblad, Jared M. Ragland, Benjamin A. Neely
- **Year:** 2026 (v1: 2026-04-23; v2: 2026-07-21)
- **Title:** Agentic AI-assisted coding offers a unique opportunity to instill epistemic grounding during software development
- **Venue:** arXiv preprint (arXiv:2604.21744), 12 pages
- **DOI:** [10.48550/arXiv.2604.21744](https://doi.org/10.48550/arXiv.2604.21744)

## Summary
Proposes GROUNDING.md — a community-governed, field-scoped epistemic grounding document that encodes domain-specific knowledge for AI coding agents. Demonstrated with a concrete example for mass spectrometry-based proteomics (`proteomics_GROUNDING.md`). The document has two components: **Hard Constraints** (non-negotiable validity invariants required for scientific correctness) and **Convention Parameters** (community-agreed defaults). These override all other contexts to enforce validity regardless of user prompts, empowering non-experts to produce correct scientific code. Core claim: "it is easier to have agentic AIs adhere to guidelines than humans," making this the moment to embed domain expertise into automated workflows.

## Key Findings
- Epistemic grounding documents separate into two categories: invariants (must hold for correctness) and conventions (community defaults, overrideable)
- The grounding document takes priority over other agent contexts — the paper says the specification "wins any conflict" and is loaded "with highest priority". ⚠ **Not an unconditional override**: the paper's own testing reports "boundary cases in which compliance degrades under explicit override instructions or weakened normative language", and that it "does not by itself guarantee correctness under all context conditions"
- ⚠ The phrase **"epistemically prior" is not the paper's** — it appears zero times in v1 and v2. The paper uses "epistemic grounding" and "epistemic foundation". The framing is this repo's; the architectural claim is theirs
- Community governance model: field-scoped (not project-scoped), maintained by domain experts rather than software engineers
- Demonstrated in proteomics; the paper suggests the document type "could be used for other domains" — extensible, but the architecture is deliberately **field-scoped**, not domain-agnostic
- Letter-format paper ("12 pages, 1 table" per the authors' own arXiv Comments field; the rendered PDF is shorter) — a proposal with a worked example plus **preliminary proof-of-principle testing** (Claude Code v2.1.90 + NVIDIA Nemotron-3, six adversarial prompts, public validation repo), not a full empirical evaluation

## Relevance to agent-ready-papers
This is a **parallel invention** of the same core pattern this project uses: a constraint document (GROUNDING.md / CLAUDE.md) that encodes domain-specific invariants an AI agent must respect, overriding other contexts. The Hard Constraints / Convention Parameters distinction maps cleanly to the framework's P0 (must-verify) vs P1/P2 (should-verify) tiering. The paper provides **external validation** that the constraint-document pattern generalizes beyond academic writing into scientific software — same architecture, different domain.

Concrete touchpoints:
- **CLAUDE.md Hard Constraints section** — same concept, different scope (project vs field)
- **DR-004 registry model** — Hard Constraints = P0 invariants, Convention Parameters = P1/P2 conventions
- **agent-ready-projects companion repo** — GROUNDING.md is directly applicable to domain-specific coding practices there
- **"Agents adhere to guidelines better than humans"** — the same bet that underlies the framework's authoring-time verification approach
- **Community governance question** — the paper's field-scoped model raises a question the framework hasn't addressed: who maintains the grounding document? (Currently: per-project maintainer; Palmblad proposes: domain community)

## Open Questions
- The paper proposes *field-scoped* grounding (one GROUNDING.md per scientific domain). The framework uses *project-scoped* grounding (one CLAUDE.md per repo). Is there a case for field-scoped constraint documents in academic writing (e.g., a `GROUNDING.md` for conceptual papers, for DSR papers, for perspective papers)?
- The paper's **two-tier constraint taxonomy** (Hard Constraints = invariants, Convention Parameters = defaults) is cleaner than the framework's current flat Hard Constraints list. Should the framework adopt this distinction structurally — splitting CLAUDE.md's Hard Constraints section into labeled invariant and convention groups, mirroring what the claim registry already does with P0/P1/P2 tiers?
- The paper is a proposal with a worked example and preliminary proof-of-principle testing — not a controlled evaluation of whether GROUNDING.md reduces errors in agent-generated code. (Corrected 2026-08-13: this line previously said there was *no* empirical evaluation. False against both versions, which both report the Nemotron testing. Note the split: the *testing* is in v1 and v2; the **degradation boundary cases** and "does not by itself guarantee correctness" are **v2 only**. Cite v2 for the caveat.) Same tier as the framework's own PROPOSITION-level claims about its efficacy.
