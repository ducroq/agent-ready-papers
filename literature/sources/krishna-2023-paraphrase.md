# Krishna et al. 2023 — Paraphrasing evades detectors of AI-generated text (L70)

**Reading status:** READ (§4, Table 1; arXiv v2 camera-ready, 2026-09-27). Step 0 PASS (no DOI; NeurIPS proceedings page and arXiv record match).

## Bibliographic Info
- **Authors:** Kalpesh Krishna, Yixiao Song, Marzena Karpinska, John Wieting, Mohit Iyyer
- **Year:** 2023
- **Title:** Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense
- **Venue:** NeurIPS 2023 (Advances in Neural Information Processing Systems 36)
- **ID:** [arXiv:2303.13408](https://arxiv.org/abs/2303.13408)
- **Local copy:** `../pdfs/krishna-2023.pdf`

## Key Findings
- The false-positive rate is fixed at 1%: "even 1% is likely too high in practice" (§4.1).
- Paraphrasing with their 11B DIPPER model cut detection sharply (Table 1): DetectGPT 70.3 → 4.6, watermarking 100 → 57.2, OpenAI's classifier 30.0 → 15.6. Meaning is preserved (§4.3).
- "GPTZero and RankGen … are only able to detect < 15% of non-paraphrased AI-generated text. Thus, we recommend against using these detectors." (§4.3)
- A retrieval defence, where the provider stores its generations, detects 80–97% of paraphrased text at 1% FPR. It needs the provider's cooperation.

## Caveats
- Early-2023 detectors and generators; an attacker with an 11B paraphraser.
- Tier **A**.
