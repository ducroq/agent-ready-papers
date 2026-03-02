# DR-005: "Agent-Ready" as Machine-Consumable Scholarship

---
status: Proposed
date: 2026-03-02
---

## Context

"Agent-ready papers" currently means: papers structured so an AI agent can help a human **write** them correctly. But there is a second meaning: papers structured so an AI agent can **consume** them as knowledge — machine-readable scholarship where agents are the primary readers.

These are different design problems:

| Dimension | Agent-assisted writing (current) | Agent-consumable papers (future) |
|-----------|--------------------------------|----------------------------------|
| Audience | Human authors + AI assistant | AI agents as primary consumers |
| Format | Markdown templates, checklists | Structured data (JSON-LD, RDF, nanopublications) |
| Goal | Prevent hallucination, verify claims | Enable knowledge extraction, reasoning, citation graphs |
| Unit | Registry entry (claim, argument, proposition) | Typed assertion with semantic links |
| Verification | Human-in-the-loop with AI support | Automated verification pipelines |

Related work in this space:
- **Nanopublications** — minimal publishable units (assertion + provenance + publication info) in RDF
- **Open Research Knowledge Graph (ORKG)** — structured, machine-readable research contributions
- **FAIR principles** — Findable, Accessible, Interoperable, Reusable data
- **Semantic publishing** — enriching papers with machine-readable metadata
- **Linked Open Data** — connecting research assertions across papers

## The Convergence Point

The verification registry we're building (DR-004) is already a proto-knowledge-graph:

- **Typed entries** (CLAIM, ARGUMENT, PROPOSITION) map to assertion types
- **Confidence tiers** map to certainty qualifiers
- **Source links** map to provenance
- **Priority levels** map to centrality in the argument graph
- **Traceability** (claim → evidence → audit) maps to provenance chains

A structured export format (e.g., JSON-LD alongside markdown) could make the same registry serve both audiences: human authors during writing, AI agents during consumption. The workflow doesn't change; an export step is added at the end.

## Decision

**Defer — capture the idea, don't build it yet.**

The current scope (verification for human authors) is not yet field-tested. Adding a second design target would split focus. But the convergence is real: the registry format is naturally close to machine-readable, and the gap can be bridged with an export layer when the time comes.

## Consequences

- No implementation now
- The registry format should remain structured enough that a future export is feasible (avoid free-text fields where structured fields would serve equally well)
- Literature research on nanopublications, ORKG, and FAIR principles should be done when this DR is activated

## Revisit If

- The project pivots to podcast generation or creative writing (agent consumption becomes the primary use case)
- A paper project requires structured knowledge output (e.g., contributing to a knowledge graph)
- Academic publishing shifts meaningfully toward machine-readable formats
- An opportunity arises to test the export layer on a real paper project
