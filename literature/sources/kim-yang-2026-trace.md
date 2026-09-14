# Kim & Yang 2026 — TRACE (L63)

**Reading status:** READ (abstract, 2026-09-14). Full text not read.

## Bibliographic Info
- **Authors:** Yundong Kim, Heyoung Yang
- **Year:** 2026 (submitted 2026-05-28)
- **Title:** TRACE: Toulmin-based Reasoning Assessment through Constructive Elements for LLM CoT Evaluation
- **Venue:** **ICML 2026** (accepted); arXiv:2605.29656
- **DOI:** [10.48550/arXiv.2605.29656](https://doi.org/10.48550/arXiv.2605.29656)
- **Local copy:** `../pdfs/kim-yang-2026-trace.pdf` — ⚠ 23 pages with **no text layer**; `pdftotext` returns nothing. Identity confirmed via PDF metadata title. Reading it requires OCR or the arXiv HTML version

## Summary
A reference-free metric for chain-of-thought quality built on Toulmin's argumentation model plus Flavell's metacognition theory. Recognises Toulmin elements per reasoning sentence with DeBERTa multi-label classification, then scores a weighted sum of *state validity* and *transition coherence*. Also works as a reinforcement-learning reward signal.

## Key Findings
- **r = 0.74** correlation with benchmark accuracy across 26.3K samples and 7 models
- Outperforms accuracy-only alternatives when used as an RL reward signal
- Stated conclusion: "logically sound reasoning leads to higher-quality answers"
- Evaluates the *reasoning process* rather than the final answer — the same unit shift this framework makes from claims to arguments

## Relevance to the framework
Matters less as a tool than as **evidence for an assumption the framework has been asserting**. The premise under DR-004 and under **S3-4** is that Toulmin structure is a meaningful quality signal — that checking warrants catches something real rather than imposing bureaucratic form. TRACE is the first external, quantitative support for that premise this repo has: Toulmin-derived structural scores correlate at r = 0.74 with independently-measured output quality, at a top-tier ML venue.

Concrete touchpoints:
- **S3-1** / **S3-4** — external support for Toulmin's operationalisability and for typed verification being more than notation
- **[L36](gupta-2024.md) Gupta et al. 2024** — same lineage (Toulmin extraction with LLMs), stronger venue, adds a validity signal Gupta lacks
- **`agents/equation-checker.md`** and the CoT framing — the RL-reward result suggests structural scoring can *steer* generation, not only assess it. Outside current scope; worth a hypothesis-log entry rather than a DR

## Caveats (tier discipline)
- ⚠ **Domain gap is substantial.** TRACE evaluates chain-of-thought reasoning on benchmark tasks with known answers. Academic argument in a non-empirical paper has no ground-truth answer, which is the entire reason the framework exists. Correlation with benchmark accuracy **cannot** transfer directly.
- The defensible transferable claim is narrow: *Toulmin structure carries quality signal in at least one machine-reasoning domain.* Anything stronger overclaims. At **EMERGING** for this repo's purposes despite the venue — the tier reflects the domain gap, not the paper's quality.
- Peer-reviewed conference paper in its own domain → tier **A** there, **B/F** as transferred evidence here.

## Open Questions
- Does "state validity" have any analogue for arguments without a ground truth? If not, the transfer stops at rhetoric and the source is context rather than support.
