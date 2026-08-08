# Verification Hooks

## Status

**SPECULATIVE on the benefit, concrete on the mechanism.** Which commands this repo can wire, and how each tool wires them, are checkable facts. The claim that closing the edit → check → fix loop *reduces* correction cost has not been measured here; it is a working position, held for the reason given below. Treat the tool table as the part to verify against current docs — this area moves fast.

Adapted from [agent-ready-projects](https://github.com/ducroq/agent-ready-projects) v1.14.0 (`docs/GUIDE.md`, *Verification Hooks*), narrowed to the checks this repo actually ships.

## What a verification hook is

A session hook orients the agent at the start of a session. A **verification hook** closes the loop at the other end: it runs a check after an edit and puts the result back in front of the agent.

The difference is who carries the error message. Without a hook, the agent edits, stops, and waits; you run `make coverage`, read the failure, and paste it back. With one, the agent edits, sees the failure, and fixes it while the reasoning that produced the mistake is still in context.

This is the same division of labour as the rest of the framework: **deterministic checks catch what a rule can decide, and the agent's judgment is reserved for what a rule cannot.** `tools/coverage.py` can decide whether P0 coverage is 100%. Nothing mechanical can decide whether a sentence's confidence tier exceeds its evidence — that is Step Z, and it stays a human-and-agent pass.

Point any hook at the commands already documented for the project. If the hook runs one command and the docs name another, there are two sources of truth for "how do I check this," and the agent will believe whichever it read most recently. In this repo that means `CLAUDE.md`'s *How to Work Here* block and the `Makefile` together — the block currently documents the `tools.coverage` and `check_dois` invocations but not `make lint` / `make test` / `make check`, so the two surfaces are already out of step and the block is the one to extend.

## What is worth wiring in this repo

The test is whether the output is **fast, diagnostic, and actionable**.

| Command | Verdict | Why |
|---------|---------|-----|
| `make lint` (`ruff check tools/ tests/`) | **Good** — wire it | Sub-second, names file and rule, fixable in place |
| `make test` (`pytest tests/ -x -q`) | **Good** — wire it | Small suite, failure output names the assertion |
| `python -m tools.coverage <registry> --strict` | **Good** — wire it, scoped to registry edits, **and assert the report is non-empty** | Fast, and the failure is exactly the thing a registry edit can break. Note `make coverage` runs *without* `--strict` and cannot fail on thresholds — wire the explicit command, not the target |
| `python -m tools.check_dois <registry> --offline` | **Good** — wire it | Catches malformed DOIs without touching the network |
| `python -m tools.check_dois <registry>` (online) | **Poor** | Sequential HEAD requests against doi.org; no proxy support. Run it deliberately, not per-edit |
| `pdflatex` × 3 + `bibtex` | **Poor** | Slow, and its failure output is a wall of TeX noise an agent will misread |
| Simulated peer review (`agents/review-prompt.md`) | **Poor** | Minutes, non-deterministic, judgment-shaped. This is a gate, not a hook |
| The anti-hallucination checklist | **Poor** — and deliberately so | Step 6 is a human-in-the-loop anchor by design. A hook here would automate away the thing the checklist exists to preserve |

A slow check does not merely waste wall-clock. It burns context on output the agent cannot act on, and it trains you to disable the hook.

## The test that catches most of it

Before the three failure modes below, one question subsumes a lot of them:

> **Can I tell this check working apart from this check being absent, by looking at its output? If not, make it print a count.**

Every silent failure in this document is an instance. A hook whose config is untracked, a glob that matches nothing, a gate that exits 0 over zero rows, a test asserting `all(...)` over an empty list — in each case the broken state and the healthy state produce byte-identical output, so no amount of watching the output distinguishes them. A count is the cheapest thing that does: *checked 19 claims*, *examined 0 files* — the second one reads as broken at a glance, where a bare green does not.

Two corollaries worth applying to any gate, not just hooks:

- **Assert non-emptiness wherever zero items is not a legitimate state.** This repo cannot legitimately have zero registry entries or zero decision records; a check that passes over them has not run.
- **A vacuous pass is a distinct outcome from a pass.** If your check can return clean over nothing, give it a third exit state, or an explicit count, or both.
- **A zero is a diagnosis, not something to whitelist.** The obvious objection to printing counts is that you will accumulate legitimately-zero cases and start suppressing them. Where this has been tried, that is not what happened: of two zeros surfaced, one was a glob that could never be non-zero and should simply not have existed, and the other *looked* legitimate and was in fact the bug — whitelisting it would have permanently blessed a rule that skipped four directories. **A zero tells you the pattern is either wrong or unnecessary, and you have to work out which.** That is a step of work, not a suppression.

*(Formulated by the agent-ready-research session, 2026-08-08, after running the mechanism-enumeration below over an 8-rule lint suite. Adopted here because the framing is more general than the instances that produced it.)*

## Finding the unguarded doors

When you write a constraint to protect a check, enumerate **mechanisms, not intents**. Intents are unbounded and you will only list the ones you happened to imagine; mechanisms are bounded and readable straight off the code.

Concretely: find the places where your checker decides an item is *not counted* — a `continue`, a `None` return, a header or path lookup that misses, a glob — and write one clause per branch. Then **execute each one** rather than reasoning about it.

This was derived here from `tools/coverage.py`, where four branches drop an item from the denominator and three were unguarded; the one intent this repo *had* guarded against turned out not to work at all.

**Where to look first: wherever a check discovers its own inputs.** The general form is broader than a glob: **any place a check decides what it is about, using a fact it did not derive from the thing it is checking.** A line number ("frontmatter starts on line 1"), a hardcoded path list ("these are the directories the rules cover"), a `pwd -P` prefix strip ("the logical path equals the physical path"), a column-header lookup ("the bucket column is called `Priority`") — all the same failure, and all invisible in the output. Where a check is instead *handed* its inputs (a pinned fixture, an explicit argument), it has fewer such surfaces.

**Fewer is not none, and this repo is the example.** Its pytest suite is fixture-pinned and the enumeration over it found no real defect — but `tools/coverage.py` has a discovery surface and it **fails open**: the sub-table header lookup decides what the tool is about, and when it misses, the whole sub-table is skipped and the report comes back with zero rows and `meets_targets: True`. That instance is three paragraphs below, in the gaming table. So the honest reading of the negative result is *the leading-bytes surface is absent here* — CRLF and BOM were tested and are clean — **not** *the class is absent here*. A count of discovery surfaces is the useful number; the suite has almost none and the tool has one, and the one it has is unguarded.

Two claims come out of this and they have very different strength, so they are stated separately:

- **A seeded-defect harness cannot find a discovery failure.** This is true *by construction*, not by observation: a seeded defect is handed to the checker, so the harness only ever exercises the handed path. A suite can pass every seeded case and still never look at whole directories. Rely on this one.
- **"Never evaluated" outnumbers "evaluated but weakened."** Observed 10-to-0 across two suites in one estate on one afternoon, both self-reported, with the two counts collected by different people using different instruments. That is suggestive and nothing more — it has not been tested on a fixture-pinned suite, which is precisely where the first bullet predicts it should *not* hold. **Do not plan around this number.**

The distinction matters because the two invite different actions: the first justifies adding a discovery-enumeration step to any check you own; the second would justify prioritising it over other review effort, and it is nowhere near strong enough to carry that.

## Three failure modes

**The silent hook.** If the check's output never reaches the agent's context, it teaches nothing and costs time. This is the *default* behaviour on at least one major tool. Before trusting a hook, break something on purpose and confirm the agent reacts.

**That last sentence is not sufficient, and it is worth knowing why.** A sibling project's hook DR prescribed exactly it; the check was run, and it **passed** — on the physical repo path, with an in-scope file. The hook nonetheless had two silent no-op paths: a scope list omitting six directories, and a `pwd -P` prefix strip that failed on a symlinked repo path, which would have made the hook exit 0 on every edit forever. Both lay outside the single path the verification exercised. So the rule needs its companion clause:

> **Does my verification of this check exercise more than one path through it?**

A one-path verification of a multi-path mechanism reports the same green as a working one. For a hook, the paths worth breaking separately are at minimum: an in-scope file, an out-of-scope file (should stay silent), a file in a directory you *believe* is in scope, and the repo reached by a different path than usual — a symlink, a worktree, a different working directory.

There is a second, sneakier version: **the hook config itself is gitignored.** A sibling project wired a `PostToolUse` hook and found its `.gitignore` had `.claude/*` with allowlist exceptions for some subdirectories but not `settings.json` — so the hook was local-only while the decision record claimed it was committed. It fails silently and is byte-identical in behaviour, for the author, to a working setup; only a collaborator (or a fresh clone) discovers it. **This repo has the same exposure in its strongest form:** `.gitignore` line 1 is a bare `.claude/`, so any `settings.json` written here is invisible to git with no exception to notice. After wiring a hook, run `git check-ignore -v .claude/settings.json` and confirm the file is actually tracked.

One data point on whether hooks earn their slot, from the same project: a structural-lint hook fired **four times during the session that adopted it, and each firing was a genuine defect rather than noise.** That is n=1, on a different repo, self-reported — not a measurement of this framework. It is included because the *method* generalises: a hook that fires only on real defects and a hook that never fires look identical from the outside, so counting the firings and classifying each one is the cheapest way to tell a working hook from a decorative one.

**The green-at-any-cost loop.** An agent told to make a check pass will sometimes weaken the check. In this repo that has a specific and dangerous shape: **the cheapest way to make `--strict` pass is to remove the failing claim from the count.** Coverage goes green and verification has been quietly gutted — the exact failure the framework exists to catch, produced by the framework's own tooling.

The routes were measured against `papers/perspective/vv/claims/claim_registry.md` with one P0 claim flipped to unverified (baseline: `--strict` exits 1):

| Edit | Result | Why |
|------|--------|-----|
| Reclassify the claim P0 → P2 | **exit 1** — still fails | `meets_targets` checks *every* bucket; re-tiering moves the failure rather than hiding it |
| Delete the row | **exit 0** — passes | the claim leaves the denominator |
| **Blank the Priority cell** (delete two characters; the row stays, still marked `[ ]`) | **exit 0** — passes | `coverage.py` skips rows with no bucket |
| **Rename the `Priority` column header** | **exit 0** — passes | the whole sub-table is skipped, and the report comes back with zero rows |

The two most dangerous are the last two, because the claim is still visibly sitting in the registry marked unverified while the tool reports green. Note that the obvious attack — downgrading a tier — is the one that *doesn't* work here; a constraint written only against downgrading would guard the wrong door.

If you wire the coverage hook, add the matching Hard Constraint to `CLAUDE.md` the same day, not after you find the first vanished claim:

> No edit removes a claim from the count in order to make a coverage check pass — not deleting the row, not blanking its Priority or Status cell, not renaming a sub-table header, not diluting a bucket with filler. If the threshold is wrong, say so and stop.

**A zero-row report is a failure, not a pass.** `--strict` over a registry whose sub-tables no longer parse returns exit 0, because every threshold is vacuously met over nothing. Any hook wired to this command should also assert the report is non-empty — otherwise the check that examines nothing is indistinguishable from the check that passes.

The same shape applies to `tests/` — a test rewritten to match new behaviour is a removed guarantee, not a refactor.

**The tightened leash.** A hook firing on every write turns drafting into a stop-start crawl. Scope it: registry checks on `papers/*/vv/claims/**`, lint and tests on `tools/**` and `tests/**`, nothing on `manuscript.tex` or `memory/**`.

## What to do with what it catches

A hook failure the agent fixes in ten seconds is a typo, not knowledge, and should leave no trace. A hook failure that **surprised you**, or that you have now seen twice, is a `memory/gotcha-log.md` entry — 2-3 lines, the lesson and the action. The hook produces the raw signal; `/curate` decides what is worth keeping.

## Tool support

Verify against your tool's current documentation before relying on any row.

| Tool | Mechanism |
|------|-----------|
| Claude Code | `PostToolUse` hook matched on the edit tools, in `.claude/settings.json` (committed), `.claude/settings.local.json` (local), or `~/.claude/settings.json` (all projects). **The exit code is the whole mechanism:** on exit 0 the command's stdout goes to a debug log the agent never sees. Exit 2 writes stderr back to the agent as actionable feedback. A `type: "prompt"` hook with `continueOnBlock: true` covers cases where the pass/fail call needs judgment. For "don't stop until it's green," a `Stop` hook fits better than a per-edit one. |
| Aider | `auto-lint` / `lint-cmd` and `auto-test` / `test-cmd` in `.aider.conf.yml`; errors are fed back to the model. Note the asymmetric defaults — linting is on, testing is not. |
| Cursor | Has an edit-time hook mechanism; check current docs for the event name and config location. |
| Copilot CLI, Continue, web chat | No verification-hook mechanism to rely on at time of writing. Put the command in the project file as an explicit instruction and accept that compliance is probabilistic. See [`non-claude-setup.md`](non-claude-setup.md). |

That last row is the honest position: **an instruction is a request; a hook is a guarantee.** Where your tool gives you the guarantee, take it. Where it doesn't, the instruction is still worth writing — it just isn't the same thing.

The Claude Code row is the cautionary one. The obvious configuration — run the check, let it exit however it exits — is precisely the silent hook above. It looks wired up, it runs on every edit, and it feeds the agent nothing.

## Why this repo ships no hook configuration

`.claude/settings.json` is not committed here, and no hook is prescribed. Two reasons. The registry path a coverage hook must match is per-paper (`papers/perspective/vv/claims/claim_registry.md` today), so a shipped matcher would be wrong for every adopter. And the green-at-any-cost risk above means wiring the coverage hook is a decision that should be made deliberately, alongside its Hard Constraint — not inherited silently from a template.

Note the difference between *not committed* and *cannot be committed*. Right now no `settings.json` exists, so nothing is silently broken; but `.gitignore` line 1 ignores `.claude/` wholesale, so the moment someone writes one it is untracked by default. **If you decide to commit a hook config here, add the allowlist exception in the same change** — `.gitignore` is a HIGH-tier path in `/review-changes` for exactly this reason.
