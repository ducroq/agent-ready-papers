# DR-023: Two Registers, and a Translation Step Where Text Reaches a Person

---
status: Proposed
date: 2026-09-30
---

## Context

The framework produces two kinds of text.

- **Text an agent reads**: `CLAUDE.md`, memory files, registries, skills, the review profile. Much of it is read at every session, so its length costs tokens every time.
- **Text a person reads**: reports to the maintainer (`/curate`, `/review-changes`), the CHANGELOG, the README, DRs, GitHub issues, commit messages, and the paper itself.

Some surfaces are both. Agents read DRs before they propose scope changes, and DR-005 names agents as future readers of papers.

The Token-economy Hard Constraint covers per-session files, and it fits them. Nothing sets a standard for text people read, and the dense style of the agent files carries over into it. The maintainer and their students report that Claude's prose is often compressed: each sentence is grammatical, but it has to be read twice (2026-09-30). The framework's own output showed the same problem that day. The `/curate` and `/review-changes` reports led with tables and internal shorthand, and put the decision the maintainer had to make at the end.

`templates/readability.md` (added 2026-09-30) gives prompts for paper prose. Nothing covers the framework's own output.

One risk shapes every option: rewriting for plainness can make claims stronger. While the template was being written, its worked examples did this twice ("fits the course" became "works like an instructor"), and review caught both. That is n=2, observed by the agent in its own work. It is registered as a maintainer hypothesis and as ducroq/agent-ready-papers#41. Neither case changed a certainty word. Each added a claim.

## Options Considered

| Option | For | Against |
|---|---|---|
| **A. Write everything readably from the start** | One text, no extra step | Conflicts with token economy for per-session files. The session that wrote a text may not judge its clarity well; the review rounds of 2026-09-30 found problems its author had missed. |
| **B. A reader lens in review only** | Cheap; fits the existing review profile | Only reviewed diffs pass through it. Reports to the maintainer never do. It finds problems but does not fix them. |
| **C. A translation step at the boundary** | Keeps the two jobs apart: agent text stays dense, human text gets rewritten | One extra pass per human-facing text. Translation can strengthen claims. |
| **D. B and C together** | C fixes generated text, B catches hand-edited docs | Two mechanisms to maintain |

## Proposed Decision

**Option D.** The translation prompt and the check script are staged in `extensions/` first (the DR-018 precedent). The reader lens lives in the maintainer's gitignored `.claude/review-profile.md`.

1. **Two registers.**
   - Agent-facing: `CLAUDE.md`, `memory/`, registries, skills, the review profile. The Token-economy constraint applies as written.
   - Human-facing: reports to the maintainer, CHANGELOG, README, DRs, issue bodies, commit messages, papers. The rules of `templates/readability.md` apply. Shorter must not mean denser.
   - DRs and papers are also read by agents. They follow the human register; readable text is expected to work for an agent too.
2. **A translation step for generated human-facing text.** Before a report, CHANGELOG entry or issue body reaches a person, a fresh context rewrites it.
   - Reports carry the content of Prompt 1 in `templates/readability.md` (where we stand, what we conclude, what we recommend), reordered so that what the reader must decide or do comes first. The sentences follow Prompt 2, including its tier guard.
   - Internal history, review rounds and shorthand IDs are dropped. A report to the maintainer links to its source; public text links only to public sources (a commit, a DR, an issue).
   - A translation of a DR, a paper or another human-authored surface is a proposal. The author approves it, per the agent-write boundary.
3. **A preservation check after each translation**, in two parts. Both report and never gate.
   - **A script.** It flags any number or tier word from the source that is missing from the translation, and any tier word that moved up a band. Digits inside identifiers (DR-022, L86, #41) do not count as numbers. The bands are the Language Calibration table in `templates/writing-guide.md` (DR-002). Identifiers are not required to survive, since step 2 drops them, but the link to the source is.
   - **A claim comparison in a fresh context.** It lists every assertion in the translation that is not in the source. The script cannot do this: the two cases of 2026-09-30 added claims without any tier word.
4. **The source is kept.** Report and CHANGELOG sources go to a stable, gitignored path (proposed: `docs/work-items/reports/`) and are not edited after translation, so they serve as a record. For documents, the translation becomes the document and git history holds the source.
5. **A reader lens in `/review-changes`.** It marks every sentence a newcomer would have to read twice, and runs on human-facing files only.

## Hypothesis and Test (acceptance condition)

**H1.** Translated reports are easier to act on than the originals, and the two-part check flags every tier word that rises and every assertion that is added.

**Test.**
- Take 10 real reports, 5 from `/curate` and 5 from `/review-changes`, and translate each one.
- Show both versions of each pair as written, in random order. Blinding is partial: the decision-first opening and the missing IDs can give the translation away. The raters give their preference before any comparison of content.
- Two raters: the maintainer and one person who did not write the reports (a student, for example). Each answers one question per pair: *which one could you act on without reading it twice?*
- **Strengthened** means a tier word moved up a band (per the Language Calibration table, which the rater gets), or an assertion appears that is not in the source. An assertion is one checkable proposition. A rater who is not the maintainer counts these for each pair, and a second person recounts 3 pairs to see whether the counts agree.

**Accept** if both raters prefer the translation in at least 8 of 10 pairs, and every strengthened claim the raters count was flagged by the check. **Reject** if either rater prefers it in 5 or fewer. Anything in between: revise the step and run it again. 8 of 10 is a preference threshold, not a significance test: on a one-sided sign test it gives p ≈ 0.055.

## Consequences

- A one-line addition to `CLAUDE.md` naming the two registers may help agents find the rule. The Token-economy constraint itself needs no change, since it is already scoped to per-session files. This is an edit to `CLAUDE.md` and needs the maintainer's approval.
- Cost: two extra passes for each human-facing text, the translation and the claim comparison. Their size in tokens is not yet measured; measuring it is part of the test.
- `/curate` and `/review-changes` are user-global skills owned by the companion framework. Changing how they report means an upstream issue at agent-ready-projects. Until then the step runs as a wrapper around their output.
- **Risk:** translation can drop details that matter. The kept source and the link to it are the mitigation.
- **Risk:** a step that has to be invoked may be skipped. A version that runs by default would be better. How to build that is an open question.

## Evidence Base

- Maintainer and student reports of hard-to-read Claude prose (2026-09-30). These are anecdotes, not measurements.
- Claims made stronger in the rewrites for `templates/readability.md`, twice on 2026-09-30, both caught by review, neither by a tier word. Recorded in the maintainer hypothesis log and in ducroq/agent-ready-papers#41.
- Chakrabarty, Laban & Wu 2025 (L86): explicitly telling models to avoid clichés did not remove them, and writer edits were ranked above model edits. The study covers creative writing, and its authors doubt that it transfers to scientific writing.

## Open Questions

- The README is read by adopters and loaded by agents. Proposed: human-facing, because its main readers are adopters.
- Are commit messages worth translating, or is a plainer first line enough?
- Output language: students may need Dutch. Should translation and language choice be one step?
- How can the step run by default? One option is a hook on report output (see `docs/verification-hooks.md`).

## Revisit If

- The test shows no clear preference, or strengthened claims get past both parts of the check.
- Models start writing readable prose by default, so the step no longer changes anything.
- The Language Calibration bands in `templates/writing-guide.md` change, which the script depends on.
