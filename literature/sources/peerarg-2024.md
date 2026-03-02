# PeerArg 2024

## Bibliographic Info
- **Authors:** (multiple authors)
- **Year:** 2024
- **Title:** PeerArg: Argumentative Peer Review with LLMs
- **Venue:** Proceedings of LREC-COLING 2024
- **URL:** https://arxiv.org/abs/2409.16813

## Summary
Framework that represents each peer review as a bipolar argumentation framework (support and attack relations), combines multiple reviews, and aggregates to predict paper acceptance. Uses symbolic AI methods from computational argumentation to enhance LLM-based review understanding. Outperforms end-to-end LLMs on review aggregation.

## Key Findings
- Formal argumentation structure + LLM capability > LLM capability alone
- Combining symbolic structure with neural methods improves review quality assessment
- Support/attack relations between review points can be automatically identified
- This validates building infrastructure rather than relying on raw LLM capabilities

## Relevance to DR-004
Strong evidence for the project's approach: verification infrastructure (templates, registries, checklists) + LLM capability > LLM alone. If this principle holds for review aggregation, it likely holds for paper writing verification too. The argument: extending the registry with structured argument types gives LLMs the scaffolding to perform better verification.
