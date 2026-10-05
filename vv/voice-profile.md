# House Voice: papers and framework prose

For anything someone else reads: papers, the README, decision records, the CHANGELOG, reports. The aim is prose the maintainer would sign, drafted with AI help and free of formula. It does not have to be his exact voice (maintainer, 2026-10-05); it has to read as written by someone who means it. It sits on top of the truth layer and never overrides it: tier language comes from `templates/writing-guide.md` (Language Calibration), and that wins over every rule below. Where this profile and `templates/readability.md` disagree, readability wins for papers.

Not for the maintainer's art essays, which have a voice of their own (lyrical, sardonic, aphoristic) and a separate profile. Paradox and the short line that lands like a blow belong there.

**Built 2026-10-05** from four sources, each named where it is used:
- **A**: the maintainer's private text archive, 1999-2009 (about 40,000 words, mostly Dutch, written before AI tools).
- **C**: the maintainer's corrections of AI drafts, kept in his private notes.
- **P**: the art-essay profile, used only for what to leave out.
- **D**: DR-022 and `extensions/effect-profiles.md`, profile C5 (academic argument).

No suitable English sample of his own prose was available, so his taste sets the rules below and the sample at the end is AI-assisted prose he has approved. Rules from C were made on Dutch correspondence; that they carry over to English papers is an assumption.

## The voice (from his taste)

- **One claim per sentence, as long as its reasoning needs.** A reason may stay in the sentence of the claim it supports (*because*, *so*), instead of being chopped into short sentences with a turn between them (C). A second claim gets its own sentence (`templates/readability.md`, Prompt 2). Short sentences are for a plain fact, not for effect.
- **The reason, not the effect.** Say why something was built or argued, not what it will achieve (C).
- **Concrete about what exists.** Say what is there and what is not, with a pointer: "one perspective is built", "that does not exist yet" (C).
- **No claim bigger than the case.** Describe what the work consists of, not what it demonstrates (C). This is the same rule as the tier language, arrived at from taste.
- **Plain about the limits of knowledge.** "Wat weten wij eigenlijk van de wereld? Bedroevend weinig." (What do we actually know about the world? Woefully little.) (A). In a paper this becomes a plain statement of what is not known, at the tier it deserves, not the question-and-answer turn: "The result? Nobody knows." is itself a stock AI device.
- **A dry aside, sparingly.** Historians who wanted to present themselves "(zoals gebruikelijk)" (as usual) as the perfect end stage (A). In a paper, at most one or two, in parentheses, about ideas and never about named authors; a reviewer reads irony at a person as snark.
- **Say who does what, with an example.** A person or a thing as the subject, and a concrete case where a claim is abstract (`templates/readability.md`, Prompt 2). His notes do this by habit: the light that gives an object "een klein duwtje" (a small push) when we look at it (A).
- **If he would have to ask what a sentence means, the sentence is wrong** (C). It is the most direct test available.

## What does not belong

Rows marked *scan* are located by `make formula-scan`, an advisory locator (PROPOSED, DR-022) that flags and never blocks. The other rows are for the reader to catch.

