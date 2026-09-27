# Chakrabarty, Laban & Wu 2025 — Taxonomy of AI-writing idiosyncrasies from expert edits (L86)

**Reading status:** READ (full incl. appendix prompts, arXiv 2409.14509v5, 2026-09-27). Step 0 PASS.

## Bibliographic Info
- **Authors:** Tuhin Chakrabarty, Philippe Laban, Chien-Sheng Wu
- **Year:** 2025
- **Title:** Can AI writing be salvaged? Mitigating Idiosyncrasies and Improving Human-AI Alignment in the Writing Process through Edits
- **Venue:** CHI 2025, pp. 1–33
- **DOI:** [10.1145/3706598.3713559](https://doi.org/10.1145/3706598.3713559)
- **Local copy:** `../pdfs/chakrabarty-2025-salvaged.pdf`

## Key Findings
- 18 MFA writers edited 1,057 paragraphs (GPT-4o, Claude 3.5 Sonnet, Llama 3.1 70B), making 8,035 edits (the LAMP corpus). About 80% literary fiction, the rest creative non-fiction.
- Edit categories (§5.1, Fig. 5a): awkward word choice and phrasing 28%, poor sentence structure 20%, unnecessary exposition 18%, clichés 17%; purple prose, lack of specificity and tense make up the rest. The three models do not differ significantly in rated quality.
- Part-of-speech templates rare in human text recur in LLM text (§5.3, Table 8).
- Explicitly asking LLMs to avoid clichés did not remove them.
- Writer-edited text ranked first 65% of the time, ahead of LLM-edited text (mean rank 1.99) and unedited text (2.51).
- "Repetitive sentence structure" came up only as a write-in, in 10 of 8,035 cases.

## Caveats
- Creative genres only (the authors doubt transfer to scientific writing), 18 US writers, paragraph level.
- §6.3 and the conclusion contradict each other on whether automatic editing matches writers; cite the conclusion ("far from matching").
- Tier **B**.

## Relevance
- Measured support for the stock-phrase and template signals. Prompting does not fix them, so a locator plus a human edit is the right shape.
- Triads and uniform rhythm are **not** measured here.
