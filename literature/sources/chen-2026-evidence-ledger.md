# Chen, Yu & Wang 2026 — Evidence-Ledger Adjudication (L60)

**Reading status:** READ (full text, 2026-09-26). The characterisation below held against the full text; the category is **cs.AI**.

## Bibliographic Info
- **Authors:** Gengyu Chen, Yongjie Yu, Weiling Wang
- **Year:** 2026 (submitted 2026-07-29)
- **Title:** Evidence-Ledger Adjudication for Claim-Evidence Traceability
- **Venue:** arXiv preprint (arXiv:2607.26512)
- **DOI:** [10.48550/arXiv.2607.26512](https://doi.org/10.48550/arXiv.2607.26512)
- **Local copy:** `../pdfs/chen-2026-evidence-ledger.pdf`

## Summary
Proposes a claim-evidence traceability workflow for AI-assisted writing: each claim is paired with an evidence packet, assigned a support relation, and — if unsupported, contradicted, or mixed — routed back to the author. Opens on the problem statement "AI agents can draft claims faster than authors can check whether the cited or retrieved evidence supports them."

## Key Findings
- Benchmark: 2,335-row blind set built from external labels in AVeriTeC, CLIMATE-FEVER and SciFact; gold relations hidden during prediction, joined only at scoring
- Agent evidence-ledger condition: **0.676 relation accuracy / 0.601 macro-F1**, against 0.383 / 0.303 for the best non-agent baseline
- Routing behaviour: 1,270 of 1,435 claims whose gold labels indicate contradiction, missing evidence or mixed evidence were routed back; **295 of 900 supported claims were also routed** (a ~33% false-routing rate on supported claims, which the abstract does not frame as a limitation)

## Relevance to the framework — PRIOR ART
This is independent convergence on the registry pattern: decompose prose into units, attach evidence to each unit, gate on the evidence relation. That is DR-004's model arriving from the fact-checking side rather than the argumentation side.

**The distinction that survives** — and the one Paper 1 must state explicitly:
- Evidence-ledger adjudication operates on **claims with retrievable evidence**. It is fact-checking with a routing layer.
- It has no ARGUMENT or PROPOSITION analogue: no warrant check, no boundary-condition check, no confidence-to-language calibration.
- Its benchmarks (AVeriTeC, CLIMATE-FEVER, SciFact) are all fact-verification corpora. Nothing in the evaluation touches a paper whose contribution is reasoning rather than fact.

Cuts both ways, and the manuscript should say both: it **narrows** the novelty claim in **S1-4** ("no process-level verification infrastructure exists"), and it **strengthens** the architectural bet, because an independent team converged on units-plus-evidence-plus-gates.

## Caveats (tier discipline)
- Preprint → tier **B**.
- The 295/900 supported-claim routing rate is a real cost the abstract underplays; if Paper 1 cites this work as a baseline, cite that number too.

## Open Questions
- ~~Does it position itself against reporting guidelines?~~ No (2026-09-26). It positions against citation checkers and review tools (SemanticCite, sciwrite-lint [L66], FactReview, Peerispect), so it is adjacent to Paper 1's framing, not a competitor to it.
