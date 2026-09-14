# EQUATOR Network Gap Analysis

## Bibliographic Info
- **Organization:** EQUATOR Network (Enhancing the QUAlity and Transparency Of health Research)
- **URL:** https://www.equator-network.org/
- **GoodReports tool:** https://www.goodreports.org/

## Summary
The EQUATOR Network maintains ~700 reporting guidelines for health research (CONSORT for RCTs, STROBE for observational, PRISMA for reviews, COREQ for qualitative, etc.). These are the gold standard for structured paper verification. However, this analysis reveals a critical gap: essentially ZERO guidelines exist for non-empirical paper types.

## Key Findings
- **704 guidelines** for empirical health research (checked 2026-09-14; 699 on 2026-03-03). The claim-registry entry S2-1 says "~700", which remains accurate; `literature/README.md` said "~500" until 2026-09-14 and was stale by ~200
- No EQUATOR guidelines for theoretical papers
- No EQUATOR guidelines for design science papers
- No EQUATOR guidelines for perspective/opinion pieces
- No EQUATOR guidelines for methodological papers (outside guidelines-for-guidelines)
- Partial exception: PRISMA covers systematic reviews (structured but non-empirical)
- The 16 top-level study-design categories (checked 2026-09-14) run from *Animal pre-clinical research* to *Systematic reviews/Meta-analyses* — every one empirical or applied. No theoretical, conceptual, perspective or design-science category exists
- ⚠ **New and worth watching: an *Artificial intelligence/Machine learning studies* category now exists.** It is the nearest encroachment on this project's territory. It covers studies *about* AI systems, not papers *written with* them — but the boundary is thinner than it was in 2026-03 and should be re-checked before submission
- Outside medicine, structured reporting guidelines are extremely rare (no CS/IS equivalents)
- GoodReports (Struthers et al. 2021, DOI: 10.1186/s12874-021-01402-x) automates guideline selection
- **Note:** Previously attributed to "Butcher et al. 2021"; corrected to Struthers et al. after DOI verification (2026-03-03)

## The AI reporting-guideline landscape (added 2026-09-14)

Three-plus AI-specific reporting guidelines now exist that did not feature in the original gap analysis. **None is a counterexample to the gap claim — all sharpen it.**

| Guideline | Covers | Status here |
|-----------|--------|-------------|
| TRIPOD-LLM (Nature Medicine, 2024) | Studies using LLMs in prediction contexts | UNVERIFIED — not read |
| CANGARU | Disclosure and accountable use of generative AI in academia | UNVERIFIED — not read |
| CHART | Chatbot assessment | UNVERIFIED — not read |
| LLM checklist for behavioural science (Nat Hum Behav, 2026) | Reporting LLM use in behavioural studies | UNVERIFIED — not read |

All govern the same two things: *disclose that you used AI*, and *report your method if your study is about an AI system*. None asks whether a warrant licenses an inference, whether confidence language tracks evidence strength, or whether a proposition states boundary conditions.

**Consequence for the manuscript:** the gap claim must now be stated against this landscape rather than into a vacuum. A reviewer who knows CANGARU exists will read an unqualified "no guidelines exist for AI-assisted writing" as uninformed. The defensible framing: *the field has built disclosure infrastructure and calls it verification infrastructure.*

## Relevance to DR-004
This is the most important landscape finding. The gap between empirical medicine (704 checklists) and non-empirical research (essentially zero) is enormous. This project's most distinctive contribution opportunity: creating verification infrastructure for paper types that have no PRISMA-equivalent. The claim registry is already a kind of reporting checklist for empirical papers; extending it to non-empirical types fills a gap nobody else is addressing.
