# arXiv submission: Paper 1

Prepared 2026-10-19. Build the package with `make paper1-arxiv`; it writes `arxiv/` (gitignored).

## Steps

1. Commit this round's changes (after `/review-changes`), then tag the commit `paper1-preprint-1` and push the tag.
   The paper's Code and data availability section names that tag, and the title-page stamp reads it.
2. `make paper1-arxiv`. The stamp must read `paper1-preprint-1`, not `…-dirty`. Check `arxiv/manuscript.pdf`.
3. If you haven't posted in the chosen category before, arXiv may ask for an **endorsement**; since 2026-01-21 an institutional email no longer qualifies on its own. Request one early: it can take days.
4. Upload `arxiv/paper1-arxiv.tar.gz` (or the three files in `arxiv/src/`), remove any extracted file arXiv flags as unnecessary, and fill in the form below. Read arXiv's generated PDF page by page before confirming: announced content is archival.
5. After the arXiv ID arrives: add it to the cover letter (prior posting) and to `backlog.md`. Declare it on submission to Learned Publishing.
6. After acceptance: update the arXiv record with a link to the published version (Wiley's preprint policy).

## Form fields

- **Title:** The Verification Gap: Checking the Reasoning in AI-Assisted Academic Writing
- **Authors:** Jeroen Veen (HAN University of Applied Sciences)
- **Primary category: undecided (maintainer).** Since 2025-10-31, arXiv CS posts review and position papers only after peer review (https://blog.arxiv.org/?p=1740). The post leaves "scientific research papers" on societal impact alone (its example is cs.CY), but it does not exempt position papers filed in cs.CY. Options:
  - (a) cs.CY primary with a cs.DL cross-list, with the paper presented as a methods paper (a documented search, a proposed register and its self-application), at the risk of a hold;
  - (b) ask arXiv moderation first;
  - (c) post after LP accepts the paper, with proof of review;
  - (d) SocArXiv or Zenodo now.
- **Comments:** 16 pages, 4 tables. Claim register, glossary and checking tools: https://github.com/ducroq/agent-ready-papers (tag paper1-preprint-1). [Add "Submitted to Learned Publishing" only if it is true when you post.]
- **Licence:** CC BY 4.0, consistent with the repository (DR-013). Wiley's preprint policy prefers a no-reuse licence but accepts CC BY. LP appears to be Gold OA since 2025, but that comes from search snippets only; confirm it. arXiv's non-exclusive licence is the alternative if you want to follow Wiley's preference.
- **Abstract** (plain text, 1788 of 1,920 characters):

> Generative AI tools now help write a growing share of academic papers. Checking their citations, that each cited work exists and says what it is cited for, has received attention. A paper can pass that check and still fail: a claim can rest on real evidence that does not carry it, or be worded more certainly than its support allows. Reporting guidelines, such as those collected by the EQUATOR (Enhancing the QUAlity and Transparency Of health Research) Network, help authors report a study completely; whether the reasoning from evidence to claim holds is a separate question, most exposed in papers that have only reasoning to offer, and a documented search found no consensus checklist that checks such reasoning step by step. This paper proposes a claim register, built on Toulmin's layout of arguments and Whetten's account of a theoretical contribution: each claim is recorded with what it rests on, each kind of grounds gets its own check, the step from grounds to claim is checked for relevance and sufficiency, and the wording of each claim is tied to how well it is supported. Each part is already in use, in safety engineering, scholarly data publishing, educational measurement and the calibrated reporting of certainty; none of the approaches compared here combines them for academic papers. Applied to this paper, the register leaves three of its six central claims at the Emerging tier, for named reasons: the search had one screener, and the records were kept by the author's own tooling. Publishing a register can make a paper's reasoning visible and traceable; whether it helps authors and reviewers find weak steps has not been tested. Authors and journals could publish registers as optional supplementary material, and trials should test them before wider adoption.

## Pre-upload checks (2026-10-20)

Checked against arXiv's [whytex](https://info.arxiv.org/help/faq/whytex.html) and [common mistakes](https://info.arxiv.org/help/faq/mistakes.html) pages, [Campbell](https://trevorcampbell.me/html/arxiv.html) and [Huston](https://www.ianhuston.net/2011/03/checklist-for-arxiv-submission/), by compiling the extracted tarball in a clean folder with pdflatex only (no BibTeX), four passes:

- Source, not PDF; three files, flat, relative paths, no `.git` or generated files; `.bbl` shipped, `.bib` not (plain BibTeX, so the biblatex `.bbl`-version issue does not apply).
- No comments beyond the stamp line; no TODOs; no `\cite` in a caption; no custom `.sty`; Latin Modern, all fonts embedded.
- No errors, undefined references or overfull boxes; text identical to the local build; spellcheck flags names and terms only.
- PDF title and author set (`pdfusetitle` plus `\hypersetup{pdfauthor=…}`; they were empty). A full `\hypersetup` title cost 15 words on the budget counter, which counts the preamble.

Redo the clean compile after the final rebuild if the source changed since.

## Not yet done (decide whether each blocks posting)

- The blind re-rating of the rows new or reworded for draft 3 (DR-029 condition 3). The "three of six" in Section 5 and in the abstract is today's registry state; a re-rating may change it. A later arXiv version can correct it.
- Source notes for Mugaanyi, Walters, Xiong and Zhou (the P0 claims S1-1 and S1-2 rest on them).
- S2-4, S3-2 and S4-3: scope widening flagged by one rater of two (hypothesis log, 2026-10-19).
