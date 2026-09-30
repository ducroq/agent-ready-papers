# Readability Prompts

<!-- SAVE AS: <paper-or-project-root>/readability.md

     Two prompts against compressed, hard-to-read AI prose: sentences that
     are grammatical but have to be read twice. They address sentence-level
     comprehension. Formula repetition (stock phrases, lists of three) is a
     separate lens: DR-022.

     A prompt may reduce the problem; do not expect it to remove it. In
     one study, explicitly asking models to avoid clichés did not remove them, and
     writer edits were ranked above model edits (Chakrabarty, Laban & Wu
     2025, CHI, doi:10.1145/3706598.3713559). That study covers creative
     writing, and its authors doubt it transfers to scientific writing. The
     author still rewrites. -->

## What goes wrong

Four patterns tend to make the prose hard to read:

1. **Too much in one sentence.** Two or three claims joined by "so that", "and" or a subordinate clause.
2. **Abstract nouns as the subject.** Nobody does anything: "a wrong number cannot be attributed to its cause".
3. **The point is never stated.** The text lists properties and leaves the reader to infer what they add up to.
4. **Precise-sounding over clear.** "In a form that fits the course as it is taught" is exact and says nothing concrete.

Two examples. Each rewrite makes the same claims as the original, no stronger and no weaker; only the sentences change.

| Before | After |
|---|---|
| Nobody outside the maker can check which measurand the number on the screen refers to, and a wrong number cannot be attributed to its cause. | Nobody outside the maker can check what the number on the screen measures. And if the number is wrong, nobody can trace its cause. |
| It gives feedback in real time, in a form that fits the course as it is taught, so that it can also run without an instructor. | It gives feedback while the student practises. The feedback fits the course as it is taught. The aim is that it can also run without an instructor. |

The second rewrite shows pattern 3's limit. What the author meant was "it tries to give the feedback an instructor would give". That sentence is not in the original, so only the author can add it; a model that adds it is inventing a claim.

## Prompt 1: Explain like I'm 18

Use it to understand where work stands, and as the first step before drafting a section. The reader is the same one throughout this file: a first-year student, or a colleague from another department.

```
Explain like I'm 18, in full sentences: what is the problem, what did we
try, what did we find, what do we conclude, and what should we do next?
For each conclusion, say how sure we are (its registry tier, if it has
one) and why.
```

Short form for a status check:

```
Explain like I'm 18, in full sentences: where do we stand now, what do we
conclude, and what do we recommend? For each conclusion, say how sure we
are (its registry tier, if it has one) and why.
```

- "In full sentences" matters. A list of headings often returns fragments, which are the compressed sentences again.
- "How sure" matters too. Simplifying tends to drop caveats, so "suggests" can turn into "shows". Check the answer against Language Calibration in `writing-guide.md`.
- If the answer is vague, the section may have no clear point yet. Check that before polishing sentences.

## Prompt 2: Write for a reader

Use it for manuscript prose. The Prompt 1 skeleton fits a report, not a paper paragraph.

```
Write for a smart reader who does not know this project, such as a
first-year student or a colleague from another department.

- Keep every claim exactly as strong as its evidence. Use the language
  for its registry tier (writing-guide.md, Language Calibration). A
  plainer word must not strengthen a hedge: "suggests" stays "suggests".
  Tier language overrides every rule below.
- One idea per sentence. If a sentence contains "so that", "which", or a
  second claim after a comma, split it. Keep a hedge or qualification in
  the same sentence as the claim it qualifies.
- Say who does what. Make a person or a thing the subject ("the
  instructor watches", "the sensor measures"), not an abstract noun
  ("attribution", "provision of feedback").
- State the point outright, at the strength its evidence allows. Do not
  leave the main point for the reader to infer. If the point is not in
  the source or the notes, ask; do not infer one yourself.
- Main point first, then the reasons or details.
- Prefer the plain word over the precise-sounding one. Give a concrete
  example when a claim is abstract.
- Repeat a key term rather than switching to a synonym.
- Vary sentence length. One idea can take a long sentence; short
  sentences are not a rhythm.
- Do not compress below clarity. Cut words that add nothing, but never
  cut a step the reader needs.
- Test each sentence: would you say it this way to a colleague at the
  coffee machine? If not, rewrite it.
```

## Workflow

1. Run Prompt 1 on what the section should say.
2. Draft the section from that answer with Prompt 2.
3. Have a fresh session mark every sentence a first-year student would have to read twice, and say why. Rewrite those sentences yourself.

If you also run the DR-022 formula lens: a key term recurring across paragraphs is expected under Prompt 2, and not a finding by itself. The two lenses have different readers in mind: this one a reader new to the topic, DR-022 an expert reader.

Two things tend to work against these prompts (maintainer observation, not measured):

- **"Be concise", "no filler", "dense".** These instructions seem to push the model toward compression. Leave them out of prompts for prose.
- **No sample of the style you want.** With rules alone, the model may have to guess the register. A sample paragraph in the style you want seems to help more than extra rules.
