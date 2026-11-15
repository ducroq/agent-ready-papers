# Preregistration: does the framework *process* catch what a review with the same sources misses? (EXP-003, v2 of EXP-002)

Written and committed 2026-11-15, before any run of this experiment. Deviations go in the concluding SUMMARY.md (not yet written), not here.

## Why a v2

EXP-002 (pilot, rejected for the blind-pass use) found the framework's rule prompt equal to a plain prompt on the text-detectable planted faults: 16 of 16 each, a ceiling, because each contradicted a caveat next to it. On source-dependent faults neither arm was reliable (2/12 vs 4/12). It tested only the prompt, never the process the framework claims (registry, then source checks, then Step Z), and for source faults the reviewer model mattered more than the prompt. v2 adds the process, gives the sources, and holds the model constant.

## Arms

All arms: Codex CLI 0.162.1, model `gpt-6.1-sol`, default reasoning effort (logged as "none"), the same settings as EXP-002. Passed explicitly as `-m gpt-6.1-sol`.

| Arm | Prompt (`prompts/`) | Sources? | Rules? | Process? |
|-----|---------------------|----------|--------|----------|
| A | `prompt-A-plain.md` (EXP-002's plain prompt, byte-identical) | no | no | no |
| B | `prompt-B-framework.md`: EXP-002's rule prompt with three changes: rule 4 revised (a figure attributed to a cited source is grounded, not an unstated input); every essay-specific pointer replaced by neutral wording (rule 3 "every normative proposal", rule 4 "derived values", rule 5 "title and introduction") | no | yes | no |
| C | `prompt-C-process.md`: E plus the process. STEP 1 claim registry, STEP 2 source check after `templates/anti-hallucination.md` (existence, Steps 0–3, condensed to one item; Steps 4–6 in the template's wording), STEP 3 the rules, registry appended (unscored) | yes | yes | yes |
| D | `prompt-D-plain-sources.md`: A plus the sources | yes | no | no |
| E | `prompt-E-framework-sources.md`: B plus the sources | yes | yes | no |

C vs E isolates the process (same rules, same sources). C vs D is the framework as a whole against a plain review with the same sources. A vs B retests the revised rule prompt. 3 repetitions per arm, 15 runs. The essay is embedded in the prompt, as in EXP-002. The source-check wording follows the template, so no prompt names any planted fault kind. C also gets about 800 extra output words for its registry (unscored), so the process comes bundled with a larger output budget.

## Materials (off-repo; SHA-256 below)

- The same essay as EXP-002: a published Dutch-language essay on the energy use and climate value of AI (2026, about 3,000 words, 10 references), anonymised here.
- `inputs/seeded.txt`: a newly seeded copy with 10 planted faults, made by `seed2.py` from `inputs/original.txt`. It adds an 11th, fabricated reference.
- `sources/ref01.txt` … `ref10.txt`: the 10 cited sources, fetched 2026-11-15 and converted to text (`html2txt.py`; ref01's body extracted from its page separately). About 37,000 words. The fabricated reference has no file.
- **Sealed answer key** (`KEY-sealed.md`): the exact planted text, per-fault locality and scoring notes. Committed here only as its SHA-256, published with the conclusion.

## Isolation and contamination guard

Under the default Codex permissions profile on this machine, this repository is readable and `~/lab` is not. So the off-repo key was never reachable, but this preregistration (fault kinds) and EXP-002's evidence are. v2 therefore runs every invocation under a per-run permissions override, with no change to `~/.codex/config.toml`:

```bash
codex exec --skip-git-repo-check -m gpt-6.1-sol -C "$RUN" -o "$OUT" \
  -c default_permissions='"exp003"' \
  -c 'permissions.exp003.filesystem.":root"="deny"' \
  -c 'permissions.exp003.filesystem.":minimal"="read"' \
  -c 'permissions.exp003.filesystem."/home/jeroen/.local/lib/node_modules/@openai/codex"="read"' \
  -c "permissions.exp003.filesystem.\"$RUN\"=\"read\"" \
  "$PROMPT" </dev/null
```

- `$RUN` is a fresh directory per run, outside any git repository (so no project doc is loaded), holding only `sources/` (arms C, D, E) or nothing (A, B). `$OUT` is written by the CLI outside every granted path, so no run can read another's output.
- **Seeded positive before the runs**: one smoke run under the same override is asked to read a canary file outside `$RUN` (in `~/lab` and in this repository). The guard counts as working only if both reads fail. The same smoke test settles where `$RUN` may sit (whether `:minimal` covers it).
- **Contamination** = a command in the run's Codex session log (`~/.codex/sessions/…/rollout-*.jsonl`) that reads a path outside `$RUN`, `:minimal` and the Codex install directory. Such a run is excluded and rerun once; a second contaminated run marks its arm as contaminated. Limit: reads inside a script the run writes are not visible in the log; the override is the real guard.

## Planted faults (by kind; exact text in the sealed key)

| ID | Stratum | Kind |
|----|---------|------|
| T1 | text | conceptual slip in what a value of the essay's proposed ratio means |
| T2 | text (also source) | a figure in the prose that disagrees with the same figure in a graphic nearby |
| T3 | text | sector-wide generalisation with no source |
| T4 | text | wrong multiple in an illustrative comparison |
| S1 | source | fabricated second citation for an existing claim: neutral wording, invented authors, DOI checked 404 |
| S2 | source | a sourced share changed |
| S3 | source | modal stripped from a cited warning |
| S4 | source | measurement period changed |
| M1 | both | the measurement boundary said to include something the source excludes |
| M2 | both | a sourced number changed so it no longer fits a percentage stated with it |

**Known limits, stated in advance.** None of the faults contradicts a caveat in the same paragraph. Still, five of the six text-detectable ones (T1, T2, T4, M1, M2) can be checked against nearby text, so **H1 may hit a ceiling again**. S1 is the only reference without a source file in arms C, D and E, so expect it to be found about equally there. M1 and M2 are detectable from the text alone, so they are excluded from the source comparisons and reported separately. Because S1 is partly given away, H2 and H2b are also reported on S2–S4 (9 opportunities), descriptively.

## Scoring (fixed in advance)

- **Detected** = a finding locates the planted text **and** names the right kind of problem. For S faults, arms A and B score on "unverifiable / check the source / suspicious". Arms C, D and E, which hold the sources, score only on "the source says otherwise" or "the source is missing". T2, M1 and M2 count if either the text inconsistency or the source mismatch is named. Locating with the wrong diagnosis = partial, reported, counted 0.
- **Precision** = (findings − invalid) / findings. Invalid = wrong, or no basis in the text or sources. The registry appendix in arm C is not scored.
- **Blind**: outputs renamed to random ids, arm markers stripped (rule numbers, "Step Z", "STEP n", the appended registry), id→arm map opened only after scores are written. Arms stay partly recognisable by wording, as in EXP-002.
- **Two scorers for detection**: Claude (also the seeder, so biased) and Mistral Vibe, independently, each given the unsealed key and the blinded outputs. Report raw agreement and Cohen's κ (κ is unstable near a ceiling). Disagreements are settled by the engineer. Precision is scored by Claude alone, labelled single-scorer.

## Hypotheses (opportunities = faults × 3 runs)

- **H1**: B − A ≥ 3 of 18 on T1–T4, M1, M2.
- **H2 (primary; the framework as a whole, given sources)**: C − D ≥ 3 of 12 on S1–S4.
- **H2b (the process alone)**: C − E ≥ 3 of 12 on S1–S4.
- **H3 (sanity; scored on different criteria, so interpretive only)**: each of C, D, E beats each of A, B by ≥ 3 of 12 on S1–S4.
- **H4**: precision B ≥ A − 10 points, C ≥ D − 10, C ≥ E − 10.

## Decision rule (per comparison, applied in this order)

1. **Both arms at ceiling** (≥ 90% of the stratum: ≥ 17/18 or ≥ 11/12) → inconclusive. This takes precedence.
2. **Difference ≥ 3 in the hypothesised direction, and the matching H4 clause holds** (B/A, C/D or C/E) → supported. H2 or H2b: the process claim at EMERGING (one essay, n = 3); the process arm becomes the recommended DR-011 source pass. H1: a new entry reverses EXP-002 for the revised rule prompt.
3. **Difference ≥ 3 in the hypothesised direction, but the matching H4 clause is violated** → mixed. Reported, not adopted.
4. **|difference| < 3** → no detectable difference. For H2: the value lies in having the sources, not the framework (evidence against). For H2b: the process adds nothing over the rules plus sources (evidence against). For H1: EXP-002 stands.
5. **Difference ≥ 3 in the opposite direction** → evidence against, reported as a reversal.

Power: n = 3 per arm. A pilot-scale test; a difference of 1–2 detections is noise.

## Cost estimate

15 Codex runs (arms C, D and E read about 37,000 words of sources, so expect minutes each), 15 Vibe scoring runs, and Claude for blind scoring and analysis. Subscription plans; Claude time unmetered.

## SHA-256

Off-repo materials (`~/lab/agent-ready-papers/experiments/2026-11-15-framework-process-arm/`):

```
c6cf23329fb2a3319f1ba64968559a1e6d0d0582beb0105e0a6216f317549768  KEY-sealed.md
4e3529800ea22dede53e967b1a95111aacaa74a33af6cf6bce0854dd3d6aa541  seed2.py
484c526ffed51fc6d4e2882cc4bd6f0a8482500157ae159e307a66a5ec18799a  html2txt.py
e39fa77d2d8c9a02167a0bd71df9cd252b17f3e3b7606553a5f1adbd023addda  inputs/original.txt
64d7a58a8a37146ccf31849e96309d8396f2ea67354a9400203e3613901e6aab  inputs/prompt-A-plain.md
9f35a4c08902db73cd0f7f08819b21dc8ad5644863e2026816bbd4efdc921cf6  inputs/prompt-B-framework.md
c7057313497f09f9461ec9abdd6da0539fa2f394ac988426e992cb292bcc7d59  inputs/prompt-C-process.md
03790a8976cfcba8ee306a8b2e849ecb07edff99b3bc77b70389689c5d4d9c7e  inputs/prompt-D-plain-sources.md
6c63eb1c96b3dbb2990e18bb0ad382f243478f5090006f4521bdc16487607d40  inputs/prompt-E-framework-sources.md
482b7fe824bfccce6fe0cde9a24a8322d76c51428ffad082f613c16f6c80087b  inputs/seeded.txt
9bc5e8e6099341e5b70191141fa8e32a5606f1d322f724bc44c132d5d342af16  sources/ref01.txt
90aa63b54899af73cbf9f7032c4ff461aa68dc76168aff90952f376b51ada34a  sources/ref02.txt
490d75d14eba4b0a9059a6c6886df4aa8a6b7091d9bdc17b0fd3039493de3b87  sources/ref03.txt
2e622a9bd0697a33db6d111914f5519363bb30bd3af79a8c7ff28e7ffcacfd9e  sources/ref04.txt
5e03bc1c7c6c655d3ce6045a15fa994d003e93b7cbf8e605443a37f7885ec6c3  sources/ref05.txt
2617d853ecb5908339989384e5634ada1932e5e4fa39d3b40aba90f0170f77c9  sources/ref06.txt
cc26bb69c8897d7a45abecdfda718adc605741cc476f22fe7e2fd43a7fe354b8  sources/ref07.txt
8a7e4987cf09629fe45ca79697639e8db930de7029ab3e5d1eb18daeed38e4c7  sources/ref08.txt
60a08e4ffd3213222a497bdc88255addd79f94b18a204ab6373654fed79d40b3  sources/ref09.txt
f680ce6d722c012f4c658dc027ebf10fb92cdfb1fea9fc15cfc28864859f3a28  sources/ref10.txt
```
