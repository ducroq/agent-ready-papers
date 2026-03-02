# Gupta, Zuckerman & O'Connor 2024

## Bibliographic Info
- **Authors:** Ankita Gupta, Ethan Zuckerman, Brendan O'Connor
- **Year:** 2024
- **Title:** Harnessing Toulmin's theory for zero-shot argument explication
- **Venue:** Proceedings of ACL 2024, pp. 10259-10276
- **DOI:** 10.18653/v1/2024.acl-long.552

## Summary
Proposes "argument explication" -- making explicit a text's argumentative structure by outputting triples of (claim, reason, warrant). Finds that simply prompting LLMs with "According to the Toulmin model" significantly improves argument extraction. Toulmin's theory yields the highest success rate for argument explication compared to other argumentation theories.

## Key Findings
- LLMs can extract Toulmin-style argument structures with zero-shot prompting
- Toulmin-based prompts outperform generic prompts for argument extraction
- The approach works across different LLMs
- Makes implicit warrants explicit -- the key verification gap

## Relevance to DR-004
Demonstrates practical feasibility of warrant-level verification using LLMs. An agent could be prompted to explicate a paper's argument structure (claim, reason, warrant) for each key argument, then the warrants could be reviewed for validity. This is exactly the kind of capability needed for argument-level verification beyond source checking.
