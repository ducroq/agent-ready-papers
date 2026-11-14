# Linardon et al. 2025 — Citation fabrication by GPT-4o in mental health literature reviews (L117)

## Bibliographic Info
- **Authors:** Jake Linardon, Hannah K. Jarman, Zoe McClure, Cleo Anderson, Claudia Liu, Mariel Messer
- **Year:** 2025 (published 2025-11-12)
- **Title:** Influence of Topic Familiarity and Prompt Specificity on Citation Fabrication in Mental Health Research Using Large Language Models: Experimental Study
- **Venue:** JMIR Mental Health 12, e80371. Peer-reviewed journal.
- **DOI:** [10.2196/80371](https://doi.org/10.2196/80371) (Crossref, 2026-11-14). PMC12658395.
- **File:** `pdfs/linardon-2025-citation-fabrication.xml` (JATS full text, Europe PMC) and `.txt` (plain-text conversion), both gitignored. The PDF links returned an HTML challenge page, so no PDF is stored; section names below stand in for page numbers.
- **Status:** READ 2026-11-14 (full text: abstract, methods, results, Table 1, discussion, limitations).

## Summary
GPT-4o was prompted in June 2025 to write six literature reviews (~2,000 words, ≥20 peer-reviewed citations) on three mental disorders of differing public visibility (major depressive, binge eating, body dysmorphic), each as a general and a specialized review. Every citation was checked against Google Scholar, Scopus, PubMed, WorldCat and publisher sites.

## Key Findings
- Results, *Fabrication Rates*: "Of the 176 citations provided by GPT-4o, 35 (19.9%) were fabricated." Where a fabricated citation had a DOI, 21/33 resolved to an unrelated article and 12/33 were invalid.
- Results, *Accuracy Rates*: "Only 77 (54.6%) of the 141 real (nonfabricated) citations provided by GPT-4o were accurate and contained no errors." (The Discussion misstates this as "77 (54.6%) contained bibliographic errors"; the Results and Table 1 agree with each other.)
- Fabrication differed by disorder: 4/68 (6%) for depression, 17/60 (28%) binge eating, 14/48 (29%) body dysmorphic (χ² = 13.7, P = .001).
- Discussion, *Comparisons With Prior Work*: against GPT-3.5/GPT-4 studies (Walters & Wilder 2023, Mugaanyi et al. 2024), "we found no clear evidence of reduced hallucination rates", with the caveat that cross-study comparisons are limited.

## Caveats (tier discipline)
- One model, one domain, one output per prompt (Limitations 2 and 4); no prompt engineering.
- Whether ChatGPT's web search was on is not stated.
- The study reports existence and bibliographic accuracy, not whether fabricated references looked plausible (that is the Introduction's framing, not a finding).

## Relevance to agent-ready-papers
Paper 1 S1-1 ground (added 2026-11-14 after the author's draft-4 note "it is 2026 now"): extends the evidence for invented references from 2023–24 models to GPT-4o in 2025. Independent of [L118](seifi-2026-neurocritical-citations.md), Mugaanyi et al. 2024 and Walters & Wilder 2023 (different authors, models, domains).
