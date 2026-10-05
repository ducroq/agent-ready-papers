# DR-022: Formula Repetition as a Readability Lens, Not a Detector

---
status: Proposed
date: 2026-09-27
---

## Context

Every gate in the framework but one is about truth: does a citation exist, does a claim's language match its tier, does an argument's warrant hold. The exception, Gate 2.8 (voice consistency, `templates/vv-framework.md`), asks whether a voice-driven text is worth reading, but only by ear (the read-aloud test) and only for voice-driven work. Nothing *locates* where prose has turned formulaic. AI-assisted prose can pass all of them and still be flat, uniform and predictable, and then it may not reach an expert or repeat-exposed audience (H1). It came up as the main open question of a literature scan of AI-text detectors (2026-09-26).

Four findings frame the decision; the fourth comes from a follow-up readability scan.

1. **Detectors answer the wrong question, unreliably.** Their error depends heavily on conditions such as generator, decoding and threshold (L69), and in 2023 tests paraphrase and editing cut the accuracy of most detectors sharply (L68, L70). In a 2023 pilot, seven detectors misclassified on average 61% of 91 essays by non-native writers (L67). The only independent support for the strongest commercial tool is a working paper that has not been peer-reviewed (L71). The work item's decision stands: no detector in any gate.
2. **The interpretable signals are formula signals.** In the explanations of expert readers judging whether an article was AI-written, the most frequent cues were stock vocabulary (53.1%), sentence structure, such as "not only … but also" and lists of three (35.9%), originality, i.e. "safe" prose that left them "bored or disengaged" (23.7%), uniform formatting (15.0%) and tidy conclusions (13.1%) (Russell et al. 2025, L72, Table 3/17). These are shares of all explanations, right or wrong, for English non-fiction articles; scientific papers were out of that study's scope. Excess LLM vocabulary is mostly style words (Kobak et al. 2025, L81). None of these signals concerns confidence calibration, so this lens does not overlap Step Z.
3. **Voice guides can generate formula (hypothesis).** A voice guide names devices because they work: a closing question to the reader, a closing box, a signature turn of phrase. A guide that prescribes such devices for every section, with no cap on how often, invites exactly the template signals of point 2. Guides that cap and vary their devices should not. This is untested; the test is below.

4. **The formula penalty so far appears to come from expert readers, and one measured cost is sameness between authors.** In the one lay-reader *preference* study of AI-written text, AI poems were rated higher than canonical ones on most dimensions, not on originality (L85; poetry, mostly inexperienced readers). Human-written stories on AI premises were also rated more enjoyable (L83), but that shows nothing about AI prose. The penalty so far appears only in expert-reader studies: MFA writers editing AI prose (L86) and literary experts (L88); frequent ChatGPT users also detect AI text by these cues (L72). No source compares expert and lay readers on the same text, so the split is inferred across studies. AI assistance made texts by *different* authors more alike (L83, L84); L84 attributes its content effect, tentatively, to instruction tuning, and L87 finds tuned models further from human style than base models. Clichés persisted in text generated under an explicit instruction to avoid them, and writer edits beat model edits (L86).

So a readability lens is possible without asking who wrote the text: count formula, locate it, and let the author judge.

## Options Considered

| Option | For | Against |
|---|---|---|
| **A. Do nothing** | No new surface | The gap stays; Gate 2.8 has no teeth on formula |
| **B. Add a detector** | Off-the-shelf | Wrong question; unreliable; biased; contradicts the work item's decision |
| **C. Formula locator + review prompt + effect-profile template, advisory, staged** | Interpretable signals with sourced provenance; author decides; fits Gate 2.8 | New surface to maintain; thresholds uncalibrated |
| **D. C as a blocking gate** | Enforcement | Formula can be deliberate; thresholds are SPECULATIVE; a gate on style would push authors to scrub tells, which L82 warns only makes detection harder |

## Proposed Decision

**No detector in any gate.** Detectors are not deterministic, their accuracy claims cannot be checked from outside, and "was this AI-written?" is not the framework's question. Revisit only if a detector with independently replicated error rates, including on non-native and edited text, exists *and* a gate needs provenance rather than content. (Stated here so adopters can see it.)

**Option C, staged in `extensions/`** (the DR-018 precedent):

