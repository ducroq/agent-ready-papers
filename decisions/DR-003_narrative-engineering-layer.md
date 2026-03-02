# DR-003: Reserve "Narrative Engineering" as a Future Layer

---
status: Proposed
date: 2026-03-02
---

## Context

The current framework handles **correctness**: are claims verified? Do citations exist? Does language match confidence? But it is silent on **argumentation quality**: is the paper compelling? Does it clearly state its contribution? Does the argument flow logically from gap to method to result to implication?

This is not a vague "creativity" concern. Academic papers follow well-studied rhetorical structures that are engineerable:

- **Swales CARS model** (Create A Research Space): the three-move introduction pattern (establish territory → establish niche → occupy niche)
- **IMRAD**: the macro-structure (Introduction, Methods, Results, And Discussion) with known rhetorical functions per section
- **Toulmin argumentation**: claim → grounds → warrant → backing → qualifier → rebuttal
- **Hourglass model**: broad → narrow → broad across the paper arc

These are not artistic choices — they are structural patterns that agents can get wrong (or right) systematically. An agent that writes a Results section with Discussion-style interpretation, or an Introduction that never establishes a gap, has made an engineering error, not a creative misstep.

Notably, the existing **architecture blueprint** (page budgets per section, claim-to-section mapping) is already a primitive narrative engineering tool — it constrains *where* content goes. A full narrative layer would also address *how* content flows.

## Options Considered

### Option A: Add narrative engineering now
- (+) Makes the framework more complete
- (+) Known frameworks (CARS, Toulmin) provide solid foundations — this isn't speculative
- (-) The verification layer isn't fully polished yet; splitting focus risks both
- (-) No field-tested templates yet — we'd be designing without data from real usage

### Option B: Reserve as a defined future layer with scope sketch
- (+) Acknowledges the gap with enough specificity to guide future work
- (+) DR-001's reframing explicitly accommodates this extension
- (+) Can be developed based on patterns that emerge from real paper projects
- (+) Lets the verification core stabilize first
- (-) The gap remains for now — papers using only the verification layer may still lack argument coherence

### Option C: Out of scope — this project only handles verification
- (+) Sharp focus
- (-) Leaves the framework vulnerable to the criticism that verified-but-boring papers don't get published
- (-) Misses a natural extension that shares the same SE-inspired methodology

## Decision

**Option B: Reserve with scope sketch**

Document the intent and rough scope. Don't template it yet. Let real paper projects surface which narrative patterns are most valuable before formalizing.

### Likely scope when developed

| Pattern | What it addresses | Possible template |
|---------|------------------|-------------------|
| Contribution statement | "What's new and why it matters" — forces articulation before writing | `contribution.md` |
| Argument flow map | Directed graph: claim A supports claim B, which enables conclusion C | Section in `writing-guide.md` |
| Section rhetorical function | What each IMRAD section must *do*, not just *contain* | Checklist in `vv-framework.md` |
| Gap-fill positioning | Swales CARS moves for the introduction | Checklist or template |
| Transition patterns | How sections hand off to each other logically | Examples in `writing-guide.md` |

### What already exists (seeds)

- Architecture blueprint with page budgets — constrains *where*
- Claim-to-section mapping in writing guide — links *what* to *where*
- Peer review simulation rubric — already scores "structure and clarity"

## Consequences

- README acknowledges this as a planned direction under a "Roadmap" or "Future work" note
- Future paper projects should log narrative/argument patterns that work well (candidates for extraction)
- The architecture blueprint is recognized as bridging both layers
- No new templates until patterns are validated across ≥2 paper projects

## Revisit If

- A paper project reveals specific, repeatable narrative failures that a template could prevent
- The verification layer stabilizes and there's bandwidth to extend
- User feedback indicates that argument structure is a bigger pain point than citation verification
