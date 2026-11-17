# Soudani, Kanoulas & Hasibi 2025 — Uncertainty estimation falls short in RAG (L122)

**Reading status:** PARTIAL (abstract only, 2026-11-17). Open: ACL Anthology, arXiv:2505.07459.

## Bibliographic Info
- **Authors:** Heydar Soudani, Evangelos Kanoulas, Faegheh Hasibi
- **Year:** 2025
- **Title:** Why Uncertainty Estimation Methods Fall Short in RAG: An Axiomatic Analysis
- **Venue:** Findings of the Association for Computational Linguistics: ACL 2025, pp. 16596–16616
- **DOI:** [10.18653/v1/2025.findings-acl.852](https://doi.org/10.18653/v1/2025.findings-acl.852), checked against Crossref 2026-11-17

## Summary
Asks whether uncertainty-estimation (UE) methods, which score how confident a model is in its answer, still track correctness once retrieved documents are put in the prompt (retrieval-augmented generation, RAG). Reports that they do not, proposes five axioms an adequate UE method should satisfy in RAG, and finds no existing method satisfies all five. A calibration function built on the axioms improves the correlation between uncertainty and correctness.

## Key Findings (from the abstract)
- Current UE methods "cannot reliably assess correctness in the RAG setting".
- No existing UE method satisfies all five axioms.
- The proposed calibration function satisfies more axioms than the baselines.

## Relevance to the framework
Model-side evidence for the framework's position that it sits downstream of model-layer trustworthiness (`docs/framework-summary.md`, *Terminology Note: "Grounding"*): adding sources to the prompt, the step meant to ground an answer, is exactly where the model's own confidence signal stops tracking correctness. That supports, but does not establish, the claim that grounding plus confidence display cannot replace checking the claim against its source. This is the precursor to the ConfidAI Vidi project (Hasibi, Radboud, announced 2026-10-22).

## Caveats (tier discipline)
- Peer-reviewed (ACL Findings) → tier **A** once read; abstract only for now.
- Question-answering benchmarks, short answers. Scholarly claims with warrants are a different unit; do not overstate the transfer.

## Open Questions
- The five axioms: do any have a document-level analogue (e.g., confidence should rise when an added source supports the claim and fall when it contradicts it)? That would be a direct bridge to tier calibration (DR-002).
