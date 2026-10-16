# DR-028: Every Paper Has a Glossary

---
status: Accepted
date: 2026-10-16
accepted: 2026-10-16
---

## Context

`templates/glossary.md` exists, but the README lists it as "useful once the paper grows", and Paper 1 never had one. The draft-1 review of Paper 1 (2026-10-16) traced several faults to undefined terms: "verification" used about 60 times and glossed only in passing ("verification asks whether the text holds"), never defined, "validation" never contrasted with it, "priority" shown in a table but never explained, and CLAIM and PROPOSITION used in senses their own sources contradict (DR-027). Four model reviewers flagged the same gaps. The maintainer then asked that a glossary be mandatory for every paper.

DR-027 introduces a framework glossary (`docs/glossary.md`). A paper's glossary is where an author records which of those terms the paper relies on and what its own field's terms mean, so that the agent writing with them and the readers judging the paper use the words the same way.

## Options Considered

### Option A: Keep the glossary optional
- (+) No new step
- (-) The failure that triggered this DR recurs: terms drift because nothing asks for definitions

### Option B: Mandatory, stated in the templates only
- (+) Cheap
- (-) A rule without a check; the repo's own constraint: "A rule that can be a script is a script"

### Option C: Mandatory, with a check
- (+) Absence is caught mechanically
- (-) One more file per paper and one more check

## Decision

**Option C.**

1. Every paper has `glossary.md` in its paper directory (the directory holding the paper's `CLAUDE.md`), created from `templates/glossary.md` at project setup.
2. It **refers to** `docs/glossary.md` for the framework's terms by link, not by copy, and defines the paper's own terms: field terms, abbreviations, any framework term the paper uses in a narrower sense, and every definition registered as a declared starting point (DR-027). A paper outside this repository links to `docs/glossary.md` at the framework release it is pinned to (a tag, not `master`), so the framework terms it relies on change only when the author bumps the pin.
3. Every abbreviation is defined there before the manuscript uses it. Until an acronym check exists ([#56](https://github.com/ducroq/agent-ready-papers/issues/56)), this is a review item, not a mechanised one.
4. `tools/check_registry.py` gains `--glossary PATH` (given explicitly; the tool does not guess it from the registry path): it fails when the file is missing, empty, or still contains the template's placeholders. Without the flag, the report says `glossary: not checked`, never a silent pass. `make check-registry` passes it for Paper 1. It sits in this tool because the registry is what a paper's terms must agree with.
5. `templates/CLAUDE.md`, which already lists the glossary under "Checking terminology" and in Key Files, adds it to the "Writing or editing prose" row. `templates/glossary.md` gains a "Framework terms" section that links to `docs/glossary.md`, and its "single source of truth for terminology" line becomes "single source of truth for this paper's terms".

## Consequences

- New papers start with a glossary; existing papers add one when they adopt v5.0.0 (UPGRADING step).
- Before writing prose, the agent consults the paper's glossary, which links to the framework's; so do co-authors and reviewers.
- Paper 1 is the first: `papers/perspective/glossary.md`, also the source of a short definitions box in draft 2.

## Acceptance Condition

Accept when DR-027 is accepted (this DR links paper glossaries to `docs/glossary.md`, which DR-027 makes normative), Paper 1 has a glossary the maintainer approves, and the check fires on a seeded missing, empty and unedited-template file and passes on Paper 1.

## Open Questions

- Should the check also flag an abbreviation used in the manuscript but absent from the glossary ([#56](https://github.com/ducroq/agent-ready-papers/issues/56) proposes an acronym check)?
- Should it flag a framework term redefined in a paper's glossary in a way that contradicts `docs/glossary.md`, or is that left to review?

## Revisit If

- Glossaries turn into copies of `docs/glossary.md` (drift returns through duplication).
- The check is routinely silenced rather than satisfied.
