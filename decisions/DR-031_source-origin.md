# DR-031: A Source Item Records Whether the Source Found the Point or Relays It

---
status: Proposed
date: 2026-11-08
---

## Context

A reader of Paper 1 (build `paper1-draft-3-13-ga7c9eeb`, comments 2026-11-07) wrote that the register "stops at the claim the source makes and does not examine it further". It matters, they wrote, whether a source took a claim from another source or established it by its own research. A source may assume the effect of temperature on the rate of electrolysis, citing another source, or it may have measured it: "an essential difference".

The framework handles this only per document, not per claim:
- **Source tiers** (`templates/claim-registry.md`, *Source Tier Reference*) grade the document: A for peer-reviewed primary research, B for a peer-reviewed review, and so on. A primary-research article (A) that makes a point in its introduction, citing someone else, is graded as if the point were its own finding.
- **The source check** (DR-027; `templates/anti-hallucination.md`) asks whether the work exists and says what is attributed to it. It does not ask whether the work *established* the point.
- **"Independent"** is defined in the glossary (`docs/glossary.md`, *independent sources*: "Sources that do not derive the point from one another or from a shared origin (same data, same group, one citing the other for it)"), and the tier rules count by it (DR-002; `templates/claim-registry.md`: "3+ independent sources"). But no step of the source check asks the question that would apply the definition, so a register cannot show that it was applied. Two sources that relay one study are counted as two unless someone happens to notice.

**Evidence that it matters.** Greenberg (2009, *BMJ* 339:b2680, L116) traced every paper making one biomedical claim (242 papers, 675 citations). Belief in the claim grew through "amplification", "the expansion of a claim's belief system by citation to papers lacking any data addressing it", and a subclaim "transformed from hypothesis to 'fact' through citation alone". He notes that "Authors could choose to cite only primary data when making claims, resulting in amplification minimal networks."

**Evidence that it occurs here.** A source-origin trace of Paper 1's register (`papers/perspective/vv/traces/2026-11-08-source-origin-trace.md`; one pass by the session agent, not yet confirmed) checked about 40 source items in 21 rows. Three relay the point attributed to them:
- Jaakkola 2020 relays "commonly accepted templates" from an editorial (Cornelissen 2017);
- Dinter & Krawatzeck 2015 partly relays Gregor & Hevner 2013, with which the paper pairs it as a second report;
- Wachsmuth et al. 2017 relays the definition of a cogent argument (acceptability, relevance, sufficiency) from Johnson & Blair (2006), and the paper attributes the warrant check's questions to Wachsmuth.

No tier changed, but two wordings and one count of agreeing sources did. Neither relayed origin could be read in the session, so the record needs a way to say "relayed, origin not read".

## Options Considered

