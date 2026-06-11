# Agent-Role Prompts

Portable agent-role prompts that operate on paper artefacts. Each file is a complete "you are X" system prompt — copy it into any agent (Claude Code, GitHub Copilot CLI, Cursor, ChatGPT, Gemini, etc.) and pair it with the artefact to be processed.

## What lives here

| File | Role | Input | Output |
|------|------|-------|--------|
| [`equation-checker.md`](equation-checker.md) | Equation & numerical verifier — mechanical reproduction, not plausibility | A paper section with equations / derived values; optionally the source equations for cross-reference | Per-equation reproduction result with discrepancies flagged |
| [`review-prompt.md`](review-prompt.md) | Peer-review simulator — multi-pass with bias-escape semantics per [DR-011](../decisions/DR-011_multi-model-review-pattern.md) | Manuscript section(s); pass number (Pass 1 intra-family small / Pass 2 intra-family large / Pass 3 cross-vendor) | Scored review against rubric + load-bearing findings |

## What does *not* live here

- **Fill-in templates** (claim registry, decision record, hypothesis log, CLAUDE.md, glossary, writing guide) — those stay in [`../templates/`](../templates/) because they're files an author copies and populates over time, not single-shot prompts.
- **Author-facing checklists** (`anti-hallucination.md` — citation verification you run by hand) stay in [`../templates/`](../templates/) because the author runs them mentally, not an agent.
- **Domain-specific assessment prompts** — agent-ready-papers has none. If a future application class needs them (e.g., a thermodynamics-paper checker), add a parallel subdirectory.

## Vendor-neutrality

These prompts are written in agent-neutral form:

- "You are an X agent. Your task is to Y."
- Operating principles framed as imperatives, not as Claude system-prompt conventions
- Output formats specified as markdown, no model-specific markup

Vendor names appear only where they describe *empirical scope* of testing or the *cross-vendor* requirement of a pattern:

- `equation-checker.md` records that the prompt was tested on Claude Sonnet, expected to work on Haiku, GPT-4o, Gemini
- `review-prompt.md` Pass 3 calls for a different vendor than Passes 1 and 2 (the cross-vendor escape per DR-011)

## Convention origin

Pattern mirrored from [`agent-ready-assessment`](https://github.com/ducroq/agent-ready-assessment)'s `agents/` directory. Introduced in agent-ready-papers v2.1.0 — see [CHANGELOG.md](../CHANGELOG.md#v210-2026-06-11) for the framing rationale.
