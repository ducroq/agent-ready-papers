# DR-004: Extending the Registry Model Beyond Factual Claims

---
status: Accepted
date: 2026-03-02
---

## Context

The claim registry tracks factual statements with priority, confidence tier, source, and verification status. This works well for the bulk of a technology paper — experimental results, literature references, methodological facts.

But even empirical papers contain units that aren't factual claims:

- **Discussion arguments** — "Our results demonstrate that simulator X has insufficient fidelity for purpose Y" combines data (grounds) + a fidelity threshold definition (warrant) + a comparison method (backing). The warrant can be challenged even if the data is solid.
- **Propositions** — "Current training standards should require X" is a novel contribution, not a verifiable fact. It can't be source-checked because it's new.
- **Design rationale** — "We chose sensor configuration A because..." is a design decision grounded in justificatory knowledge, not a factual claim.

These are the parts where reviewers spend their critical attention, yet the registry currently has no way to track or verify them.

A literature review (see `literature/`, 47 sources indexed) identified argumentation models that decompose arguments beyond claim-source pairs. Key insight: Wachsmuth et al. (2017) showed argument quality has 15 dimensions; the current claim registry covers one of them (local acceptability — "does the source exist?").

## Immediate Scope vs. Future Scope

**Now (technology papers):** CLAIM + ARGUMENT + PROPOSITION — the three types that appear in empirical engineering papers.

**Later (creative/non-empirical pivot):** The literature folder preserves the full research on DESIGN PRINCIPLE, PROCEDURE, and SYNTHESIS unit types, plus the underlying frameworks (Toulmin, Walton, Hevner, PRISMA). These can be activated when the project pivots to podcast generation, creative writing, or non-empirical paper types.

## Options Considered

### Option A: Keep the registry for claims only
- (+) Simple, no changes needed
- (-) The most reviewer-scrutinized parts of the paper go untracked
- (-) Misses the opportunity identified by the EQUATOR gap (zero guidelines for non-empirical content)

### Option B: Add a "Type" column with all six unit types now
- (+) Complete coverage
- (-) Over-engineered for the current use case (technology papers)
- (-) DESIGN PRINCIPLE, PROCEDURE, SYNTHESIS are untested

### Option C: Add a "Type" column with three unit types now; document the rest for later
- (+) Covers what technology papers actually need
- (+) Minimal added complexity (one column, two new types)
- (+) Full research preserved in `literature/` for the creative/non-empirical pivot
- (+) Progressive disclosure — CLAIM is the default, other types are opt-in
- (-) Still needs field testing

## Decision

**Option C: Three unit types now, rest documented for later**

The registry gets a `Type` column (default: CLAIM). Two additional types are available:

### Unit Types (immediate)

| Type | Where it appears | Verification question |
|------|-----------------|----------------------|
| **CLAIM** | Everywhere (default) | Does the source exist and say this? |
| **ARGUMENT** | Discussion, Conclusion | Warrant valid? Evidence sufficient? Counter-arguments addressed? |
| **PROPOSITION** | Conclusion, Recommendations | Premises verified? Reasoning valid? Boundary conditions stated? |

### Unit Types (reserved for later — see `literature/`)

| Type | For | Trigger |
|------|-----|---------|
| DESIGN PRINCIPLE | Design science papers, creative frameworks | When project pivots to non-empirical work |
| PROCEDURE | Methodological papers | When proposing new methods |
| SYNTHESIS | Review papers, podcast research | When aggregating across multiple sources |

### Verification Guide

**CLAIM** — no change. Existing anti-hallucination checklist, source tier, confidence tier.

**ARGUMENT** — adapted from Toulmin (1958) and Walton (2008):
1. Is the claim clearly stated?
2. Are the grounds (evidence) verified? (These are CLAIMs in the registry)
3. Is the warrant (inferential bridge) explicit and valid for the target audience?
4. Is the qualifier calibrated to evidence strength? (Maps to confidence tiers)
5. Are the strongest counter-arguments addressed? (Not strawmen)