### Option A: Record the origin of each source item, and define independence by origin
Each `src:` item states whether the source reports the point as its own (a study, analysis, definition, tool or stated position), as a synthesis (a review's own analysis of other studies), or relays it from another work. A relayed item names the origin and says whether the origin was read. Items that relay the same origin count as one source for the tier rules.
- (+) Answers the reader's point at the level it was made: per claim, not per document.
- (+) Makes the glossary's definition of "independent" checkable in the record, and the tier rules already depend on it.
- (+) Fits the existing schema: an annotation inside the Grounds item, with no new column.
- (-) One more question in every source check. The trace took about 40 item-level judgements, most of them obvious from the row.

### Option B: Require every relayed point to be traced to its origin and cited there
- (+) Greenberg's "amplification minimal" practice.
- (-) The origin is often unreadable (books out of print, paywalled editorials; both origins in the trace). The rule would force authors to cite works they have not read, which the anti-hallucination checklist forbids.

### Option C: Rely on the document grade (A primary, B review)
- (+) No change.
- (-) Fails the reader's own example, and two of the three cases in the trace: an article graded for its type, relaying a point in its introduction.

### Option D: Build a claim-specific citation network (Greenberg's method)
- (+) The only option that detects amplification across a literature.
- (-) A study in itself, for each claim. A method for a P0 claim under dispute, perhaps, not a routine check.

## Decision (proposed)

**Option A.**

1. **Source check, a third question.** After "the work exists" and "it says what the claim attributes to it", ask: *does the work report this as its own finding, or relay it?* Record one of:
   - `own`: the source's study, data, analysis, definition, tool or stated position;
   - `synthesis`: a review's own analysis across studies (a review cited for one study's result is `relays`, not `synthesis`: Greenberg's amplification route);
   - `relays: <origin>`, plus `(read)` or `(not read)`.
   The default is `own` and needs no annotation, so only `synthesis` and `relays` are written, for example `src: Jaakkola 2020 (relays: Cornelissen 2017, not read)`.
2. **Independence.** The glossary's definition of *independent sources* is applied through the origin annotation: items relaying one origin count once, and an item that relays the origin of another item in the same row adds nothing to the count.
3. **Prose.** Where a claim's sentence names the relaying source as if it were the origin ("taken from Wachsmuth's definition"), the sentence names the origin or says the point is relayed ("the definition of a cogent argument that Wachsmuth et al. take from Johnson and Blair").
4. **Not adopted:** tracing every point to its origin (B), the document grade alone (C), citation networks as routine (D, which stays available for disputed P0 claims).

## Consequences

- **Templates and glossary:** the source check in `templates/anti-hallucination.md` and `templates/claim-registry.md` gains the origin question and the annotation; *Source Tier Reference* points to the glossary's *independent sources* and the origin annotation; `docs/glossary.md` *source check* is updated. A worked example is added (the Jaakkola case).
- **Tools:** optional. `tools/check_registry.py` could parse `relays:` and warn when two items in one row relay the same origin. It is not required for acceptance.
- **Paper 1:** the source check (§4) gains one clause and a sentence citing Greenberg (L116); Table 2's note says relayed items count once. The three items in the trace are annotated in the register, and the sentences at §2 (Jaakkola; Gregor & Hevner with Dinter & Krawatzeck) and §4 (the warrant check) are reworded. The annotated rows rejoin the DR-029 re-rating queue.
- **Relation to DR-029** (Proposed): its counting rule already says "Count sources, not citations: two papers reporting the same dataset count once". This DR supplies the record that makes that rule checkable for relayed points.
- **Relation to DR-030** (Proposed): both refine step 2 of the source check, DR-030 for scope and this DR for origin. If both are accepted, the template change makes them one step with two parts.
- **Adopters:** a MINOR release. Existing registries stay valid; an unannotated item reads as `own`.

## Acceptance Condition

Accept when the origin question, applied by someone other than the session agent to a registry other than Paper 1's, finds at least one relayed item whose author agrees with the verdict. Also accept if a human rater confirms at least two of the three verdicts in the Paper 1 trace.

## Open Questions

- **Partly relayed** (the trace's Dinter & Krawatzeck case: one sentence its own, the supporting one relayed). Is that `relays`, with a note, or a fourth value? And does a row that pairs a partial relayer with its origin count one source or two?

- Should `own` be recorded explicitly, for audit, instead of being the default? An explicit field shows that the question was asked; a default cannot be told apart from "not checked".
- Amplification across a literature (a source that reports its own data but also cites an earlier source for the same point) is outside this check. Is there a cheap signal short of Option D?
- A reader also asked whether "whether the field accepts" a declared starting point can be answered at all. That is a separate question, for the declared-starting-point check, not this DR.

## Revisit If

- Re-rating finds origin verdicts unreliable between raters: the `own`/`synthesis` line for reviews is the likely weak point.
- Relayed items turn out to be rare in other registries (fewer than 1 in 20 items). The check's cost would then exceed its yield, and the question could move to P0 rows only.
