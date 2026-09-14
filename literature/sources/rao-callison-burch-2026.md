# Rao & Callison-Burch 2026 — BibTeX citation errors in publishing agents (L58)

**Reading status:** READ (abstract, 2026-09-14). Full text not read.

## Bibliographic Info
- **Authors:** Delip Rao, Chris Callison-Burch
- **Year:** 2026 (v1: 2026-04-03; v2: 2026-08-08)
- **Title:** BibTeX Citation Errors in Scientific Publishing Agents: Evaluation and Mitigation
- **Venue:** **COLM 2026** (title page: "Published as a conference paper at COLM 2026"); arXiv:2604.03159
- **DOI:** [10.48550/arXiv.2604.03159](https://doi.org/10.48550/arXiv.2604.03159)
- **Local copy:** `../pdfs/rao-callison-burch-2026.pdf`

## Summary
Benchmarks search-enabled frontier models on BibTeX generation across 931 papers, four domains, and three citation tiers (popular / low-citation / recent post-cutoff), with version-aware ground truth. Introduces `clibib`, an open-source deterministic BibTeX retrieval tool, as the mitigation.

## Key Findings
- Field-level accuracy **83.6%**, but only **50.9% of entries are fully correct** — the gap between the two numbers is the finding
- Accuracy drops **27.7 percentage points** from popular to recent post-cutoff papers, "revealing heavy reliance on parametric memory even when search is available"
- Two distinct failure modes identified by co-occurrence analysis: **wholesale entry substitution** and **isolated field error**
- Two-stage integration of `clibib` raises accuracy to 91.5% (+8.0 pp) and fully-correct entries to 78.3%, with a 0.8% regression rate
- Models evaluated: GPT-5, Claude Sonnet-4.6, Gemini-3 Flash

## Relevance to the framework
Refines what "citation hallucination" means, in a way the anti-hallucination checklist should absorb. The dominant failure is **not** the invented paper — it is the *real paper with corrupted metadata*. A DOI that resolves is therefore not sufficient evidence that an entry is correct, which is exactly the blind spot in a DOI-resolution check like `tools/check_dois.py`.

Concrete touchpoints:
- **`templates/anti-hallucination.md`** — the 6-step checklist verifies existence. This paper is the argument for a field-level correctness step (authors, year, venue, volume/pages) on top of existence.
- **`tools/check_dois.py`** — its known limits section should acknowledge that resolution ≠ correctness. `clibib` is a candidate reference implementation for a deterministic-retrieval mitigation.
- **S1-1** in the perspective registry — supplies a second, orthogonal source and a sharper mechanism.

## Caveats (tier discipline)
- **Peer-reviewed conference paper (COLM 2026) → tier A**, not B. Corrected 2026-09-14 on obtaining the PDF: the arXiv listing alone reads as a preprint and the abstract does not mention the venue. Worth noting as a recurring trap — arXiv-first discovery systematically under-tiers published work.
- The post-cutoff degradation result is the most transferable finding; the headline accuracy figures are model-version-specific and will date quickly.

## Open Questions
- Does the "isolated field error" mode survive into published manuscripts, or is it caught by copy-editing? Topaz (L57) counts fabrications reaching print; this paper counts errors at generation. The two together would bound the filter's effectiveness, and neither alone does.
