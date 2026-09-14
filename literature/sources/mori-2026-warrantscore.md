# Mori et al. 2026 — WarrantScore (L62)

**Reading status:** READ (abstract, 2026-09-14). Full text not read.

## Bibliographic Info
- **Authors:** Kiyotada Mori, Shohei Tanaka, Tosho Hirasawa, Tadashi Kozuno, Koichiro Yoshino, Yoshitaka Ushiku
- **Year:** 2026 (submitted 2026-01-24)
- **Title:** WarrantScore: Modeling Warrants between Claims and Evidence for Substantiation Evaluation in Peer Reviews
- **Venue:** arXiv preprint (arXiv:2601.17377)
- **DOI:** [10.48550/arXiv.2601.17377](https://doi.org/10.48550/arXiv.2601.17377)
- **Local copy:** `../pdfs/mori-2026-warrantscore.pdf`

## Summary
An evaluation metric for the substantiation level of peer-review comments. Prior work measured substantiation as the proportion of claims that have *some* supporting evidence; this paper's argument is that presence of evidence is insufficient — the **logical inference between claim and evidence** must itself be assessed. Reports higher correlation with human scores than conventional methods.

## Key Findings
- Explicit statement of the gap this framework's ARGUMENT type also targets: detecting the presence or absence of supporting evidence for a claim is not enough; the inference connecting them must be assessed
- Operationalises the **warrant** specifically — Toulmin's inferential bridge — as a scored quantity
- Applied to review comments rather than manuscripts, but the unit (claim + evidence + inference) is identical
- Beats conventional substantiation metrics on correlation with human scores

## Relevance to the framework
The most directly useful new source in this batch. The framework's ARGUMENT type asks a human to check whether the warrant licenses the inference from grounds to claim; WarrantScore is a computational implementation of that check. It is therefore either **a tool to adopt** (a mechanical pre-pass before human Toulmin analysis, in the spirit of `tools/`) or **a baseline to position against** (automated warrant scoring exists; the framework's contribution is the typed process around it, not the scoring).

Concrete touchpoints:
- **S3-1** (Toulmin provides operationalizable argument verification, P1, SUPPORTED) — currently sourced to Toulmin plus Gupta et al. 2024. This is a second, stronger operationalisation and specifically of the *warrant*, which is the component Gupta handles least well
- **S4-3** (structured verification + LLM outperforms LLM alone, P1, SUPPORTED) — a third instance alongside PeerArg and Gupta
- **[L40](peerarg-2024.md) PeerArg** — same problem space (argumentative peer review), complementary approach
- **`agents/review-prompt.md`** — a substantiation check on the simulator's *own* output is a natural extension

## Caveats (tier discipline)
- Preprint → tier **B**.
- Domain is peer-review comments, which are shorter and more formulaic than manuscript prose. Transfer to manuscript argument is plausible but not shown — do not claim it is.

## Open Questions
- Does the metric generalise to a manuscript's own arguments, or does it depend on review-comment structure? Determines "tool to adopt" versus "baseline to cite".
- Is an implementation released? A usable warrant scorer would change `templates/vv-framework.md` §4 from wholly manual to partly mechanical, which is a larger change than a citation.