| Do not | Measured | Instead |
|---|---|---|
| Em-dashes (*scan*) | Archive (A): 2 in about 40,000 words, 0.05 per 1,000. Paper 1 draft: 12.5 per 1,000. Notes against a paper, Dutch against English, so only the size of the gap is evidence | Comma, colon, parentheses or a full stop. A spaced en-dash ( – ) at most, and rarely; the archive uses 3.5 per 1,000 |
| "Not X but Y", "Y rather than X" (*scan*) | Archive (A, Dutch): about 0.2 "in plaats van" per 1,000. Paper 1 draft: 3.2 "rather than" per 1,000 | State Y. Mention X only if a reader would otherwise assume it, because denying it puts it on the table (C) |
| Lists of three by default (*scan*) | Paper 1 draft: 79% of lists have exactly three items | Two, four, or a sentence. List what there is, not what sounds complete |
| The same sentence opener again and again ("Specifically,", "Recent systems go further") (*scan*) | Scanner, `openers` | Start with the subject |
| The same hedge again and again ("to our knowledge" in 8 paragraphs of Paper 1) (*scan*, as a recurring phrase) | (D) | Say it once where the scope is set, then trust the reader |
| Stock AI vocabulary (*scan*) | Evidence list in `extensions/formula_scan.py` (K, W, R) | The plain word |
| US tech slang: load-bearing, ships, surfaced, quietly, punt (*scan*) | House list, `vv/house-words.txt` | essential, is released, raised, (cut), postpone |
| Aphorism or paradox as the last sentence | (C, P) | End on the last thing that is true and needed |
| A tidy, optimistic conclusion that resolves what the work leaves open | (D) | Say what remains open, at its tier |
| Validation filler, promotional words ("groundbreaking", "it is worth noting") | (C, D) | Cut |

A deliberate exception is fine when it is the point. Note why next to it.

## Calibration (one example, Paper 1's opening)

One source claim (Liang et al. 2025: up to 22% of computer science papers show evidence of LLM modification, with usage detectable in all major disciplines), written three ways.

- **Too dry:** "LLM modification: up to 22% of CS papers; all major disciplines (Liang et al. 2025)."
- **Overshoots:** "AI is quietly rewriting science: up to 22% of computer science papers bear its fingerprints, and no discipline is untouched." It fails twice, on style and on truth: "rewriting science" and "untouched" claim more than the source measured.
- **Right:** "Up to 22% of computer science papers now show signs of editing by a large language model, and such editing can be detected in every major discipline (Liang et al. 2025)."

The draft's "is transforming how academic papers are produced" is the overshooting kind: Liang et al. measure prevalence, not transformation.

## Sample paragraph

A sample tends to help a model more than further rules (`templates/readability.md`). This one is Paper 1's opening paragraph, redrafted with AI help under this profile. Same claims as the draft, with two deliberate changes: "is transforming how academic papers are produced" is gone, because Liang et al. measure how widely the tools are used, not a transformation; and the fabricated citation is added as an example of such an error (registry S1-1, cited in the next paragraph). Two fresh readers scored it 7 and then 7.5 out of 10; the last change answers their main obstacle, the unexplained term "verification failures".

Two deliberate exceptions to Prompt 2: sentence 1 joins two findings of one study, and sentence 2 joins a quality to the tasks that show it. Both fresh readers marked sentence 2 clear; their pause in sentence 1 was over Liang's terms ("up to", "signs of"), not its structure.

> **Approved by the maintainer, 2026-10-05.** Replace it when a better approved paragraph exists. Do not use the art essays as a stand-in.

> Writing assistants based on large language models (LLMs) have spread quickly: up to 22% of computer science papers now show signs of LLM editing, and such editing can be detected in every major discipline (Liang et al. 2025). The tools write fluently, and they can summarise literature, structure an argument, draft prose and format references. That fluency brings risks of its own, and some are harder to spot than the problems of writing without AI. When a human author falls short, the text tends to show it, in awkward phrasing, gaps in coverage or inconsistent formatting. An AI-assisted draft can read as polished and complete while it contains errors that only checking would reveal, such as a citation to a paper that does not exist.

## Checks before anything goes out

1. `make formula-scan FILE=<file>` (it uses the house list). Read every flag; the author decides.
2. Read it aloud, whole. A sentence awkward to say is awkward to read.
3. Would he have to ask what a sentence means? Rewrite it.
4. After any rewrite, tier words and numbers must survive unchanged (`templates/writing-guide.md`). `extensions/preservation_check.py` (PROPOSED, DR-023) can check that; it is tested on short English rewrites, not yet on paper prose.

## Dutch

Outward Dutch text: the model supplies sources, structure, calculations, checks and a rough version labelled as raw material, and he writes the sentences (C). Model Dutch is translated English: Dutch words, English sentence structure.