- `extensions/formula_scan.py`: a deterministic, stdlib-only locator. It reports rhythm (sentence-length variation, monotone runs), paragraph uniformity, negation-contrast turns, the rate of the reversed form "Y rather than X" (counted apart, since academic prose uses it honestly), em-dashes per 1,000 words, the share of three-item lists, stock style words with per-item provenance (K/W/R) plus an optional project house list (`--house-words`, source H: a style rule, not evidence; this repo's is `vv/house-words.txt`), phrases recurring across paragraphs, recurring openers, and section-template features. It exits 0 whenever it emits a report and 2 only on a tooling error: **a locator, never a gate** (the DR-021 posture). Its signals are English-only; it flags text that looks non-English instead of reporting zeros. Tested with seeded formulaic and varied fixtures (`tests/test_formula_scan.py`).
- `extensions/formula-review.md`: a judgement pass. It triages the scan, checks the cues no count captures, runs the bored-reader check and the device register. It never judges authorship or truth.
- `extensions/effect-profiles.md`: a voice layer on top of `templates/writing-guide.md`. It has generic rules common to voice guides, the **device register** (every recurring device gets a dose cap and a variation rule, or is declared a deliberate template), and five effect profiles (provocation, comedy as diagnosis, lyric polemic, wonder, academic argument).

- **Multi-file mode (required before acceptance; not yet built).** In a book of essays the template recurs across files, not across sections of one file, so test step 2 cannot run per file (point 3). The mode will compare recurring features across a set of files. It measures repetition *within* one author's work; the between-author sameness of point 4 is a different quantity, which no single-author scan measures.
- **Engagement-marker density (proposed, not built).** For the academic profile (C5): reader mentions, directives, questions and personal asides per 1,000 words, advisory and English-only, on Hyland's categories (L89). ChatGPT essays carry about a third of the student rate, with questions and asides near zero (L91). Sword's exemplary authors use asides and opening questions (L90, partial read). Caveats: L91 compares against student essays, and its authors note that more such devices "do not necessarily mean more effective texts". There is no research-article reference rate yet, so a count must not be read against 16.99 per 1,000 words.

On acceptance: the scanner moves to `tools/`, the prompt to `agents/`, and the profile template to `templates/`. Gate 2.8 in `templates/vv-framework.md` gains "device register filled; formula review resolved". The academic profile (C5) makes the lens available to papers, not only voice-driven work.

## Hypothesis and Test (acceptance condition)

**H1:** Formula density, meaning template features plus negation-contrast rate plus triad share plus recurring phrases, is higher in the texts that expert readers and detectors flag, and in texts that readers *from the intended audience, where that audience is expert or repeat-exposed,* find less engaging, than in texts on the same topic without the formula. Lay readers are excluded from the claim: the one lay-reader preference study of AI-written text found a preference for it (L85).

**Test, in order of cost:**
1. **Paired baseline.** Run the scanner on pairs of texts produced by the same AI-assisted process that a detector scored very differently. The higher-scoring text should show more template and contrast flags. This is a sanity check, not evidence.
2. **Corpus.** Scan a set of works written under voice guides with and without dose caps, in multi-file mode. Works under capped guides should show fewer template features.
3. **Reader check.** On one work whose intended audience is expert or repeat-exposed, revise only the flagged formula, keeping content constant, and ask 3+ readers from the intended audience which version they would keep reading. Before the check, write the inclusion threshold for "expert or repeat-exposed" into `vv/hypothesis-log.md` and screen readers against it before they read. Log the result in `vv/hypothesis-log.md`.

Accept if the multi-file mode exists, step 3 favours the revision and the scanner produced no finding the author judged harmful. Reject or narrow if a majority of the screened readers prefer the original or cannot tell the versions apart. Readers who fail the screen are not counted, and a null from them is out of scope, not a rejection.

## Consequences

- The framework gains its first *locator* for formula that expert readers are hypothesised (H1) to penalise, next to Gate 2.8's read-aloud test and deliberately disjoint from truth (Step Z) and from authorship (detectors).
- Paper 1 gets an immediate, low-stakes finding: a hedge phrase in 8 paragraphs.
- New maintenance: the style-word list goes stale with each model generation (L82 notes "delve" falling in 2025). The list carries provenance per item and stays conservative.
- **Risk:** authors may read flags as "sounds like AI" and scrub tells. Both the prompt and the report say explicitly that the signals are formula, not authorship, and that the fix is for the reader, not the detector.

## Evidence Base

L67–L71 (detector reliability and bias), L73 (vendor report), L74–L76 (detector mechanisms), L72 (cue taxonomy), L77–L80 (publisher policy), L81 (excess style vocabulary), L82 (community sign list, tier D), L83–L91 (readability: lay-reader preference, homogenisation, the house style, engagement markers; L89 and L90 read only in part).

**Evidence gap:** triads, "not X but Y" turns and uniform sentence rhythm, the scanner's most distinctive signals, rest only on L72's cue shares. None of L83–L91 measures them. The expert-versus-lay split (point 4) is also inferred across studies, not measured.

## Open Questions

- Are the SPECULATIVE thresholds (sentence CV 0.35, triad share 0.8, template share 0.4) anywhere near useful? Calibrate them on real works (test step 2) before acceptance.
- Where does the multi-file mode draw the unit: a directory, a manifest list, or the book's build order?
- Should the device register live in the voice manifest (per project) or in the writing guide? Proposed: the manifest, since devices are per work.
- Is recurring *terminology* in papers separable from recurring *rhetoric* mechanically, for example with a glossary allow-list? Until then the review pass triages it.

## Revisit If

- A detector with independently replicated error rates on non-native and edited text appears. That still would not change this DR's question, but it would change the adopter note.
- Expert or repeat-exposed readers cannot distinguish formula-revised text from the original (H1 fails).
