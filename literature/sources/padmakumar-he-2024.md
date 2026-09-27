# Padmakumar & He 2024 — Writing with an instruction-tuned model reduces content diversity (L84)

**Reading status:** READ (full, arXiv 2309.05196v3, 2026-09-27). Step 0 PASS (arXiv record; no DOI; venue per the PDF header, not independently confirmed).

## Bibliographic Info
- **Authors:** Vishakh Padmakumar, He He
- **Year:** 2024
- **Title:** Does Writing with Language Models Reduce Content Diversity?
- **Venue:** ICLR 2024
- **URL:** https://arxiv.org/abs/2309.05196
- **Local copy:** `../pdfs/padmakumar-he-2024.pdf`

## Key Findings
- 38 Upwork writers with writing or copyediting experience, 300 argumentative essays of about 300 words: Solo, GPT-3 (davinci) or InstructGPT (text-davinci-003) autocomplete (CoAuthor interface).
- Key-point homogenisation (Rouge-L, §4.2): 0.1536 Solo, 0.1578 GPT-3, 0.1660 InstructGPT. Only InstructGPT is significant.
- Lexical diversity is lowest with InstructGPT (Table 3a). The drop comes from the model's own suggestions; the text users wrote themselves stays unaffected (§6).
- Syntactic homogenisation (fewer unique POS n-grams) is "even between GPT3 and InstructGPT": the base model homogenises syntax too.
- Essay quality: "no significance in essay quality across setups" (App. C).

## Caveats
- No independent reader ratings; the authors' own quality check found no difference. Autocomplete interface, OpenAI models only, single sessions.
- Tier **B**.

## Relevance
- Content homogenisation is attributed, tentatively ("This suggests"), to instruction tuning; the comparison is two different models, not tuning in isolation. Measures similarity *between* authors.
