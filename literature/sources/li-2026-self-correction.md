# Li 2026 — Decomposing LLM Self-Correction (L64)

**Reading status:** READ (abstract + summary, 2026-09-14). Full text not read.

## Bibliographic Info
- **Author:** Yin Li
- **Year:** 2026 (submitted 2025-12-24)
- **Title:** Decomposing LLM Self-Correction: The Accuracy-Correction Paradox and Error Depth Hypothesis
- **Venue:** arXiv preprint (arXiv:2601.00828)
- **DOI:** [10.48550/arXiv.2601.00828](https://doi.org/10.48550/arXiv.2601.00828)
- **Local copy:** `../pdfs/li-2026-self-correction.pdf`

## Summary
Examines intrinsic self-correction (a model checking its own output with no external feedback) across three LLMs. Reports an inverse relationship between base accuracy and correction rate, proposing an "error depth" account: stronger models' residual errors are the ones least visible to self-inspection.

## Key Findings
- Intrinsic correction rates **16.7%–26.8%**, across three models (GPT-3.5, DeepSeek, Claude)
- **The paradox:** weaker models correct more. GPT-3.5 (66% base accuracy) achieves 26.8% correction; DeepSeek (94% base accuracy) achieves 16.7% — a 1.6× difference in the counterintuitive direction
- Implication: as base capability rises, self-correction gets *less* effective, not more

## The wider correlated-error account (context, not this paper)
Several 2026 works converge on an information-theoretic framing: when generator and evaluator share failure modes, self-evaluation provides weak evidence of correctness, and repeated self-critique amplifies confidence without adding information. Framed as **structural rather than a matter of scale** — a verifier trained on different data or using a different architecture fails on *different inputs*, which is why external verification outperforms self-verification. Sources not yet individually verified; see Open Questions.

## Relevance to the framework — DR-020 and DR-011
The most valuable find in this batch for the *repo* as distinct from the paper.

- **DR-020 (circular evidence)** declares both its gap and its remedy EMERGING. The correlated-error account is **external, independent support for the gap half**: it explains *why* AI-verified AI output is weak evidence, rather than merely asserting that it is. It supplies nothing for the remedy half.
- **DR-011 Pass 3 (cross-vendor)** is argued here on first principles. This literature turns it into the load-bearing pass rather than the optional high-stakes extra: if failure-mode independence is what makes verification informative, then same-vendor passes are near-redundant and the cross-vendor pass is where the evidence actually comes from.
- **The third-party-audit-ceiling position** (resolved SPLIT, 2026-08) — bears directly; re-read alongside.
- ⚠ DR-019 modifies the same Step Z section as DR-020. Whichever is touched second should re-read that section rather than patching blind (per the root CLAUDE.md routing row).

## Caveats (tier discipline)
- Preprint, three models, benchmark tasks → tier **B**. EMERGING at most.
- ⚠ **A widely-repeated figure could not be traced.** "64.5% of self-generated errors survive self-checking across 14 open models" circulates in secondary summaries and was attributed to this paper during the 2026-09-14 scan. It is **inconsistent with what this paper actually reports** (16.7–26.8% correction across three models). Do not cite the 64.5% figure until a primary source is found.
- The framework's interest is in a *different* configuration — one model verifying *another* model's output with a structured checklist, not a model checking itself. Intrinsic self-correction is the adjacent case, not the case. Don't overstate the transfer.

## Open Questions
- Locate and verify the primary sources for the correlated-error account (candidates seen: an information-theoretic analysis of correlated errors, TechRxiv/Preprints.org 2026-01; "When Can LLMs Actually Correct Their Own Mistakes?" critical survey). Those, not this paper, are what DR-020 would actually cite.
- Does the error-depth hypothesis predict anything about *structured* external checklists? If deep errors are invisible to self-inspection but visible to a differently-shaped probe, that is a direct argument for typed verification and would move DR-020's remedy half.
