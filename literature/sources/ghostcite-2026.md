# GhostCite 2026 — Citation validity at scale (L59)

**Reading status:** TO VERIFY — **not read**. PDF now held locally (`../pdfs/ghostcite-2026.pdf`), and authorship is confirmed from the title page; the *figures* below are still unchecked. Every figure below comes from a search-engine summary and none has been checked against the paper. Do not cite until the abstract is read directly.

## Bibliographic Info
- **Authors:** Zuyao Xu, Yuqi Qiu, Lu Sun, Fasheng Miao, Fubin Wu, Xiang Li (corresponding), Xinyi Wang, Haozhe Lu, Zhengze Zhang, Yuxin Hu, Jialu Li, Luo Jin *(confirmed from title page 2026-09-14; first three marked equal contribution)*
- **Year:** 2026
- **Title:** GhostCite: A Large-Scale Analysis of Citation Validity in the Age of Large Language Models
- **Venue:** arXiv preprint (arXiv:2602.06718; v1 and v2 exist)
- **DOI:** [10.48550/arXiv.2602.06718](https://doi.org/10.48550/arXiv.2602.06718)
- **Local copy:** `../pdfs/ghostcite-2026.pdf`

## What to extract (→ claim map)
- Reported hallucination rates of **14.23%–94.93%** across 13 models and 40 research domains, 375,440 citations — if it holds, the widest published spread and a per-domain breakdown this repo has no equivalent for
- Reported domain sensitivity: 28.80% (Computation and Language) to 80.19% (Digital Libraries), a 51.39 pp gap
- A separate corpus analysis: 2.2M citations across 56,381 papers (2020–2025), 1.07% with invalid citations, +80.9% in 2025, with error *propagation* up to 16 repetitions
- An open-source verification framework — potentially a tooling reference, not just a citation

## Caveats (tier discipline)
- ⚠ **Provenance warning.** During the 2026-09-14 scan a search summary attributed these rates to a *different* arXiv entry (2604.03159, Rao & Callison-Burch — see [L58](rao-callison-burch-2026.md), which reports different metrics entirely). The conflation is on record; treat any GhostCite number encountered second-hand as suspect until read at source.
- Preprint → tier **B** at best, and **F** (unverified) until read.
- The propagation finding (errors copied forward into later papers) is the most novel-sounding claim and therefore the one most worth checking first.

## Relevance to the Verification Gap paper
Potentially supports **S1-1**. Lower priority than [L57](topaz-2026.md) and [L58](rao-callison-burch-2026.md), both of which are further along and better sourced — read those first and only come back here if a per-domain breakdown is actually needed.
