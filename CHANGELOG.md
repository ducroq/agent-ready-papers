# Changelog

All notable changes to `agent-ready-papers`. Adopters can check their paper project's framework version against this log to see what has changed.

<!-- Maintainer release process:
     When promoting a `vX.Y.Z (candidate, unreleased)` block to a dated release,
     also tag the release commit:

         git tag vX.Y.Z <commit>
         git push --tags

     Tags let adopters `git checkout vX.Y.Z` to inspect a pinned version and
     `git diff vX.Y.Z..vX.Y+1.0 -- templates/` to preview an upgrade.

     Versioning convention (mirrors agent-ready-projects):
     - MAJOR — breaking changes to template surfaces or DR semantics
     - MINOR — new templates, patterns, application classes, or behaviours
     - PATCH — docs-only changes, clarifications, cross-reference adds
-->

## v1.3.0 (2026-06-01)

Seven items landed: DR-012 names decision-support as a third opt-in application class; DR-011 evidence base extended to N=2 within-Claude; anti-hallucination gains WebFetch fallback discipline; claim-registry adds Coverage-by-Type cut; Paper 1 registry migrated to per-type sub-tables; Engineering Fidelity audit files archived outside the repo; Paper 1 §4 rewritten from "three audits" to "two audits" to reflect the reduced evidence base (Gate 2 invalidation acknowledged — Gate 2.5 re-check is co-author's call at Gate 3).

### New decisions
- **[DR-012](decisions/DR-012_decision-support-artefacts.md)** — *Decision-Support Artefacts as Third Non-Paper Application Class.* Status: Proposed. N=1 worked example (`new_hardware/vv/`, 2026-05-30). Five sufficient conditions for the class named; what is paper-specific and does not apply (page budgets, LaTeX, journal style, author guidelines, co-author signoff, submission gates) explicitly listed. Self-critique applied before commit — see commit message.

### New templates / pattern additions
- **`templates/claim-registry.md`** — Coverage Summary now cuts both by Priority (existing) and by Type (new). Type-level Gate 2 expectation: every registered ARGUMENT and PROPOSITION should be `[x]` before gating, since each is load-bearing for the contribution. Closes #10.
- **`templates/anti-hallucination.md`** — Adds "Verifying Web Sources: WebFetch Fallback Discipline" between *Verifying Negative Claims* and Step Z. Names two failure modes (subpage blindspot; transport failure) and prescribes a fallback ladder (specific URL → homepage → `site:` search → sitemap). Two worked examples from the 2026-05-22 NLnet v3 application. Closes #8 (Proposal 2; Proposal 4 closed via the DR-011 evidence-base extension below).

### Decision extensions
- **[DR-011](decisions/DR-011_multi-model-review-pattern.md)** Evidence Base + Open Questions extended with grant-scale N=2 replication (NLnet NGI Zero Commons Fund v3, 2026-05-22). Within-Claude disjoint-coverage pattern replicated; cross-family generality still untested. (Addresses #8 Proposal 4.)

### New audits
- **`audits/feedback-from-decision-support.md`** — Worked example for DR-012. Captures the 2026-05-30 session, what confirmed unchanged, what did not apply, three patterns surfaced at decision-support scale (each marked *incubate* pending a second sighting), and open questions (sub-class differentiation, calibration to stakes, time-pressured application).

### Paper 1
- **`papers/perspective/vv/claims/claim_registry.md`** — Migrated from legacy single-mixed-type table per section to per-type sub-tables (CLAIMs / ARGUMENTs / PROPOSITIONs). Prose verification blocks (S3-4 warrant, S4-4 warrant, S5-1 premises/reasoning/boundaries) folded into checklist-aligned columns. List delimiter normalised to `;`. Coverage Summary gains by-type cut. Closes #11. Self-eating-dog-food restored between template and first instance.

### Removals
- **Engineering Fidelity audits archived externally.** `audits/engineering-fidelity-retrofit.md` and `audits/engineering-fidelity-audit-2.md` moved to `OneDrive/.../Johan/EngineeringFidelity/framework-audits/` on 2026-06-01. The Engineering Fidelity content belongs with its own project, not as evidence carried by this framework repo.
  - **Adopter action:** none required for new adopters. Existing adopters who linked to either file in their own work need to re-link to the external archive or replace with their own audit.
- **Paper 1 manuscript §4** rewritten from "three audits" to "two audits" (proposition + technology). The third-audit paragraph (lines 457-464 previously) describing the engineering-characterisation audit is removed. Limitations updated from "all three audits" / "all three projects" to "both audits" / "both projects." Domain cluster updated from "medical simulation and measurement science" to "medical simulation and instrumentation." Abstract reflects the count change. **Gate 2 invalidation:** this is a content change to a registry that previously held a verification freeze. Gate 2.5 (Internal Consistency) re-check is the co-author's call at Gate 3.
- **Paper 1 supporting files** (`papers/perspective/CLAUDE.md`, `backlog.md`, `backlog-paper2.md`, `writing-guide.md`, `vv/claims/claim_registry.md`): EF references removed or repathed. S4-4 ARGUMENT in the registry rewritten to cite two audits with N=2 caveat explicit.
- **`docs/METHODOLOGY.md`**: removed the EngineeringFidelity (MST Paper) source-project subsection; updated opening from "Three" to "Two paper projects"; removed broken `engineering-fidelity-retrofit.md` link; updated remaining "all three" / "original three" mentions to source-project-agnostic phrasing; "What Survived" table's *Where it came from* column updated to refer to "earlier source-project work" rather than naming EF.
- **README**: dropped "across two journals (IEEE TIM, MST)" parenthetical and the "three real paper projects" count from the tagline and Further Reading. The framework's tagline is now journal-agnostic and count-agnostic.
- **`decisions/DR-006_publication-roadmap.md`**: updated "three real paper projects (IEEE TIM, MST, medical education)" to "two real paper projects (IEEE TIM, medical education)"; Paper 2 evaluation-evidence list updated to drop EngineeringFidelity; Paper 2 timeline annotation acknowledges that a prospective case study is likely needed.
- **`decisions/DR-008_empirical-paper-support.md`**: top-of-file note added pointing to the external archive. Findings table preserved as historical record of the audits that motivated this DR.
- **`audits/driven-pendulum-retrofit.md`**: top-of-file note added pointing to the external archive. Cross-project comparison data (Appendix) preserved as historical record reflecting framework state at audit time.
- **`audits/equation-verification-journey.md`** and **`audits/proposition-retrofit.md`**: "three paper projects" / "three source projects" mentions softened to project-count-agnostic phrasing.

### Versioning
This is the framework's first explicitly-versioned release. Prior versions (v1.0.0 through v1.2.0 below) are reconstructed retroactively from the git history. Going forward, releases follow the maintainer-release-process block at the top of this file.

---

## v1.2.0 (2026-05-29)

Multi-pass review pattern + structural rationale + per-type registry surface. The framework's most consequential mid-2026 expansion — DR-011 made *bias-escape* a first-class verification dimension; the subsequent rationale work named the structural principles already implicit across the framework.

### New decisions
- **[DR-011](decisions/DR-011_multi-model-review-pattern.md)** (2026-05-12) — *Multi-Model Review Pattern.* Three-pass review with explicit bias-escape semantics: Pass 1 (intra-family small) escapes sunk-cost from the drafting session; Pass 2 (intra-family large) does the same with argument-shape critique character; Pass 3 (cross-vendor) escapes training-data and stylistic priors and requires a mandatory style/voice filter. Naming convention chosen ("Pass", not "Tier") to avoid collision with existing tier semantics. Status: Proposed; evidence N=1 at blog scale.
  - **Design Rationale: Functorial Composition** added 2026-05-29 (commit `74d7976`, closes #13). Each pass is a different functorial view; their combined verification is the limit. Makes adding/skipping/retiring a pass decidable on invariant-coverage grounds, not empirical hand-waving. Background: `docs/category-theory-as-design-lens.md`.
- **[DR-005](decisions/DR-005_nanoarguments-as-argument-layer-peer.md)** addition — Nanoarguments (NLnet NGI Zero) added as an argument-layer peer + revisit trigger (commit `299a521`).

### Template / pattern additions
- **`templates/claim-registry.md`** (commit `97f3c3b`, closes #9) — Per-type sub-tables (one each for CLAIMs / ARGUMENTs / PROPOSITIONs / PROVOCATIONs) with checklist-aligned columns. Required verification fields (Grounds, Warrant, Rebuttal for ARGUMENT; Constructs, Relationship, Premises, Reasoning, Boundary conditions, Alternatives engaged for PROPOSITION; Plausibility evidence, Generative move, Reflexive marker, Ethics commitment for PROVOCATION) now have structural homes in columns rather than orbiting prose blocks below the table. `;` list-delimiter convention named explicitly. Replaces the legacy single-mixed-type table.
- **`templates/writing-guide.md`** (commit `a294361`, closes #12) — Tier-monotonicity principle added: manuscript language must sit at or below the registered confidence tier. Citation drift is named as a tier-monotonicity failure, not a separate rule of thumb.
- **`templates/review-prompt.md`** — "Style/voice rules to filter against" added as a required-with-default field per DR-011 Pass 3 requirement.
- **`templates/anti-hallucination.md`** — Step 7 (Multi-Pass Review Across Model Families) added per DR-011.

### Docs / structural rationale
- **`docs/category-theory-as-design-lens.md`** (commit `f79b6f0`) — New note. Names the structural lens implicit across DR-004 (typed registry), DR-011 (multi-pass functors), and the layered memory system. Vocabulary stays in the rationale doc; templates and slash commands remain free of category-theory terminology.
- **Grounding disambiguation** (commit `ff44246`) — "Grounding" in the AI sense (RAG, retrieval-augmented generation) explicitly distinguished from PROVOCATION-tier GROUNDED in the writing-guide and framework-summary.

### Audits added
- **`audits/feedback-from-blog-application.md`** — DR-011 triggering observation, three-reviewer comparison on a LinkedIn cross-post.
- **`audits/feedback-from-grant-application.md`** — NLnet NGI Zero Commons Fund v3 (2026-05-22) application: surfaces WebFetch subpage-blindspot, WebFetch 403 fallback, cross-document inheritance patterns (each captured as Proposals in #8).
- **`audits/feedback-from-template-revision.md`** — Multi-model review log for #9 (claim-registry per-type sub-tables).

### Adopter notes
- Pre-existing registries with the legacy single-mixed-type table still work; migration to per-type sub-tables is mechanical and recommended at next major revision. Paper 1's registry migrates in v1.3.0 (closes #11).
- Pass 1 + Pass 2 default applicability ("every publish" / "every major revision") is provisional at blog and grant scale; full-paper scale untested as of v1.2.0.

---

## v1.1.0 (2026-05-10)

Speculative-design extension. DR-010 activates DR-004's reserved non-empirical slot with PROVOCATION as a fifth opt-in unit type. The framework now formally supports speculative-design / design-fiction / diegetic-prototype work.

### New decisions
- **[DR-010](decisions/DR-010_provocation-unit-type.md)** — *PROVOCATION as Fifth Unit Type for Speculative-Design Work.* Status: Accepted. PROVOCATION is a designed artefact that makes no truth claim. Verification: Auger 2013 four criteria (plausible / generative / reflexive / ethically held). Separate confidence axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL), each tier carrying a required prose marker. Opt-in: default registry type remains CLAIM. Activated by the FSD speculative-design book.

### Template / pattern additions
- **`templates/claim-registry.md`** — PROVOCATION row in the Unit Type Reference; PROVOCATION-tier confidence row in the Confidence Tiers table; reflexive-marker required field. Detecting-mistyped-entries decision tree extended (questions 6 and 7).
- **`templates/anti-hallucination.md`** — Step Z (Inverse Hallucination Check, PROVOCATION-specific) added. Catches the failure mode where speculation is presented as if sourced — the opposite of standard citation hallucination.
- **`templates/vv-framework.md` / quality gates** — Three project-conditional gates added:
  - **Gate 2.6 — Reflexivity.** Every PROVOCATION carries a reflexive marker visible in the prose.
  - **Gate 2.7 — Ethical Review.** For projects engaging contested topics (multi-case treatment, paired-mirror rule, no real-world group pathologised).
  - **Gate 2.8 — Voice Consistency.** For voice-driven work (defined voice manifest binding for every chapter).

### Audits added
- **`audits/feedback-from-fsd.md`** — *Fascism Spectrum Disorder* speculative-design book scaffolded against the framework. Tier 1 / Tier 2 / Tier 3 adoption-readiness discipline introduced. Tier 1 (PROVOCATION + tiers + gates + Step Z) lands as v1.1.0; Tier 2 items (multi-reviewer round template; cross-model verification; DR amendment pattern) carried as incubation; Tier 3 patterns (per-chapter obviousness test; compositional discipline; genre-mismatch reception risk; calibration vs awareness) noted but not promoted.

### Framework scope extension
- **`README.md`** — Scope note added: framework now covers non-fiction beyond academic papers. Speculative-design / design-fiction work supported via PROVOCATION opt-in.
- **`docs/METHODOLOGY.md`** — FSD documented as a forward extension; forward-extension pattern itself documented as part of the methodology.

### Adopter notes
- PROVOCATION is opt-in. Projects without speculative-design content can ignore the new unit type, gates 2.6/2.7/2.8, and Step Z entirely. The standard CLAIM / ARGUMENT / PROPOSITION trio remains unchanged.
- Tier 2 / Tier 3 patterns from the FSD audit are deferred until corroborating evidence accumulates (battle-tested-once is not enough for full promotion).

---

## v1.0.0 (2026-05-09)

Baseline release of the framework as developed through 2026-04. Captures the state reached through three retrospective paper-project audits, ten decision records (DR-001 through DR-009 plus DR-010 reserved), 47 indexed literature sources, and active development of Paper 1 (Verification Gap).

### Decisions in scope at v1.0.0
- **DR-001** through **DR-009** as documented in [`decisions/`](decisions/).
- Notable highlights:
  - **DR-002** — Confidence tiers (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) and the language-calibration mapping.
  - **DR-004** — Typed verification model (CLAIM / ARGUMENT / PROPOSITION); reserved slots for DESIGN PRINCIPLE / PROCEDURE / SYNTHESIS for future non-empirical work (DR-010 activates one such slot in v1.1.0).
  - **DR-005** — Nanoarguments / argument-layer peer concept (extended in v1.2.0).
  - **DR-006** — Publication roadmap (Papers 1 / 2 / 3).
  - **DR-007** — SE-inspired verification identity.
  - **DR-008** — Methodological-facts exception for own-data claims.
  - **DR-009** — Calculation verification as distinct procedure (prompt-matters-more-than-model finding).

### Templates in scope at v1.0.0
- `templates/CLAUDE.md` — Paper project identity template.
- `templates/claim-registry.md` — Registry structure with P0/P1/P2 priority, typed verification (legacy single-mixed-type table format; migrated to per-type sub-tables in v1.2.0).
- `templates/vv-framework.md` — Verification & validation framework, quality gates.
- `templates/writing-guide.md` — Confidence-tier to language mapping.
- `templates/review-prompt.md` — Structured peer review simulation (single-shot pre-DR-011).
- `templates/anti-hallucination.md` — Step 0 + 6-step citation verification (pre-Step-Z, pre-Step-7).
- `templates/equation-checker.md` — Mechanical equation verification (DR-009).
- `templates/decision-record.md` — DR template.
- `templates/glossary.md` — Cross-domain terminology.
- `templates/key-quotes.md` — Reference quotes.
- `templates/physics-verification/` — Physics-verification template family (cross-document consistency, scope-domain registry, estimation/limiting-case/dimensional/two-paths checkers, lean-as-optional-tier).

### Audits in scope at v1.0.0
- Three retrospective paper-project audits: proposition (CPR manikin feedback accuracy), technology (IEEE TIM sensor integration), and engineering fidelity (MST manikin characterisation). The engineering-fidelity audits are archived externally as of v1.3.0; the audit findings remain in the framework's history but are no longer carried in the repo.
- `audits/equation-verification-journey.md` — DR-009 discovery log.
- `audits/driven-pendulum-retrofit.md` — Cross-project comparison with the driven-pendulum design project.

### Paper 1 state at v1.0.0
- First draft of `papers/perspective/manuscript.tex` (~3,450 words, 5 sections + Appendix A).
- 19-entry claim registry at 100% coverage (P0 / P1 / P2 all 100%).
- 14 references in `references.bib`, all DOI-verified.
- Anti-hallucination checklist: 14/14 references pass.
- Peer-review simulation: 3.95/5.0 (upper "Minor revision").

### Adopter notes
- v1.0.0 is the baseline pin for adopters who started with this framework before the speculative-design extension. Upgrading to v1.1.0 is opt-in (PROVOCATION is opt-in); upgrading to v1.2.0 brings the multi-pass review pattern as a recommended-but-not-required workflow improvement.

---

*The framework's pre-v1.0.0 history (template extraction from three real paper projects, DR-001 through DR-009 evolution) is documented in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) rather than enumerated as separate version blocks here.*
