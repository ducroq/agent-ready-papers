# Restatement trace of the P0 entries, 2026-11-04

Grounds for S3-8. Checks whether each restatement of a P0 entry says what its register row says, in scope, conditions and strength. The tier and source checks read rows; this trace reads the sentences.

**Status:** one pass, by an AI agent (Claude Opus 5.5) in a session with the author. The verdicts are not yet confirmed by the author or anyone else.

## Method

1. Base: commit `7d6c22b`, before any fix.
2. Take every P0 entry in `vv/claims/claim_registry.md`: S1-1, S1-2, S2-1, S2-2, S3-4, C1.
3. Read the surfaces where a claim can be restated: Key Points, abstract (`abstract.tex`), body, Tables 3 and 4, Recommendations.
4. For each restatement, compare it with the row's statement, grounds and rebuttal: scope, period, kind (descriptive or normative), qualifier, and what it says it rests on. Also flag a sentence tagged to a row that says something the row does not carry.
5. Mark each mismatch *clear* or *judgement* (a reasonable reader could accept the sentence).
6. Run `make check-registry` and `make formula-scan` to see whether a tool flags any of them.

## Findings

| # | Where (at `7d6c22b`) | Entry | Row | Restatement | Kind | Verdict |
|---|---|---|---|---|---|---|
| 1 | Table 3, `manuscript.tex:549` | S1-1 | LLMs tested in 2023–24 invented references | "AI citation hallucination is a distinct failure mode." No period | Scope lost by shortening | Clear |
| 2 | Table 4, `:572` | S2-2 | No consensus checklist for checking reasoning step by step; JBI and SANRA judge an argument as a whole | "no checklist was found for the reasoning" | Scope lost by shortening | Clear |
| 3 | Table 4, `:572`; also C1's Why | S3-4 | Descriptive: a check chosen by the kind of grounds "may avoid both" errors | "each claim needs the check its grounds call for" | Rewording: kind and qualifier change | Clear |
| 4 | §2, `:140` | S2-1 | About 700 reporting guidelines | Adds "the most developed infrastructure for checking academic writing" | Second claim with no row | Clear |
| 5 | Table 4, `:574`; Table 3, `:551` | C1 | Rests on S1-7, S2-2, S2-5, S3-4 | Grounds the novelty in S4-9, which the row does not list | Link missing from the row | Clear |
| 6 | Key Points `:58` and abstract vs `:632` and Table 3 | C1 | "makes", at Emerging | "can make" twice, "makes" twice | Two strengths | Judgement |
| 7 | Abstract vs §5, `:588` | S3-4 | Tried by no other author | Abstract: "records were kept by the author's own tooling"; §5: "tried only by one author" | Two stated reasons | Judgement |

Four of the seven (1, 2, 3, 5) are in the summary tables. Five of the six P0 entries have at least one mismatch; S1-2 has none.

Cleared on inspection: "the interpretive parts of empirical papers" is in C1's Who/Where/When column, so it does not widen the row; the "second error" framing of confidence inflation is limited by S1-2's "unsettled", stated in the next sentence.

**Tools:** `make check-registry` reported 22 findings, all rows resting on claims not yet verified, and 0 tier problems; `make formula-scan` reports style only. Neither flagged any of the seven.

## Limits

- One paper, six entries, one pass, by reading. Restatements may have been missed.
- The reader is an AI agent, and an AI tool drafted the paper, so the check is not independent of it.
- P0 entries only. P1 and P2 entries were not traced.

All seven were corrected in the working tree after this record was written; the table above keeps the text as found.
