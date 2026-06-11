# Agent-Role Prompts

Portable agent-role prompts that operate on paper artefacts. Each file is a complete "you are X" system prompt — copy it into any agent (Claude Code, GitHub Copilot CLI, Cursor, ChatGPT, Gemini, etc.) and pair it with the artefact to be processed.

## What lives here

| File | Role | Input | Output |
|------|------|-------|--------|
| [`equation-checker.md`](equation-checker.md) | Equation & numerical verifier — mechanical reproduction, not plausibility | A paper section with equations / derived values; optionally the source equations for cross-reference | Per-equation reproduction result with discrepancies flagged |
| [`review-prompt.md`](review-prompt.md) | Peer-review simulator — multi-pass with bias-escape semantics per [DR-011](../decisions/DR-011_multi-model-review-pattern.md) | Manuscript section(s); pass number (Pass 1 intra-family small / Pass 2 intra-family large / Pass 3 cross-vendor) | Scored review against rubric + load-bearing findings |

## The principle: primary mode of use

`agents/` holds prompts whose **primary mode of use is paste-as-system-prompt** — load once into the agent's system-prompt slot, then feed the artefact. The prompt itself doesn't change as the project evolves.

[`templates/`](../templates/) holds artefacts whose primary mode is **author-edited over project lifetime** — files the author copies once and then revises continuously as the work grows (`claim-registry.md` populates, `CLAUDE.md`'s status updates, `decision-record.md` accumulates).

This is the cleanest cut. Edge cases follow.

## Edge cases

- **[`../templates/anti-hallucination.md`](../templates/anti-hallucination.md)** is both an author-facing checklist (the author walks it mentally) *and* an agent procedure (v2.1.2's Quickstart prompts have the agent walk it on each new citation). Primary mode is author-facing — the author is supposed to internalise the steps — so it stays in `templates/`. When an agent runs it, that's secondary use; the agent re-reads it from source each time, doesn't load it as a persistent system prompt.
- **[`../templates/writing-guide.md`](../templates/writing-guide.md)** is operationally an agent-applicable rubric (an agent can scan a section and flag tier mismatches). But it's also paper-specific: each paper's writing guide gets adapted to its sections, claims, and target journal's style. Primary mode is fill-in-and-revise, so it stays in `templates/`.
- **[`equation-checker.md`](equation-checker.md) and [`review-prompt.md`](review-prompt.md)** were originally in `templates/` for legacy reasons (the framework's first version put everything there). The v2.1.0 split moved them here because their primary mode is paste-as-system-prompt — they don't accumulate state, they don't get adapted per session, they just run.

The principle is a heuristic, not a strict typology. When in doubt: ask "would I edit this file as the paper grows?" If yes → `templates/`. If no → `agents/`.

## What does *not* live here

- **Fill-in templates** (claim registry, decision record, hypothesis log, CLAUDE.md, glossary, writing guide, anti-hallucination checklist) → see [`../templates/`](../templates/)
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

Pattern mirrored from [`agent-ready-assessment`](https://github.com/ducroq/agent-ready-assessment)'s `agents/` directory. Introduced in agent-ready-papers v2.1.0 — see [CHANGELOG.md](../CHANGELOG.md#v210-2026-06-11) for the framing rationale. Principle clarified in v2.2.0 after DR-011 Pass 2 review surfaced the edge cases above — see [CHANGELOG.md](../CHANGELOG.md#v220-2026-06-11).
