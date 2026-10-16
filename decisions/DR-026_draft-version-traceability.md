# DR-026: Draft Version Traceability

---
status: Proposed
date: 2026-10-16
---

## Context

The framework traces each claim to its evidence and its verification result (`templates/vv-framework.md` §6: Goal → Claim → Evidence → Verification → Status). It never records *which draft* a verification result, a review pass or a piece of feedback applies to. Gate 2 asks for a "timestamped snapshot for co-author review", but a timestamp does not identify a manuscript state, and the paper template has no version line: `templates/CLAUDE.md` carries a Status phase and the framework pin, nothing for the paper itself.

Trigger (2026-10-16): the maintainer sat down to write feedback on Paper 1 and asked what the current draft number was. The same feedback asked for line numbers, as another of the maintainer's papers already has. There was none. `manuscript.tex` had `\date{}`, `papers/perspective/CLAUDE.md` said "first draft complete" in one place and "revised draft" in another, and no tag yet named a paper state. The only exact identifier was a commit hash (`e7e444d`), which the feedback file then carried in its name by hand.

The gap matters more as a paper accumulates readers. Feedback on draft 1 read against draft 3 points at sentences that moved or vanished; a DR-011 review pass whose input is unrecorded cannot be compared with the next; a coverage report quoted in an AI-use statement (DR-025) is only true of one state. In systems-engineering terms this is configuration management: a baseline, and every review record pointing at one. The framework claims an SE identity (DR-007) without this piece.

## Options Considered

| Option | For | Against |
|---|---|---|
| **A. Nothing; adopters use commit hashes when they think of it** | No new surface | It happened by luck once; a hash on a printed PDF is unreadable, and nothing ties a review to it |
| **B. Mandate a mechanism (git tags + a LaTeX stamp)** | Fully mechanical | The framework supports LaTeX, pandoc and Word (`templates/CLAUDE.md`, Supported Paper Formats), and not every adopter keeps the paper in git |
| **C. A three-part convention, with git tags and a build stamp as the reference implementation** | Format-independent; every review record gains an anchor; LaTeX + git adopters get it nearly free | Adopters without git number drafts by hand, which can drift |

## Proposed Decision

**Option C.** Three rules, each independent of tooling:

1. **A draft that leaves the author's hands gets a version ID.** Default: an annotated git tag `<paper>-draft-N` on the commit sent out, `<paper>` in letters, digits and hyphens (the stamp is typeset: `_` or `#` break the build, and `%` would silently cut the stamp short). Without git: a number the author increments by hand and records in the paper's `CLAUDE.md`.
2. **The distributed artefact shows its ID on its face** (title page, header or footer), so a PDF passed on by email can be traced back. A draft sent out for review also carries line numbers (LaTeX: `lineno`), so feedback can point at "l. 212" instead of "page 8, below".
3. **Every review record names the ID it applies to**: feedback files, DR-011 review passes, coverage snapshots for Gate 2, and the slot-3 verification record of a DR-025 statement.

**Reference implementation (LaTeX + git), trialled on Paper 1.** `make paper1-pdf` passes the output of `git describe --tags --dirty --match 'paper1-*'` to pdflatex as `\paperversion`, defined on the command line, so no file is left behind to go stale. With no reachable draft tag it passes `untagged <hash>`. The manuscript's `\date{}` prints `\paperversion` when it is defined and "unversioned build" otherwise, so a plain `pdflatex` run, or a build outside a git work tree, still works and says so. The first build from a clean checkout of a tagged commit reads exactly `paper1-draft-1`; work in progress reads `paper1-draft-1-<n>-g<hash>[-dirty]`.

**Placement in the framework, on acceptance.**

- `templates/CLAUDE.md`: a `- **Draft:**` header line beside the framework pin, and a Build Commands note on stamping.
- `templates/vv-framework.md`: §6 gains a Version node (Verification → *against draft ID* → Status); Gate 2's snapshot line names the draft ID instead of a timestamp.
- `agents/review-prompt.md`: a "Draft reviewed" field in the output header.
- `UPGRADING.md`: an optional row.
- No new tool in `tools/`. The stamp is a few lines of build script per format.

## Consequences

- Feedback, review passes and verification records become comparable across drafts, and a later reader can tell which draft a comment was about.
- Draft tags share the repo's tag namespace with framework releases. `/release` selects only `v[0-9]*` tags, so a `<paper>-` prefix does not disturb it; a monorepo with several papers needs the per-paper prefix to keep `git describe --match` apart.
- `git describe`'s commit count and its `-dirty` flag are repo-wide, not paper-specific: in a monorepo it counts framework commits too, and an unrelated uncommitted edit marks the paper dirty. The tag and hash parts are exact; the count is only a rough distance.
- A committed PDF can never carry its own commit's ID. It shows the parent state, `-dirty`. A distributed PDF should therefore be built after tagging, from a clean tree.
- `--dirty` looks at the whole work tree. Paper 1 tracks its PDF, so the build itself normally makes the tree dirty (pdflatex embeds the build time): only the first build after checking out a tag reads exactly the tag, unless the build is made reproducible.
- Adopters gain one step per distributed draft. It costs one `git tag` command, or one number edited by hand.

## Acceptance Condition

Accept when both hold:

1. Paper 1 distributes a second draft (`paper1-draft-2`) built from a clean tagged tree, with line numbers, and its stamp reads exactly the tag.
2. At least one review record for draft 2 (feedback file, review pass or coverage snapshot) names the draft ID, and the maintainer judges that the anchor was useful when acting on it. Paper 1's feedback files are gitignored, so this record may stay private; the maintainer's judgement is the evidence.

## Open Questions

- Should a draft tag also mark a gate result, e.g. a tag message recording which gates passed at that baseline?
- Should `make drift` or `check-registry` warn when a distributed PDF's stamp is `unversioned build` or `-dirty`?
- Should a paper keep its PDF in git at all? Tracking it is what makes every rebuild `-dirty` (Consequences).
- Is "draft" the right word once a paper is submitted? Submission and revision rounds may want their own prefix (`-sub1`, `-rev1`).

## Revisit If

- Adopters without git report that hand-numbered drafts drift from the artefact: consider a template field the build reads.
- A review record is found pointing at the wrong draft despite the convention: rule 3 needs a check, not prose.
