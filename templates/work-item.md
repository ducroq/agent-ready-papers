# [Work Item Title]

<!-- SAVE AS: docs/work-items/short-slug.md (paper repo or framework repo)

     One file per work item. Create at the start of multi-session work.
     Complete the Outcome section when the work lands or is abandoned.

     When creating: add a one-line pointer in the memory index's
     "Current State" section:
       - [Short description] → docs/work-items/slug.md [in progress]
     On completion: update the pointer to "[done]" or remove it.

     This is NOT a lifecycle state machine. No "draft → in-progress →
     review → done" progression. The sections are structure for a
     savepoint — enough context to resume after a context reset.

     The work-item file is temporary. It captures what the manuscript or
     code alone does not show: why you chose the approach, what you tried
     and abandoned, what is still open. When the work is done, the Outcome
     section is the durable residue. Delete the file or leave it as
     implementation history once its residue has been promoted to more
     permanent homes (DRs, gotcha log, topic files).

     Differs from:
     - DRs: those freeze one-way-door decisions. Work-item decisions
       are reversible implementation choices.
     - Gotcha log: that captures problems already solved. Work items
       capture what's in flight.
     - Hypothesis log: that pins bets whose evidence is in the future.
       Work items track active implementation. -->

## What & Why

<!-- 3-5 lines: what this is building and why. Frame for a future agent
     arriving without context — enough that they understand the goal
     without re-reading the full manuscript or codebase. -->

[Description of the work item.]

## Current Status

<!-- THE SAVEPOINT. Updated at the end of every working session.

     Start-of-session: the agent reads this first to pick up where it
     left off. End-of-session: the agent updates this to record progress,
     blockers, and anything the next session needs to know.

     Keep this concrete. "Working on X" is not a savepoint. "Section 3
     drafted, claim registry updated, but S3-4 calculation still fails
     verification" IS a savepoint.

     The memory index's "Current State" section tracks active work items
     as one-line pointers. If the index and this file disagree about
     status, the index wins — it is curated at end-of-session; this file
     is written during work. Update this file to match the index. -->

- [ ] Next steps
- [x] Completed items
- [ ] Blocked on (why)

## Decisions

<!-- Key decisions made during implementation. Not full DRs — just
     enough to prevent a future session from re-debating settled choices.
     2-3 lines each, with date. When a decision is substantial enough to
     need a DR (one-way door, cross-cutting impact), create one in
     decisions/ and link it here. -->

- [YYYY-MM-DD] Chose [approach] over [alternative] because [rationale]

## Open Questions

<!-- Things not yet resolved. Keeps the agent from re-asking or guessing
     wrong. When answered, move the resolution to Decisions above. -->

- [question]

## Outcome

<!-- Filled when the work is complete, abandoned, or otherwise resolved.
     This is the durable residue — the knowledge that survives the work
     item itself. Promote anything reusable to DRs, gotcha log, or
     topic files before deleting or archiving this file. -->

**Status**: [Completed | Abandoned | Merged into ...]
**Date**: YYYY-MM-DD

**What happened**: 2-5 lines describing the actual outcome.

**What remains**: Things still open or deferred.

**Related**: [DRs, commits, gotchas, or paper sections that came out of this work]
