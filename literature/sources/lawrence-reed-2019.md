# Lawrence & Reed 2019

## Bibliographic Info
- **Authors:** John Lawrence, Chris Reed
- **Year:** 2019
- **Title:** Argument Mining: A Survey
- **Venue:** Computational Linguistics, 45(4), 765-818
- **DOI:** 10.1162/coli_a_00364

## Summary
Comprehensive survey of argument mining -- the automatic identification and extraction of inference and reasoning structures from natural language text. Defines the field's pipeline: segment text, identify argument components, classify relations, reconstruct structure. Draws on Toulmin, Walton, and RST as theoretical foundations.

## Key Findings
- Argument mining pipeline: segmentation -> component detection -> relation prediction -> structure reconstruction
- Field historically focused on extraction (finding arguments) not evaluation (assessing quality)
- Datasets exist for persuasive essays (AAEC), abstracts (AbstRCT), debate (IBM Debater)
- No major benchmark for full academic papers
- Gap between "extract arguments from a paragraph" and "verify argument structure of a 20-page paper" is substantial

## Relevance to DR-004
The computational bridge between theoretical argumentation models and practical implementation. Argument mining provides the NLP techniques needed to operationalize Toulmin/Walton verification in an automated or semi-automated way. However, the field is more mature for short texts than for full academic papers.

## Related
- Stab & Gurevych (2017). "Parsing Argumentation Structures in Persuasive Essays." Computational Linguistics, 43(3), 619-659. DOI: 10.1162/COLI_a_00295
- Lippi & Torroni (2016). ACM Transactions on Internet Technology, 16(2). DOI: 10.1145/2850417
- Chen et al. (2024). "Exploring the Potential of LLMs in Computational Argumentation." ACL 2024. DOI: 10.18653/v1/2024.acl-long.126
