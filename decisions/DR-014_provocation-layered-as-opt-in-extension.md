# DR-014: PROVOCATION as Explicit Opt-In Extension Over Core Unit Types

---
status: Proposed
date: 2026-06-08
---

## Context

External feedback (June 2026, Reviewer 1) flagged that PROVOCATION (added in DR-010, v1.1.0) adds complexity to the core framework that empirical-paper readers must mentally filter:

> The PROVOCATION unit type is well-motivated by the speculative-design project (DR-010), and the GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL confidence axis is genuinely useful for that genre. But it adds meaningful complexity to the core framework and applies to a narrow audience. A reader working on a standard empirical paper has to mentally filter out the PROVOCATION references throughout the README, the quality gates, the claim registry, and the anti-hallucination checklist.

Reviewer 3 (Copilot) raised a parallel concern about target-audience boundaries — the framework now supports three application classes (paper, speculative-design via DR-010, decision-support via DR-012), and the README should state more bluntly which audience is primary.

This DR proposes how to keep the speculative-design support (DR-010 is binding and not under reconsideration) while reducing cognitive load for empirical-paper readers, who are the majority audience.

### Status of related work

- **DR-010** — Accepted (v1.1.0). PROVOCATION as fifth opt-in unit type. Verification via Auger 2013 four criteria. Separate confidence axis: GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL with required prose markers.
- **DR-012** — Proposed (v1.3.0). Decision-support artefacts as third application class.
- **Gates 2.6 (Reflexivity) / 2.7 (Ethical Review) / 2.8 (Voice Consistency)** — landed in v1.1.0, marked *conditional* in the README. These already follow the opt-in pattern this DR proposes to extend to PROVOCATION itself. The conditional-gate precedent matters: the framework already knows how to do opt-in cleanly; PROVOCATION's current placement is inconsistent with that pattern.

## Options Considered

### Option A: Status quo
- (+) No restructure cost.
- (+) Honours DR-010 verbatim.
- (-) Empirical-paper readers continue to filter PROVOCATION references through the README, registry template, anti-hallucination checklist (Step Z), writing guide.
- (-) Inconsistent with the conditional-gates pattern (2.6–2.8) that the framework already uses for opt-in content.

### Option B: PROVOCATION + Step Z + the GROUNDED/EXTRAPOLATED/PROVOCATIVE/CRITICAL axis move into a separate extension doc, referenced from core but not inlined
- (+) Empirical readers see only CLAIM / ARGUMENT / PROPOSITION / CALCULATION in core templates and main README sections.
- (+) Speculative-design adopters reference one extension doc plus DR-010 (already required).
- (+) Mirrors the conditional-gates pattern already in use.
- (+) Establishes a `templates/extensions/` pattern future application-class-specific content can follow.
- (-) Restructure cost: README, `templates/claim-registry.md`, `templates/writing-guide.md`, `templates/anti-hallucination.md`, `templates/vv-framework.md`, `docs/framework-summary.md` need editing.
- (-) Risk of breaking Paper 1's registry or supporting files if any reference is missed.
- (-) Splits content currently in one place — adopters may not find the extension immediately.

### Option C: Hide PROVOCATION behind a CSS-style fold in the README only; keep templates unchanged
- (+) Minimal restructure cost.
- (+) Empirical-paper readers see fewer PROVOCATION references on the public-facing README.
- (-) Templates still inline PROVOCATION; adopters who reach the templates still filter.
- (-) Cosmetic, not structural — the reviewer's concern was about cognitive load across multiple files, not just the README.

### Option D: Inline + label everywhere as "speculative-design only"
- (+) Less restructure than Option B.
- (+) Clear which content is for which audience.
- (-) Labels add their own clutter; reading "(speculative-design only)" repeatedly is also cognitive load.
- (-) Does not solve the reviewer's concern, just relabels it.

## Proposed Decision (pending Paper 1 impact assessment)

**Option B: PROVOCATION + Step Z + the GROUNDED/EXTRAPOLATED/PROVOCATIVE/CRITICAL axis move into a separate extension doc, referenced from core but not inlined.**

This DR is **Proposed**, not Accepted. The decision is contingent on three pending checks documented in *Pending Assessment* below.

### Reconciliation with DR-017 (2026-06-24): Step Z decouples from PROVOCATION

