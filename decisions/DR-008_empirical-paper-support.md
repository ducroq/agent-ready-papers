# DR-008: Empirical Paper Support

---
status: Accepted
date: 2026-03-02
---

## Context

Three retrofit audits (Proposition, EngineeringFidelity, Technology Paper) validated the framework against real paper projects. All three independently surfaced the same root issue: the framework was designed around non-empirical papers and needs explicit support for empirical papers where the primary evidence is the authors' own experimental data.

Five specific gaps were identified across the audits:

| Finding | Audit | Section |
|---------|-------|---------|
| Own data penalized by Tier E weight | Technology Paper | 7.1 |
| GUM results should be ESTABLISHED | Technology Paper | 7.3 |
| Pre-submission checklist needs empirical items | Technology Paper | 7.5 |
| Tag-to-tier migration not documented | EngineeringFidelity | 7.1 |
| Claims have lifecycle in empirical papers | EngineeringFidelity | 7.2 |
| Coverage report needs phase awareness | EngineeringFidelity | 7.4 |
| Reference claims confirmed as issue | EngineeringFidelity | 7.5 |
| Reference claims don't fit tiers | Proposition | 7.2 |

The reference claims issue was already addressed by DR-004's "Special Cases: Reference Claims" addition. This DR addresses the remaining five gaps.

## Decision

Five targeted additions to the existing templates, bundled into a single DR because they share a common cause (empirical paper support) and are interdependent.

### 1. Methodological Facts as Special Case

**Problem:** GUM uncertainty budgets, ISO statistical tests, and validated analytical methods are penalized by the confidence tier system. "Expanded uncertainty is ±2.29%" is not an evidence-strength claim — it's a calculation following a published standard. But the confidence tiers assess it as if it needs multiple independent sources.

**Decision:** Add a "Special Cases: Methodological Facts" subsection to `claim-registry.md`, parallel to the existing "Special Cases: Reference Claims" section. Methodological facts are ESTABLISHED when: (a) the calculation follows a published standard, (b) inputs are documented, and (c) the result is reproducible.

**Key distinction:** "Expanded uncertainty is ±2.29%" = methodological fact (ESTABLISHED). "This uncertainty is acceptable for clinical use" = ARGUMENT (needs Toulmin verification).

### 2. Own Data vs. Own Work Guidance

**Problem:** Tier E (weight 0.6) was designed for "own unpublished work (under review)" — meaning results from a separate paper not yet peer-reviewed. But in empirical papers, the primary evidence is own experimental data from the current paper. Applying 0.6 weight to your own results penalizes the paper's core contribution.

**Decision:** Add guidance to the Source Tier Reference distinguishing own-data claims (results from experiments reported in the current paper) from own-work claims (results cited from papers under review elsewhere). For own-data claims, confidence reflects methodological rigor — sample size, statistical power, reproducibility — not source count. The 0.6 weight applies to own work cited from papers under review elsewhere. Also add an exception to the Cross-Reference Rules for own-data claims with documented methodology.

### 3. Tag-to-Tier Migration Guide

**Problem:** The EngineeringFidelity audit found that projects using ad-hoc status tags ([VERIFIED], [HIGH CONF], [OWN DATA]) have no documented path for migrating to the framework's structured system (Status + Confidence Tier + Source Tier). The concepts are conflated — verification status, confidence level, and source type are three independent dimensions, but tags blend them.

**Decision:** Add a "Migrating from Status-Based Tags" section to `claim-registry.md` with a concept mapping table (what each tag actually encodes) and a common migration patterns table. Key principle: verification and confidence are independent dimensions.

### 4. Claim Lifecycle for Pending Experiments

**Problem:** In empirical papers, claims have a lifecycle — they start as hypotheses, move through data collection, analysis, and finally verification. The current registry treats all claims as static. This means coverage metrics are misleading during the writing process: a paper at the analysis stage might show 40% coverage, but that's expected — the remaining claims are pending data, not missing evidence.

**Decision:** Add a "Claim Lifecycle (Empirical Papers)" section to `claim-registry.md` with a 4-stage table mapping lifecycle stages to Status and Confidence. Update the Coverage Summary to include a "Pending Data" column, with coverage calculated as Verified / (Total - Pending Data). Also add phase-aware coverage guidance and Gate 2 checklist items to `vv-framework.md`.

### 5. Empirical Pre-Submission Checklist

**Problem:** The pre-submission checklist in `writing-guide.md` covers CLAIMs, ARGUMENTs, and PROPOSITIONs — all verification-focused items. Empirical papers have additional requirements that fall outside argument verification: data availability, statistical completeness, measurement documentation, figure quality, and empirical claim traceability.

**Decision:** Add an "Empirical Paper Supplement" section after the General checklist in `writing-guide.md` with five subsections: Data & Reproducibility, Statistical Completeness, Measurement & Equipment, Figures & Tables, and Empirical Claim Verification.

## Consequences

| File | Changes |
|------|---------|
| `templates/claim-registry.md` | 4 section additions (Methodological Facts, Own Data guidance, Migration Guide, Claim Lifecycle) + 2 minor edits (Source Tier asterisk, Cross-Reference exception) |
| `templates/writing-guide.md` | 1 section addition (Empirical Paper Supplement) |
| `templates/vv-framework.md` | 1 note addition (phase-aware coverage) + 2 Gate 2 items |

The changes are additive — no existing content is removed or restructured. Empirical-specific sections are clearly marked so non-empirical paper projects can skip them.

## Revisit If

- Field testing reveals the own-data vs. own-work distinction creates confusion — may need clearer naming
- A paper project encounters a lifecycle stage not covered by the 4-stage model
- The migration guide proves insufficient for a real project's tag inventory — may need project-specific migration tooling
- Empirical checklist items overlap significantly with journal-specific checklists (e.g., CONSORT, STROBE) — may need to integrate rather than supplement
