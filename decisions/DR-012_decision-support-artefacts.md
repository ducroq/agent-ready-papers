# DR-012: Decision-Support Artefacts as Third Non-Paper Application Class

---
status: Proposed
date: 2026-06-01
---

## Context

The framework was originally developed for academic papers. It has since extended along two axes the original name (`agent-ready-papers`) does not advertise:

- **DR-010** (2026-05-10) added PROVOCATION as a fifth unit type for **speculative-design / design-fiction** work, after the FSD book activated DR-004's reserved non-empirical slot.
- **DR-011** (2026-05-12) generalised the multi-model review pattern using a **LinkedIn cross-post + a blog article** as the empirical surface, not a paper. Subsequent applications at grant scale (NLnet v3, 2026-05-22) and at template-revision scale (2026-05-27) widened the evidence base further.

A worked third non-paper application emerged 2026-05-30 in `C:/local_dev/new_hardware/vv/`: a **decision-support artefact for a personal hardware-purchase decision** (~€2k–5k commit, gated on revenue, November 2026 deadline). The framework was applied largely unchanged — typed registry, source tiering, confidence-to-language mapping, anti-hallucination Step 0 + 6-step, DR-011 multi-pass review, Toulmin/Whetten checklists, and the gotcha-log curate loop all worked first time without paper-specific scaffolding adapted.

The framework's README already notes that informal technical communication (Slack, WhatsApp, emails) is in-scope. What is missing is a named *third application class* — alongside the academic-paper class and the speculative-design class — that decision-support artefacts can be recognised as, so future projects know whether the framework applies before they invest in the scaffold.

This DR proposes naming that class.

### Triggering observation (2026-05-30 session at `new_hardware/vv/`)

79-entry registry across 8 sections; 71% overall coverage / 78% on P0; DR-011 Pass 1 (Haiku) + Pass 2 (Opus) applied with near-zero overlap (DR-011 disjoint-coverage prediction replicated). Confidence-to-language mapping, anti-hallucination Step 0 + 6-step, and Whetten boundary-condition machinery all fired correctly. Full session record and pattern observations in [`audits/feedback-from-decision-support.md`](../audits/feedback-from-decision-support.md).

## Options Considered

### Option A: Leave the framework unscoped beyond paper + speculative-design
- (+) Simplest; no new class
- (+) Honours the framework's name (`agent-ready-papers`)
- (-) Decision-support work that fits the framework gets discovered ad-hoc rather than scoped intentionally; future maintainers cannot tell the framework was already proven on a non-paper, non-design surface
- (-) The README extension noted in DR-010 / DR-011 stays informal; no canonical entry point for the third class

### Option B: Rename the repo to acknowledge wider scope
- (+) Honest about the framework's current span
- (-) Breaks every external reference (commits, links, citations in published work, GitHub issues)
- (-) The repo-name caveat is already deferred per `audits/feedback-from-fsd.md`; this DR is not the right surface to force that decision
- (-) Conflates *scope expansion* (a methodological question) with *naming* (a logistical question)

### Option C: Name decision-support artefacts as a third opt-in application class, leave the repo name alone
- (+) Methodological clarity without renaming overhead
- (+) Parallels DR-010 (speculative-design class) and DR-011 (the methodological pattern that crossed paper/non-paper boundary)
- (+) Gives future maintainers a named scope to recognise; one-line scope statements in README per class
- (+) Empirical evidence is N=1 worked example, structurally consistent with how DR-010 and DR-011 landed
- (-) Adds a third application class to the framework's surface; risk of over-naming
- (-) The structural-assumptions list (below) needs care — too narrow and the class misses cases; too broad and it loses meaning

## Decision

**Option C: Decision-support artefact as a third opt-in application class.**

### Definition

A **decision-support artefact** is a structured V&V scaffold built around a consequential decision — vendor selection, hardware purchase, architectural choice, regulated-domain adoption, strategic / policy decision — where the artefact is the basis for the commit and the cost of being wrong exceeds the cost of running V&V.

