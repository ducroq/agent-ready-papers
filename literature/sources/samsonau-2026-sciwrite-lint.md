# Samsonau 2026 — sciwrite-lint (L66)

**Reading status:** READ (full text, 2026-09-26).

## Bibliographic Info
- **Author:** Sergey V. Samsonau (Authentic Research Partners, Princeton)
- **Year:** 2026 (v1 2026-04-09; v2 2026-05-24)
- **Title:** sciwrite-lint: Verification Infrastructure for the Age of Science Vibe-Writing
- **Venue:** arXiv preprint (arXiv:2604.08501, cs.DL)
- **DOI:** [10.48550/arXiv.2604.08501](https://doi.org/10.48550/arXiv.2604.08501) (resolves, 2026-09-26)
- **Code:** open source, `pip install sciwrite-lint` (v0.5.0 at publication)
- **Local copy:** `../pdfs/samsonau-2026-sciwrite-lint.pdf`

## Summary
A local linter for manuscripts that runs 23 checks on one consumer GPU. The checks cover reference existence, metadata, retraction and claim support. It follows citations one level into the cited papers and their bibliographies, and it also checks internal consistency (numbers vs tables, abstract vs body) and figures against text. It is built to run in an agent write→check→fix loop. An experimental "SciLint Score" multiplies integrity by a contribution component based on Popper, Lakatos, Kitcher, Laudan and Mayo.

## Key Findings
- It names itself "verification infrastructure", so the tool-vs-process line in Paper 1's S1-4 does not separate us from it
- Checks that touch argument quality:
  - `causal-language-audit`: causal claims the study design does not support
  - `statistical-reporting`: statistical results that contradict their verbal interpretation
  - `cite-purpose`: the argumentative role of each citation, in eight weighted functions
- The contribution component classifies each claim by type, specificity, testability, support and scope. It is aimed at "structural quality of arguments"
- Evaluation:
  - Error injection: 67/68 recall (dangling cites and references only)
  - False positives: of 379 findings judged by an LLM, 14% TP, 60% FP, 26% uncertain, measured before its matching engine existed
  - Contribution calibration: 30/38 ordinal constraints pass, against expectations the author set

## Relevance to the framework — PRIOR ART (S1-4)
The closest prior art found. It falsifies S1-4 as originally worded and also the 2026-09-14 narrowing ("no process-level infrastructure addresses argument quality … confidence calibration"), because it audits confidence language against empirical study design.

**What survives:**
- There is no Toulmin or warrant analysis and no sorting of entries into claims, arguments and propositions with a procedure per kind
- Boundary conditions are not required. Laudan only counts acknowledged limitations
- It is calibrated only on empirical papers (ablations, baselines, RCTs)

## Caveats (tier discipline)
- Preprint → tier **B**. Single author, self-evaluated; the contribution component is explicitly experimental.
- Its framing sources (e.g. GPTZero's 100 fabricated citations in NeurIPS 2025, via Ansari 2026, arXiv:2602.05930) are secondary here and unverified.
