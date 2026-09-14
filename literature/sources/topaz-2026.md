# Topaz et al. 2026 — Fabricated citations audit (L57)

**Reading status:** PARTIAL — press coverage read (STAT, Retraction Watch, Nature news, The Scientist); **primary Lancet article not yet read**. Figures below are second-hand. Do not promote to a P0 source until the article itself is read.

## Bibliographic Info
- **Authors:** Maxim Topaz et al. (Columbia University Data Science Institute / School of Nursing)
- **Year:** 2026 (published 2026-05-07)
- **Title:** Fabricated citations: an audit across 2·5 million biomedical papers
- **Venue:** The Lancet
- **DOI/URL:** article ID `PIIS0140-6736(26)00603-3` — https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(26)00603-3/fulltext *(DOI not captured; resolve before citing)*
- **Companion piece:** "Fabricated references: a new threat to editorial integrity", The Lancet, `PIIS0140-6736(26)00798-1`

## Summary
Audit of ~2.5 million open-access biomedical papers on PubMed Central and 97.1 million references, published 2023-01-01 to 2026-02-18. 4,046 references across 2,810 papers were classified as fabricated. The authors used automated tooling to separate genuine fabrications from formatting artifacts such as informally abbreviated titles.

## Key Findings
- Prevalence of papers containing ≥1 fabricated reference: **1 in 2,828 (2023) → 1 in 458 (2025) → 1 in 277 (first seven weeks of 2026)** — reported as a ~12-fold increase over two years
- Sharpest inflection located in **mid-2024**, which the authors note coincides with the uptake of AI writing tools
- Scale: 97.1M references evaluated, 4,046 judged fake across 2,810 papers

## Relevance to the Verification Gap paper
This is the strongest available population-level warrant for the paper's motivating problem, and it did not exist when the manuscript was drafted. It currently bears on **S1-1** (AI citation hallucination is a distinct failure mode, P0, SUPPORTED), whose only source is Mugaanyi et al. 2024 — an experimental fabrication-rate study. Topaz supplies the complementary evidence type: not "how often does a model fabricate when asked" but "how often does a fabrication reach the published record."

## Caveats (tier discipline)
- ⚠ **Scope mismatch.** Biomedical, overwhelmingly *empirical* papers. This repo's paper is about *non-empirical* writing. Using Topaz to motivate a claim about non-empirical papers is an inference, and the manuscript must make that inference visible rather than glide over it.
- ⚠ **Attribution of cause.** The mid-2024 inflection *coincides* with AI writing-tool uptake. Co-occurrence, not demonstrated causation — the correlational framing is the authors' own and should be preserved.
- ⚠ Detection was itself automated. False-positive rate for the fabrication classifier is not known to this note.
- Source tier once the primary is read: **A** (peer-reviewed, top-tier general medical journal, very large N).

## Open Questions
- Does the article report a breakdown by article type? If perspective / review / commentary papers carry a different rate than research articles, that is directly on-thesis and worth far more to this paper than the headline figure.
- Is the fabrication classifier published or reproducible? If so it is a tooling reference for `tools/check_dois.py`, not just a citation.