### Structural assumptions (where the class is well-formed)

The framework was applied first time without paper-specific adaptation when the following five conditions held in the worked example:

1. There is at least one load-bearing PROPOSITION whose grounding chain can be traced.
2. Claims have external evidence (literature, vendor docs, market data, public reporting) that varies in credibility and benefits from typing + tiering.
3. The output is mostly prose / structured tables (not code, not media).
4. The cost of being wrong on the PROPOSITION exceeds the cost of running V&V.
5. The decision spans enough time that session continuity matters.

These five conditions are **sufficient** based on N=1. Whether all five are *necessary* is untested — some projects may benefit from the framework with only three or four conditions met, and others may need additional conditions the worked example did not surface. Treat the list as a starting heuristic, not a gate.

### Where the class is NOT well-formed

The framework should not be applied to:

- Small purchases (cost of V&V exceeds cost of being wrong)
- Real-time chat (no session continuity needed)
- Throwaway scripts (no PROPOSITION; correctness verified by execution)
- Pure creative writing without truth claims
- Anything with established compliance audit conventions (use those, not this)

### What the class inherits unchanged from the paper-application class

- Typed registry (CLAIM / ARGUMENT / PROPOSITION; PROVOCATION opt-in)
- Source tiering A–F
- Confidence-to-language mapping
- Anti-hallucination Step 0 + 6-step (and Step Z for projects with PROVOCATION semantics)
- DR-011 multi-pass review (Pass 1 + Pass 2 default; Pass 3 for high-stakes only)
- Toulmin checklist for ARGUMENTs; Whetten checklist for PROPOSITIONs
- Gotcha-log + curate loop
- Decision records for scope and methodology choices

### What is paper-specific and does not apply

- Page budgets (registry is the size it needs to be)
- LaTeX / BibTeX validation
- Journal style guides as oracle
- Author guidelines as oracle
- Co-author signoff as a gate
- Submission format gates

### Adoption readiness

Borrowing the Tier 1/2/3 merge-readiness split from `audits/feedback-from-fsd.md`:

- **Ready to merge (battle-tested through this decision):**
  - The application-class definition and structural assumptions above
  - A README scope section listing the three classes (academic / speculative-design / decision-support) with one-line scope each
  - Acknowledgement that the framework's existing scaffolding applied unchanged in the worked example

- **Incubate (proven once at decision-artefact scale, re-evaluate at next application):**
  - The five-condition test as a sufficient gate for applying the framework (currently sufficient but not necessary; some projects may benefit even when one condition is borderline)
  - Whether the framework needs a per-class adaptation pattern (e.g., "what to skip for decision-support") in `templates/CLAUDE.md`, or whether the README scope statement suffices

- **Pattern note (useful when applicable):**
  - Three specific failure modes surfaced at decision-support scale (see `audits/feedback-from-decision-support.md`) that may generalise back to paper work; each marked *incubate* pending a second sighting.

## Patterns Surfaced — Filed Separately

The worked example surfaced three patterns that are general framework improvements (category-swap traps in evidence selection; trade-press headline numbers as inverse-hallucination candidates; workload-fit smuggling in synthesis prose). These are not specific to the decision-support class; they are observations made during the application. To keep this DR focused on the application-class question, the patterns are filed in [`audits/feedback-from-decision-support.md`](../audits/feedback-from-decision-support.md), each marked *incubate* pending a second sighting before promotion to a template checklist line.

## Consequences

