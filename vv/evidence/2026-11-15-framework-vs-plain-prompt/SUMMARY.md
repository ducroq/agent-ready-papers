# Summary: framework rules vs a competent plain prompt (pilot, 2026-11-15)

Preregistration: `PREREGISTRATION.md` (this folder; an anonymised copy of the file written before the runs, see its first line and *Provenance*). Scores: `scores.tsv` (unblinded copy of the blind score sheet). The essay, the seeded copy, the prompts' embedded text and the raw reviewer outputs quote a third-party essay (published, Dutch, 2026; anonymised here) and stay off this repository; their SHA-256 is listed below (DR-024 rule 6 applied by analogy). Reviewers: Codex CLI 0.162.1 and Mistral Vibe, headless, text only.
## Bottom line

**On this essay the framework's rule set, used as a reviewer prompt, added nothing measurable over a competent plain prompt, and cost precision.** Both arms found every planted text-detectable fault (16/16 each). The framework arm produced more findings (41 vs 28) at lower precision (88% vs 100%). On source-fault detection, which *model* reviewed mattered more than which *prompt* it got; on findings count and precision the prompt mattered more. By the preregistered decision rule, H1 fails and H3 is violated: this is evidence against using the rule prompt as the DR-011 blind pass in its current form.

What the test does **not** show: anything about the framework as a *process* (registry + source checks). No arm checked sources, and the one fault no run found (P2) is exactly the kind a source check catches. That claim is untested here (see *What next*).

## Results: seeded essay, 8 runs

| Arm | Model | Run | Text faults P4–P7 | Source faults P1–P3 | Findings | Valid | Natives found |
|-----|-------|-----|------|------|------|------|------|
| FRAMEWORK | Codex | r1 | 4/4 | 2/3 (P1, P3) | 12 | 11 | N2 N3 N4 N5 |
| FRAMEWORK | Codex | r2 | 4/4 | 0/3 | 11 | 9 | N2 N3 N4 N5 N9 |
| FRAMEWORK | Vibe | r1 | 4/4 | 0/3 | 9 | 8 | N2 N4 |
| FRAMEWORK | Vibe | r2 | 4/4 | 0/3 | 9 | 8 | N2 N4 N5 |
| PLAIN | Codex | r1 | 4/4 | 2/3 (P1, P3) | 8 | 8 | N2 N5 |
| PLAIN | Codex | r2 | 4/4 | 2/3 (P1, P3) | 9 | 9 | N2 N5 N9 |
| PLAIN | Vibe | r1 | 4/4 | 0/3 (P1 partial) | 5 | 5 | — |
| PLAIN | Vibe | r2 | 4/4 | 0/3 | 6 | 6 | — |

| Totals | FRAMEWORK | PLAIN |
|--------|-----------|-------|
| Planted text-detectable (P4–P7) | 16/16 | 16/16 |
| Planted source-dependent (P1–P3) | 2/12 | 4/12 |
| P2 (0.03 → 0.3 g CO₂e) | 0/4 | 0/4 |
| Findings | 41 | 28 |
| Valid | 36 | 28 |
| Precision | 87.8% | 100% |
| Native issues (N1–N9) found | 14 | 5 |

## Hypotheses (as preregistered)

- **H1, framework detects more P4–P7: not supported.** 16 vs 16. All 8 runs found all four: a **ceiling effect**. The planted text faults were too blatant to tell the arms apart, and that is a design flaw in my seeding. Each one contradicted the essay's own caveats, so any careful reader catches it.
- **H2, neither arm detects P1–P3 reliably (≤ 1/4 runs per fault): partly refuted.** FRAMEWORK holds (P1 1/4, P3 1/4). PLAIN does not: Codex-plain flagged the fabricated replication and the wrong attribution in both runs, Codex-framework in one of two, Vibe never. Even the hits were "cannot verify, check the source", never "this source does not exist". Nobody caught the tenfold change of a sourced number (P2).
- **H3, framework precision ≥ plain: violated, by 12.2 points** (preregistered tolerance: 10). 3 of the 5 invalid findings are the same pattern: "state the denominators of the percentages", raised on figures the essay takes from the IEA. This looks driven by framework rule 4 ("note any input that is not stated"), so the prompt itself generates a systematic false positive.