DR-017's cross-repo evidence (agent-ready-assessment's `Reproduction_Verification_Prompt.md`) falsifies a premise this DR rested on: that **Step Z is PROVOCATION-coupled**. Assessment applies Step Z — the *tier-monotonicity violation* check, where a sentence's language tier exceeds the confidence tier its evidence supports — to ordinary student reports containing **no PROVOCATION entries at all** (single-run-as-measurement, uncited numbers, latency claims with no protocol). Step Z is therefore **audience-general**, not speculative-design-only.

This changes the layering for Step Z *only*:

- **PROVOCATION + the GROUNDED / EXTRAPOLATED / PROVOCATIVE / CRITICAL axis** → extraction to `templates/extensions/provocation.md` proceeds as proposed. Unchanged.
- **Step Z** → **stays in core** `templates/anti-hallucination.md`, *generalized* from its current PROVOCATION-gated form (the present "standard empirical and methodological projects can skip this section" gate is removed) to the general tier-monotonicity check. The proposed `templates/extensions/anti-hallucination-step-z.md` is **withdrawn** — not created.

This serves DR-014's own goal *better*. The cognitive-load concern was that empirical readers must filter narrow-audience content. A general Step Z is **not** narrow-audience content — overclaiming (language above evidence) is a failure mode of empirical papers too — so keeping it in core is correct, while only the genuinely speculative-design material (PROVOCATION) moves out. The scope bullets below are amended accordingly.

### Scope of the proposed change

If accepted, the following changes land together as a single coordinated commit batch:

- **New file**: `templates/extensions/provocation.md` — the PROVOCATION unit type definition, Auger 2013 four criteria, the GROUNDED/EXTRAPOLATED/PROVOCATIVE/CRITICAL axis with required prose markers, the registry sub-table format for PROVOCATION entries.
- ~~**New file**: `templates/extensions/anti-hallucination-step-z.md` — Step Z as a standalone extension.~~ **Withdrawn per DR-017 reconciliation (2026-06-24)** — Step Z is audience-general; it stays in core, generalized (see *Reconciliation with DR-017* above).
- **`templates/claim-registry.md`**: PROVOCATION row removed from the main Unit Type table; per-type sub-tables section keeps CLAIM / ARGUMENT / PROPOSITION; PROVOCATION sub-table moves to `templates/extensions/provocation.md` with a one-line opt-in hook from the main template.
- **`templates/writing-guide.md`**: PROVOCATION confidence axis moves to extension; main template keeps the four-tier mapping (ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE).
- **`templates/anti-hallucination.md`**: ~~Step Z reference becomes a hook; the full Step Z content moves to the extension.~~ **Amended per DR-017 (2026-06-24):** Step Z content **stays in core** and is generalized — drop the "empirical/methodological projects can skip" gate so the tier-monotonicity check applies to all project types. Any PROVOCATION-*specific* inverse-fabrication example is cross-referenced from `extensions/provocation.md`, but the general check is core.
- **`templates/vv-framework.md`**: PROVOCATION mentions stay only in the Gate 2.6 (Reflexivity) section, which is already explicitly conditional. Main framework body discusses CLAIM / ARGUMENT / PROPOSITION / CALCULATION only.
- **`README.md`**: PROVOCATION paragraph moves out of the main "Verification Registry" section into a brief "Extensions for non-empirical work" subsection at the end of that section. Existing conditional-gates section unchanged.
- **`docs/framework-summary.md`**: PROVOCATION section moves to a clearly-labelled extension subsection or splits into a separate extensions-summary doc.

### What stays unchanged

- **DR-010 itself.** The decision content (PROVOCATION = designed artefact, Auger criteria, separate confidence axis, opt-in default) is not revisited; only its surface in the templates and README is restructured.
- **Existing PROVOCATION semantics** for projects that already use them. The extension doc is the same content, in a different location.
- **Conditional gates** (2.6, 2.7, 2.8) and the application-class statements (paper / speculative-design / decision-support). Those already follow the opt-in pattern this DR proposes to extend to PROVOCATION.

## Consequences

If Accepted:

- Empirical-paper readers see only CLAIM / ARGUMENT / PROPOSITION / CALCULATION in core templates and main README sections. PROVOCATION becomes findable via the "Extensions for non-empirical work" subsection and the `templates/extensions/` directory.
- Speculative-design adopters read one extension doc (`templates/extensions/provocation.md`) plus DR-010 (already required reading via the DR-010 link).
- `templates/extensions/` directory establishes a pattern for future application-class-specific content (decision-support per DR-012 may eventually want a similar extension if specific scaffolding diverges further).
- CHANGELOG version bump: MAJOR if the restructure is visible to template readers; MINOR if framed as "core simplified, extension introduced, behaviour unchanged." This is itself a sub-decision in the impact assessment.

