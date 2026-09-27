# AI-text detector mechanisms (L74–L76)

**Reading status:** READ (method sections, 2026-09-27). Step 0 PASS for all three. Page numbers refer to the arXiv PDFs in `../pdfs/`.

| ID | Source | Mechanism | Key point for this framework |
|---|---|---|---|
| L74 | Mitchell, Lee, Khazatsky, Manning & Finn 2023. DetectGPT. ICML 2023, PMLR 202. [arXiv:2301.11305](https://doi.org/10.48550/arXiv.2301.11305). `mitchell-2023-detectgpt.pdf` | Perturbs the text about 100 times; LLM text sits near a local maximum of log-probability (§4, p. 3) | Needs the model's log-probabilities (p. 9), so it is white-box and impractical for a style check |
| L75 | Hans et al. 2024. Binoculars. ICML 2024, PMLR 235. [arXiv:2401.12070](https://doi.org/10.48550/arXiv.2401.12070). `hans-2024-binoculars.pdf` | Perplexity divided by cross-perplexity between two models (§3) | "humans produce more surprising text than LLMs" (§3.1, p. 3), yet memorised human text such as the US Constitution scores "well into the machine range" (§5.3, p. 6). Predictability is not authorship |
| L76 | Kirchenbauer et al. 2023. A Watermark for Large Language Models. ICML 2023, PMLR 202. [arXiv:2301.10226](https://doi.org/10.48550/arXiv.2301.10226). `kirchenbauer-2023-watermark.pdf` | The provider biases generation toward a hashed "green list" of tokens; the detector runs a z-test (p. 3) | A planted signal, not a property of prose: nothing carries over |

**Vendor, one line:** GPTZero's page "Perplexity, burstiness, and statistical AI detection" (E. Tian, gptzero.me, 2023-03-01) defines burstiness as variation in writing patterns and perplexity across a document. It is a vendor claim with no validation (tier D).

**Tier:** B (peer-reviewed methods papers).

**Relevance:** none of these mechanisms measures hedges, boosters or confidence. The signal they share, low surprise and low variation, is a *uniformity* signal, and bears on readability only.