**Decision (preregistered rule): the rule prompt does not earn its place in the DR-011 pass on this evidence.**

## Secondary: native issues

On the seeded text the framework arm found almost three times as many native issues (14 vs 5). Above all it found the normative and contribution problems: the missing warrant behind the essay's proposed normative duty (N4) in 4/4 runs vs 0/4, and the unsourced savings claim for the author's own technology (N3) in 2/4 vs 0/4.

Two things weaken this:
1. **Prompt steering, a confound I didn't flag in the preregistration.** The framework prompt names the essay's two proposals (a ratio metric and a normative duty) explicitly ("Check … against this"); the plain prompt does not. The N4/N5 advantage is at least partly "the prompt pointed there".
2. **On the original essay the gap disappears.** Plain prompt (today, 2 runs) vs framework prompt (2026-11-14, 2 runs): 9 vs 10 native issues. Plain-Codex found N2 N3 N4 N5 N6 N9; plain-Vibe found N2 N4 N5 and half of N1. Plain-Vibe also raised a valid point no framework run made: the proposed ratio isn't scale-invariant, so shrinking the denominator inflates the ratio. Those 4 runs weren't blinded.

The most likely reading: the plain reviewers spent their ~900 words on the planted faults; the framework prompt's checklist pushed reviewers to keep going through the normative section. That's a real but modest effect, mostly reproducible with one line ("also check the argument behind each normative proposal").

## Model vs prompt

| | Findings | Valid | Source faults | Natives (seeded) |
|---|---|---|---|---|
| Codex (4 runs) | 40 | 37 | 6/12 (P1+P3: 6/8; P2: 0/4) | 14 |
| Vibe (4 runs) | 29 | 27 | 0/12 | 5 |

Codex flagged suspicious references; Vibe accepted them. The model gap is larger than the prompt gap on source faults (6 vs 0, against 2 vs 4). It is smaller on findings (11 vs 13) and precision (0.6 vs 12.2 points), and equal on native issues (14 vs 5 both ways).

## Threats to validity

- **n = 4 per arm, one essay.** A pilot; differences of 1–2 findings are noise.
- **Ceiling on P4–P7**, as above: the primary comparison can't discriminate.
- **Blinding was partial.** Arm-revealing words (Rule N, Step Z) were stripped, but at least 3 of 4 framework outputs stayed recognisable by their wording ("against all six rules", "who/where/when"). The planted-fault key is objective; the valid/invalid calls are where bias could enter.
- **Seeder = scorer** (Claude), stated in advance.
- **The native key is my own** review from 2026-11-14, which used the framework, so it may favour issues the framework surfaces.

## What next (proposed, not run)

1. **Harder seeding**: faults that don't contradict nearby caveats. A subtly overstated qualifier, a warrant gap between two *correct* sourced claims, a boundary mismatch only visible through numbers. That breaks the ceiling.
2. **Test the process, not the prompt**: a third arm that gets the sources (or web access) and runs the registry + Step 4–6 checks, scored on P1–P3 and N1. That's where yesterday's review found what no blind pass did, and it's the framework's actual claim. Here, only Claude has the sources, and Claude knows the key: a second-model process run is needed.
3. **Fix rule 4's false positive**: "note any input that is not stated" → "… that the text computes with; figures attributed to a cited source are grounded, not unstated."
4. **Drop essay-specific steering** from the framework prompt, or add the same pointer to the plain prompt.

## Cost

12 headless runs: 10 today (Codex 44–61 s, Vibe 113–195 s each) and the 2 framework runs on the original essay from 2026-11-14; on subscription plans: no metered spend recorded (`spend_usd`: null). The Claude share (seeding, blind scoring of ~6,600 words, analysis) wasn't metered separately.

## Provenance

**Precision as computed.** `scores.tsv`'s `valid` column already includes the detections, so the reported precision is (findings − invalid) / findings. That is the intent of the preregistered formula; read literally, the formula would double-count detections.

**Hypothesis-log deviation.** The preregistered rule sends a tie or a reversal to the hypothesis log. Here the `rejected` registry entry is the record of the evidence against, and the follow-up is a v2 preregistration (process arm, harder seeding), committed before its runs.

