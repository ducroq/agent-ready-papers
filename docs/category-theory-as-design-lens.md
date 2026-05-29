# Category Theory as a Design Lens

Category theory (CT) is the mathematics of structure-preserving maps between mathematical structures. For verification and scoring infrastructure (this framework, the news pipeline, the requirements-review tool), the useful pieces are small.

This note is a design-discussion artifact, not a code-style guide. CT vocabulary belongs in ADRs and methodology notes, not in identifiers, comments, or class names.

## Three primitives

- **Category**: a collection of objects with arrows (morphisms) between them, an identity arrow on every object, and a way to compose arrows that is associative.
- **Functor**: a structure-preserving map between categories. Carries objects to objects, arrows to arrows, preserves composition and identity.
- **Natural transformation**: a structure-preserving map between functors. The "canonical" mappings, defined without arbitrary choices.

## Two ideas that do most of the work

**Composition is the load-bearing notion.** Pay attention to how the pieces of a system compose. Most of the structural information you need is there. Implementations should be analysed by how their pieces compose, not by what is inside them.

**Labels are about equations satisfied.** Whether a morphism is "an inverse", "a projection", "a verification" is determined by which equations it satisfies relative to other morphisms. The morphism itself is just data. Two arrows that satisfy the same equations play the same role.

## Why it matters for these projects

A verification or scoring pipeline can usually be described as a category: artifacts or states are objects, transformations or checks are morphisms. Once that is true:

- A change of representation (raw score → calibrated → percentile rank, or time-domain signal → frequency-domain spectrum) is a functor. Each functor preserves some structure and not other structure. Knowing which is operational.
- Cross-comparison between values from different transforms is structurally suspect: they live in different spaces with different invariants. Comparing requires an explicit common-ground mapping.
- Multi-pass verification combining different perspectives is a limit construction. The claim that survives every pass is the verified one. Each pass is partial; combination yields faithfulness.
- A label like "verified" is a constraint on morphisms: the verification morphism must exist and satisfy specific equations. Drift = claiming a morphism exists when it does not, or claiming it has a stronger property than the evidence supports.

## Five operational principles

1. **Score-space mixing is structural error.** Values from different learned functions live in different metric spaces. Compare within, not across, unless explicitly mapped to common ground.
2. **Pipeline steps preserve different invariants.** Document what each step does and does not preserve. Recalibration debugging becomes much easier.
3. **Multi-pass verification is a limit of functors.** Each pass is a different view. Combination catches what no single view does.
4. **Citation or claim drift is monotonicity failure.** Language used must be ≤ the confidence the evidence chain supports.
5. **Validation is compositional, not monolithic.** Verification of a complex artifact factors as composition of verifications of its parts. The decomposition is the design choice.

## What CT does not give

- New training methods, models, or numerical algorithms.
- New code abstractions worth introducing into existing codebases.
- Magic for debugging specific filter regressions.

## What CT does give

- Vocabulary for talking about design rationale without ambiguity.
- A unifying principle that subsumes several rule-of-thumb checks.
- Cleaner ADR templates for compositional architectures.

If you find yourself reaching for CT vocabulary inside the codebase, you have gone too far. The use is at the design-discussion level.

## Where this lives in practice

Issues referencing this primer (as of writing):

- `agent-ready-papers`: writing-guide drift principle, DR-011 multi-pass review rationale
- `NexusMind`: cross-filter score comparison audit, calibration-pipeline invariant documentation
- `ovr.news`: cross-lens similarity policy
