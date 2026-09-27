# Effect Profiles: a Voice Layer for the Writing Guide

<!-- TEMPLATE. STATUS: PROPOSED under DR-022. Staged in extensions/; not an
     accepted templates/ surface until DR-022 is Accepted.

     templates/writing-guide.md maps confidence tiers to language: it keeps
     prose TRUE. This layer keeps it WORTH READING. It sits on top: pick the
     profile for the effect the work is after, copy it into the project's
     voice manifest (Gate 2.8), and fill in the device table.

     Derived from five working voice guides in a maintainer-local essay
     corpus (patterns only, no text), tested against the detector and
     readability literature: Russell et al. 2025 (L72), Kobak et al. 2025
     (L81), Wikipedia "Signs of AI writing" (L82). -->

**Project:** [name]
**Profile:** [one of Part C, or a named blend]
**Last updated:** [date]

---

## Part A: The generic layer (every profile)

The voice guides of four projects written for different effects share these rules. They are the candidate generic core.

| Rule | What it means | Check |
|---|---|---|
| **Name the excluded registers** | List the voices this work must not slip into, each with the reason it fails *here*. Common ones: academic hedging (in essays), snark, the righteous register, the explainer, guru certainty, breathless enthusiasm | Drift-tell table (below) |
| **Hold the tension; refuse false resolution** | Where the work holds two true things, do not resolve them in the last paragraph. Keep a red-flag list of the phrases that resolve it too early (e.g. a closing call for balance) | Read the endings |
| **Concrete over abstract** | At the moment of revelation, drop to objects, bodies, numbers. Keep abstract nouns for argument passages | Grep the image passages |
| **Drift-tell table** | A searchable list of telltale phrases, each tied to the rule it breaks | Mechanical |
| **Calibration triad** | For the core register, write one example that is too dry, one that overshoots (snark, purple, cute), and one that is right | Once, when the guide is written |
| **Read aloud, whole** | The last gate. A sentence awkward to say is awkward to read; a sentence that wants applause gets cut | Human |
| **The guide against itself** | The guide describes a manner, not props to import. A collection of past lines is for recognising the voice, not for reusing lines. The guide yields when obeying it would make the prose worse. | Human |
| **Dose and vary every device** | See Part B. The rule the source guides apply unevenly (three cap or vary their devices; one fixes a per-section structure without a cap on its signature devices), and the one this layer makes explicit | `extensions/formula_scan.py` + `extensions/formula-review.md` |

## Part B: The device register (the anti-formula rule)

**Why.** A voice guide names devices because they work. Applied to every section, a device that works once becomes a tic. It then becomes predictable, and predictability is what expert readers cite when they flag a text, and what bores them. In Russell et al. (L72, English non-fiction articles), "originality" cues (safe, no surprise, "leaving annotators bored or disengaged") made up 23.7% of the experts' explanations, sentence structure ("not only … but also", lists of three) 35.9%, and uniform formatting 15.0%. In the corpus this layer was derived from, the one guide that fixes a per-section structure without a cap on its signature devices is the one whose manuscript showed section-template flags in the first scan ("Ask:" closing 4 of 9 sections). The comparison is not yet fair: the other books spread their template across separate essay files, which the scanner does not compare, and the one other book with enough lists had an even higher share of three-item lists. That is one observation (n=1), a hypothesis rather than a finding; DR-022 says how to test it.

**Rule.** Every recurring device the voice manifest names gets a row:

