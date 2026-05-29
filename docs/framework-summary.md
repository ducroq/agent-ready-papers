# Framework Summary

<!-- Reference card for the verification framework. Loaded when working with
     claims, registry entries, quality gates, or confidence-to-language
     calibration. Normative source remains the templates — this file
     summarises so CLAUDE.md doesn't have to. -->

## Registry Unit Types

Three default types, each with a structured verification procedure:

| Type | Question | Framework |
|------|----------|-----------|
| CLAIM | Does the source say this? | Citation checking + anti-hallucination |
| ARGUMENT | Is the reasoning valid? | Toulmin (claim, grounds, warrant, backing, qualifier, rebuttal) |
| PROPOSITION | Are conditions specified? | Whetten (What/How/Why/Who-Where-When, boundary conditions) |

For papers with quantitative content, a fourth verification procedure (not a registry unit type):

| Type | Question | Framework |
|------|----------|-----------|
| CALCULATION | Does the result follow from the formula? | Numerical reproduction (equation-checker) |

For speculative-design / design-fiction / diegetic-prototype work, an opt-in fifth registry unit type (see DR-010):

| Type | Question | Framework |
|------|----------|-----------|
| PROVOCATION | Plausible, generative, reflexive, ethically held? | Auger 2013 four criteria; separate confidence axis (GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL) with required prose markers |

Normative source: `templates/vv-framework.md` §1 + §4.1; `templates/claim-registry.md` Unit Type Reference.

## Quality Gates

```
Gate 1 (Draft Complete)
  → Gate 2 (Verification Complete)
    → Gate 2.5 (Internal Consistency)
      → [conditional gates 2.6 / 2.7 / 2.8 if triggered]
        → Gate 3 (Review Complete)
          → Gate 4 (Submission Ready)
```

Conditional gates between 2.5 and 3, activated by trigger only:

| Gate | Activates when |
|------|----------------|
| 2.6 Reflexivity | PROVOCATIONs are present in the registry |
| 2.7 Ethical Review | The project engages contested topics |
| 2.8 Voice Consistency | The work has a voice-driven register beyond standard academic prose |

Normative source: `templates/vv-framework.md` §7.

## Confidence Tiers → Language

For CLAIM / ARGUMENT / PROPOSITION:

| Tier | Language examples |
|------|-----------------|
| ESTABLISHED | "demonstrates", "shows", "confirms" |
| SUPPORTED | "indicates", "supports", "evidence suggests" |
| EMERGING | "may", "preliminary evidence", "initial findings suggest" |
| SPECULATIVE | "warrants investigation", "remains unclear", "we hypothesize" |

For PROVOCATION (separate axis — quality of speculation, not strength of evidence; see DR-010):

| Tier | Required prose marker |
|------|------------------------|
| GROUNDED | *"If X (source Y), then a speculative manifestation might look like…"* |
| EXTRAPOLATED | *"By analogy with X, we propose a fictional Y…"* |
| PROVOCATIVE | *"Deliberately uncomfortable: what if…"* |
| CRITICAL | *"By imitating this DSM form we ask…"* |

Normative source: `templates/writing-guide.md` Language Calibration; `templates/claim-registry.md` Confidence Tier Reference.

## Terminology Note: "Grounding" / "GROUNDED"

Two senses appear in this repo. Don't conflate:

| Sense | Meaning | Layer |
|-------|---------|-------|
| **Grounding (AI sense)** | Anchoring model output to retrieved, verifiable sources at inference time — RAG, citation-enforced generation, web-search-augmented answers. A model-level technique for reducing hallucination. | Model layer |
| **GROUNDED (PROVOCATION tier)** | A speculative-design entry explicitly anchored in cited research, with mechanism named and warrant visible (DR-010). A *confidence tier* for speculation, not a generation technique. | Process layer |

The framework sits **downstream** of model-layer grounding (see `README.md` opening). Even a well-grounded model can produce un-warranted arguments, mis-calibrated confidence, or PROVOCATIONs without the required reflexive marker. Grounding addresses *did the source say this*; the framework adds *is the reasoning valid, is the confidence calibrated, is the speculation held ethically*.

Other grounding senses from AI literature — *temporal* (current-state retrieval), *symbolic* (word-to-referent correspondence), *multimodal* (cross-sensory anchoring) — are noted here only to prevent confusion when reading source literature; they are not load-bearing for this framework.
