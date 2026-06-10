# Contributing

Thanks for your interest in `agent-ready-papers`. This repo holds a *methodology framework* for AI-augmented academic and structured non-fiction writing — templates, decision records, and active papers using the framework. Below: who this is for, what contributions are welcome, what is out of scope, and how to file useful issues.

## Three audiences

### For adopters

If you want to apply the framework to your own paper, decision-support artefact, or speculative-design work:

- Start with the [Quickstart](README.md#quickstart) in the main README.
- Copy `templates/CLAUDE.md`, `templates/claim-registry.md`, `templates/anti-hallucination.md`, and `templates/writing-guide.md` into your project. These four are the minimum-viable adoption.
- Pin your project's version in CLAUDE.md (e.g. `agent-ready-papers: v1.3.0`) and surface drift at session start.
- You are *not* expected to upstream changes. Local adaptations are normal and encouraged — the framework is designed to be forked into your project, not imported as a dependency.

### For collaborators

If you want to propose changes to the framework itself:

- **Open an issue first** describing the proposed change. Most framework changes are recorded as Decision Records (DRs); the issue triggers a discussion before the DR is drafted.
- The framework is *not* "design first, deploy later" — it is "apply, surface gaps, promote what survives." Pattern proposals that have not been applied somewhere are usually returned with a request for evidence.
- Check [`decisions/`](decisions/) to see whether your proposal touches an existing decision. DRs are binding; superseding one requires a new DR explicitly named as such.
- **Application reports** — where you applied the framework to a new domain and found something — are the most welcome contribution. Each such report has historically led to a DR or a template revision that other adopters benefit from.

### For issue filing

What makes a useful issue, roughly in descending order of signal:

- **Application reports** — "I tried the framework on X; here's what worked, what didn't, what surfaced." Highest signal. Drives the empirical evidence base.
- **Specific friction** — "Step Y in template Z confused me because A; suggested fix B." Concrete and reproducible.
- **Conceptual gaps** — "The framework doesn't cover situation P; here's why it might or might not warrant Q." DRs often start here.
- **Convergent external review** — independent reviewers landing on the same observation.

Less useful:

- "Is X supported?" — try it and report back as an application report.
- Open-ended "what about Y?" — specifics help; an example of the failure mode you're worried about helps more.
- PRs without a prior issue — most framework changes need a discussion first.

## What is in scope

- Framework changes — templates, DRs, audits, methodology.
- Application reports from new domains.
- Evidence: literature additions, audit findings, replication of empirical claims.
- Tooling that automates manual steps (see [#17](https://github.com/ducroq/agent-ready-papers/issues/17) for the scoped tooling work).
- Documentation and discoverability improvements.

## What is out of scope

- **PRs to active paper artefacts** (`papers/perspective/manuscript.tex`, `papers/perspective/references.bib`, etc.) without prior discussion. These are author-controlled work-in-progress and unsolicited changes are generally not merged.
- **Code generation for unrelated tools.** This repo is the *paper* framework; code patterns live in the companion [`agent-ready-projects`](https://github.com/ducroq/agent-ready-projects) repo.

## Licence

By contributing, you agree that your contribution is licensed under the same terms as the repo — **Creative Commons Attribution 4.0 International (CC BY 4.0)** — recorded in [`decisions/DR-013_license-choice.md`](decisions/DR-013_license-choice.md).

If you contribute substantial code (for example tooling scripts under [#17](https://github.com/ducroq/agent-ready-papers/issues/17)), the DR-013 *Revisit If* conditions may apply: flag it in your PR so the licence choice can be reconsidered before merge (a dual MIT + CC BY split is an explicitly-considered option in DR-013).

## Process

1. **Open an issue** describing the proposed change.
2. **Wait for triage** before investing in a PR. Some changes belong as DRs (discussion + decision before implementation), some as direct PRs.
3. **PRs should be focused** — one concern per PR, referencing the originating issue. Multi-concern PRs are commonly split before merge.
4. **PRs that modify templates may affect active papers** — call this out in the PR description so the impact on `papers/` can be assessed.
5. **Commit-message style** mirrors the existing convention:
   - Title with a scope prefix and a `(closes #NN)` footer hint.
   - Body explains *what* and *why*; use multiple paragraphs if the rationale needs it.
   - For multiple issues, repeat the keyword: `Closes #A. Closes #B. Closes #C.` (GitHub's parser is more reliable when each issue gets its own keyword.)
   - Co-authorship lines (e.g. `Co-Authored-By:`) are welcome if an AI tool helped draft.

## What this framework looks for in practice

If your application of the framework surfaces a recurring pattern the framework doesn't capture, that's the highest-value contribution. The framework's evidence base grows by application, not by speculation.