**PROPOSITION** — adapted from Whetten (1989):
1. Are all key constructs defined?
2. Is the relationship clearly stated?
3. Is the reasoning (warrant) explicit and valid?
4. Are boundary conditions specified?
5. Does it engage with alternative explanations?

### Confidence Tiers (adapted)

| Type | ESTABLISHED | SUPPORTED | EMERGING | SPECULATIVE |
|------|------------|-----------|----------|-------------|
| CLAIM | Multiple independent sources | 2-3 sources agree | 1-2 sources | Inference only |
| ARGUMENT | Complete Toulmin + fair engagement | Warrant valid + evidence sufficient | Evidence partial or warrant debatable | Position stated, logic incomplete |
| PROPOSITION | Premises verified + logic valid + tested | Premises verified + logic valid | Premises plausible + logic sound | Conjectural |

## Consequences

- `claim-registry.md` template: add `Type` column (default CLAIM), update reference section; boundary conditions as required PROPOSITION field with quality criteria and anti-patterns; framework component confidence progression; falsification criteria checklist; Toulmin grounds traceability (Issue #1, #2, #3)
- `vv-framework.md` template: add ARGUMENT and PROPOSITION verification as subsections; Whetten Q4 expanded with inline boundary condition quality checklist; falsification criteria block; Gate 2.5 (internal consistency) added (Issue #1, #3)
- `writing-guide.md` template: framework component language special case added (Issue #2); pre-submission checklist items for framework components
- `anti-hallucination.md` template: Step 0 web-search-first procedure added; Quick Version repositioned to content-level checks (Issue #4)
- README: brief mention of unit types in the Claim Verification section; Gate 2.5 added to quality gates
- `CLAUDE.md` template: format support table added (Issue #4); "Ending a session" row added (v1.1.0); self-demonstrating framework variant note added
- Full reflection pass (2026-03-16): mistype decision tree added to `claim-registry.md`; section-level coverage analysis added to `vv-framework.md`; overclaiming-by-category and negative claim hedging added to `writing-guide.md`; negative claim verification added to `anti-hallucination.md`; scope expanded to informal technical communication; DR-009 created for calculation verification; 3 gotcha entries added, 3 marked [RESOLVED]

## Evidence Base

| Source | Contribution | Lit ID |
|--------|-------------|--------|
| Toulmin (1958) | Warrant concept — verification beyond source checking | L01 |
| Walton et al. (2008) | Critical questions as verification checklists | L02 |
| Wachsmuth et al. (2017) | 15 quality dimensions; registry covers 1 | L09 |
| Whetten (1989) | What/How/Why/When structure for propositions | L11 |
| PeerArg (2024) | Structure + LLM > LLM alone | L40 |
| Gupta et al. (2024) | LLMs can extract Toulmin structures (feasibility) | L36 |
| Liang et al. (2024) | LLM feedback useful but shallow without infrastructure | L39 |
| EQUATOR Network | ~500 empirical checklists; zero non-empirical | L47 |

## Boundary Condition Quality Criteria

Full implementation with annotated examples in `templates/claim-registry.md` (Verifying PROPOSITIONs section) and `templates/vv-framework.md` (Section 4.1).

PROPOSITION entries systematically lack boundary conditions (Whetten Q4 is the most commonly missed criterion). Boundary conditions are a required, prominent field rather than one of five checklist items.

Anti-patterns:
- **Tautological** — boundary condition restates the proposition ("applies when applicable")
- **Moving target** — boundary condition can never be falsified ("unless future evidence suggests otherwise")
- **Overgeneralized** — no upper bound on scope ("applies to all domains")

Quality criteria for falsification:
- Testable (not "if we decide it's false")
- Independent of the proposition (not circular)
- Specific enough to be measurable
- Not a moving target

## Revisit If

- Project pivots to podcast generation, creative writing, or non-empirical paper types — activate the reserved unit types from `literature/`
- Field testing reveals ARGUMENT and PROPOSITION types are too complex — simplify verification questions
- A paper project encounters a unit type not covered here
- Automated argument mining matures enough to extract unit types automatically
