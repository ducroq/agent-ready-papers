<!-- Anonymised copy (2026-11-15): the essay's author, title, site, coined terms and the planted sentences built from its wording are replaced by descriptions. Paths below are relative to the off-repo experiment folder, and the ANALYSIS.md named below is published here as SUMMARY.md. Otherwise identical to the file written before the runs, whose SHA-256 is in SUMMARY.md (Provenance). -->

# Preregistration: does the framework's rule set find more than a competent plain review prompt?

Written 2026-11-15, before any run of this experiment. Not edited after the runs; deviations go in ANALYSIS.md.

## Question

On a well-written, sourced non-fiction essay, does a reviewer prompted with the agent-ready-papers rules (Step Z tiers, Toulmin grounds/warrant, normative boundary conditions, calculation recompute, scope drift, Whetten contribution check) find more **planted** faults, at equal or better precision, than the same reviewer prompted with a competent plain review prompt?

## Subject and limits (stated in advance)

- Tested: **the framework's rules used as a reviewer prompt** (the DR-011 blind-pass use). Not tested: the full process (registry + source checks), because reviewers run text-only. Source-dependent faults are included to measure what text-only review misses in *both* arms.
- The baseline is deliberately strong: the plain prompt names the categories (factual, unsupported, citation, calculation, argument, overclaiming). A weak baseline would flatter the framework.
- The essay was already reviewed by the framework yesterday. The planted faults were written by the same agent (Claude) that scores, which is a known bias. Mitigation: a fixed answer key (below) and blind scoring on shuffled file names.

## Materials

- `inputs/original.txt`: a published Dutch-language essay on the energy use and climate value of AI (2026, about 3,000 words, 10 references), text extracted 2026-11-14.
- `inputs/seeded.txt`: the same text with 7 planted faults (answer key below). No other changes.
- `inputs/prompt-framework.md`: identical to the 2026-11-14 review prompt.
- `inputs/prompt-plain.md`: same output format, length cap, no-web and language instructions; the framework rules replaced by one category sentence.

## Answer key: planted faults

| ID | Stratum | Fault | Planted text (gist) |
|----|---------|-------|---------------------|
| P1 | source-dependent | Fabricated citation (DOI 404 checked 2026-11-15) | (an "independent replication" reporting 0.31 Wh per prompt, cited to a fabricated ref 11 with an invented journal article and a DOI that does not resolve) |
| P2 | source-dependent (weakly text-detectable: 0.3 g for 0.24 Wh implies ~1.25 kg/kWh) | Number changed vs source: 0.03 → 0.3 g CO₂e | (the per-prompt CO₂e figure given tenfold) |
| P3 | source-dependent (weak textual hint: ref 8's title is about Jevons) | Attribution error: IEA 1,400 Mt scenario attributed to Luccioni et al. [8] | (the avoided-emissions scenario sentence with its subject changed to the ref-8 authors) |
| P4 | text-detectable | Calculation error in a worked example | (amortisation example: the 10× larger-usage case given 10× too small) |
| P5 | text-detectable | Overclaim, contradicts own caveats | (a sentence claiming the comparison proves AI is now more efficient than search) |
| P6 | text-detectable | Ungrounded empirical claim | (a claim that over 40% of search traffic now goes through generative answers) |
| P7 | text-detectable | Warrant fault: scenario → certainty, ignores the barriers and rebound just stated | (a sentence concluding from the scenario that AI's net climate benefit is certain) |

Secondary key: native issues found 2026-11-14 (report findings #1–#9): N1 boundary asymmetry (src-dep), N2 hidden retrieval input, N3 savings claim for the author's own technology unsourced, N4 the proposed normative duty: warrant/value, N5 the proposed ratio metric: how/novelty, N6 "laat zien", N7 "beloont", N8 convergence claim, N9 efficiency formula.

## Design

- Arms: FRAMEWORK vs PLAIN. Reviewers: Codex CLI and Mistral Vibe (both headless, text-only, essay embedded in the prompt).
- Seeded text: 2 arms × 2 reviewers × 2 repetitions = 8 runs.
- Original text: PLAIN × 2 reviewers = 2 runs (the FRAMEWORK runs on the original exist from 2026-11-14), to compare native recall.

## Scoring rule (fixed in advance)

- A planted fault counts as **detected** if a finding quotes or unambiguously locates the planted text **and** names a problem of the right kind (wrong / unsupported / inconsistent / overclaimed / fabricated or unverifiable). Locating it with the wrong diagnosis = **partial**, reported separately and counted 0.
- Every other finding is classed **valid** (a real issue in the text, native or not) or **invalid** (wrong, or a matter of taste with no textual basis). Precision = (detected + valid) / total findings.
- Scored blind: outputs renamed to random ids; the id→arm map is opened only after all scores are written.

## Hypotheses and decision rule

- H1: FRAMEWORK detects more planted text-detectable faults (P4–P7) than PLAIN, summed over the 4 runs per arm.
- H2: Neither arm detects source-dependent faults (P1–P3) reliably (≤ 1/4 runs each), which supports keeping source checks as a separate step.
- H3: FRAMEWORK precision ≥ PLAIN precision.
- Decision: the framework prompt earns its place in the DR-011 pass only if H1 holds by ≥ 2 detections out of 16 opportunities with H3 not violated by more than 10 percentage points. A tie or a reversal is reported as such and goes to the hypothesis log as evidence against.
- Power: n = 4 per arm. This is a pilot; a difference of 1–2 detections is noise.
