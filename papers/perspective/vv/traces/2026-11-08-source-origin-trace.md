# Source-origin trace of the register's source items, 2026-11-08

Checks, for each source item in `vv/claims/claim_registry.md`, whether the cited source reports the point as **its own** finding (its data, analysis, definition, tool or position) or **relays** it from another source. Prompted by a reader's comment that the register stops at what a source says and doesn't ask where the source got it. Proposed as a check in the DR on source origin.

**Status:** one pass, by an AI agent (Claude Opus 5.5) in a session with the author. The verdicts are not yet confirmed by the author or anyone else.

## Method

1. Base: commit `331a599`.
2. Take every row with a `src:` item: 21 rows, all priorities, not only P0.
3. For each item, classify by what the row attributes to it: **own** (the source's study, data, survey, definition, tool description or editorial position), **synthesis** (a review's own analysis of others' studies), or **relayed** (the attributed sentence cites another work for the point).
4. Where the row alone does not settle it, read the passage in the local copy (`literature/pdfs/`) and look for a citation inside the attributed sentence.
5. For a relayed item, look up the origin's existence (Crossref or Open Library). Record whether it was read.

## Findings

| # | Row | Item | Origin | Evidence | Effect |
|---|-----|------|--------|----------|--------|
| 1 | S2-2 | Jaakkola 2020 | **Relayed** from Cornelissen 2017, *AMR* 42(1), editorial ([10.5465/amr.2016.0196](https://doi.org/10.5465/amr.2016.0196), Crossref 2026-11-08; not read) | p. 18 body: "a lack of commonly accepted templates or 'recipes' for building the paper means that writing a conceptual piece can be a struggle (Cornelissen 2017)". The abstract repeats the point without a citation | `manuscript.tex` §2 quotes "commonly accepted templates" from Jaakkola p. 18. The point originates in an editorial. The S2-2 tier is unaffected (already EMERGING) |
| 2 | S2-2 | Dinter & Krawatzeck 2015 | **Partly relayed** from Gregor & Hevner 2013 | Introduction: "there is still a need for support in how to publish (and to review) DSR contributions (Goes 2014; Gregor and Hevner 2013)". The abstract sentence carries no citation. Already noted in `literature/sources/dinter-krawatzeck-2015.md` ("Not independent of Gregor & Hevner 2013") | §2 cites the two together as design-science reports ("have reported no agreed guidance"). They are not two independent statements. The S2-2 tier is unaffected |
| 3 | S4-5 and the warrant-check paragraph | Wachsmuth et al. 2017 | **Relayed** from Johnson & Blair, *Logical Self-Defense* (IDEA 2006; Open Library ISBN 9781932716184; not read) | p. 177: "A cogent (or logically good) argument has individually acceptable premises that are relevant to the argument's conclusion and, together, sufficient to draw the conclusion (Johnson and Blair, 2006)" | S4-5's own statement (the three aspects of argument quality) is Wachsmuth's survey framing, so it stands. But `manuscript.tex` attributes the warrant check's relevance and sufficiency questions to "Wachsmuth and colleagues' definition of a cogent argument": the definition is Johnson and Blair's, relayed |

The other items are own or synthesis:
- **Own:** Mugaanyi 2024, Walters & Wilder 2023, Xiong 2024, Zhou 2024, Rao & Callison-Burch 2026, Jabarian & Imas 2025, Budescu 2009 (studies); Samsonau, Chen, Zhou & Yu, VANRA (tool descriptions); ICMJE, EQUATOR, JBI, SANRA, Ralph 2020, Moher 2010, Kent 1964, Mastrandrea 2010, Santesso 2020 (guidance, standards, definitions); Gregor 2006, Toulmin 2003, Whetten 1989, Kane 2013, Clark 2014, Groth 2010, the safety-case methods (their own frameworks); Yang 2022, Divya & Alamelu 2026 (studies); Gregor & Hevner 2013 (an editorial position from experience: "Experience shows…", p. 338); Larsen 2025 (its own literature review).
- **Synthesis:** Turner 2012 (Cochrane review, its own meta-analysis); McArthur 2025.

## Result

3 of about 40 source items relay the point attributed to them. None changes a tier, because the affected rows (S2-2, S4-5) are held by other limits. Two change wording, though: an origin should be named or the relay stated. And one weakens a count: the design-science gap is one statement plus a partly dependent one, not two independent ones.

## Not checked

- Whether a source that reports its own finding *also* cites a prior source for the same point (amplification in Greenberg's sense, at the level of the whole literature). This pass checks only the attributed sentence.
- The relayed origins themselves (Cornelissen 2017, Johnson & Blair 2006) were found to exist but not read.