**Deviation from DR-024 rule 1.** The preregistration was written before any run but kept off-repo (it sits next to third-party text), so it was not committed first. The evidence of order is the file timeline (local clock, CET):

| Time | Event |
|------|-------|
| 08:23:59 | `PREREGISTRATION.md` last written |
| 08:24:16 | seeded essay written |
| 08:25:19 | first reviewer output |
| 08:29:37 | id→arm map written (not opened) |
| 08:29:43 | outputs copied to random ids |
| 08:30:20 | blind score sheet written; map opened afterwards |

File times prove the order of writing, not of reading: that the map stayed unopened until after scoring rests on the scorer's (Claude's) word.

`inputs/original.txt` has mtime 08:23:37 on 2026-11-15: it is a copy of the 2026-11-14 extraction, made before the preregistration was written.

SHA-256 of the off-repo files. `ANALYSIS.md` there is the unanonymised original of this SUMMARY.md. The two 2026-11-14 framework runs on the original essay, which the *Secondary* comparison uses, live in `~/lab/agent-ready-papers/reviews/`:

```
15512acb5ba97840fc6d4c0ee55cf51987747d00ef6f202e0bb99823d8a561cd  ANALYSIS.md
bc127fe0839f1b6c12248e96502fd81235fa397b4536d26604085843011a0c81  reviews/2026-11-14-codex-(essay).md
b5708a303bbb38d0cda24f2421f0ea9c773700bf5421ce68aebc6e8493e18243  reviews/2026-11-14-vibe-(essay).md
```

Experiment folder (`~/lab/agent-ready-papers/experiments/2026-11-15-framework-vs-plain-prompt/`):

```
8009100f72cbc2d75c51a80ba7f9d869431866bbf1b5d483bafa060fce2694f3  PREREGISTRATION.md
e39fa77d2d8c9a02167a0bd71df9cd252b17f3e3b7606553a5f1adbd023addda  inputs/original.txt
a459d1bd94ee90a0d27cb1ec618e9449ff3b6a1c0aef3fc92adc07d176d2eae4  inputs/prompt-framework.md
64d7a58a8a37146ccf31849e96309d8396f2ea67354a9400203e3613901e6aab  inputs/prompt-plain.md
7e9ab883dd5a8bf3e6827d04382e3891423c1d691ec7d96e2ea1ddbcc1b8b07f  inputs/seeded.txt
0784fd556616004815fcab3e9a9689da2db3c46a6b86fbcc86c70fc0e12dc7d5  runs/codex-framework-seeded-r1.md
18a12e6b5a057f4a10aa7b1a5083811edeb90fad92b1197d06e7731f231cca50  runs/codex-framework-seeded-r2.md
3d5b37d5d0f9d0de2b777fb1b2f2e752e34eade8ad41503564b51cfb1e2f5680  runs/codex-plain-original-r1.md
ea2e5d14cae77374b0395703ae2268f655d6a84d4d3c515f2117f3f18707c63f  runs/codex-plain-seeded-r1.md
c4f605727c1b3b879bacecfb94fda3bc254eca1ac89050e69ba008b14c7b71fc  runs/codex-plain-seeded-r2.md
50e0d51c945916070416c338fc4dfa9e018841a177128cef1cbede3ca698eb7b  runs/vibe-framework-seeded-r1.md
4e696f391d30ddd3885e16e1714a25cb4f87920b921324f8d72b7a62939c29fe  runs/vibe-framework-seeded-r2.md
6da2a3641ae29f844a5da40b9b6b0f5e13adc9d28e6d3a64bff455b12911fd75  runs/vibe-plain-original-r1.md
5728204200be5ceba6f1f8e8933e4196cd48cdc053f0d7bb507eba1b4d2dd41a  runs/vibe-plain-seeded-r1.md
827aa8754ec2abab53416b4c89aab90687f3a243a85d86a7ec22e08fb6ad8f75  runs/vibe-plain-seeded-r2.md
cf4c6297f136e68eca123df53fedb8e841b1325a375f58a33fb1a94745359c56  SCORES-blind.tsv
7864dd057159a02256c3dc6982023e967a3293ba970e988c16de862fbf313293  blind/_MAP_do_not_open_until_scored.json
```
