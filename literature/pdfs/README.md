# Literature PDFs

Local full-text copies of sources indexed in [`../README.md`](../README.md).

## Naming

One rule: **the PDF basename equals the source-note basename.** `sources/<slug>.md` ↔ `pdfs/<slug>.pdf`. No dates, no author-year variants, no arXiv IDs in filenames — the note is the entry point and the PDF is its attachment, so a reader who has one can always find the other.

## Not tracked by git — deliberately

`/literature/pdfs/` is gitignored. This repo is public under CC BY 4.0, and these are third-party copyrighted works: arXiv's default non-exclusive licence does not grant redistribution, and publisher PDFs certainly do not. Committing them would republish other people's papers as a side effect of tracking our reading — the same trade the `papers/*` allowlist above it refuses to make.

Consequence for adopters and for future sessions: **this directory will be empty on a fresh clone.** Source notes must therefore stand on their own — never write a note that depends on the PDF being present, and put every figure the note relies on *in the note*.

## Current contents (2026-09-14)

| File | L# | Note |
|------|----|------|
| `chen-2026-evidence-ledger.pdf` | L60 | |
| `ghostcite-2026.pdf` | L59 | |
| `kim-yang-2026-trace.pdf` | L63 | ⚠ **No text layer** — 23 pages, `pdftotext` returns nothing. Needs OCR, or read the arXiv HTML version instead |
| `li-2026-self-correction.pdf` | L64 | |
| `mori-2026-warrantscore.pdf` | L62 | |
| `rao-callison-burch-2026.pdf` | L58 | Title page reads "Published as a conference paper at COLM 2026" — peer-reviewed, not a bare preprint |
| `zhou-yu-2026.pdf` | L61 | |

Each was fetched from arXiv on 2026-09-14 and verified against its title page.

## Not obtainable

| Source | L# | Why |
|--------|----|-----|
| Topaz et al., *The Lancet* | L57 | Paywalled |
| Song, Hu & Dunn, *AI & SOCIETY* | L65 | Paywalled (Springer IdP redirect); not in PMC or Europe PMC |

Both notes are marked PARTIAL / NOT READ accordingly. Institutional access would close both.
