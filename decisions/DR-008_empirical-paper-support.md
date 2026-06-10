# DR-008: Empirical Paper Support

---
status: Accepted
date: 2026-03-02
---

## Context

The framework was originally designed around non-empirical papers; review against empirical paper projects surfaces a recurring issue: the framework needs explicit support for empirical papers where the primary evidence is the authors' own experimental data.

Specific gaps identified:

| Finding |
|---------|
| Own data penalized by Tier E weight |
| GUM results should be ESTABLISHED |
| Pre-submission checklist needs empirical items |
| Tag-to-tier migration not documented |
| Claims have lifecycle in empirical papers |
| Coverage report needs phase awareness |
| Reference claims confirmed as issue |
| Reference claims don't fit tiers |

The reference claims issue was already addressed by DR-004's "Special Cases: Reference Claims" addition. This DR addresses two of the remaining gaps — the ones that fix real design flaws in the framework. The others are deferred as process guidance (see below).

## Decision

Two targeted additions to `claim-registry.md` that fix design flaws where the framework incorrectly penalizes valid empirical evidence.

### 1. Methodological Facts as Special Case

**Problem:** GUM uncertainty budgets, ISO statistical tests, and validated analytical methods are penalized by the confidence tier system. "Expanded uncertainty is ±2.29%" is not an evidence-strength claim — it's a calculation following a published standard. But the confidence tiers assess it as if it needs multiple independent sources.

**Decision:** Add a "Special Cases: Methodological Facts" subsection to `claim-registry.md`, parallel to the existing "Special Cases: Reference Claims" section. Methodological facts are ESTABLISHED when: (a) the calculation follows a published standard, (b) inputs are documented, and (c) the result is reproducible.

**Key distinction:** "Expanded uncertainty is ±2.29%" = methodological fact (ESTABLISHED). "This uncertainty is acceptable for clinical use" = ARGUMENT (needs Toulmin verification).

### 2. Own Data vs. Own Work Guidance

**Problem:** Tier E (weight 0.6) was designed for "own unpublished work (under review)" — meaning results from a separate paper not yet peer-reviewed. But in empirical papers, the primary evidence is own experimental data from the current paper. Applying 0.6 weight to your own results penalizes the paper's core contribution.

**Decision:** Add guidance to the Source Tier Reference distinguishing own-data claims (results from experiments reported in the current paper) from own-work claims (results cited from papers under review elsewhere). For own-data claims, confidence reflects methodological rigor — sample size, statistical power, reproducibility — not source count. The 0.6 weight applies to own work cited from papers under review elsewhere. Also add an exception to the Cross-Reference Rules for own-data claims with documented methodology.

## Considered but Deferred

Three additional items were identified but deferred because they add process guidance rather than fixing design flaws in the framework:

### Tag-to-Tier Migration Guide

**Gap:** Projects using ad-hoc status tags ([VERIFIED], [HIGH CONF], [OWN DATA]) have no documented path for migrating to the framework's structured system. The key insight is that verification, confidence, and source type are independent dimensions.

**Why deferred:** Convenience documentation for onboarding, not a template concern. Individual projects can document their own migration in project-specific notes.

### Claim Lifecycle + Phase-Aware Coverage

**Gap:** In empirical papers, claims progress through stages (hypothesis → data collection → analysis → verified). Coverage metrics can be misleading during writing — a paper at the analysis stage might show 40% naive coverage but 85% adjusted coverage. This included a "Pending Data" column in the Coverage Summary and phase-aware gate items.

**Why deferred:** Coverage calculation methodology is a workflow concern. The framework's coverage targets are correct; how a project counts pending claims is project-specific.

### Empirical Pre-Submission Checklist

**Gap:** The pre-submission checklist lacks empirical-specific items: data availability, statistical completeness, measurement documentation, figure traceability.

**Why deferred:** These are journal-specific requirements (often covered by CONSORT, STROBE, or similar reporting guidelines) rather than framework-level template additions.

## Consequences

| File | Changes |
|------|---------|
| `templates/claim-registry.md` | 2 section additions (Methodological Facts, Own Data guidance) + 1 minor edit (Cross-Reference exception) |

The changes are additive — no existing content is removed or restructured.

## Revisit If

- Field testing reveals the own-data vs. own-work distinction creates confusion — may need clearer naming
- A project needs the deferred items badly enough to justify the template complexity
- Empirical checklist items overlap significantly with journal-specific checklists (e.g., CONSORT, STROBE) — may need to integrate rather than supplement