If Rejected:

- DR-014 is closed with the rationale (e.g., Paper 1 impact too high, or speculative-design adopters assume inlined templates). Reviewer 1's concern is addressed via Option C or D as fallback (lighter relabelling rather than restructure).

## Revisit If

- The Paper 1 impact assessment reveals migration cost exceeds the cognitive-load saving (e.g., dozens of cross-references that would need updating). Option C (README-only fold) becomes the fallback.
- A speculative-design adopter reports that extension-as-separate-doc is harder to follow than inlined. The pattern would be reconsidered, possibly with a hybrid (inline for adopters opted into PROVOCATION via a flag in their CLAUDE.md).
- DR-012's decision-support class accumulates similar friction (decision-support-only content cluttering the empirical-paper core). The `extensions/` directory pattern would generalise.
- A fourth application class emerges where the `extensions/` pattern visibly does not scale (e.g., extensions overlapping or contradicting). The framework would need a higher-level layering scheme.

## Evidence Base

- External feedback from the June 2026 convergent review (Reviewer 1 substantive observation; Reviewer 3 confirmation).
- Convergent observation from Reviewer 3 (Copilot): *"the README should state more bluntly which audience is primary and which extensions are optional."* This DR's Option B answers that by separating core from extensions explicitly.
- Pattern precedent: Conditional Gates 2.6, 2.7, 2.8 already follow the opt-in pattern. The extension-doc-with-hook structure is also used in the companion `agent-ready-projects` repo.
- N=0 evidence base for this DR specifically — no project has yet used a separate `templates/extensions/` doc. Risk is structurally similar to other restructures the framework has survived (the per-type sub-tables migration in v1.2.0 was structurally analogous; that migration worked).

## Pending Assessment

Before this DR can be promoted from Proposed to Accepted, three checks are needed:

1. **Paper 1 reference audit.** Grep `papers/perspective/` for `PROVOCATION`, `Step Z`, and `GROUNDED` / `EXTRAPOLATED` / `PROVOCATIVE` / `CRITICAL` (in the confidence-tier sense, not as ordinary English). Confirm no broken references after the restructure. Paper 1 does not currently use PROVOCATION entries (per CHANGELOG v1.2.0: registry migrated to CLAIM / ARGUMENT / PROPOSITION sub-tables), so the audit should be clean — but checking before changing templates is the discipline this framework exists for.
2. **Speculative-design adopter check.** If a speculative-design adopter has locally-adapted templates that inline PROVOCATION content, confirm whether the extension-as-separate-doc structure is acceptable from the adopter side before committing the restructure.
3. **Version-impact decision.** Decide whether the restructure ships as **v1.4.0** (MINOR — behaviour unchanged from adopter perspective, content relocated) or **v2.0.0** (MAJOR — template surface visibly changed). This affects how the change is described in `UPGRADING.md` and whether existing pinned consumers are expected to review the new extension docs.

The DR ships as Proposed so the layering decision is visible and discussable without forcing template changes in this session.

## Open Questions Carried Forward

- **PROVOCATION sub-table size.** The PROVOCATION sub-table in `templates/claim-registry.md` is the longest of the four (CLAIM / ARGUMENT / PROPOSITION / PROVOCATION) because of the required-field count. Moving it to an extension may reveal that the per-type sub-table pattern itself is at its complexity limit for in-template inlining.
- **Step Z naming.** "Step Z" is named to follow Steps 0–6 in `anti-hallucination.md`. As an extension, it could be renamed (e.g., "Inverse Hallucination Check") to decouple from the step-numbering, though "Step Z" is now established terminology.
- **Future extensions.** If `templates/extensions/` becomes the pattern, candidates include: decision-support-specific notes (DR-012), voice-driven-work-specific notes (Gate 2.8), domain-specific gates beyond 2.6/2.7/2.8. Risk of fragmenting the framework into many small extensions if growth is unmanaged.
- **Templates/extensions/ vs decisions/extensions/.** The decision content (Auger criteria etc.) belongs structurally with DR-010 in `decisions/`. The template-shaped content (sub-table format, prose-marker checklist) belongs in `templates/extensions/`. Splitting cleanly between the two is part of the impact-assessment work.
