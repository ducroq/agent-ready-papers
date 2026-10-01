# Translation Prompts

<!-- STATUS: PROPOSED under DR-023. Staged in extensions/; NOT an accepted
     surface until DR-023 is Accepted.

     Two prompts for the translation step in DR-023: text written by an agent
     for an agent (a /curate or /review-changes report, a CHANGELOG draft, an
     issue body) is rewritten for a person before it reaches one.

     USAGE, per text:
     1. Save the source where it will not be edited (proposed in DR-023:
        docs/work-items/archive/reports/, gitignored).
     2. Prompt T, in a FRESH context: give it the source only.
     3. python extensions/preservation_check.py <source> <translation> --link <the link from Prompt T step 4>
        (make preservation-check SRC=... TRN=... LINK=...). For public text
        the link is public (a commit, DR or issue), so the local source path
        never reaches the published text.
     4. Prompt C, in another fresh context: give it the source and the
        translation. The script cannot see an added claim that has no number
        and no tier word; Prompt C is for that.
     5. Fix what 3 and 4 found, or send it back to step 2. The source stays
        as written.

     A translation of a DR, a paper or another human-authored surface is a
     proposal the author approves (agent-write boundary). Both prompts build
     on templates/readability.md: Prompt T is its Prompt 1 content in its
     Prompt 2 sentences, reordered so the reader's decision comes first. -->

## Prompt T: translate for a person

```
You are rewriting a text so that the person it is for can act on it after
one reading. The reader knows the project but did not see the work that
produced this text. Give the rewrite only, no commentary.

Order:
1. First, what the reader must decide or do, if anything. Name only a
   decision the source asks for, and only a recommendation the source
   makes. If the source asks nothing of the reader, say so in one
   sentence; do not invent a decision to put first.
2. Then where things stand and what was concluded, with how sure the
   source says each conclusion is (its registry tier, if it has one). If
   the source does not say how sure it is, do not add a level.
3. Then the details a reader needs to check or act on, as full sentences.
   A short table is fine for a list of like items.
4. Last, a link to the source: <SOURCE LINK>. For public text (CHANGELOG,
   issues, commits) this is a public link, such as the commit, DR or issue
   the text is about; never a maintainer-local path.

Rules:
- Keep every claim exactly as strong as the source makes it. Do not add a
  claim, a reason, a consequence or an interpretation that is not in the
  source. If the source's point is unclear, keep it unclear and say what is
  missing; do not infer one.
- Keep every number, date and count from the source, in digits. When you
  add up items yourself ("3 warnings"), count them again in the source.
- Keep verdict and status words as the source gives them. "Not refuted"
  is not "passed"; "open" is not "pending"; "proposed" is not "planned".
- Keep certainty words at their level: "may" stays "may", "suggests" stays
  "suggests", "roughly 7%" stays roughly. Keep a hedge in the same sentence
  as the claim it qualifies. Do not add "all", "every", "never", "only" or
  "exactly" unless the source says it.
- Drop internal history (review rounds, earlier drafts, who found what) and
  internal shorthand, unless the reader needs it to act. Explain any ID you
  keep in a few words the first time ("DR-023, the decision on translation").
- One idea per sentence. Say who does what. Plain words over precise-
  sounding ones. Do not compress below clarity.
- Public text (CHANGELOG, issues, commits) links only to public sources: a
  commit, a DR, an issue. Never to maintainer-local files.
```

## Prompt C: claim comparison

```
You are checking a rewrite against its source. You did not write either.

List every assertion in the REWRITE that the SOURCE does not make. An
assertion is one checkable proposition: something that could be true or
false. Count it as not in the source if:
- the source does not state it, even if it seems to follow from it;
- the rewrite states it more strongly: less hedged, wider in scope, more
  certain, or with a cause or consequence the source leaves open;
- the rewrite names a different number, date, subject or status.

Then list every assertion in the SOURCE that the rewrite drops, if a reader
would act differently without it.

For each item give the rewrite's sentence, the closest source sentence (or
"none"), and one line on what changed. If there are none, write "No added
or strengthened assertions" and "No dropped assertions that change what a
reader would do". Do not judge style or readability.

SOURCE:
<paste>

REWRITE:
<paste>
```
