# Kobak et al. 2025 — Excess vocabulary in LLM-assisted biomedical writing (L81)

**Reading status:** READ (§2, Discussion, Fig. S6; arXiv v5, checked against the PMC full text, 2026-09-27). Step 0 PASS (DOI redirects to science.org; open access as PMC12219543).

## Bibliographic Info
- **Authors:** Dmitry Kobak, Rita González-Márquez, Emőke-Ágnes Horvát, Jan Lause
- **Year:** 2025
- **Title:** Delving into LLM-assisted writing in biomedical publications through excess vocabulary
- **Venue:** Science Advances 11(27), eadt3813
- **DOI:** [10.1126/sciadv.adt3813](https://doi.org/10.1126/sciadv.adt3813)
- **Local copy:** `../pdfs/kobak-2025-excess-vocabulary.pdf` (arXiv 2406.07016v5; page numbers refer to it)

## Key Findings
- "at least 13.5% of 2024 abstracts were processed with LLMs" (abstract; §2.2, p. 4). This is a lower bound, and it ranges from under 5% to over 40% across subcorpora (p. 5).
- The excess words of 2024 are "almost entirely" *style* words: 66% verbs and 14% adjectives. Covid-era excess words were 79.2% nouns (p. 3).
- Top rare excess words: delves (r = 28.0), underscores (13.8), showcasing (10.7). Common: potential, findings, crucial (p. 2).
- Fig. S6 (p. 15) prints the full set of 291 rare excess style words.

## Caveats
- Corpus-level: it cannot identify individual texts.
- Native speakers may strip style words, so group differences may reflect detectability rather than use.
- It cannot separate LLM use from humans adopting LLM-favoured words.
- Tier **A**.

## Relevance
Provenance "K" for the default word list in `extensions/formula_scan.py`. Its common-word findings (potential, findings) are deliberately left out of the defaults: they are only signals at corpus scale.
