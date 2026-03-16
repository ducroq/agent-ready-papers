# DR-007: Upgrade SE Mapping from Pedagogical Metaphor to Identity Claim

---
status: Accepted
date: 2026-03-02
supersedes: DR-001 (partially — SE mapping characterization only; DR-001 structure remains valid)
superseded_by:
---

## Context

DR-001 established a dual framing: the project's identity is "verification infrastructure for AI-augmented academic writing," and the SE mapping (claims as components, verification as testing, coverage as test coverage) is a pedagogical tool — useful for explaining the approach, but not the project's core identity. The concern was that calling it "systems engineering" overstates the analogy and invites the criticism that papers aren't systems.

The Proposition retrofit audit (2026-03-02) tested this framing empirically. The audit applied the framework's templates to a real paper project and found that what was performed was not metaphorical SE — it was actual SE:

- **Conformance audit** of a project against a specification (the templates)
- **Gap analysis** with severity classification (Critical/Moderate/Minor) and traceability
- **Requirements reclassification** (retyping 21 registry entries by unit type = reclassifying requirements)
- **Type-specific test execution** (Toulmin/Whetten checklists = unit test procedures with pass/fail criteria)
- **Coverage measurement** (76% overall, 100% P0 = test coverage metrics)
- **Traceability matrix** linking every finding to source artifacts in both directions

The most telling evidence: entry H4 was scored 0.25/SPECULATIVE because it was evaluated as a source-backed claim. It has no citation because it is not a claim — it is an argument. Applying the correct test procedure (Toulmin checklist instead of source verification) revealed that all three premises are verified and the warrant is logically valid. This is exactly what happens in SE when the wrong test procedure is applied to a component: you get a false failure. The fix was correct classification followed by the appropriate test — not better evidence.

## Options Considered

### Option A: Keep the pedagogical metaphor framing (status quo)
- (+) Conservative; avoids overstating the contribution
- (+) DR-001's reasoning still holds in principle
- (-) Undersells what the framework actually does — the audit proves it functions as SE
- (-) "Metaphor" framing makes the contribution sound derivative rather than substantive
- (-) Weakens Paper 2's argument: "we borrowed vocabulary" is less publishable than "we applied SE"

### Option B: Upgrade to "lightweight systems engineering applied to academic writing"
- (+) Honest — the audit evidence supports this claim
- (+) Stronger contribution for Paper 2 (applied SE to a new domain, demonstrated it works)
- (+) The qualifier "lightweight" acknowledges the absence of formal methods, quantitative reliability targets, and change control boards
- (+) Distinguishes from tool-level (citation checkers) and model-level (RAG) approaches more sharply
- (-) Requires defending the claim that this constitutes SE, not just SE-inspired practice
- (-) Some SE practitioners may object to informal application being called SE

### Option C: Hybrid — "systems engineering principles" rather than "systems engineering"
- (+) Hedges appropriately: we use SE principles, not full formal SE
- (+) Still stronger than "metaphor"
- (-) Wishy-washy — either it is or it isn't
- (-) "Principles" framing is common and undifferentiated

## Decision

**Option B: Upgrade to "lightweight systems engineering applied to academic writing"**

The audit provides sufficient evidence that the framework operates as SE, not merely as SE-inspired practice. The key test: the framework's artifacts (registry, checklists, quality gates, traceability matrix) function as SE artifacts — they detect real defects, enforce real quality thresholds, and produce auditable verification records. When the wrong test procedure was applied (CLAIM verification on an ARGUMENT), it produced a false failure that the correct procedure (Toulmin checklist) resolved. That is not metaphor — that is type-specific verification.

"Lightweight" is the honest qualifier. The framework lacks:
- Formal specification languages
- Quantitative reliability targets (SIL levels map to priority, not to failure probability)
- Change control boards
- Formal proof of verification completeness

But most practicing SE is also informal compared to textbook definitions. Lightweight SE is still SE.

This partially supersedes DR-001's framing. DR-001's structure (problem → solution → mental model) remains valid for the README. What changes is the characterization of the SE mapping: it moves from "pedagogical device that explains the approach" to "accurate description of what the framework does."

## Consequences

- **Paper 2 framing:** The contribution claim upgrades from "verification infrastructure inspired by SE" to "lightweight SE applied to academic writing, validated through retrofit audit"
- **README:** The SE mapping table moves from "mental model" status to "this is what the framework is" — though the table itself doesn't change
- **Audit as evidence:** The Proposition retrofit audit (`audits/proposition-retrofit.md`) becomes the primary evidence for the identity claim. H4's reclassification is the clearest single example.
- **DR-001:** Not fully superseded — the dual framing structure and the process-level positioning remain. Only the characterization of the SE mapping changes from metaphor to identity.
- **Defensibility requirement:** Paper 2 must explicitly address the objection that informal SE application doesn't qualify as SE. The counter: formal vs. informal is a spectrum, and the framework's artifacts pass the functional test (they detect real defects using SE methods).

## Revisit If

- Peer review of Paper 2 rejects the SE identity claim as overstated — may need to retreat to "SE principles" (Option C)
- A formal SE practitioner provides a compelling argument for why this doesn't qualify as SE even in lightweight form
- The framework adds formal elements (specification language, quantitative targets) that make the "lightweight" qualifier unnecessary