- `README.md`: add a "What does this framework apply to?" section listing the three application classes (academic / speculative-design / decision-support) with one-line scope each. The existing "what doesn't work" section that names informal technical communication remains as a finer-grained negative scope.
- `decisions/DR-006_publication-roadmap.md`: review whether Paper 2 (DSR) should engage the third class as part of its evaluation scope, or whether the third class is out-of-scope for Paper 2 and warrants its own write-up.
- `templates/CLAUDE.md`: consider a per-class adaptation note (what to keep, what to skip) — incubate pending second decision-support application.
- `audits/feedback-from-decision-support.md`: filed with this DR. Captures the worked example, what confirmed unchanged, what did not apply, and the three patterns surfaced (each marked *incubate*). Follows the pattern of `feedback-from-fsd.md`, `feedback-from-blog-application.md`, `feedback-from-grant-application.md`, `feedback-from-template-revision.md`.
- Active papers (`papers/perspective/`): no immediate action. If Paper 1 is later restructured along the methodological-reframe axis the maintainer is currently considering, the three-class scope statement may inform §2's gap description.
- The repo-name question (`agent-ready-papers` vs. a wider name) remains deferred per `audits/feedback-from-fsd.md`. This DR does not force that decision; it does, however, raise the cost of *not* deciding by adding a third application class beyond the name's scope.

## Key Insight (Hypothesis, Not Established)

The N=1 evidence is consistent with — but does not establish — a methodological hypothesis: *the framework's core (typed registries, confidence-to-language mapping, multi-pass review, anti-hallucination, the curate loop) may be domain-general, with paper-specific scaffolding (page budgets, LaTeX, journal style) as a thin layer above it.*

Three observations are consistent with this hypothesis:

- Paper-application class: original realisation.
- Speculative-design class (DR-010): required *one addition* (PROVOCATION unit type with Auger-criteria verification and a separate confidence axis), not a re-architecting.
- Decision-support class (this DR): required *nothing new* in the worked example.

What would refute the hypothesis: a harder decision-support application (regulated, multi-stakeholder, time-pressured) that requires new core machinery rather than scaffolding tweaks. What would strengthen it: a fourth application class activating with only scaffolding adjustments. Until then, the hypothesis is at SPECULATIVE confidence by the framework's own tier discipline.

Naming the third class is justified by the worked example without committing to the broader hypothesis.

## Evidence Base

- Worked example: `C:/local_dev/new_hardware/vv/` (2026-05-30 session). 79 registry entries, 71% coverage, DR-011 multi-pass applied (Pass 1 + Pass 2; Pass 3 deferred).
- Originating issue: [ducroq/agent-ready-papers#14](https://github.com/ducroq/agent-ready-papers/issues/14)
- Precedent for forward-feedback flowing back as a DR: `audits/feedback-from-fsd.md` (DR-010), DR-011 (blog application).
- N=1 caveat: the worked example is a single project, single author, single domain (hardware purchase). Generalisability to vendor-selection, architectural choice, regulated-domain adoption, and policy-decision support is *plausible* on the structural-assumptions argument but not yet exercised.

## Open Questions Carried Forward

- **Sufficient vs. necessary conditions.** The five-condition test (above) is currently *sufficient* for applying the framework. Whether all five are *necessary* is untested — some decision-support work may benefit from the framework with only three or four conditions met.
- **Per-class adaptation pattern.** Does `templates/CLAUDE.md` need a per-class "what to skip" section, or is the README scope statement enough? Re-evaluate after a second decision-support application.
- **Repo-name overhead.** Each additional application class makes the `agent-ready-papers` name slightly more misleading. The repo-name question is deferred but the cost compounds.

## Revisit If

- A second decision-support application fails to apply the framework cleanly (some claimed-unchanged element actually needed adaptation) → revise the *"inherits unchanged"* list.
- The five-condition test misses a project that intuitively belongs (or includes a project that intuitively doesn't) → tune the conditions.
- A fourth application class emerges (e.g., regulated-domain compliance work) → consider whether the README scope statement scales, or whether the framework needs a higher-level taxonomy.
- The Paper 1 reframe pushes the framework's methodological identity to the front of the contribution → this DR's "framework is methodological, not domain-specific" key insight may become a citable claim in Paper 1 itself, in which case the DR's evidence base should be hardened.
