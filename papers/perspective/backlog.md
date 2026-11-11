# Paper 1 — Backlog

Last updated: 2026-11-04. The draft-3 plan and its next steps are in `../../docs/work-items/paper1-draft3.md` (maintainer-local), which comes first. Done items, the tier-remediation log, the draft-1 feedback triage (2026-10-16) and the Decision A/B record: this file's git history before 2026-10-19; draft 3 answers most of them (Toulmin's "claim", priority explained, acronyms, S1-5 dropped, Decision B became DR-029, venue chosen: Learned Publishing Opinion).

## Active

- [ ] Restatement trace (S3-8, #73): author confirms the seven verdicts, then the remaining steps at the top of the work item's NEXT.
- [ ] Draft 3: friends' read, blind re-rating (DR-029 condition 3), Section 5 figures, scope follow-ups. The order is in the work item.
- [ ] Learned Publishing upload: `figures/fig-register.pdf` as a separate figure file (its rules: figures in separate files).
- [ ] Refresh `writing-guide.md`'s claim mapping: it still lists S1-5 (dropped for draft 3) and S4-3 (cut for draft 4) as live claims, and lacks S3-8.
- [x] DR-025 slot 3: the verification record is filled from the 2026-10-19 tool runs. Rerun it at submission.

## Maintainer decisions

- [ ] Sole author, or seek co-authors (Gate 3 assumes none found)
- [ ] arXiv preprint after the friends' read; package prepared and checked 2026-10-20; category undecided (arXiv's CS position-paper rule). Steps: `arxiv-submission.md`
- [ ] Pre-submission enquiry to the Learned Publishing editors
- [ ] Gate 3 review before submission: by the maintainer unless a co-author is found

## Parked

- [ ] Journalism: readers judging a story's support from its wording (C1 lists journalism as untested; a separate paper, DR-006). Don't use "microjournalism": Poynter used it in 2008 for reporting by microblog.
- [ ] Framing as a method paper vs the current proposal (parked 2026-06-01)
- [ ] Paper 2 (DSR): LEAN as the formal end of a spectrum from fully formal proofs to no checking; not for Learned Publishing
  - Why Lean is an end point and not a replacement for Toulmin (2026-11-10; [#79](https://github.com/ducroq/agent-ready-papers/issues/79)): (1) Paper 1's claims are empirical or argued, not theorems; a qualifier or confidence tier can be encoded in Lean, and Lean could check an assignment against encoded criteria, but that alone does not establish that the criteria are adequate or their empirical inputs reliable; (2) Lean checks the derivation under its assumptions, so the faithfulness of the translation into Lean and the justification of its premises still need separate review: a premise smuggled in at the start passes; (3) the failures this repo has logged (in the maintainer's local log, triaged 2026-09-15) were mostly references that did not resolve or said something else, and restatements that went stale after a cut; checking formal proofs alone would not necessarily catch these, and which ones formalisation could expose is unassessed; (4) a checker accepting a proof does not by itself show that the proof communicates its reasoning to readers, which is where Toulmin's layout comes from. Narrow use: papers with real theorems (Paper 3's equation checker), though numerical reproduction with a computer-algebra system may fit better there. Replacing Toulmin would need a DR superseding DR-027.
