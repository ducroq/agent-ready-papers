# Paper 1 — Backlog

Last updated: 2026-09-26

## Done

- [x] Verify P2 claim S5-2 (next steps — SPECULATIVE, logical inference verified)
- [x] Add 3–5 references (added 4: Liang 2025, Turner 2012, Glasziou 2014, Peffers 2007 — all DOIs verified)
- [x] Check Learned Publishing abstract word limit (limit: <200 words; trimmed from ~240 to ~170)
- [x] Add Key Points section (LP requirement: 2–6 bullets, ~140 chars each)
- [x] Add self-demonstrating Appendix A (registry summary table, 3 worked examples, corrections discovered)
- [x] Add forward reference to Appendix A in Section 4 limitations paragraph
- [x] Broaden title: "Reporting Guidelines for Reasoning" (was "Beyond Citation Checking")
- [x] Add Discussion-section bridging sentence in Section 2
- [x] Add fourth future direction (Discussion sections of empirical papers) in Section 5
- [x] Add calculation verification as failure mode (S1-5)
- [x] Add fifth future direction (calculation verification as distinct procedure) in Section 5
- [x] Integrate calculation verification into framework README
- [x] Update claim registry (S1-5, coverage 19/19)
- [x] Full framework reflection (2026-03-16): sync Paper 1 files with templates, DR-009, gotcha log cleanup
- [x] Migrate Paper 1 registry to per-type sub-tables (v1.3.0, closes #11) — self-eating-dog-food restored

## Active (Paper 1)

### Tier remediation (opened 2026-09-24 by `828f9cd`)
Tiers were re-derived from DR-002; the registry header states the consequence. Decisions, not chores:
- [x] **Decided 2026-09-26: withdrawn**, S5-1 re-grounded on S2-1/S2-2/S3-4; `check_registry` green. *Was:* **Decide first: do S4-1, S4-2, S4-4 still exist?** Their prose was removed in `1d8c68c`; the registry rows stayed, so `check_registry` fails `anchors`. Dropping or withdrawing them also takes S4-1 out of the P0 count (floor 1 of 7) — **but S4-1 and S4-4 are listed premises of S5-1**, the P0 proposition (registry line 150), so dropping them means re-grounding S5-1 on S2-1, S2-2 and S3-4 alone. Asked in [#38](https://github.com/ducroq/agent-ready-papers/issues/38)
- [ ] **P0 tier gate fails** (enforced since v4.0.0: `coverage --strict` is red) — 3 of 6 P0 entries below SUPPORTED (S2-2, S3-4, S5-1; 2026-09-26: S1-4 moved to P1, S1-1/S1-2 raised). S3-4 and S5-1 are capped by tier-monotonicity (premises S3-1/S3-2/S3-3, S2-2 are EMERGING): raise the premises, no DR (DR-004 already types the tiers). DR-002 has no exception. Per claim: find 2–3 agreeing peer-reviewed sources, re-prioritise to P1, or record a DR on how the P0 floor applies to a perspective paper
- [x] **S1-2 sources**: reworded and sourced on 2026-09-26 (Xiong, Zhou, Peters, El-Dakhs); Liang 2024 dropped
- [ ] **S2-2 to SUPPORTED**: read Jaakkola 2020 and Gregor & Hevner 2013 in full (the maintainer can supply the PDFs). They are candidate equivalents and, for Jaakkola, a gap statement for conceptual papers. Neither is cited until read.
- [ ] Raise S3-4/S5-1: lift premises S3-1 (Toulmin; candidates L62 WarrantScore, L63 TRACE, Gupta 2024), S3-2 (Whetten), S3-3 (own proposal, the hardest)
- [ ] **SPECULATIVE or EMERGING?** DR-002 puts inference and extrapolation at SPECULATIVE; the registry's own notes use those words for S1-2, S2-3, S2-4, S4-3, and S1-3 rests on own design rationale
- [ ] **Hedge prose under EMERGING anchors** — S2-3 "This absence is not accidental", S3-2 "Propositions can be evaluated" (S2-2's "reveals" and S1-2's Liang sentence fixed 2026-09-26)
- [ ] **Split S2-3** — Gregor's five types (reference claim, ESTABLISHED) vs. the non-empirical interpretation (ours)
- [ ] S3-4 Warrant cell says "This demonstrates" on an EMERGING entry
- [x] Writing guide cleaned of the scrubbed audits and the withdrawn S4-1/S4-2/S4-4 (2026-09-26)
- [ ] S5-1 cites "AI writing amplifies the verification challenge" (manuscript §5 opening and appendix *Why*; registry Reasoning) with no registered premise behind it — register a Section 1 premise or drop the clause (pre-existing; surfaced by review 2026-09-26)

### Gate 3 — Co-author Review
- [ ] Co-author review of revised manuscript — significant additions to discuss:
  - Title broadening: "Reporting Guidelines for Reasoning"
  - Appendix A self-demonstration
  - S1-5 calculation verification as a failure mode
- [ ] Decide submission article type: "Original Article" or "Opinion"
- [ ] Consider pre-submission enquiry to LP editor (Laura Dormer or Michelle Urberg)

### Direction question (parked 2026-06-01)
- [ ] Decide on Paper 1 framing — case-leaning (current) vs methodological reframe. Three options sketched in session conversation: light pivot (one-paragraph §4 + appendix), real pivot (expand §3 methodology depth), full method-paper reframe. Status: think-out-loud only; revisit with co-author.

## Parked (Paper 2 — DSR)

- [ ] **LEAN as formalization contrast.** Position the typed verification framework on a spectrum from LEAN (fully formal, machine-checkable mathematical proofs) to nothing (current state for non-empirical papers). The framework is a pragmatic middle ground. Useful for Related Work or Discussion. *Note: not suitable for Paper 1's Learned Publishing audience.*
