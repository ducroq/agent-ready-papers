# Jabarian & Imas 2025 — Artificial Writing and Automated Detection (L71)

**Reading status:** READ (Tables 3–6, §4.2; 2026-09-27). Step 0 PASS. **Not peer-reviewed** (title page: "They have not been peer-reviewed").

## Bibliographic Info
- **Authors:** Brian Jabarian, Alex Imas
- **Year:** 2025 (September)
- **Title:** Artificial Writing and Automated Detection
- **Venue:** NBER Working Paper 34223 (also on SSRN, 10.2139/ssrn.5407424)
- **DOI:** [10.3386/w34223](https://doi.org/10.3386/w34223)
- **Local copy:** `../pdfs/jabarian-imas-2025.pdf`
- A claimed PNAS version is **unverified**: Crossref shows no journal record.

## Key Findings
- 1,992 human passages from before 2020, in six genres, each matched with output from GPT-4.1, Claude Opus 4, Claude Sonnet 4 and Gemini 2.0 Flash. Detectors: Pangram (API v2025-05), GPTZero, Originality, and a RoBERTa classifier.
- False-positive rate (Table 3): Pangram 0.0000 at τ ≥ 0.5, GPTZero 0.0071, Originality 0.0011, RoBERTa 0.90–0.98.
- False-negative rate (Table 4): Pangram 0.0045–0.038; Originality up to 0.424.
- Against the StealthGPT humanizer (§4.2), GPTZero's FNR rises to "around 0.50 and above", while "Pangram's performance is largely robust to the humanizer".
- The authors declare no conflicts.

## Caveats
- A working paper; one humanizer; detector versions from mid-2025.
- The human texts are published, largely native prose. **Says nothing about non-native or learner writing.**
- Tier **C**. The only independent support for Pangram's accuracy, so any use in prose stays EMERGING at most.
