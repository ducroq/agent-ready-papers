# DR-027: A Verification Model Grounded in Toulmin and Whetten

---
status: Proposed
date: 2026-10-16
---

## Context

DR-004 typed every registry entry as a CLAIM (source-checkable fact), an ARGUMENT (Toulmin-checked reasoning) or a PROPOSITION (a recommendation checked with Whetten's What/How/Why/Who-Where-When). Reviewing Paper 1's draft 1 on 2026-10-16, the maintainer (feedback point #16) and three of four model reviewers found that these names contradict their own sources, and the full texts confirm it ([Toulmin 2003](../literature/sources/toulmin-1958.md), [Whetten 1989](../literature/sources/whetten-1989.md), quotes verified with `tools/check_quotes`):

- **Toulmin's claim is any assertion**: "the claim which any assertion necessarily involves" (p. 90). DR-004's CLAIM is only one kind, and Paper 1's Table 4 shows a "Claim" row inside an ARGUMENT.
- **Whetten's proposition relates concepts**: "propositions involve concepts, whereas hypotheses require measures" (p. 491); they specify "the logically deduced implications for research of a theoretical argument" (p. 492). DR-004's PROPOSITION is a recommendation.
- **Whetten's checklist judges a contribution**, a theory paper as a whole ("What constitutes a publishable theory paper?", p. 494), not a single statement.
- **The types overlap**: one sentence can be a CLAIM and a premise of a PROPOSITION. What decides the check is what a statement rests on, not what kind of thing it is.

The maintainer judged that Toulmin and Whetten define these better than the framework does and chose a full rethink on their model, glossary first. The glossary (`docs/glossary.md`, draft) was reviewed by four models (ChatGPT, DeepSeek, Gemini, Claude Fable; the reviews are kept in the maintainer's work items, not shipped). All four rejected the first draft's three-kind classification ("primary justification") because "normative" describes what a claim says while "sourced" and "argued" describe what it rests on. The maintainer then chose two axes, "qualifier" for the hedge with "confidence tier" for the rating, and "grounds" as the term for what a claim rests on.

Scope of impact (measured 2026-10-16): parsing depends on the sub-table marker regex (`tools/coverage.py:65-71`, imported by `tools/check_registry.py:77`), the per-type schema (`check_registry.py:143-153`), and ID and anchor regexes that accept only `S<n>-<n>` (`check_registry.py:79-80,108-109,112`), so `check_registry` drops rows with other IDs silently today (`:268`) while `coverage` stops with an error on such a row if it has no Priority (`coverage.py:488`); about 360 uppercase type labels on 240 lines across templates, DRs and docs; 9 paper registries in this repo (8 gitignored) and about 38 files in other repositories. Under DR-017 this repo is custodian of the typed layer; `agent-ready-assessment` and `agent-ready-research` vendor it with provenance, and `agent-ready-projects` owns the generic concepts (including "Toulmin for ARGUMENTs").

## Options Considered

### Option A: Keep DR-004's types and names
- (+) No migration
- (-) Leaves the contradictions with Toulmin and Whetten in place, in a framework whose Paper 1 presents those authors as its grounding

### Option B: Rename the three types, keep the model
- (+) Smaller change: relabel markers, keep sub-tables
- (-) Keeps the overlap: the types still sort sentences, which the sources do not support; any three names mix "what it says" with "what it rests on"

### Option C: One unit, two axes (the glossary model)
- (+) Faithful to both sources; dissolves the overlap; checks follow from what is recorded instead of from a type the author picks
- (+) Gives theory papers a place for assumptions, definitions and values (the "declared starting points" all four reviewers found missing)
- (-) Changes the registry schema, both tools that parse it, every template that shows it, and every adopter's registry: a MAJOR release

## Proposed Decision

**Option C.** Terms as defined in `docs/glossary.md`, which becomes normative on acceptance.

### The model

1. Every statement the paper puts forward and supports is a **claim**. Two other things are registered alongside claims: **declared starting points** (adopted, not argued for) and, in speculative-design work, **provocations** (DR-010: they make no truth claim).
2. Each claim records **what it says**: `descriptive` or `normative`.
3. Each claim records its **grounds**, item by item, each typed: a **source** (what a cited work reports), another **claim** (joined by a warrant), or a **declared starting point** (an assumption, definition or value the paper adopts).
4. Checks follow the items: **source check** per source (two steps: it exists; it says what is attributed), with its Source Tier recorded; **warrant check** whenever a claim rests on other claims or combines several sources into a point none of them makes alone; every declared starting point stated explicitly with its contestedness recorded. A normative claim also needs **boundary conditions** and at least one declared value among its grounds.
5. Every claim carries a **qualifier** (the hedge in the sentence), which its **confidence tier** (DR-002's ESTABLISHED / SUPPORTED / EMERGING / SPECULATIVE) must permit. The tier values and their wording are unchanged.
6. Each **contribution** is a root claim: P0 by definition, with a confidence tier no higher than its weakest supporting claim, so it counts in DR-002's P0 floor. Consequence, stated deliberately: a contribution resting on any EMERGING or SPECULATIVE claim fails the floor, whatever that claim's own priority. The floor then applies to the paper's core, which is its purpose; a paper whose contribution rests on preliminary evidence says so, and the gate records it. It is checked once with Whetten's elements and questions (the **contribution check**, a validation step). The per-claim checks are **verification**.

**The dead-end gate.** `memory/dead-ends.md` (maintainer-local) rules out a new registry unit unless it is "a unit of the paper's argument" rather than "a check that runs alongside it", and names ASSUMPTION as a past candidate. Declared starting points pass that gate: they are premises the argument rests on, recorded so they can be seen and contested, and they receive no check of their own beyond being stated. Calculations (DR-009) do not pass it and stay a procedure.

### Registry schema (recommended)

Per paper, three tables:

- **Contributions**: `ID (C1…) | Contribution | Says | Rests on | What | How | Why | Who/Where/When | Objections engaged | Priority | Confidence tier | Status`. Rests on lists `claim:` and `decl:` items (a normative contribution names its value there); Priority is always P0, kept as a column so the tools need no special case.
- **Declared starting points**: `ID (D1…) | Statement | Kind (assumption / definition / value) | Contestedness (accepted / contested / own) | Status`
- **Claims**, per manuscript section: `ID | Statement | Says | Grounds | Warrant | Backing | Rebuttal | Objections engaged | Priority | Confidence tier | Source Tier | Status`, where Grounds lists typed items: `src: Author Year`, `claim: S1-2`, `decl: D1`, semicolon-separated. For a normative claim, Rebuttal holds its boundary conditions.

Columns that do not apply stay empty: Warrant when every source supports the claim on its own; Backing when the audience accepts the warrant. Source Tier F ("logical inference") has been used for two different things, as the Paper 1 trial migration showed: an inference from other claims (on migration it becomes a Warrant over `claim:` or `decl:` grounds) and the author's own observation or experiment (it becomes own work, Source Tier E). Tier F is retired. Declared starting points carry no priority and no confidence tier: they are excluded from coverage and the P0 floor and reported separately (stated / not stated in the text). Tier monotonicity runs over `claim:` grounds, as today; `src:` grounds feed a claim's tier through DR-002's assignment rule. A claim resting on a *contested* starting point must say so in its text (Step Z). PROVOCATION (DR-010) keeps its own sub-table: a provocation "makes no truth claim", so it is not a claim in this model. Calculation verification (DR-009) stays a procedure applied to claims whose grounds include a computation, consistent with the standing dead-end against a fourth unit type.

The alternative considered: keep per-section sub-tables keyed by grounds kind. Rejected because a claim with mixed grounds (the common case the reviewers named) would have no single home.

### Tools

- `tools/coverage.py`: reads the Claims, Contributions and Declared tables; coverage by priority, by Says and by grounds type; P0 tier floor unchanged.
- Both tools: ID and anchor regexes accept `C<n>` and `D<n>` as well as `S<n>-<n>`, so contributions and declared starting points can be anchored in the manuscript and are never dropped silently; a row whose ID matches no pattern is reported, not skipped.
- `tools/check_registry.py`: schema rules for new-schema tables: a claim with `claim:` grounds needs a Warrant; a normative claim needs a Rebuttal (boundary conditions) and a `decl:` value; every `claim:`, `decl:` and Rests-on reference must resolve; premise graph and tier monotonicity over `src:` and `claim:` grounds; a contribution's tier may not exceed its weakest supporting claim. Anchor comments keep three fields: `% S1-1: label (descriptive, P0, SUPPORTED)`, `% C1: label (contribution, P0, EMERGING)`; the tool reads the last field as the tier, as before. Declared starting points are anchored as `% D1: label (value, contested)` and get no tier comparison. A claim combining several sources is not forced to have a Warrant by the tool until the synthesis question below is settled.
- **Aliases through v5.x**: registries using `**CLAIMs:**`, `**ARGUMENTs**`, `**PROPOSITIONs**` are read as before, **checked under DR-004's rules** (the new schema rules apply only to new-schema tables), and reported under their old labels with a deprecation note in the output (new-schema rows report as descriptive, normative or contribution). Removal no earlier than v6.0.0, announced in UPGRADING. Migration maps the old columns: CLAIM Source → `src:` grounds (a Tier-F source becomes a Warrant or own work, as above); ARGUMENT Grounds → `claim:` grounds, Warrant, Rebuttal and backing citation (Source) → their own columns; PROPOSITION Premises → `claim:` grounds, Relationship and Reasoning → Warrant, Boundary conditions → Rebuttal, Alternatives engaged → Objections engaged, Constructs → `decl:` definitions; and the PROPOSITION gains a declared value.
- Tests seed positives for each rule, the alias path, and the schema check on mapped rows (guarding the silent `.get()` skip found at `check_registry.py:663`).

### Amendments to other DRs (on acceptance, an "Amended by DR-027" line in each, no rewrite of accepted text)

- **DR-004**: its three types are superseded by this model; its per-type checks survive as the source, warrant and contribution checks.
- **DR-002**: "tier" is named **confidence tier**; values and wording unchanged; its P0 floor now also covers contributions. Its source-counting assignment rule is the framework's own (Toulmin p. 35: terms of assessment travel across fields, the criteria may not) and is due its own review; this DR does not change it.
- **DR-009**: calculation verification applies to claims whose grounds include a computation; unchanged in substance.
- **DR-012**: its applicability test ("at least one central PROPOSITION") reads "at least one central normative claim or contribution".
- **DR-010, DR-017**: references updated; DR-017's custody now covers this model.
- **DR-015** (Proposed): its sub-typing of the ARGUMENT Rebuttal field moves to the Claims table's Rebuttal and Objections columns.

### Other repositories

`agent-ready-assessment` and `agent-ready-research` re-vendor at v5.0.0 on their own schedule. An issue on `agent-ready-projects` proposes aligning its generic vocabulary ("Toulmin for ARGUMENTs") with the glossary; this DR does not depend on it.

## Consequences

- Authors no longer sort statements into types; they record what a claim says and type each item it rests on, and the checks follow.
- With contributions in the P0 floor, every claim a contribution rests on must reach SUPPORTED for the floor to pass (see model step 6).
- Theory and perspective papers can register assumptions, definitions and values instead of forcing them into CLAIM rows.
- A MAJOR release (v5.0.0) under the versioning rules in `CHANGELOG.md`: required registry structure changes. Existing registries keep working through the alias period.
- Every template, `README.md`, `docs/framework-summary.md`, `docs/THRESHOLDS.md` and `tools/README.md` change; Paper 1's registry (also the test fixture) migrates in the same commit as the tools.
- Paper 1 draft 2 is written in this vocabulary, as the first paper to use it.

## Acceptance Condition

Accept when all hold:

1. `docs/glossary.md` approved by the maintainer.
2. Paper 1's registry and one gitignored paper's registry migrated by hand to the recommended schema, **as copies** (Paper 1's tracked registry is the test fixture and migrates only with the tools), and the maintainer judges the result clearer than the DR-004 version.
3. A tools prototype reads both migrated copies and an unmigrated registry (alias path). Coverage and P0-floor results match before and after migration, or every difference is explained by the migration itself (a contribution entering the floor, a Tier-F source becoming a warrant).

## Open Questions

- Should the contribution check become a named gate (e.g. inside Gate 3), or a section of the review prompt?
- DR-002's counting rule: what replaces "count agreeing independent sources" for argued claims, whose strength is the warrant's? (A later DR.)
- Does a migration script (`tools/registry_edit.py` or a new one) pay for itself across ~10 registries, or is a written procedure in UPGRADING enough?
- How does a warrant check recognise a synthesis of sources (several `src:` items jointly) as opposed to independent corroboration? The author marks it, or every multi-source claim gets a Warrant cell?
- Should a contested declared starting point cap the tier of claims resting on it, rather than only requiring that the text say so?

## Revisit If

- Authors misclassify grounds items as often as they misclassified DR-004 types (the problem this DR exists to remove).
- The alias path is still in heavy use at v6.0.0.
