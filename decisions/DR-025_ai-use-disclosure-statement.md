# DR-025: An AI-Use Disclosure Statement as Framework Output

---
status: Proposed
date: 2026-10-12
---

## Context

The framework verifies whether a text holds. It produces no statement telling a reader how AI was used, or what was checked. Paper 1, a paper about AI-assisted writing, has an Acknowledgements section reading `[To be added.]` and no AI-use statement.

The four publisher and standards-body policies the framework has read judge disclosure, not detector scores ([L77–L80](../literature/sources/detector-policies-2026.md); Science, Wiley, T&F and IEEE were not read):

- **ICMJE §V.A:** authors disclose AI use at submission and describe how it was used. Nondisclosure "may be construed as misconduct in some circumstances".
- **COPE:** authors disclose which tool was used and how, and are fully responsible for the content.
- **Elsevier:** a separate AI declaration, published with the article.
- **Springer Nature:** a high AI-text score triggers a human check.

ICMJE and COPE do not mention detectors, Elsevier names none, and Springer Nature uses a score only to trigger a human check. The README's detector FAQ already tells adopters to "disclose AI use the way your target journal asks" and to keep the registry as their answer to a flag, but the framework has no statement that carries that record to the reader.

Trigger (2026-10-12): on 2026-09-26 the maintainer ran Pangram on two of their own texts, both written in heavy collaboration with AI by the same process. A short bullet-point text scored "100% human", a long-form chapter "100% AI" (n=1, recorded in a maintainer-local work item). A style score could not tell two texts from the same process apart. The maintainer asked whether a fixed sentence, "Ideas, structure and judgement are mine; AI drafted and rephrased; every claim was verified", should be part of every output.

## Options Considered

| Option | For | Against |
|---|---|---|
| **A. Nothing; leave disclosure to each journal's form** | No new surface | Adopters write it from memory, and the verification record the framework holds never reaches the reader |
| **B. One fixed sentence in every output** | Zero effort per paper | The roles differ by paper, so for some adopters it is false. "Every claim was verified" overstates: verification covers registered units only, prose can carry unregistered ones, and the tools check consistency, not that a tier is right. That breaks the framework's own calibration rule |
| **C. A fill-in statement with three slots, the third filled from tool output** | True by construction where it can be; the verification record is what a detector score cannot give | One more pre-submission step; the author must still write the roles slot honestly |

## Proposed Decision

**Option C.** Before submission, every paper produces an AI-use statement with three slots.

1. **Roles, written by the author.** Who originated the ideas, the structure and the judgements, and what the AI did (drafting, rephrasing, source search, checking). Only the author knows this, so no tool fills it.
2. **Tools.** The models and services used, and for which tasks.
3. **Verification record, copied from tool output, never written from memory.** The registry counts from `make coverage`, the source checks from `make check-dois` / `make verify-bib`, and **any failing gate, stated as failing**. Each number is quoted from the run it came from, with the run's date.

The statement goes where the target journal asks for it (methods, acknowledgements, or a separate declaration) and follows its format; the three slots set the content, not the form.

**Wording rules.** The tier language rules apply to the statement itself. "Verified" names what was checked and for which unit type (factual claims against sources, arguments and propositions for premises and reasoning, per DR-004), never "every claim". Name a passing gate only by the check that ran.

**Placement in the framework.**

- `templates/CLAUDE.md`: a pre-submission step, "Write the AI-use statement (DR-025)".
- `templates/writing-guide.md`: the three slots, the wording rules and the worked example below.
- No new tool. Slot 3 is filled by copying the output of commands that already exist. A generator waits until the copying proves error-prone (Revisit If).

### Worked example: Paper 1, slot 3 (from `make coverage` and `make check-dois`, 2026-10-12)

> The paper's claim registry holds 17 entries. All 15 factual claims are marked verified against their sources; the 1 argument and 1 proposition are marked verified for their premises and reasoning. All 20 DOIs in the registry resolve. Three of the six highest-priority entries are tiered below SUPPORTED, so the paper does not pass its own gate for those entries. The registry is available at [URL].

Slots 1 and 2 for Paper 1 are the maintainer's to write.

## Consequences

- A reader, editor or detector-flag reviewer gets a record of what was checked, which a style score cannot provide.
- A failing gate becomes visible outside the repo. For Paper 1 this is the P0 floor, so the statement and the manuscript sentence stating the gate result (Paper 1 `backlog.md`) should agree.
- Adopters gain one pre-submission step. Its cost is expected to be small, because slot 3 is copied, not composed.
- The framework does not tell adopters how much AI use is acceptable; that stays with the journal.
- Scope versus DR-001, which places publisher disclosure at the policy level and the framework at the process level: the framework now supplies the content of a disclosure, while its form and its judgement stay at the policy level.
- If a declared-exception rule for the P0 floor is accepted, Paper 1's gate result may change; the same-date rule in the Acceptance Condition keeps the example honest.

## Acceptance Condition

Accept when both hold:

1. Paper 1's statement is written with all three slots, and each number in slot 3 matches a tool run of the same date.
2. The maintainer has read it and judges that slot 1 says what they would say to an editor who asked.

## Open Questions

- Should slot 3 also report the readability and reader-panel passes where a paper ran them (DR-022, DR-023)?
- Should DR-010 and DR-012 artefacts (essays, decision-support documents) use the same statement, with no journal to set its form?

## Revisit If

- A slot-3 number is found to disagree with its tool run: build the generator.
- A publisher policy starts naming detector scores as a basis for judgement.
- Adopters leave slot 1 as boilerplate: the roles slot is not doing its job.
