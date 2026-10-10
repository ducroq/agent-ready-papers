# DR-024: An Experiment Registry, Ported in Full from llm-distillery

---
status: Proposed
date: 2026-10-10
---

## Context

The framework places bets and tests them, but it keeps no record of what it concluded.

- **Open bets have a home.** `vv/hypothesis-log.md` and each paper's `hypothesis-log.md` pin a Method before the data lands, and resolved entries move to `vv/hypothesis-log-resolved.md`.
- **Concluded experiments do not.** Their evidence sits in reader-panel folders, issue bodies, session notes and DR sections. Their cost sits in `vv/cost-log.md`, apart from the result. No single place answers "did we ever test X, what did we decide, and what did it cost?"

On 2026-10-10, three experiments were waiting with nowhere to record their outcome:

1. **Cross-model review.** A review by a model from another vendor raised method-level problems in a full draft of a private narrative review. Two reviews and three rounds of a same-family reader panel had missed them. The bet that this repeats is open in that paper's hypothesis log, and it bears on DR-011's Pass 3.
2. **An outside fact-checking service tested on known errors.** ducroq/agent-ready-papers#51 reports 19 factual errors that passed V&V and were later confirmed against the sources. #51 gives their classes; the errors themselves are recorded in a private paper's reader-panel files. That makes them a test set for any checker, but one that can enter this public repo only as a summary (rule 5 below).
3. **DR-023's acceptance test** (H1, ducroq/agent-ready-papers#42), and the guard measurement asked for in ducroq/agent-ready-papers#41.

A sister project, llm-distillery, solved the same problem. Its solution is adapted from a third project, augur:

- an append-only `experiments/registry.jsonl`, one line per concluded experiment;
- a README that serves as the schema;
- `docs/evidence/<date>-<name>/` folders or files holding the analysis and the committed output, with a `PREREGISTRATION.md` for experiments that pin their test in advance;
- a checker script with unit tests. It validates the schema and the id order, checks that every artifact path exists, and checks that every metric in an entry appears in one of its artifacts.

The llm-distillery README records why the checker matters. Before augur added a checker, an audit there found 19 registry numbers that could not be traced to any artifact, and the fix was to automate the check. That figure comes from the llm-distillery README; this DR has not checked it in augur itself.

The checker is weaker than "verbatim" suggests. Read on 2026-10-10, it tests whether the metric's text occurs anywhere in an artifact, so a metric of `4` passes against any file containing a date. In a folder it reads only `.md`, `.txt`, `.json`, `.py` and `.jsonl` files. And it tests only that an artifact path exists on disk, so a gitignored file passes on the maintainer's machine and fails in every clone.

## Options Considered

| Option | For | Against |
|---|---|---|
| **A. Nothing new; keep using the hypothesis logs** | No new surface | A resolved hypothesis records a verdict, not the cost, the evidence files or the decision taken. No single place to search. |
| **B. Registry and README only, no checker** | Smaller; no new code | Repeats augur's defect: numbers in the registry drift from their evidence, and only an audit finds it. |
| **C. Full port: registry, README, checker, tests, evidence folders** | Tried in llm-distillery over 47 experiments. Traceability is checked by a script, not asked for. | About 400 lines of README, code and tests to maintain. One more V&V surface. The checker needs tightening first (Context). |
| **D. Ask agent-ready-projects for a template first, then adopt it** | One design for every adopter | Delays the three waiting experiments. The template is better written after a third adoption shows which parts are generic. |

## Proposed Decision

**Option C**, at framework level, with these adaptations. Then raise Option D upstream, using this port as the third adoption, and offer the checker fixes in rule 4 back to llm-distillery.

1. **Layout.**
   - `vv/experiments/registry.jsonl` holds the entries.
   - `vv/experiments/README.md` is the schema and the rules.
   - `vv/evidence/<date>-<name>/` holds the evidence.
   - The checker is `check_experiments.py` with `make check-experiments`. While this DR is Proposed it is staged in `extensions/` (rule 6); on acceptance it moves to `tools/`, and `make check` runs it. Its tests go in `tests/`.
2. **Keep from llm-distillery unchanged:**
   - the `EXP-NNN` ids;
   - the decision values (`kept`, `parked`, `rejected`, `rolled_back`, `superseded`);
   - the append-only rule: correct an entry by appending a new one that references it;
   - the rule that a metric must appear in an artifact, or be `null`;
   - the warning to ask the checker, not the prose;
   - preregistration before any result is seen.
3. **Adapt the fields.**
   - `oracle` becomes `judge`: who or what produced the verdicts (a reviewer, a model, a service).
   - `population` describes drafts, claims or registry rows, not datasets.
   - `spend_usd` covers model and API cost and stays a number, so totals can be summed. A new field, `cost_ref`, points to the entry in `vv/cost-log.md` for the same operation, or is `null`. It is a pointer only: the cost log records tokens, not dollars, and its rows have no ids, so the checker cannot compare the two.