| Device | Effect it serves | Dose cap (per unit) | Variation required | Scanner signal |
|---|---|---|---|---|
| [e.g. closing question to the reader] | [turns the argument on the reader] | [≤ 1 per essay; not in consecutive sections] | [vary the form: question, image, silence] | `template: closes on a question` |
| [e.g. negation-contrast turn, "It is not X. It is Y."] | [reframes] | [≤ 1 per section, and only at a real turn] | [n/a] | `contrast` |
| [e.g. list of three] | [rhythm, closure] | [not the default list length] | [let lists be two, four, or prose] | `lists` |
| [e.g. closing box or paradox block] | [thesis stated plainly] | [one per work, or per essay if the form is the point] | [the box changes state: straight, marked, hollow, refusing] | `template`, `phrases` |
| [e.g. mythic-present passage] | [the reader's body in the room] | [≥ 1 per essay] | [different image each time] | (human) |

**A deliberate template is allowed.** If a recurring form *is* the point (a book whose thesis is that bestsellers repeat a formula, say), declare it here with its reason. The review pass then checks that the template is *marked*: the reader can tell it is on purpose.

**Units.** "Per unit" means per essay, chapter or section, whichever the work's rhythm uses. State it.

## Part C: Effect profiles

Pick the effect the work is after. Each profile names the devices it tends to use, its typical formula risk, and what must vary. They are starting points; blends are normal (one book used four registers deliberately, and the switching *was* the design).

### C1. Provocation / mirror
- **Effect:** the reader recognises themselves in what they came to judge.
- **Typical devices:** a straight-faced artefact (a form, a diagnosis) presented without winking; a paradox held open; direct second-person address; a closing turn onto the reader.
- **Formula risk: high.** The house moves are compact and quotable, so they are easy to repeat per section: the closing question, the negation turn, the paradox box, uniform short sentences.
- **Must vary:** how each section ends; sentence length at the turn. Keep the artefact itself fixed; the frame around it changes.
- **Excluded registers:** righteous, campaign ("we must"), the explainer.

### C2. Comedy as diagnosis
- **Effect:** the reader laughs at a mechanism and then sees themselves inside it.
- **Typical devices:** a translation (what the sentence says vs what it does); a recursion or chain whose punchline is also the argument about evidence; a scholarly interruption (certify, then deflate); a take-away box with changing states.
- **Formula risk: medium.** Past a small per-essay count, a device stops registering with the reader.
- **Must vary:** which devices each essay uses (fewer, used well, rather than all of them); the state of the box.
- **Excluded registers:** snark aimed at people; wit that asserts nothing; the therapeutic register.

### C3. Lyric polemic
- **Effect:** recognition through images; the argument arrives as a shape the reader sees.
- **Typical devices:** a mythic present tense; types instead of names ("the consultant"); body vocabulary in image passages; closing on an image, not a summary; gnomic two-clause symmetry.
- **Formula risk: medium-high.** A recurring opening becomes a habit the reader sees coming, and gnomic symmetry repeated becomes a cadence.
- **Must vary:** the opening image per essay; where the mythic passage falls. Give the modern the same bodily treatment as the ancient, or it tips into nostalgia.
- **Excluded registers:** academic citation-voice in image passages; pastiche of the touchstone authors.

### C4. Wonder / exploration
- **Effect:** the reader holds an open question with pleasure, not anxiety.
- **Typical devices:** deliberate register switching (scientist, guide, bridge, question-holder); flagged speculation tiers; the unresolved close.
- **Formula risk: low for structure, medium for closers.** The question-holder close can become every chapter's ending.
- **Must vary:** which register closes a chapter.
- **Excluded registers:** breathless pop-science; guru certainty; mysticism.

### C5. Academic argument (papers)
- **Effect:** the reader follows and trusts the argument; the contribution is findable.
- **Typical devices:** a signposted structure; hedges calibrated by tier (the writing guide); defined terms used consistently.
- **Formula risk: different in kind.** Consistent terminology is a virtue, so recurring technical phrases are expected, and a scanner will list them. The risk is *rhetorical* formula: a hedge phrase repeated until it stops meaning anything ("to our knowledge" eight times), stock style words (L81), a tidy optimistic conclusion.
- **Must vary:** hedging phrasing, where the tier allows; paragraph openings.
- **Excluded registers:** promotional ("groundbreaking"); confidence above tier (DR-002; that is Step Z, not this layer).

## Part D: Filling it in

1. Pick a profile (or a blend) and copy its bullet list into the voice manifest.
2. Fill the Part B device table for *this* work: every device the manifest names gets a dose cap and a variation rule, or is declared a deliberate template with its reason.
3. Run `python extensions/formula_scan.py <manuscript>` on a full draft. The first run sets the baseline.
4. Run the review pass (`extensions/formula-review.md`) with the manuscript, the scan report and this file.
5. Gate 2.8: the device table is filled, the review pass findings are resolved or consciously kept, and the read-aloud test passes.
