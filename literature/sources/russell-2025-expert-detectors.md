# Russell, Karpinska & Iyyer 2025 — Frequent ChatGPT users as detectors of AI text (L72)

**Reading status:** READ (§3–5, Table 3, Table 17; arXiv version, 2026-09-27). Step 0 PASS.

## Bibliographic Info
- **Authors:** Jenna Russell, Marzena Karpinska, Mohit Iyyer
- **Year:** 2025
- **Title:** People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text
- **Venue:** ACL 2025 (Long Papers)
- **DOI:** [10.18653/v1/2025.acl-long.267](https://doi.org/10.18653/v1/2025.acl-long.267)
- **Local copy:** `../pdfs/russell-2025-expert-detectors.pdf` (arXiv 2501.15654)

## Key Findings
- 300 English non-fiction articles under 1,000 words, each judged by 5 "expert" annotators. Scientific papers are out of scope (p. 2).
- Experts: average TPR 92.7%, FPR 3.3%, and the majority vote was right on all 60 articles in Experiment 1 (p. 3). Non-experts performed near chance yet were confident.
- Cues in the experts' explanations (Table 3, p. 6; share of explanations, correct or not):
  - vocabulary 53.1%: stock words and phrases
  - sentence structure 35.9%: predictable templates such as "not only … but also" and lists of three; human sentences vary more in length
  - grammar 24.8%; originality 23.7%
  - formatting 15.0%: overly consistent, paragraphs of similar length
  - conclusions 13.1%: "repetitive and overly optimistic summaries"
  - tone 9.3%
- "Close behind are formulaic sentence and document structures (e.g., optimistically vague conclusions)" (p. 2).

## Caveats
- Only five annotators, and GPT-4o coded the explanations into categories.
- Tier **A**, small sample.

## Relevance
- **The only interpretable, peer-reviewed cue list in the detector scan.** It links detectability to formula repetition and uniformity, which is the readability hypothesis in `docs/work-items/ai-detector-scan.md`.
- **Nothing on confidence calibration.** No cue category covers hedges or boosters.