4. **Tighten the checker** (the weaknesses in Context):
   - an artifact must be tracked by git (`git ls-files --error-unmatch`), not merely exist on disk;
   - a numeric metric must not match by accident. This DR does not fix the algorithm. The port must pass seeded tests in which each of these is the only occurrence and the metric does not match: `4` in "4 October", `41` in "#41" or "DR-041", `0.35` in "+0.350". It may reuse the identifier exclusions of `extensions/preservation_check.py`. How fractions ("76/83") and intervals are matched is an open question;
   - folders are also searched in `.tex` and `.csv` files.
5. **Leave out** what belongs only to llm-distillery: its GPU-host data rules and its production-site protocol. Keep the idea behind that protocol as one line in the README: preregister what the end reader will see, not only whether the gate passes.
6. **Public repo, private papers.** Evidence from a gitignored paper enters only as an anonymised summary in `vv/evidence/`, the way #51 describes its paper. Such a summary is written to contain its numbers, so the check that a metric appears in it is circular. To keep it honest:
   - the summary records the SHA-256 of each private file it draws on. This gives the maintainer tamper evidence, dated by the commit that added the hash. It gives no one else a check, since they cannot read the file, and it says nothing about whether the summary reports the source correctly;
   - the entry's `notes` say that its metrics trace to a private source, so a reader knows the check is circular for them.

   Experiments scoped to one paper stay in that paper's own hypothesis log, unless they test the framework.
7. **Staging.** Like DR-018 and DR-023, the checker is staged in `extensions/` while this DR is Proposed, with the `STATUS: PROPOSED` docstring and `--help` banner that `extensions/*.py` carries, and a `check-experiments` Makefile target (listed in `.PHONY`) that is not yet a prerequisite of `check`. The original design has run in llm-distillery, but the adaptations above have not run anywhere. Registry entries may be written during staging. Each time the checker is run on them by hand, its output is committed to the entry's evidence folder, so the run has a date and a commit.

## Consequences

- **First entries.** Experiment 1 above would be preregistered in `vv/evidence/` before the next full draft of that paper is reviewed, and its hypothesis would move from the paper's log to `vv/hypothesis-log.md`, anonymised. Experiments 2 and 3 follow if the maintainer decides to run them.
- **No backfill.** Past experiments are not retro-registered, because their evidence was not kept in a form the checker can verify.
- **`CLAUDE.md`** needs one row in *Before You Start*: "Concluding an experiment, or 'did we ever test X?'". The DR count in its verify comment changes from 23 to 24. Both are edits to `CLAUDE.md` and need the maintainer's approval.
- **`UPGRADING.md` and `CHANGELOG.md`** get an entry at the next release. Adopters are not required to do anything; papers may adopt the registry later (see Open Questions).
- **Cost:** about 400 lines to maintain, and, after acceptance, one checker run in `make check`. `make check` runs only ruff and pytest today, so the new target must be added as its prerequisite.
- **Risk:** the registry goes unused, because experiments end in a session without anyone registering them. Mitigation: `/curate` could ask "did an experiment conclude this session?". That skill is user-global, so it needs an issue at agent-ready-projects.

## Acceptance Condition

Accept when all of these hold:

1. The staged checker passes its tests, including seeded positives, each of which must make it fail:
   - an artifact that exists on disk but is gitignored;
   - a metric `4` whose only occurrence is inside a date;
   - each accidental match listed in rule 4.
2. Experiment 1 is preregistered, and its entry passes the checker, with the output committed as in rule 7.
3. The maintainer has read one entry end to end and could answer "what did we decide, and why?" from it alone.

## Evidence Base

- llm-distillery `experiments/README.md` (schema, rules, adaptations from augur), `scripts/verification/check_experiment_registry.py` (126 lines) and `tests/unit/test_experiment_registry.py` (134 lines), read 2026-10-10. Its registry held 47 entries that day. The checker's weaknesses in Context come from a review of that code on 2026-10-10.
- The augur audit of untraceable registry numbers, as reported in that README. Second-hand.
- This repo's waiting experiments: #41, #42, #51, and the cross-model review bet of 2026-10-10.

## Open Questions

- Should papers get their own registry (a `templates/` file), or should paper experiments stay in hypothesis logs?
- Should an entry be required before a hypothesis moves to *Resolved*? That would link the two logs, at the cost of one more step.
- Should the checker also confirm that each `references` id (issue, DR, hypothesis) exists?
- How should a metric that is a fraction or an interval ("76/83", "95% CI [...]") be matched against its artifact?

## Revisit If

- Six months pass with fewer than three entries: the registry is not earning its upkeep.
- agent-ready-projects ships a registry template; then adopt it and retire the local README.
- The checker's verbatim rule blocks legitimate entries often, for example numbers that a script computes and prints with different rounding.
