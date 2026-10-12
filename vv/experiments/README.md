# Experiment Registry

This folder records, under DR-024, what the framework tested, what it decided, and what it cost. The entries are in `registry.jsonl`, one JSON object per line. This README is the schema and the rules. It holds no entries, so to find an experiment, ask the checker or search the registry, never this file:

```bash
make check-experiments                                          # entries, metrics, open preregistrations
command grep -o '"id": *"EXP-[0-9]*"' vv/experiments/registry.jsonl | tail -5
```

Adapted from llm-distillery's `experiments/README.md`, which adapted it from augur. DR-024 lists the changes.

## Where things go

| Place | What it holds |
|---|---|
| `vv/hypothesis-log.md` | A bet while it is open, with its Method fixed in advance |
| `vv/evidence/<date>-<name>/` | The evidence: `PREREGISTRATION.md`, the analysis, the committed checker output |
| `vv/experiments/registry.jsonl` | One line per experiment: what was asked, what was decided, what it cost, and where the evidence is |
| `vv/cost-log.md` | Token counts per operation; an entry points to its row with `cost_ref` |

## Numbers live in the evidence, not here

Every metric in an entry must appear in a file the entry cites, or be `null`. The checker enforces this. The file must be tracked by git, and the number must stand alone: `41` does not match `#41`, and `4` does not match `4 October`. A `PREREGISTRATION.md` and the checker's saved output (`check-*.txt`) are never searched, and neither are commit messages. An entry that is not `preregistered` needs at least one metric that is not `null`. Write a metric exactly as the evidence prints it. If a script prints `0.350`, the metric is the string `"0.350"`, not the number `0.35`. Write a fraction such as `"76/83"` as a string. A number that cannot be recovered is `null`, with the reason in `notes`.

## Schema

| Field | Type | Notes |
|---|---|---|
| `id` | string | `EXP-NNN`, in ascending order, never reused |
| `date` | string | ISO date the experiment was concluded, or preregistered for a `preregistered` entry |
| `title` | string | One line |
| `hypothesis` | string | What was asked, and why it matters |
| `subject` | string | What was under test: a prompt, a template, a review step, a checker |
| `judge` | string or null | Who or what produced the verdicts: a reviewer, a model, a service |
| `branch` | string | Where the work was committed |
| `commits` | array of strings | Hashes (7 to 40 hex characters); each must exist. Their messages are not evidence |
| `spend_usd` | number or null | Model and API cost. `0` means no paid calls, and is a claim a reader can check |
| `cost_ref` | string or null | The matching row in `vv/cost-log.md` (by date and operation). A pointer only: the checker does not compare the two |
| `population` | object | What was measured: drafts, claims, registry rows; exclusions. `{}` if none |
| `metrics` | object | The headline numbers. Each value is a number, a string, or `null` |
| `decision` | string | See below |
| `decision_rationale` | string | One or two sentences |
| `artifacts` | array of strings | Tracked paths inside `vv/evidence/<date>-<name>/` that hold the evidence |
| `references` | array of strings | Issues, DRs, hypotheses, and the `EXP-NNN` an entry concludes or corrects |
| `review` | string or null | Which review passes ran on the result, and what they found |
| `notes` | string, optional | Caveats, confounds. Say here when the metrics trace to a private source |

**Decision values.** `kept`: adopted. `parked`: works, not adopted. `rejected`: does not work. `rolled_back`: adopted, then reverted. `superseded`: replaced by a later approach. `preregistered`: written before any result was seen. A `preregistered` entry has no metric values, cites a `PREREGISTRATION.md`, and stays open until a later entry names its id in `references`.

## Rules

1. **Preregister before any result is seen.** Commit `vv/evidence/<date>-<name>/PREREGISTRATION.md` and a `preregistered` entry. Say what the end reader will see if the result holds, not only whether a test passes.
2. **Append only.** To correct or conclude an entry, append a new one that names it in `references`. Editing in place destroys the record of what was once believed.
3. **Run the checker and commit its output** (DR-024 rule 7). Stage the evidence first (`git add`), since the checker reads only tracked files. Save the output in the entry's evidence folder as `check-<date>.txt`, so the run has a date and a commit. `make check` also runs it.
4. **Private papers** (DR-024 rule 6). Evidence from a gitignored paper enters only as an anonymised summary in `vv/evidence/`. The summary records the SHA-256 of each private file it draws on, and the entry's `notes` say that its metrics trace to a private source. For a reader without that file, the metric check is circular.
5. **Scope.** Experiments that test the framework go here. An experiment that concerns one paper only stays in that paper's hypothesis log.
