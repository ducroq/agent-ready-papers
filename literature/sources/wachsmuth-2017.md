# Wachsmuth et al. 2017

## Bibliographic Info
- **Authors:** Henning Wachsmuth, Nona Naderi, Yufang Hou, Yonatan Bilu, Vinodkumar Prabhakaran, Tim Alberdingk Thijm, Graeme Hirst, Benno Stein
- **Year:** 2017
- **Title:** Computational Argumentation Quality Assessment in Natural Language
- **Venue:** Proceedings of EACL 2017, pp. 176-187
- **DOI:** 10.18653/v1/e17-1017

## Summary
Presents the first holistic taxonomy of argument quality with 15 dimensions across three categories: logical (cogency), rhetorical (effectiveness), and dialectical (global quality). Provides a corpus of 320 arguments annotated across all dimensions. This is the most comprehensive framework for defining what "argument quality" means.

## Key Findings
- **Logical quality (cogency):** local acceptability, local relevance, local sufficiency
- **Rhetorical quality (effectiveness):** credibility, emotional appeal, clarity, appropriateness, arrangement — **five** sub-dimensions (the arithmetic checks: 1 overall + cogency + 3 + effectiveness + 5 + reasonableness + 3 = 15)
- **Dialectical quality:** global acceptability, global relevance, global sufficiency
- Current claim registries check local acceptability only (does the source exist and support?)
- Missing: local relevance (does evidence support THIS claim?), local sufficiency (ENOUGH evidence?), and all global dimensions

## Relevance to DR-004
Maps exactly where the current verification infrastructure sits and what's missing. The claim registry covers "local acceptability" (one of 15 dimensions). Extending to non-empirical papers requires at minimum adding local relevance and local sufficiency at the argument level, plus global coherence at the paper level. Provides the theoretical foundation for what "verification beyond factual claims" means.

## Verified quotes (2026-10-16, for Paper 1 draft 2; checked with `tools/check_quotes`)

Source: literature/pdfs/wachsmuth-2017-argquality.pdf (ACL Anthology E17-1017, full text; printed pp. 176-187 = 175 + PDF page)

- "a common understanding of argumentation quality is still missing" (p. 176, abstract)
- "Logical quality in terms of the cogency or strength of an argument" (p. 177)
- "Rhetorical quality in terms of the persuasive effect of an argument or argumentation" (p. 177)
- "Dialectical quality in terms of the reasonableness of argumentation for resolving issues" (p. 177)
- "A cogent (or logically good) argument has individually acceptable premises that are relevant to the argument’s conclusion and, together, sufficient to draw the conclusion" (p. 177)
- "agreement of all seven annotators was low for all dimensions" (p. 183; Krippendorff's alpha at most .22). Context: a pilot with "simple initial guidelines"; on the same page the three most-agreeing annotators reached alpha .23–.60. Do not cite it as "argument quality cannot be annotated reliably".
