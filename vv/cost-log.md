# Operation Cost Log — agent-ready-papers framework (self-application)

<!-- Token-cost tracking for framework operations applied to the framework
     itself. Companion to the per-paper cost-log convention introduced in
     v1.6.0 (templates/cost-log.md, papers/perspective/vv/cost-log.md).
     This file logs framework-scale operations: reviews of the README and
     templates, audits of the framework's own artefacts, batch checks
     across the public surface.

     Why a framework-level log: the framework's own home document is
     itself an artefact the framework can verify. DR-011 multi-model
     reviews on the README, audits of templates against the framework's
     own checklists, /curate on the framework repo — all are operations
     whose cost-vs-value is worth tracking.

     Convention introduced in v2.2.0 alongside vv/hypothesis-log.md as
     part of the framework's self-verification surface. -->

**Repo:** agent-ready-papers
**Started logging:** 2026-06-11

## How to use this log

Same convention as [`templates/cost-log.md`](../templates/cost-log.md): note `/status` deltas (or subagent `total_tokens`) for named, repeatable framework operations. The framework-level log differs from a paper-level log only in subject — framework operations target the framework's own artefacts (README, templates, DRs, docs), not a specific paper.

## Log

| Date | Operation | Total tokens | Input Δ | Output Δ | Cache read | Wall clock | Notes |
|------|-----------|--------------|---------|----------|------------|------------|-------|
| 2026-06-11 | DR-011 Pass 1 (Haiku) on v2.1.0–v2.1.2: four new README sections + `docs/non-claude-setup.md` + `agents/README.md` + CHANGELOG entries | 81,464 | – | – | – | ~56 s | 10 tool uses (heavy file-read pattern for checklist verification). 5 load-bearing findings: stale paths in *Three tiers of adoption* table; CHANGELOG v2.1.2 closing pointer not markdown-linked; date marker missing from `docs/non-claude-setup.md`; re-read discipline gap in verify-citation / register-claims prompts; tier 2 label tension vs. EMERGING tier on three-pass review. |
| 2026-06-11 | DR-011 Pass 2 (Opus) on same scope | 69,747 | – | – | – | ~53 s | 5 tool uses (focused argument-shape analysis from fewer reads). 5 load-bearing findings: Toulmin Warrant dynamic counter unengaged (RAG-could-close); "most of five steps delegated" → actually four of five; v2.1.1 CHANGELOG reads as motivated retrospection; `agents/` vs `templates/` distinction has soft edge (writing-guide, anti-hallucination); auto-memory generalisation overreaches across agent types. |

## Notable findings from the first round

- **Pass 2 < Pass 1 in tokens** (~0.86× Pass 1) — opposite of the 2026-06-08 code-tooling result where Pass 2 was ~1.4× Pass 1. Hypothesis: Pass 1's checklist character required more file reads (10 tool uses) than Pass 2's argument-shape character (5 tool uses). At code-tooling scale the artefacts are short and Pass 2's longer reasoning dominated; at paper-scale prose Pass 1's broader checklist sweep dominated. Worth a third data point at mixed scale to test which side of the prose/code threshold matters.
- **Zero overlap on load-bearing findings between Pass 1 and Pass 2** (paper-scale prose, 2026-06-11). First paper-scale prose replication of DR-011's disjoint-coverage prediction. The two sets are structurally disjoint, not coincidentally:
  - Pass 1 caught: stale path references, format consistency, freshness markers, procedural-discipline gaps, label-vs-tier tensions (checklist-rigour failure modes)
  - Pass 2 caught: warrant-counter omissions, aspirational framing, motivated retrospection, principled-distinction edge cases, principle-overreach (argument-shape failure modes)
  - Logged in DR-011 Evidence Base 2026-06-11 as the first paper-scale prose confirmation.

## Aggregation (after ~10 entries)

| Operation type | N | Mean total tokens | Load-bearing findings (or value delivered) | Notes |
|----------------|---|-------------------|--------------------------------------------|-------|
| DR-011 Pass 1 Haiku (paper-scale prose) | 1 | 81,464 | 5 / 1 round | Pre-N=2; not yet aggregable |
| DR-011 Pass 2 Opus (paper-scale prose) | 1 | 69,747 | 5 / 1 round, fully disjoint from Pass 1 | Pre-N=2; not yet aggregable |

When the table has enough N to be load-bearing, the data point goes into DR-011's Evidence Base with a back-pointer here.
