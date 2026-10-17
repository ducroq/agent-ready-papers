# Paper 1 — Backlog

Last updated: 2026-10-17

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
- [x] Prose rewrite for readability under the house voice (2026-10-05, `e7e444d`): no em-dashes or "rather than", hedges varied, claims and tiers unchanged; reviewed in two rounds (round-1 report: `docs/work-items/archive/reports/2026-10-05-review-5.md`, local)

## Active (Paper 1)

**Status 2026-10-17:** draft 3 is next; the plan, the manuscript gaps and the evidence still to gather are in `../../docs/work-items/paper1-draft3.md` (maintainer-local), which supersedes the tier items below where they differ. P0 floor 3 of 6 (C1, S2-2, S3-4 EMERGING).

### Tier remediation (opened 2026-09-24 by `828f9cd`)
Tiers were re-derived from DR-002; the registry header states the consequence. Decisions, not chores:
- [x] **Decided 2026-09-26: withdrawn**, S5-1 re-grounded on S2-1/S2-2/S3-4; `check_registry` green. *Was:* **Decide first: do S4-1, S4-2, S4-4 still exist?** Their prose was removed in `1d8c68c`; the registry rows stayed, so `check_registry` fails `anchors`. Dropping or withdrawing them also takes S4-1 out of the P0 count (floor 1 of 7) — **but S4-1 and S4-4 are listed premises of S5-1**, the P0 proposition (registry line 150), so dropping them means re-grounding S5-1 on S2-1, S2-2 and S3-4 alone. Asked in [#38](https://github.com/ducroq/agent-ready-papers/issues/38)
- [ ] **P0 tier gate fails** (2026-10-17: below the floor are C1, S2-2, S3-4; S5-1 became C1, so read "S5-1" below as C1) (enforced since v4.0.0: `coverage --strict` is red) — 3 of 6 P0 entries below SUPPORTED (S2-2, S3-4, S5-1; 2026-09-26: S1-4 moved to P1, S1-1/S1-2 raised). S3-4 and S5-1 are capped by tier-monotonicity (premises S3-1/S3-2/S3-3, S2-2 are EMERGING): raise the premises, no DR (DR-004 already types the tiers) [superseded 2026-10-09 by Decision B: a DR after all, scoped below]. DR-002 has no exception. Per claim: find 2–3 agreeing peer-reviewed sources, re-prioritise to P1, or record a DR on how the P0 floor applies to a perspective paper
- [x] **S1-2 sources**: reworded and sourced on 2026-09-26 (Xiong, Zhou, Peters, El-Dakhs); Liang 2024 dropped
- [ ] **S2-2 to SUPPORTED**: design science now has two agreeing peer-reviewed gap statements (Gregor & Hevner 2013, Dinter & Krawatzeck 2015, read 2026-10-01), conceptual one (Jaakkola), theoretical and perspective none (searched 2026-10-01: editorials only). Routes: a second source stating Jaakkola's gap for conceptual papers, then narrow the named types to design science and conceptual (a core-claim change: co-author) [narrowing route closed 2026-10-09 by Decision A: all four kinds stay, at EMERGING].
- [ ] Raise S3-4: lift premises S3-1 (Toulmin; candidates L62 WarrantScore, L63 TRACE, Gupta 2024), S3-2 (Whetten); S3-3 waits for the DR. S5-1 also rests on S2-2, which Decision A keeps at EMERGING, so S5-1 depends on the DR's point (3)
- [ ] **SPECULATIVE or EMERGING?** Proposed answer: DR-029 (an inference's tier comes from its warrant check), pending acceptance. DR-002 puts inference and extrapolation at SPECULATIVE; the registry's own notes use those words for S1-2, S2-3, S2-4, S4-3, and S1-3 rests on own design rationale
- [ ] **Hedge prose under EMERGING anchors** — S3-2 "Propositions can be evaluated" (S2-2's "reveals" and S1-2's Liang sentence fixed 2026-09-26)
- [x] **Split S2-3** (done in draft 2: S2-3a, S2-3b) — Gregor's five types (reference claim, ESTABLISHED) vs. the non-empirical interpretation (ours)
- [ ] S3-4 Warrant cell says "This demonstrates" on an EMERGING entry
- [x] Writing guide cleaned of the scrubbed audits and the withdrawn S4-1/S4-2/S4-4 (2026-09-26)
- [ ] S5-1 cites "AI writing amplifies the verification challenge" (manuscript §5 opening and appendix *Why*; registry Reasoning) with no registered premise behind it — register a Section 1 premise or drop the clause (pre-existing; surfaced by review 2026-09-26)

### Draft 2 review (2026-10-16) → draft 3
Four model referees reviewed `paper1-draft-2`. Their shared finding is a framework flaw: the counting rule caps every inference at Emerging, so every argument-based paper fails the P0 gate. Next: a DR that derives an inference's tier from its warrant check, then a narrower draft 3 (register makes reasoning visible; prior work and a comparison first; warrant check with content). Pilot with other users parked.

### Draft 1 feedback (maintainer, 2026-10-16, on `paper1-draft-1` = `e7e444d`)
Source: `feedback/2026-10-16_e7e444d.txt` (gitignored: keep it local). Page numbers refer to the draft-1 PDF. Triaged by Claude; findings checked against the manuscript are marked *checked*.

**A. Possible errors (check first)**
- [ ] **Toulmin's "claim" collides with our Claim.** *Checked:* in Toulmin, "claim" is the conclusion of an argument; in Table 1 a Claim is a source-verifiable fact; Table 4 then has a "Claim" row inside an Argument. Fix: call Toulmin's component "conclusion" (noting Toulmin's term once), or add a sentence on the two senses
- [ ] **Rebuttal in Table 4.** *Checked:* not a contradiction. §3 says the operationalisation drops *backing*, not rebuttal, and Table 4 has no backing row. But the parenthesis is easy to misread, and Table 4's rebuttal reads as a limitation, not Toulmin's "conditions under which the claim fails". Make §3 name the five components it keeps; rewrite the rebuttal cell
- [ ] **Priority is never explained.** *Checked:* the body never mentions priority; it appears only as a column in Table 3. Define P0/P1/P2 (what fails if the entry is wrong; how it is assigned) where Table 3 is introduced, or drop the column
- [ ] **Worked examples hide how priority and confidence were set.** Add both to the S2-1, S3-4 and S5-1 examples; give the Whetten decomposition (S5-1) a table like Table 4 for Toulmin
- [ ] **Abbreviations.** *Checked:* LLM is introduced (§1, l. 78) and EQUATOR is expanded at its first body use (§2), but "IS" (§2) is never introduced, and EQUATOR is used unexpanded in the abstract and Key Points. Sweep all of them

- [ ] **S2-1 tier vs DR-002** (found 2026-10-16 in the glossary review): S2-1 is ESTABLISHED on one source (the EQUATOR website, the primary record), while DR-002's ESTABLISHED requires "multiple independent sources". Either add an independent source, re-tier to SUPPORTED, or record why a primary record counts

**B. Prose and structure (Claude drafts, maintainer approves)**
- [ ] Shorten §1 and §2
- [ ] New section names (propose a set)
- [ ] "AI" vs "generative AI": decide once, apply throughout
- [ ] p. 8: Toulmin came from jurisprudence/practical argument, not academic writing; one sentence on why it transfers
- [ ] p. 8: "may be technically feasible" — add that this paper is a first step
- [ ] p. 8 below (§3, "these three types"): recap the three types before the central argument
- [ ] p. 9 (§4 opening): explain "typed addition"
- [ ] p. 10 (§5): drop the EQUATOR name ("yet existing guidelines address…")
- [ ] Table 3 (registry) adds little next to the worked examples: shrink, move to supplementary material, or drop
- [ ] Remove "Corrections discovered during verification" (Appendix A)
- [ ] Acknowledgements: AI-use statement (what AI did; authors take responsibility). DR-025 (Proposed) gives the three-slot structure
- [ ] Line numbers in review drafts (`lineno`); folded into DR-026 rule 2

**C. Questions the repo can answer (Claude answers with sources, then decide)**
- [ ] Are the four kinds of paper (§2) exhaustive? (S2-2/S2-3; Gregor's taxonomy; Decision A keeps all four)
- [ ] Verification vs validation: does the paper use the terms in the SE sense? More SE / V-model framing overall?
- [ ] Split claim verification into two steps, "source exists" and "source says it" (the anti-hallucination checklist already separates them)
- [ ] Why can't we find more sources for the EMERGING entries? (searches logged under *Tier remediation* above; #38)
- [ ] Is tying confidence to wording really original? (hedging / evidentiality literature; S3-3)
- [ ] Multi-model review is not mentioned: DR-011 is still Proposed, so the paper cannot claim it yet. Same for "the framework is richer than the paper": list what is accepted vs staged
- [ ] Was the house-voice profile used? The 2026-10-05 rewrite (`e7e444d`) was "under the house voice"; confirm which file

**D. Maintainer decisions**
- [ ] Sole author, or seek co-authors (Gate 3 currently assumes none found)
- [ ] Venue route: arXiv preprint first, journal (LP), or both
- [ ] Cite the public GitHub repo as the first implementation
- [ ] Publish the full claim registry / traceability for this paper (links to DR-025's "[URL]")

**E. New work (park)**
- [ ] Journalism: readers judging a story's support from its wording. S5-1's boundary conditions currently *exclude* journalism (Appendix A, §5); a separate paper, so note under DR-006 if pursued

### Gate 3 — Co-author Review
- [ ] Co-author review of revised manuscript — significant additions to discuss:
  - Title broadening: "Reporting Guidelines for Reasoning"
  - Appendix A self-demonstration
  - S1-5 calculation verification as a failure mode
  - The 2026-10-05 prose rewrite (house voice; claims and tiers unchanged)
- [x] Decisions A and B (P0 floor), decided by the maintainer 2026-10-09 (no co-author found): **A** keep all four kinds of paper in the gap claim, hedged ("to our knowledge"), at EMERGING; **B** change the rule via a new DR (scope below); until it is accepted the P0 gate keeps failing. `handoff-coauthor.md` (untracked, kept local) is superseded on both points
- [ ] **Draft the DR for Decision B** (Proposed, for the maintainer). Scope (from review 2026-10-09): DR-004 already judges ARGUMENT/PROPOSITION by warrant, not sources. Three blockers, all in scope: (1) S3-3, the paper's own proposal, registered as a CLAIM; (2) tier-monotonicity (DR-017, `templates/writing-guide.md`, `templates/vv-framework.md`) capping S3-4 and S5-1 at their weakest premise; (3) how the P0 floor (DR-002) treats a P0 entry kept at EMERGING by choice, which is S2-2 under Decision A and a premise of S5-1. Without (3) the gate cannot pass, whatever (1) and (2) say. S3-1 and S3-2 can still be raised by sources
- [ ] **Manuscript: state the gate result.** Until the DR is accepted, add one sentence (e.g. near Appendix A) saying three of six critical entries stay below SUPPORTED and why; manuscript edit, maintainer approves the wording
- [x] Two overfull lines (Section 2 paragraph: `\sloppy` scoped to it; Section 3 table: `\footnotesize`) and `turner2012`'s missing volume (`volume = {2012}`, Cochrane's "2012, Issue 11"; Crossref lists 2013(1)), 2026-10-02
- [ ] Decide submission article type: "Original Article" or "Opinion"
- [ ] Consider pre-submission enquiry to LP editor (Laura Dormer or Michelle Urberg)

### Direction question (parked 2026-06-01)
- [ ] Decide on Paper 1 framing — case-leaning (current) vs methodological reframe. Three options sketched in session conversation: light pivot (one-paragraph §4 + appendix), real pivot (expand §3 methodology depth), full method-paper reframe. Status: think-out-loud only; revisit with co-author.

## Parked (Paper 2 — DSR)

- [ ] **LEAN as formalization contrast.** Position the typed verification framework on a spectrum from LEAN (fully formal, machine-checkable mathematical proofs) to nothing (current state for non-empirical papers). The framework is a pragmatic middle ground. Useful for Related Work or Discussion. *Note: not suitable for Paper 1's Learned Publishing audience.*
