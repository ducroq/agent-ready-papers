# DR-010: PROVOCATION as Fifth Unit Type for Speculative-Design Work

---
status: Accepted
date: 2026-05-10
---

## Context

DR-004 (2026-03-02) added three registry unit types — CLAIM, ARGUMENT, PROPOSITION — and reserved DESIGN PRINCIPLE, PROCEDURE, and SYNTHESIS as slots to activate when the framework was applied to non-empirical work. DR-006 (publication roadmap) anticipated such a project. *Fascism Spectrum Disorder* (FSD), a speculative-design book scaffolded against the framework in April–May 2026, is that project. The full audit is in [`audits/feedback-from-fsd.md`](../audits/feedback-from-fsd.md).

FSD surfaced a class of registry units that none of the existing or reserved types describes:

- The DSM-form *FSD diagnostic entry* — a fictional clinical category, held with seriousness inside the fiction while the reader knows it is fictional (a *diegetic prototype* in Kirby's sense).
- A reflexive *Ask* directed at the reader.
- An *It Is Both* paradox box that refuses resolution by design.

These are designed artefacts that make no truth claim. Verifying them as CLAIMs is incoherent (no source applies). They are not ARGUMENTs (no inferential bridge from grounds to conclusion). They are not PROPOSITIONs (no recommendation prescribing action). DESIGN PRINCIPLE in the Hevner sense suggests something empirically testable; PROVOCATIONs specifically refuse that claim.

A literature search surfaced Auger (2013, *Digital Creativity* 24:1) on speculative-design verification: artefacts hold up when they are **plausible, generative, reflexive, and ethically held**. This is not a claim-verification procedure but a *quality-of-speculation* procedure — the right axis for designed artefacts that aren't trying to be true.

## Options Considered

### Option A: Reuse DESIGN PRINCIPLE for speculative-design artefacts
- (+) Slot already reserved; no new type
- (-) DESIGN PRINCIPLE in Hevner's design science sense implies a testable design contribution; speculative-design artefacts refuse that claim by construction
- (-) Conflates two different verification axes (testable design rule vs. quality of speculation)

### Option B: Track speculative artefacts as SPECULATIVE-tier CLAIMs
- (+) Uses existing types
- (-) The diegetic-prototype risk is the *opposite* of CLAIM hallucination: a CLAIM hallucination invents a source for a real-sounding statement, while a PROVOCATION risks being read as a CLAIM with a citable source. The two need different verification procedures, not different tiers of the same one
- (-) "SPECULATIVE CLAIM" still asserts a truth value the artefact rejects

### Option C: Add PROVOCATION as a fifth unit type with Auger-criteria verification and a separate confidence axis
- (+) Names the artefact accurately and gives it a verification procedure that fits its mode
- (+) Confidence tiers (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) measure quality of speculation, not strength of evidence — distinct axis, no conflation with the ESTABLISHED/SUPPORTED/EMERGING/SPECULATIVE scale
- (+) Battle-tested in the FSD scaffold across the diagnostic entry, reflexive Asks, paradox boxes, and the calibration practice
- (-) Adds complexity for projects that don't need it — mitigated by opt-in (default registry type stays CLAIM)
- (-) PROVOCATION joins DESIGN PRINCIPLE / PROCEDURE / SYNTHESIS as four reserved-and-now-active types; clearer naming may be needed if more activate

## Decision

**Option C: PROVOCATION as a fifth unit type, opt-in, activated by speculative-design / design-fiction / diegetic-prototype work.**

### Definition

A **PROVOCATION** is a designed artefact that makes no truth claim. It includes:

- Diegetic prototypes (fictional artefacts presented inside a fiction that signals its fictionality to the reader)
- Reflexive Asks (questions to the reader that change how the reader reads what follows)
- Paradox boxes (constructions that refuse resolution by design)
- Speculative categories that imitate authoritative forms (DSM entries, technical specifications, taxonomic keys) to surface what those forms do

### Verification (Auger 2013 four criteria)

| Criterion | Question | Required marker in prose |
|-----------|----------|--------------------------|
| **Plausible** | Could this exist in some adjacent world consistent enough that a reader holds it seriously? | Internally consistent details; no genre-breaking elements |
| **Generative** | Does the artefact open new questions or interpretive moves that the surrounding prose develops? | Subsequent prose reaches into the artefact, not around it |
| **Reflexive** | Does the artefact, or its framing, signal its own fictionality? | Visible reflexive marker in the prose at every load-bearing moment |
| **Ethically held** | Has the artefact's potential for harm been considered, with mitigations binding for chapter writing? | DR-level pre-commitment; harm consideration documented |

### Confidence Tiers — separate axis

Unlike CLAIM/ARGUMENT/PROPOSITION (which use ESTABLISHED → SPECULATIVE on an evidence-strength axis), PROVOCATIONs use a *quality-of-speculation* axis. Each tier carries a required prose marker so a charitable reader cannot mistake fiction for claim.

| Tier | Assign when… | Required prose marker |
|------|--------------|------------------------|
| **GROUNDED** | Speculation explicitly anchored in cited research; mechanism named; warrant visible | *"If X (source Y), then a speculative manifestation might look like…"* |
| **EXTRAPOLATED** | Extension of an existing pattern (e.g., DSM dimensional approach) into fictional territory; warrant visible but underpinning partial | *"By analogy with X, we propose a fictional Y…"* |
| **PROVOCATIVE** | Deliberately uncomfortable, rhetorical; ethical hedge explicit; no empirical pretension | *"Deliberately uncomfortable: what if…"* |
| **CRITICAL** | The fiction itself critiques an existing system (e.g., DSM form imitated to surface diagnostic reification) | *"By imitating this DSM form we ask…"* |

No marker = indefensible PROVOCATION. Remediation: rewrite to add the marker, or downgrade the entry to EMERGING CLAIM with additional sources.

### Detection rule (round-trip with the existing types)

Run on every entry during registration:

1. Refers to an external source? → **CLAIM**
2. Combines multiple pieces of evidence into a conclusion? → **ARGUMENT**
3. Recommends, proposes, prescribes? → **PROPOSITION**
4. Makes no truth claim, is a designed/fictional artefact? → **PROVOCATION**
5. Looks like a truth claim but is actually a design choice? → **PROVOCATION**; add explicit reflexive marker
6. Reflexive marker absent in the prose? → rewrite, or downgrade to EMERGING CLAIM with additional sources

### Activation

PROVOCATION is **opt-in**. Default registry type remains CLAIM. Activate when the project contains designed artefacts that make no truth claim — speculative design, design fiction, diegetic prototypes, or reflexive constructions inside a non-fiction work. Standard empirical and methodological papers do not need it.

### What this does *not* do

- Does not change CLAIM, ARGUMENT, or PROPOSITION verification
- Does not relax the anti-hallucination checklist for CLAIMs that *do* cite sources inside a speculative-design work
- Does not authorise unsourced authoritative-toned prose as PROVOCATION — the reflexive marker requirement is binding
- Does not activate DESIGN PRINCIPLE, PROCEDURE, or SYNTHESIS — those remain reserved per DR-004

## Consequences

- `templates/vv-framework.md`: PROVOCATION added to §1 (core principle) and §4.1 (verification procedure with Auger criteria)
- `templates/claim-registry.md`: Unit Type Reference table extended; decision tree adds PROVOCATION step; new "Verifying PROVOCATIONs" section; PROVOCATION confidence tiers added as separate axis
- `README.md`: Verification Registry section adds PROVOCATION row; Confidence-to-Language Mapping notes PROVOCATION uses separate axis
- `CLAUDE.md` (root): three-unit-types table updated to four
- DR-004's "non-empirical pivot" reservation: partially activated (PROVOCATION); DESIGN PRINCIPLE / PROCEDURE / SYNTHESIS remain reserved

## Evidence Base

| Source | Contribution |
|--------|-------------|
| Auger (2013, *Digital Creativity* 24:1) | Four-criteria verification (plausible, generative, reflexive, ethically held) |
| Kirby (2010) on diegetic prototypes | Fictional artefacts held with seriousness inside the fiction; reader knows fictional |
| FSD scaffold (`vv/PAPER_VV_FRAMEWORK.md`) | Battle-tested registration of PROVOCATIONs across diagnostic entry, Asks, paradox boxes, calibration practice |
| FSD audit (`audits/feedback-from-fsd.md`) | Synthesis of what generalised back from the FSD scaffold |
| DR-004 (2026-03-02) | Reserved the non-empirical-pivot slot this DR partially activates |

## Revisit If

- A second speculative-design project exposes a PROVOCATION sub-class not covered by the four Auger criteria
- The reflexive marker requirement proves too restrictive for some legitimate speculative form
- DESIGN PRINCIPLE or PROCEDURE need to activate alongside PROVOCATION on the same project (review the naming and overlap)
- Field testing reveals PROVOCATION confidence tiers need refinement
