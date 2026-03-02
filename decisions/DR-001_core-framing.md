# DR-001: Core Framing — "Verification Infrastructure" over "Paper-as-System"

---
status: Partially superseded
date: 2026-03-02
superseded_by: DR-007 (SE mapping upgraded from metaphor to identity; structure and process-level positioning unchanged)
---

## Context

The project launched with a central metaphor: "treat a paper like an engineered system" — claims as components, verification as testing, coverage as test coverage. This metaphor is central to the README and shapes how every template is presented.

A landscape review revealed that the AI-assisted academic writing space is active at three levels:
- **Tool-level**: automated citation checkers (RefChecker, scite.ai, LLM Citation Verifier)
- **Model-level**: RAG, grounded generation, span-level verification (ALCE, CiteLLM, REFIND)
- **Policy-level**: publisher disclosure requirements (Elsevier, university policies)

This project operates at a fourth level — **process-level** — providing workflow templates, session continuity, and quality gates. That's its distinctive contribution. The question is whether "paper-as-system" accurately frames that contribution, or whether it overstates the analogy.

## Options Considered

### Option A: Keep "paper-as-engineered-system" as the core identity
- (+) Memorable, distinctive framing
- (+) Already written up in README with detailed mapping table
- (+) Immediately intuitive to the target audience (engineers writing papers)
- (-) Invites the criticism that papers aren't systems — they're arguments with rhetorical intent
- (-) Implies the framework covers everything a paper needs; it doesn't address novelty, argument quality, or rhetorical effectiveness
- (-) May make the approach feel like compliance rather than scholarship

### Option B: Reframe as "verification infrastructure for AI-augmented academic writing"
- (+) More defensible — accurately scopes what the project provides
- (+) Positions the SE mapping as a useful *tool*, not the project's *identity*
- (+) Leaves room for future layers (narrative engineering, argument quality)
- (-) Less catchy; harder to pitch in a sentence
- (-) Loses the pedagogical power of the analogy

### Option C: Dual framing — metaphor as pedagogical device, verification as identity
- (+) The mapping table remains as a teaching tool — it's genuinely effective for explaining the approach to engineers
- (+) The project identity accurately scopes what it delivers today
- (+) README can open with the problem (AI hallucination, overclaiming) and introduce the metaphor as the *response*, not the premise
- (-) Requires careful writing to avoid confusion between the two levels
- (-) Two framings may dilute the message if not handled well

## Decision

**Option C: Dual framing**

The SE mapping table is too useful to discard — it makes the framework immediately intuitive. But the project's identity should be "verification infrastructure for AI-augmented academic writing." The metaphor explains the approach; it doesn't define the project.

In practice: the README should open with the problem (AI failure modes in academic writing), present the process-level solution (templates, session continuity, quality gates), and introduce the SE mapping as "here's the mental model behind this approach."

## Consequences

- README restructure: lead with the verification problem and AI failure modes, not the metaphor
- The mapping table moves from "core concept" to "mental model" — an explanatory section, not the introduction
- Project subtitle/tagline shifts from system-metaphor to verification-infrastructure language
- The framing explicitly accommodates future layers (DR-003: narrative engineering) without contradiction

## Revisit If

- Adoption feedback shows the SE metaphor is what actually sells the approach (lean into it)
- A competing project claims the "verification infrastructure" framing and we need differentiation
