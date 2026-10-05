"""Formula-repetition scanner: a locator for formulaic prose, never a gate.

STATUS: PROPOSED under DR-022. Staged in extensions/ (the DR-018 precedent);
it is not a tools/ surface until DR-022 is Accepted.

What it asks is *is this prose formulaic?*, never *who wrote it?*. The
framework keeps detectors out of every gate (DR-022's decision, and
literature L67-L71: detector error is condition-dependent, evadable, and was
biased against non-native writers). The signals below are the interpretable
ones: the cues expert readers cite (Russell, Karpinska & Iyyer 2025, L72,
Table 3/17), the stock style vocabulary measured in the literature (see
STYLE_WORDS for per-item provenance), and the formula devices that voice
guides mandate without a dose cap.

Every flag is for the author to decide. A deliberate template can be the
point: a closing device that ends every essay can be a design choice, and the
scanner can only say that it recurs, not that it should not. The thresholds
are SPECULATIVE defaults (docs/THRESHOLDS.md convention), not calibrated
constants; they decide what gets *shown*, never a pass or fail.

Signals:

  rhythm      Sentence-length variation (coefficient of variation), the
              share of short sentences, and runs of consecutive sentences of
              near-equal length. Low variation is the "burstiness" idea
              (GPTZero, vendor) and Russell's "human sentences vary more in
              length".
  paragraphs  Paragraph-length variation ("paragraphs of similar length").
  contrast    The negation-contrast turn: "It's not X. It's Y.", "not just X
              but Y", "not only ... but also", "not X but rather Y". The
              reversed form, "Y rather than X" (Wikipedia, L82), is counted
              apart as signal "rather": academic prose uses it honestly, so
              its rate is what matters.
  dashes      Em-dashes per 1,000 words (Wikipedia, L82: LLM output uses
              them where a writer would use a comma, colon or parentheses).
              Counted from U+2014, LaTeX --- and \\textemdash; a Markdown file
              that writes dashes as " -- " is noted, not counted.
  lists       Share of comma lists with exactly three items ("consistently
              listing three items").
  vocabulary  Stock style words per 1,000 words, each hit located.
  house       Optional: a project's own word list (--house-words), reported
              as source H, a style rule and not evidence. It is matched after
              the evidence list and counted apart, so it never takes or
              inflates an evidence hit.
  phrases     Word n-grams (3-6) recurring across paragraphs: a house tic
              such as a stock closer shows up here without any word list.
  openers     Sentence openings that recur.
  template    Section-level features shared by most sections: the same
              opening words, the same closing label ("Takeaway:"), a closing
              question, a one-sentence closing paragraph. This is the
              "one section template repeated seven times" case.

Input: Markdown or plain text; LaTeX roughly, and only for a .tex/.ltx/.latex
file (decided by suffix, never by content). Skipped: Markdown tables, code
fences, HTML comments and tags, YAML front matter; in LaTeX also comments, the
preamble before \\begin{document}, and non-prose environments (tables,
figures, equations, listings; see SKIP_ENVS), keeping text outside them on the
same line. An environment that never closes is reported as a "parse" flag. \\section and Markdown/setext headings start a
section; each list item is its own paragraph but is left out of paragraph
rhythm. Style-word and phrase hits report the line of the hit; other signals
report the line where the sentence starts.

Known limits (the review pass triages them; they are why this never gates):
  - English only. A text is flagged "language" instead of reported as clean
    when Dutch function words outnumber English ones, or when it has 300+ words
    and few English function words. Short texts in other languages can slip
    through.
  - Lists: a chain of short clauses ("When he came, she left and I stayed")
    or of places ("Paris, France, and Berlin") can count as a list. Dates,
    years and author lists are excluded.
  - Contrast: an ordinary hedge followed by a restatement ("The effect was not
    significant. It was small.") counts as a turn.
  - Recurring phrases include legitimate terminology; in papers most of them
    are terms, not tics.

CLI:
    python extensions/formula_scan.py <file> [--json] [--house-words FILE]

Exit codes:
    0  report emitted (whatever it finds: this is a locator, not a gate)
    2  tooling error (unreadable path, not UTF-8, or no prose found)
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

# --- SPECULATIVE thresholds: they decide what is shown, never pass/fail ---
MIN_SENTENCES_FOR_RHYTHM = 20
LOW_SENTENCE_CV = 0.35
MONOTONE_RUN = 5  # consecutive sentences ...
MONOTONE_SPREAD = 3  # ... all within this many words of each other
SHORT_SENTENCE = 8  # words
MIN_PARAGRAPHS = 6
LOW_PARAGRAPH_CV = 0.25
MIN_LISTS = 5
HIGH_TRIAD_SHARE = 0.8
PHRASE_MIN_PARAGRAPHS = 3  # an n-gram must recur in this many paragraphs
OPENER_MIN = 4
MIN_SECTIONS = 3
TEMPLATE_SHARE = 0.4  # a feature shared by this share of sections (a closing label: any 3+)
CONTRAST_PER_1000 = 2.0
# Checked 2026-10-05 against 29 papers in literature/pdfs (pdftotext, references included):
# em-dashes max 5.3 per 1,000 words (a style guide, 2012), median about 0.3; "rather than"
# max 1.3 in the four pre-2023 papers, 4.5 in one 2026 paper. Still SPECULATIVE: 29 papers.
RATHER_THAN_PER_1000 = 2.0
EM_DASH_PER_1000 = 6.0
MIN_ENGLISH_STOPWORD_SHARE = 0.2  # below this the text is probably not English ...
MIN_WORDS_FOR_LANGUAGE = 300  # ... but only judged on this many words or more

# Stock style vocabulary. Each item carries its provenance; an item without
# a verified source does not belong here. K = Kobak et al. 2025 (L81;
# Figs. 1-2, S6), W = Wikipedia "Signs of AI writing" rev. 1376889964
# (L82, tier D), R = Russell et al. 2025 (L72, Table 12). Deliberately
# conservative: ordinary academic words that the sources list only at
# corpus scale (significant, potential, findings, robust, key, comprehensive)
# are left out, because on a single paper they would mostly flag honest use.
# Both W and R warn that one hit proves nothing; density is the signal.
# Matched as whole words, case-insensitive, with simple inflections.
# A house list (--house-words) adds words with source H: a project's own
# style rule, never mixed into this evidence list.
STYLE_WORDS: dict[str, str] = {
    "delve": "K,W,R",
    "underscore": "K,W,R",
    "pivotal": "K,W,R",
    "intricate": "K,W,R",
    "foster": "K,W,R",
    "enhance": "K,W,R",
    "crucial": "K,W,R",
    "showcase": "K,W",
    "meticulous": "K,W",
    "garner": "K,W",
    "bolster": "K,W",
    "interplay": "K,W",
    "realm": "K,R",
    "seamless": "K,R",
    "transformative": "K,R",
    "multifaceted": "K,R",
    "elevate": "K,R",
    "harness": "K,R",
    "tapestry": "W,R",
    "testament": "W,R",
    "vibrant": "W,R",
    "resonate": "W,R",
    "paramount": "R",
    "navigate": "R",
    "boast": "W",
    "nestled": "W",
    "it's important to note": "W,R",
    "it's crucial to": "R",
    "worth noting": "W",
    "paving the way": "K,R",
    "in the heart of": "W",
    "when it comes to": "R",
    "in a world where": "R",
    "despite these challenges": "W",
    "in conclusion": "W,R",
    "in summary": "W,R",
}

STOPWORDS = frozenset(
    """a an the and or but if of to in on at by for with from as is are was were be been being it its
    this that these those there here i you he she we they me him her us them my your his our their
    not no so than then too very can could would should will shall may might must do does did done
    has have had what which who whom whose when where why how all any each both more most other some
    such only own same just also into over under about again further once up down out off""".split()
)

ABBREVIATIONS = (
    "e.g.", "i.e.", "et al.", "etc.", "vs.", "cf.", "Dr.", "Mr.", "Ms.", "Mrs.", "Prof.",
    "Fig.", "Figs.", "Eq.", "Eqs.", "Sec.", "Tab.", "pp.", "vol.",  # not "No.": it is also a sentence
)  # fmt: skip

# Digits count as words, so "nearly 700 guidelines" stays three tokens.
WORD_RE = re.compile(r"[A-Za-z0-9\u00C0-\u024F][A-Za-z0-9\u00C0-\u024F'\u2019-]*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])[\"'\u201d\u2019)\]*_]*\s+(?=[\"'\u201c\u2018(\[*_]*[A-Z0-9\u00C0-\u00DE])")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)$")
SETEXT_RE = re.compile(r"^\s{0,3}(?:=+|-+)\s*$")
LATEX_SECTION_RE = re.compile(r"^\s*\\(?:sub)*section\*?\{(.*?)\}")
LABEL_RE = re.compile(r"^[*_]{0,2}([A-Z][A-Za-z ]{0,20}?)[*_]{0,2}:[*_]{0,2}\s")
BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
YAML_KEY_RE = re.compile(r"^[\"']?[A-Za-z_][A-Za-z0-9_.-]*[\"']?\s*:")
# LaTeX environments whose bodies are not prose.
SKIP_ENVS = frozenset(
    """tabular tabular* tabularx longtable table table* figure figure* equation equation* align align*
    gather gather* multline multline* eqnarray eqnarray* math displaymath verbatim lstlisting minted
    tikzpicture thebibliography""".split()
)
BEGIN_RE = re.compile(r"\\begin\{([^}]*)\}")
END_RE = re.compile(r"\\end\{([^}]*)\}")

NEG_SENTENCE_RE = re.compile(r"\b(?:not|n't|n\u2019t|never|no longer)\b", re.I)
AFFIRM_OPENER_RE = re.compile(
    r"^[\"'\u201c*_]*(?:it|this|that|they|he|she)(?:'s|\u2019s|'re|\u2019re|\s+(?:is|are|was|were))\b", re.I
)
INLINE_CONTRAST_RES = (
    re.compile(r"\bnot\s+(?:just|only|merely|simply)\b[^.;!?]{1,80}?\bbut\b", re.I),
    re.compile(r"(?:\b(?:not|cannot)\b|n't\b|n\u2019t\b)[^.;!?]{1,80}?\bbut\s+rather\b", re.I),
    re.compile(
        r"\b(?:is|are|was|were)(?:n't|n\u2019t|\s+not)\b[^.;!?]{1,60}?[,;\u2014\u2013]\s*"
        r"(?:it|this|that|they)(?:'s|\u2019s|'re|\u2019re|\s+(?:is|are|was|were))\b",
        re.I,
    ),
)
RATHER_THAN_RE = re.compile(r"\brather\s+than\b", re.I)
EM_DASH = "\u2014"
ASCII_DASH_RE = re.compile(r"\s---?\s")  # " -- " or " --- " in Markdown prose
# Items before the conjunction (comma-separated), an optional last item with no
# serial comma, then the final item. Validated in _list_items.
LIST_RE = re.compile(
    r"((?:[^,.;:!?()\n]{1,40},\s+){1,20})(?:([^,.;:!?()\n]{1,40}?)\s+)?(?:and|or)\s+([^,.;:!?()\n]{1,40})"
)
NO_SERIAL_COMMA_MAX_WORDS = 4  # without a serial comma, only short items count as a list
CITATION_AFTER_RE = re.compile(r"^\s*(?:[\(\[]\s*\d{4}|et al)")
NUMERIC_ITEM_RE = re.compile(r"^[\s\w.]*\d[\d\s.]*$")


@dataclass
class Sentence:
    text: str
    line: int  # the line the sentence starts on
    words: int
    paragraph: int
    section: int
    offset: int = 0  # start offset within its paragraph's text
    para: Paragraph | None = field(default=None, repr=False, compare=False)

    def line_of(self, pos: int) -> int:
        """Source line of character `pos` within this sentence."""
        return self.para.line_at(self.offset + pos) if self.para else self.line


@dataclass
class Paragraph:
    text: str
    line: int
    section: int
    is_list_item: bool = False
    line_starts: list[tuple[int, int]] = field(default_factory=list)  # (char offset, source line)
    sentences: list[Sentence] = field(default_factory=list)

    @property
    def words(self) -> int:
        return sum(s.words for s in self.sentences)

    def line_at(self, offset: int) -> int:
        line = self.line
        for off, ln in self.line_starts:
            if off > offset:
                break
            line = ln
        return line


@dataclass
class Section:
    title: str
    line: int
    paragraphs: list[Paragraph] = field(default_factory=list)


@dataclass
class Flag:
    signal: str
    message: str
    lines: list[int] = field(default_factory=list)


@dataclass
class ScanReport:
    path: str
    words: int
    sentences: int
    paragraphs: int
    sections: int
    metrics: dict[str, float | int | None]
    flags: list[Flag]
    vocabulary: dict[str, list[int]]
    phrases: list[tuple[str, int, list[int]]]
    openers: list[tuple[str, int]]
    not_evaluated: dict[str, str] = field(default_factory=dict)
    sources: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["phrases"] = [{"phrase": p, "paragraphs": n, "lines": ln} for p, n, ln in self.phrases]
        d["openers"] = [{"opener": o, "count": n} for o, n in self.openers]
        return d

    def to_markdown(self) -> str:
        out = [
            f"# Formula scan: `{self.path}`",
            "",
            "Advisory locator (PROPOSED, DR-022). It flags formula, not authorship; a deliberate "
            "template can be the point, and the author decides. Thresholds are SPECULATIVE.",
            "",
            f"Examined: {self.words} words, {self.sentences} sentences, {self.paragraphs} paragraphs, "
            f"{self.sections} sections.",
            "",
            "| Metric | Value |",
            "|---|---|",
        ]
        for k, v in self.metrics.items():
            shown = "n/a" if v is None else v
            if k in self.not_evaluated:
                shown = f"{shown} (not evaluated: {self.not_evaluated[k]})"
            out.append(f"| {k} | {shown} |")
        out += ["", f"## Flags ({len(self.flags)})", ""]
        if not self.flags:
            out.append("None above the display thresholds. That is not a verdict that the prose is varied.")
        for f in self.flags:
            loc = f" (lines {', '.join(map(str, f.lines[:12]))}{', ...' if len(f.lines) > 12 else ''})" if f.lines else ""
            out.append(f"- **{f.signal}**: {f.message}{loc}")
        if self.vocabulary:
            out += ["", "## Style vocabulary hits", "", "| Word | Source | Count | Lines |", "|---|---|---|---|"]
            for w, lines in sorted(self.vocabulary.items(), key=lambda kv: -len(kv[1])):
                out.append(f"| {w} | {self.sources.get(w, STYLE_WORDS.get(w, '?'))} | {len(lines)} | {', '.join(map(str, lines[:10]))} |")
        if self.phrases:
            out += ["", "## Recurring phrases (across paragraphs)", "", "| Phrase | Paragraphs | Lines |", "|---|---|---|"]
            for p, n, lines in self.phrases:
                out.append(f"| {p} | {n} | {', '.join(map(str, lines[:10]))} |")
        if self.openers:
            out += ["", "## Recurring sentence openers", "", "| Opener | Count |", "|---|---|"]
            out += [f"| {o} | {n} |" for o, n in self.openers]
        return "\n".join(out)


# --------------------------------------------------------------------------
# Parsing


def _clean_line(line: str, latex: bool = False, strip_bullet: bool = True) -> str:
    if latex:
        line = re.sub(r"(?<!\\)%.*$", "", line)  # LaTeX comment ("50%" in Markdown is prose)
        line = re.sub(r"\\(?:url|href)\{(?:[^{}]|\{[^{}]*\})*\}", " ", line)  # URLs: their dashes are not prose
        line = re.sub(r"\\verb\*?([^A-Za-z\s]).*?\1", " ", line)
        line = re.sub(r"\\textemdash\b\s?", "\u2014", line)
        line = line.replace("---", "\u2014").replace("--", "\u2013")  # LaTeX dashes
        line = re.sub(r"\\(?:cite[pt]?|ref|eqref|label|autoref|cref)\*?(\[[^\]]*\])?\{[^}]*\}", "", line)
        line = re.sub(r"\\(?:emph|textit|textbf|textsc|footnote)\*?(\[[^\]]*\])?\{([^}]*)\}", r"\2", line)
        line = re.sub(r"\$[^$]*\$", " ", line)  # inline math
        line = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", "", line)
        line = line.replace("{", "").replace("}", "").replace("~", " ")
    line = re.sub(r"<[^>]{1,200}>", " ", line)  # HTML tags
    line = re.sub(r"^\s*>\s?", "", line)  # blockquote marker
    if strip_bullet:
        line = BULLET_RE.sub("", line)
    return line


LATEX_SUFFIXES = frozenset({".tex", ".ltx", ".latex"})


def _strip_skip_envs(line: str, stack: list[str]) -> str:
    """Drop the parts of `line` inside non-prose environments; `stack` carries open ones across lines."""
    out, rest = "", line
    while rest:
        if stack:
            ev = re.search(r"\\(begin|end)\{" + re.escape(stack[-1]) + r"\}", rest)
            if not ev:
                return out
            if ev.group(1) == "begin":
                stack.append(stack[-1])
            else:
                stack.pop()
            rest = rest[ev.end() :]
            continue
        b = next((m for m in BEGIN_RE.finditer(rest) if m.group(1) in SKIP_ENVS), None)
        if not b:
            return out + rest
        out += rest[: b.start()]
        stack.append(b.group(1))
        rest = rest[b.end() :]
    return out


def parse(text: str, latex: bool = False, notes: list[str] | None = None) -> list[Section]:
    """Split text into sections, paragraphs and sentences. `latex` switches on LaTeX handling
    (decided by file suffix in scan(), never by content: a Markdown file may mention LaTeX).
    Parse problems worth reporting are appended to `notes`."""
    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    sections = [Section(title="(preamble)", line=1)]
    buf: list[tuple[int, str]] = []
    buf_is_list = False
    in_fence = ""
    in_html_comment = False
    skip_env: list[str] = []
    in_document = not (latex and "\\begin{document}" in text)  # no \begin{document}: all of it is body
    # YAML front matter only when line 1 is `---` and line 2 looks like a key.
    front_matter = len(lines) > 1 and lines[0].strip() == "---" and bool(YAML_KEY_RE.match(lines[1].strip()))

    def flush() -> None:
        nonlocal buf_is_list
        if buf:
            parts, starts, off = [], [], 0
            for ln, t in buf:
                starts.append((off, ln))
                parts.append(t)
                off += len(t) + 1
            para_text = " ".join(parts).strip()
            if para_text:
                sections[-1].paragraphs.append(
                    Paragraph(
                        text=para_text,
                        line=buf[0][0],
                        section=len(sections) - 1,
                        is_list_item=buf_is_list,
                        line_starts=starts,
                    )
                )
        buf.clear()
        buf_is_list = False

    for i, raw in enumerate(lines, start=1):
        s = raw.strip()
        if front_matter:
            if i > 1 and s in ("---", "..."):
                front_matter = False
            continue
        if latex:
            if not in_document:
                if "\\begin{document}" in s:
                    in_document = True
                continue
            if "\\end{document}" in s:
                break
            was_skipping = bool(skip_env)
            kept = _strip_skip_envs(raw, skip_env)
            if kept.strip() != raw.strip():  # something was cut: a non-prose environment
                if not kept.strip():
                    if not was_skipping:
                        flush()  # an environment on its own line ends the paragraph
                    continue
                raw = kept
                s = raw.strip()
        fence = re.match(r"^(`{3,}|~{3,})", s)
        if fence:
            if not in_fence:
                in_fence = fence.group(1)[0]
            elif fence.group(1)[0] == in_fence:
                in_fence = ""
            flush()
            continue
        if in_fence:
            continue
        if in_html_comment:
            if "-->" in s:
                in_html_comment = False
            continue
        if s.startswith("<!--"):
            if "-->" not in s:
                in_html_comment = True
            flush()
            continue
        heading = HEADING_RE.match(raw) or LATEX_SECTION_RE.match(raw)
        if heading:
            flush()
            sections.append(Section(title=heading.group(1).strip(), line=i))
            continue
        if SETEXT_RE.match(raw) and len(buf) == 1:  # "Title\n=====": the buffered line is a heading
            ln, title = buf[0]
            buf.clear()
            sections.append(Section(title=title.strip(), line=ln))
            continue
        if not s or s.startswith("|") or re.fullmatch(r"[-*_=\s]{3,}", s) or re.fullmatch(r">\s*", s):
            flush()
            continue
        if latex:
            s_raw = BEGIN_RE.sub("", END_RE.sub("", raw))  # keep text on a \begin{abstract} line
            if not s_raw.strip():
                flush()
                continue
            raw = s_raw
        bullet = BULLET_RE.match(raw)
        # CommonMark: only "-", "*", "+" or an ordered list starting at 1 may interrupt a
        # paragraph; "The war ended in\n1945. That year" is a wrapped line, not a list.
        if bullet and (not buf or buf_is_list or not bullet.group(0).strip()[0].isdigit()
                       or bullet.group(0).strip()[:-1] == "1"):
            flush()
            buf_is_list = True
        elif bullet:
            bullet = None
        cleaned = _clean_line(raw, latex, strip_bullet=bool(bullet)).strip()
        if cleaned:
            buf.append((i, cleaned))
    flush()
    if skip_env and notes is not None:
        notes.append(f"LaTeX environment `{skip_env[0]}` is never closed; everything after it was skipped")

    for si, sec in enumerate(sections):
        for pi, para in enumerate(sec.paragraphs):
            cursor = 0
            for t in split_sentences(para.text):
                off = para.text.find(t, cursor)
                cursor = off + len(t) if off >= 0 else cursor
                if WORD_RE.search(t):
                    para.sentences.append(
                        Sentence(
                            text=t,
                            line=para.line_at(max(off, 0)),
                            words=len(WORD_RE.findall(t)),
                            paragraph=pi,
                            section=si,
                            offset=max(off, 0),
                            para=para,
                        )
                    )
    return [s for s in sections if s.paragraphs]


def split_sentences(text: str) -> list[str]:
    protected = text
    for abbr in ABBREVIATIONS:  # a private-use character stands in for the protected dot
        protected = protected.replace(abbr, abbr.replace(".", "\ue000"))
    return [p.replace("\ue000", ".").strip() for p in SENTENCE_SPLIT_RE.split(protected) if p.strip()]


def _word_pattern(word: str) -> re.Pattern[str]:
    if " " in word:
        return re.compile(r"\b" + r"\s+".join(re.escape(w) for w in word.split()) + r"\b", re.I)
    stem = word[:-1] if word.endswith("e") else word
    return re.compile(r"\b" + re.escape(stem) + r"(?:e|es|s|ed|d|ing|ly|ely)?\b", re.I)


def _cv(values: list[int]) -> float | None:
    if len(values) < 2 or statistics.mean(values) == 0:
        return None
    return round(statistics.pstdev(values) / statistics.mean(values), 3)


# --------------------------------------------------------------------------
# Signals


def _rhythm(sentences: list[Sentence], flags: list[Flag], metrics: dict, skipped: dict) -> None:
    lengths = [s.words for s in sentences]
    cv = _cv(lengths)
    metrics["sentence_length_mean"] = round(statistics.mean(lengths), 1) if lengths else None
    metrics["sentence_length_cv"] = cv
    metrics["short_sentence_share"] = round(sum(n <= SHORT_SENTENCE for n in lengths) / len(lengths), 3) if lengths else None
    if len(lengths) < MIN_SENTENCES_FOR_RHYTHM:
        skipped["sentence_length_cv"] = f"fewer than {MIN_SENTENCES_FOR_RHYTHM} sentences"
    elif cv is not None and cv < LOW_SENTENCE_CV:
        flags.append(Flag("rhythm", f"sentence-length variation is low (CV {cv} < {LOW_SENTENCE_CV})"))
    run_starts: list[int] = []
    i = 0
    while i < len(lengths):
        j, lo, hi = i, lengths[i], lengths[i]
        while j + 1 < len(lengths) and max(hi, lengths[j + 1]) - min(lo, lengths[j + 1]) <= MONOTONE_SPREAD:
            j += 1
            lo, hi = min(lo, lengths[j]), max(hi, lengths[j])
        if j - i + 1 >= MONOTONE_RUN:
            run_starts.append(sentences[i].line)
            i = j + 1
        else:
            i += 1
    metrics["monotone_runs"] = len(run_starts)
    if run_starts:
        flags.append(
            Flag("rhythm", f"{len(run_starts)} run(s) of {MONOTONE_RUN}+ consecutive sentences of near-equal length", run_starts)
        )


def _paragraphs(paragraphs: list[Paragraph], flags: list[Flag], metrics: dict, skipped: dict) -> None:
    # List items are paragraphs for sentence purposes, but not for paragraph rhythm.
    lengths = [p.words for p in paragraphs if not p.is_list_item]
    cv = _cv(lengths)
    metrics["paragraph_length_cv"] = cv
    if len(lengths) < MIN_PARAGRAPHS:
        skipped["paragraph_length_cv"] = f"fewer than {MIN_PARAGRAPHS} prose paragraphs"
    elif cv is not None and cv < LOW_PARAGRAPH_CV:
        flags.append(Flag("paragraphs", f"paragraph lengths are uniform (CV {cv} < {LOW_PARAGRAPH_CV})"))


def _contrast(sentences: list[Sentence], words: int, flags: list[Flag], metrics: dict) -> None:
    lines: list[int] = []
    for i, s in enumerate(sentences):
        if any(r.search(s.text) for r in INLINE_CONTRAST_RES):
            lines.append(s.line)
            continue
        if i + 1 < len(sentences):
            nxt = sentences[i + 1]
            if (
                nxt.paragraph == s.paragraph
                and nxt.section == s.section
                and s.words <= 14
                and nxt.words <= 14
                and NEG_SENTENCE_RE.search(s.text)
                and AFFIRM_OPENER_RE.search(nxt.text)
            ):
                lines.append(s.line)
    rate = round(1000 * len(lines) / words, 2) if words else 0.0
    metrics["negation_contrast"] = len(lines)
    metrics["negation_contrast_per_1000"] = rate
    if lines and rate >= CONTRAST_PER_1000:
        flags.append(Flag("contrast", f"{len(lines)} negation-contrast turns ({rate} per 1,000 words)", lines))
    rather = [s.line_of(m.start()) for s in sentences for m in RATHER_THAN_RE.finditer(s.text)]
    rate = round(1000 * len(rather) / words, 2) if words else 0.0
    metrics["rather_than"] = len(rather)
    metrics["rather_than_per_1000"] = rate
    if rather and rate >= RATHER_THAN_PER_1000:
        flags.append(Flag("rather", f'{len(rather)} "rather than" turns ({rate} per 1,000 words)', rather))


def _dashes(sentences: list[Sentence], words: int, flags: list[Flag], metrics: dict, skipped: dict) -> None:
    lines = [s.line_of(i) for s in sentences for i, ch in enumerate(s.text) if ch == EM_DASH]
    ascii_dashes = sum(len(ASCII_DASH_RE.findall(re.sub(r"`[^`]*`", " ", s.text))) for s in sentences)
    if ascii_dashes:
        skipped["em_dashes"] = f'{ascii_dashes} spaced ASCII dash(es) such as " -- " not counted'

    rate = round(1000 * len(lines) / words, 2) if words else 0.0
    metrics["em_dashes"] = len(lines)
    metrics["em_dashes_per_1000"] = rate
    if lines and rate >= EM_DASH_PER_1000:
        flags.append(Flag("dashes", f"{len(lines)} em-dashes ({rate} per 1,000 words)", sorted(set(lines))))


def _list_items(m: re.Match[str]) -> list[str] | None:
    """Items of a comma list, or None when the match is probably not a list."""
    items = [x.strip() for x in m.group(1).split(",") if x.strip()]
    if m.group(2):
        items.append(m.group(2).strip())
    items.append(m.group(3).strip())
    if len(items) < 3:
        return None
    # The first and last items absorb surrounding words, so only inner items are measured.
    if m.group(2) and any(len(x.split()) > NO_SERIAL_COMMA_MAX_WORDS for x in items[1:-1]):
        return None
    return items


def _lists(paragraphs: list[Paragraph], flags: list[Flag], metrics: dict, skipped: dict) -> None:
    sizes: list[int] = []
    triad_lines: list[int] = []
    for p in paragraphs:
        for s in p.sentences:
            for m in LIST_RE.finditer(s.text):
                items = _list_items(m)
                # Dates, years and author lists are not rhetorical triads.
                if (
                    items is None
                    or any(NUMERIC_ITEM_RE.match(x) or "et al" in x for x in items)
                    or CITATION_AFTER_RE.match(s.text[m.end() :])
                ):
                    continue
                sizes.append(len(items))
                if len(items) == 3:
                    triad_lines.append(s.line)
    share = round(sizes.count(3) / len(sizes), 3) if sizes else None
    metrics["lists"] = len(sizes)
    metrics["triad_share"] = share
    if len(sizes) < MIN_LISTS:
        skipped["triad_share"] = f"fewer than {MIN_LISTS} lists"
    elif share is not None and share >= HIGH_TRIAD_SHARE:
        flags.append(Flag("lists", f"{sizes.count(3)} of {len(sizes)} lists have exactly three items", triad_lines))


def _vocabulary(
    sentences: list[Sentence], words: int, flags: list[Flag], metrics: dict, house: dict[str, str] | None = None
) -> dict[str, list[int]]:
    hits: dict[str, list[int]] = {}
    # Evidence list first, then the house list, so a house phrase can never take an
    # evidence hit. Within each: phrases first, longest first; a word inside a matched
    # phrase is not counted again.
    def by_length(ws: object) -> list[str]:
        return sorted(ws, key=lambda w: (-len(w.split()), -len(w)))

    order = by_length(STYLE_WORDS) + by_length(w for w in (house or {}) if w not in STYLE_WORDS)
    texts = [s.text.replace("\u2019", "'") for s in sentences]
    for w in order:
        pat = _word_pattern(w)
        for idx, s in enumerate(sentences):
            def mask(m: re.Match[str], w: str = w, s: Sentence = s) -> str:
                hits.setdefault(w, []).append(s.line_of(m.start()))
                return "\x00" * len(m.group(0))

            texts[idx] = pat.sub(mask, texts[idx])
    evidence = {w: v for w, v in hits.items() if w in STYLE_WORDS}
    total = sum(len(v) for v in evidence.values())
    metrics["style_words"] = total
    metrics["style_words_per_1000"] = round(1000 * total / words, 2) if words else 0.0
    if total:
        flags.append(Flag("vocabulary", f"{total} stock style word(s), {len(evidence)} distinct; see table"))
    if house is not None:
        own = {w: v for w, v in hits.items() if w not in STYLE_WORDS}
        n = sum(len(v) for v in own.values())
        metrics["house_list_entries"] = len(house)
        metrics["house_words"] = n
        if n:
            flags.append(Flag("house", f"{n} house-list word(s), {len(own)} distinct (source H, a style rule); see table"))
    return hits


CLAUSE_SPLIT_RE = re.compile(r"[,;:()\[\]\u2014\u2013\"\u201c\u201d]| - ")


def _phrases(paragraphs: list[Paragraph], flags: list[Flag]) -> list[tuple[str, int, list[int]]]:
    where: dict[str, set[int]] = defaultdict(set)
    lines: dict[str, list[int]] = defaultdict(list)
    for pi, p in enumerate(paragraphs):
        for s in p.sentences:
            # Clauses of (start offset, token); n-grams do not cross punctuation.
            clauses: list[list[tuple[int, str]]] = [[]]
            prev_end = 0
            for m in WORD_RE.finditer(s.text):
                if clauses[-1] and CLAUSE_SPLIT_RE.search(s.text[prev_end : m.start()]):
                    clauses.append([])
                clauses[-1].append((m.start(), m.group(0).lower().replace("\u2019", "'")))
                prev_end = m.end()
            for toks in clauses:
                for n in range(3, 7):
                    for k in range(len(toks) - n + 1):
                        gram = [t for _, t in toks[k : k + n]]
                        if all(t in STOPWORDS for t in gram):
                            continue
                        key = " ".join(gram)
                        if pi not in where[key]:
                            where[key].add(pi)
                            lines[key].append(s.line_of(toks[k][0]))
    found = {k: v for k, v in where.items() if len(v) >= PHRASE_MIN_PARAGRAPHS}
    # keep the longest: drop a phrase contained in a longer one with the same reach
    keep = [
        k
        for k in found
        if not any(k != o and f" {k} " in f" {o} " and len(found[o]) >= len(found[k]) for o in found)
    ]
    keep.sort(key=lambda k: (-len(found[k]), -len(k)))
    result = [(k, len(found[k]), sorted(lines[k])) for k in keep[:15]]
    if result:
        flags.append(Flag("phrases", f"{len(result)} phrase(s) recur in {PHRASE_MIN_PARAGRAPHS}+ paragraphs; see table"))
    return result


def _openers(sentences: list[Sentence], flags: list[Flag]) -> list[tuple[str, int]]:
    c: Counter[str] = Counter()
    for s in sentences:
        toks = [t.lower() for t in WORD_RE.findall(s.text)[:2]]
        if len(toks) == 2:
            c[" ".join(toks)] += 1
    result = [(o, n) for o, n in c.most_common(10) if n >= OPENER_MIN]
    if result:
        flags.append(Flag("openers", f"{len(result)} sentence opener(s) used {OPENER_MIN}+ times; see table"))
    return result


def _template(sections: list[Section], flags: list[Flag], metrics: dict, skipped: dict) -> None:
    body = [s for s in sections if s.title != "(preamble)"] or sections
    metrics["template_features"] = 0
    if len(body) < MIN_SECTIONS:
        skipped["template_features"] = f"fewer than {MIN_SECTIONS} sections"
        return
    features: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for sec in body:
        paras = [p for p in sec.paragraphs if p.sentences]
        if not paras:
            continue
        first, last = paras[0], paras[-1]
        opening = " ".join(t.lower() for t in WORD_RE.findall(first.sentences[0].text)[:2])
        features[f'open with "{opening}"'].append((sec.title, first.line))
        label = LABEL_RE.match(last.text)
        if label:
            features[f'close with the label "{label.group(1).strip()}:"'].append((sec.title, last.line))
        if last.sentences[-1].text.rstrip(" *_\"'\u201d").endswith("?"):
            features["close on a question"].append((sec.title, last.line))
        if len(last.sentences) == 1 and len(paras) > 1:
            features["close with a one-sentence paragraph"].append((sec.title, last.line))
    n = len(body)
    shared = {
        k: v
        for k, v in features.items()
        if len(v) >= MIN_SECTIONS and (k.startswith("close with the label") or len(v) >= TEMPLATE_SHARE * n)
    }
    metrics["template_features"] = len(shared)
    for k, v in shared.items():
        flags.append(Flag("template", f"{len(v)} of {n} sections {k}", [line for _, line in v]))


# Dutch function words, for a positive non-English check on short texts.
DUTCH_STOPWORDS = frozenset(
    "de het een en van dat die zijn niet met voor op te aan er ook als maar om dan wat nog wel bij door naar uit zo wij ze".split()
)


def _stopword_shares(sentences: list[Sentence]) -> tuple[float, float, int]:
    toks = [t.lower() for s in sentences for t in WORD_RE.findall(s.text)]
    if not toks:
        return 0.0, 0.0, 0
    return sum(t in STOPWORDS for t in toks) / len(toks), sum(t in DUTCH_STOPWORDS for t in toks) / len(toks), len(toks)


def load_house_words(path: str | Path) -> dict[str, str]:
    """One word or phrase per line. A # at the line start or after a space starts a comment,
    so "c#" stays an entry."""
    out: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        w = " ".join(re.split(r"(?:^|\s)#", line, maxsplit=1)[0].lower().split())
        if w:
            out[w] = "H"
    return out


def scan(path: str | Path, house_words: dict[str, str] | None = None) -> ScanReport:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    notes: list[str] = []
    sections = parse(text, latex=p.suffix.lower() in LATEX_SUFFIXES, notes=notes)
    paragraphs = [pa for s in sections for pa in s.paragraphs if pa.sentences]
    sentences = [se for pa in paragraphs for se in pa.sentences]
    if not sentences:
        raise ValueError(f"no prose found in {p}")
    words = sum(s.words for s in sentences)
    flags: list[Flag] = []
    metrics: dict[str, float | int | None] = {}
    skipped: dict[str, str] = {}
    en, nl, ntok = _stopword_shares(sentences)
    # Short English texts (bullets, reference lists) have few function words, so the
    # share test needs enough words; a positive Dutch match works at any length.
    if nl > en or (ntok >= MIN_WORDS_FOR_LANGUAGE and en < MIN_ENGLISH_STOPWORD_SHARE):
        flags.append(
            Flag(
                "language",
                f"text looks non-English (English function words {en:.0%}); the contrast, list, vocabulary, "
                "phrase and house-word signals are English-only, so their zeros mean nothing here",
            )
        )
    for note in notes:
        flags.append(Flag("parse", note))
    _rhythm(sentences, flags, metrics, skipped)
    _paragraphs(paragraphs, flags, metrics, skipped)
    _contrast(sentences, words, flags, metrics)
    _dashes(sentences, words, flags, metrics, skipped)
    _lists(paragraphs, flags, metrics, skipped)
    vocab = _vocabulary(sentences, words, flags, metrics, house_words)
    phrases = _phrases(paragraphs, flags)
    openers = _openers(sentences, flags)
    _template(sections, flags, metrics, skipped)
    return ScanReport(
        path=str(p),
        words=words,
        sentences=len(sentences),
        paragraphs=len(paragraphs),
        sections=len(sections),
        metrics=metrics,
        flags=flags,
        vocabulary=vocab,
        phrases=phrases,
        openers=openers,
        not_evaluated=skipped,
        sources={w: STYLE_WORDS.get(w, "H") for w in vocab},
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Advisory formula-repetition scan (PROPOSED, DR-022).")
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--house-words", metavar="FILE", help="a project's own word list, one per line (source H)")
    args = ap.parse_args(argv)
    try:
        house = load_house_words(args.house_words) if args.house_words is not None else None
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: house list {args.house_words}: {exc}", file=sys.stderr)
        return 2
    try:
        report = scan(args.file, house)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report.to_dict(), indent=2) if args.json else report.to_markdown())
    return 0


if __name__ == "__main__":
    sys.exit(main())
