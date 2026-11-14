# DR-034: Paper 1 Goes Out as a Preprint; the 4,000-Word Venue Limit No Longer Binds

---
status: Accepted
date: 2026-11-14
---

## Context

Paper 1 was written for Learned Publishing (Opinion, 1,000–4,000 words). On 2026-11-14 the author decided to publish it as a preprint and not to plan a journal submission for now, because the paper cannot meet its own P0 floor without a second screener for S2-2, and none is available. The 4,000-word limit came from that venue. After the 2026-11-14 round the paper has 4,513 words (`make check-registry`), and `test_paper1_v5_consistency` fails on the budget (and on two expectations the round changed: the P0-below-floor set and the premises count).

## Options Considered

- **A: Drop the venue limit; keep a guard against growth** (chosen). The limit stops binding; the checker's budget moves to 5,000 words, so further growth still shows up as a finding.
- **B: Keep 4,000 and trim** about 510 words. This keeps the journal open, but it cuts content for a venue that is no longer planned.
- **C: Remove the budget check entirely.** Rejected: that loosens a check with nothing to replace it.

## Decision

Option A, decided by the author in session on 2026-11-14 ("drop it via a short DR"; "the number of words is also not so strict anymore"). Readability still argues for tightening, and that is a writing matter, not a limit.

## Consequences

- `Makefile` (`check-registry`) and `tests/test_paper1_v5.py`: the budget goes from 4000 to 5000.
- `papers/perspective/CLAUDE.md`: the 4,000-word Hard Constraint and the Target line point here (edited 2026-11-14 with the maintainer's approval).
- If a journal submission returns, the venue's limit applies again, and that needs a new record.
- The arXiv route: computer-science position papers need peer review first (`papers/perspective/arxiv-submission.md`), so the author asks arXiv moderation before submitting.

## Open Questions

- If a journal submission returns, which limit applies, and is the 5,000-word guard then lowered or kept as a preprint-only budget?
- The budget is written in four places (`Makefile`, `tests/test_paper1_v5.py`, a `memory/` verify probe, `papers/perspective/CLAUDE.md`). One shared constant would stop them drifting apart.
