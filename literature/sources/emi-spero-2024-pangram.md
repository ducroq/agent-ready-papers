# Emi & Spero 2024 — Pangram technical report (L73) — VENDOR

**Reading status:** READ (§4, 2026-09-27). Step 0 PASS. **Vendor material: every accuracy figure is a vendor claim.**

## Bibliographic Info
- **Authors:** Bradley Emi, Max Spero (Pangram Labs)
- **Year:** 2024
- **Title:** Technical Report on the Pangram AI-Generated Text Classifier
- **Venue:** arXiv preprint (v3)
- **DOI:** [10.48550/arXiv.2402.14873](https://doi.org/10.48550/arXiv.2402.14873)
- **Local copy:** `../pdfs/emi-spero-2024-pangram.pdf`

## Key Findings
- A transformer classifier trained with "hard negative mining with synthetic mirrors": each human document is paired with an AI "mirror" matched in topic, length and style.
- "Mirror prompts must be hand-tuned for each domain to remove obvious AI tells" (p. 10).
- Vendor claims: 38× lower error than competitors, and 0% false positives on TOEFL essays. Neither is independently verified; the only independent check is L71, which has no learner text.

## Caveats
- Tier **D**. Never use it as support for a P0 or P1 entry.
- Its features are not interpretable, so it yields nothing for a style check.
