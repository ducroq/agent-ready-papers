# Dugan et al. 2024 — RAID benchmark for machine-generated text detectors (L69)

**Reading status:** READ (Findings, §7, Tables 4–6; arXiv v2, 2026-09-27). Step 0 PASS.

## Bibliographic Info
- **Authors:** Liam Dugan, Alyssa Hwang, Filip Trhlík, Andrew Zhu, Josh Magnus Ludan, Hainiu Xu, Daphne Ippolito, Chris Callison-Burch
- **Year:** 2024
- **Title:** RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors
- **Venue:** ACL 2024 (Long Papers), pp. 12463–12492
- **DOI:** [10.18653/v1/2024.acl-long.674](https://doi.org/10.18653/v1/2024.acl-long.674)
- **Local copy:** `../pdfs/dugan-2024-raid.pdf` (arXiv 2405.07940v2)

## Key Findings
- 6M+ generations from 11 generators across 8 domains, with 11 adversarial attacks; 12 detectors tested.
- At default thresholds the commercial detectors kept false positives low, "none having an FPR above 1.7%" (Table 4). Open-source detectors were "dangerously high".
- High accuracy is reachable "but only at similarly high FPR" (Finding 2), and "few detectors can operate at FPR<1%" (Fig. 4).
- A repetition penalty in generation cuts accuracy by up to 32 points (Finding 3). Simple changes to generation settings produced up to 95+% error (Finding 4).
- Paraphrase effects are mixed by detector (Table 6). Homoglyph attacks collapse some detectors.
- Conclusion: detectors are "not yet robust enough for widespread deployment or high-stakes use" (§7).

## Caveats
- 2023–24 generators and detector versions. No non-native human text.
- Tier **A**.
