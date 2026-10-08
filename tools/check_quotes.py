"""Check that quoted phrases occur verbatim in a source's full text (issue #48).

A quote is checked word by word, after Unicode folding, so extraction noise does not produce false
misses (curly quotes and other punctuation, ligatures and six OCR substitutions, hyphenated words
split across lines, soft hyphens) while numbers, decimal marks and signs must match exactly (see
`normalise`). A quote found only by a lenient reading (a ':' read as '.', a footnote marker
dropped) is reported CHECK and counts as not found for the exit code. An elided quote ("A ... B",
text left out) is not matched as one: check its parts separately. Quotes
shorter than three words are refused. Two-column PDFs are tried
in both pdftotext reading orders and once split into columns. A scan without a text layer is reported as NO TEXT LAYER, never as
a miss.

    python -m tools.check_quotes SOURCE "quote one" "quote two"
    python -m tools.check_quotes SOURCE --quotes-file quotes.txt   # one quote per line
    python -m tools.check_quotes SOURCE "..." --json

SOURCE: .pdf (needs `pdftotext` from poppler), .epub, .txt, .md, .html/.xhtml.
Exit: 0 every quote found; 1 at least one quote not found or only found as CHECK; 2 a tooling error (source or quotes file
unreadable, no text layer, a quote under three words). A FOUND says the words and numbers occur in
that order, punctuation aside; it does not say they mean what the citing sentence claims. Pages: printed page numbers where the source carries them (epub page markers),
otherwise the PDF's own page index ("pdf p. N").
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.parse
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

# Characters NFKC leaves alone but OCR or typesetting substitutes for letters.
_FOLD = str.maketrans({"®": "fi", "ß": "ss", "æ": "ae", "œ": "oe", "ø": "o", "ł": "l"})
MIN_CHARS_PER_PAGE = 200  # a page under this is near-empty; most pages near-empty means a scan


_INVISIBLE = re.compile("[\u00ad\u200b\u200c\u200d\ufeff]")  # soft hyphen, zero-width spaces
_SUPERSCRIPT = str.maketrans("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u207b",
                             "0123456789\u2212")
_NUMBER = r"[\u2027]?[^\W_]+(?:[\u2027\u02cc\u02d0][^\W_]+)*"
_NOT = "\ue000"  # a negating overlay (U+0338) left over after composition


def _is_sign(ch: str) -> bool:
    return unicodedata.category(ch) == "Sm" or ch in "~%\u00b0" or ch == _NOT


def normalise(text: str, lenient: bool = False) -> str:
    """Word, number and sign tokens joined by single spaces, lowercased, extraction noise folded.

    Word boundaries are kept, so "the rapist" does not match "therapist". A hyphen inside a word,
    or at a line end before the rest of the word, is removed in both quote and source. Numbers keep
    their marks inside the token: a `.` decimal (also a leading ".45"), a `,` before three digits
    (thousands) and a `:` (ratio) are three different marks, so "48.5", "4.85", "1,000", "1.000"
    and "3:1" all differ. An exponent is its own token ("10⁶", "10^6" and a PDF's "10 6" all read
    "10 6", never "106"). Every Unicode maths symbol, `~`, `%` and `°` is a token, a negating
    overlay (LaTeX's "≠" extracted as "̸=") is recomposed, `!=` is "≠", and a minus is read from
    context (a dash before a number, not after a digit), so "p < 0.05" does not match "p > 0.05",
    "r = -.45" does not match "r = .45", and a range "279–296" stays a range.

    `lenient` (reported as CHECK, never FOUND) also reads `:` between digits as a decimal point
    (OCR), drops a 1-3 digit footnote marker glued to a word ("model12"), and joins "11, 000".
    """
    text = _INVISIBLE.sub("", text)
    text = re.sub(r"\u0338\s*(\S)", "\\1\u0338", text)  # overlay extracted before its sign
    text = unicodedata.normalize("NFC", text).replace("!=", "\u2260").replace("*", "\u2217")
    text = re.sub(r"[\u2070\u00b9\u00b2\u00b3\u2074-\u2079\u207b]+",
                  lambda m: " " + m.group(0).translate(_SUPERSCRIPT) + " ", text)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"([^\W\d_])[-\u2010\u2011][ \t]*\n\s*([^\W\d_])", r"\1\2", text)
    text = re.sub(r"([^\W\d_])[-\u2010\u2011]([^\W\d_])", r"\1\2", text)
    text = re.sub(r"(?<=\d)(\s*)[-\u2013](\s*)(?=\d)", " ", text)  # a range between numbers, first
    # A dash before a number is a minus unless the last non-space character is a digit, letter or
    # closing bracket (then it is a range or a hyphen).
    text = re.sub(r"(?<![\w)\]])(\s*)[-\u2013\u2212](?=\.?\d)", "\\1 \u2212 ", text)
    if lenient:
        text = re.sub(r"(?<=[^\W\d_]{3})\d{1,3}\b", "", text)  # footnote marker glued to a word
        text = re.sub(r"(?<=\d), (?=\d{3}(?!\d))", ",", text)
    text = text.lower().translate(_FOLD)
    text = unicodedata.normalize("NFKD", text).replace("\u0338", f" {_NOT} ")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"(?<![\w\u2027])\.(?=\d)", "\u2027", text)  # leading-dot decimal ".45"
    text = re.sub(r"(?<=\d)\.(?=\d)", "\u2027", text)
    text = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "\u02cc", text)
    text = re.sub(r"(?<=\d):(?=\d)", "\u2027" if lenient else "\u02d0", text)
    out = []
    for m in re.finditer(_NUMBER + r"|\S", text):
        tok = m.group(0)
        if tok[0].isalnum() or tok[0] == "\u2027" or _is_sign(tok):
            out.append(tok)
    return " ".join(out)


MIN_QUOTE_WORDS = 3  # shorter quotes match by accident too easily to certify anything
TEXT_SUFFIXES = (".txt", ".md", ".html", ".xhtml", ".htm")  # shorter quotes match by accident too easily to certify anything


@dataclass
class Page:
    label: str  # "p. 23" (printed) or "pdf p. 4"
    text: str


@dataclass
class Result:
    quote: str
    found: bool
    page: str | None
    context: str | None
    note: str | None = None


Word = tuple[float, float, float, str]  # xMin, xMax, yMin, text


def columns_text(words: list[Word], page_width: float) -> str:
    """Read one page's words column by column (two- and three-column articles).

    Gutters are vertical strips that few words cover (at most 8% of the busiest strip, so a title
    or footer across the page does not hide them), at least 4 pt wide, between 10% and 90% of the
    page width. Words go to the column their midpoint falls in, then are read top to bottom.
    """
    if not words:
        return ""
    w = int(page_width) + 1
    cover = [0] * w
    for x0, x1, _, _ in words:
        for x in range(max(0, int(x0)), min(w, int(x1) + 1)):
            cover[x] += 1
    limit = 0.08 * max(cover)
    cuts, start = [], None
    for x in range(int(0.1 * w), int(0.9 * w) + 1):
        if cover[x] <= limit:
            start = x if start is None else start
        else:
            if start is not None and x - start >= 4:
                cuts.append((start + x) // 2)
            start = None
    bounds = [0.0, *cuts, float(w)]
    out = []
    for lo, hi in zip(bounds, bounds[1:], strict=False):
        col = sorted((y, x0, t) for x0, x1, y, t in words if lo <= (x0 + x1) / 2 < hi)
        lines: list[list[tuple[float, str]]] = []
        line_y = None
        for y, x0, t in col:  # words within 3 pt of a line's first word share the line
            if line_y is None or y - line_y > 3:
                lines.append([])
                line_y = y
            lines[-1].append((x0, t))
        out.append("\n".join(" ".join(t for _, t in sorted(line)) for line in lines))
    return "\n".join(out)


def _attach_overlays(words: list[Word]) -> list[Word]:
    """Put a combining-only glyph (LaTeX's negating slash in "≠") in front of the word it overlaps.

    In word-position output the overlay is a word of its own, which sorting by position can move
    past the sign it negates ("= 0 ̸" instead of "̸= 0"), turning "≠" into "=".
    """
    marks = [w for w in words if w[3] and all(unicodedata.combining(ch) for ch in w[3])]
    rest = [w for w in words if w not in marks]
    for x0, x1, y, t in marks:
        # A zero-width overlay sits at its sign's left edge, so a touching interval counts.
        near = [(min(x1, b) - max(x0, a), k) for k, (a, b, yy, _) in enumerate(rest) if abs(yy - y) < 4]
        best = max(near, default=(-1.0, -1))
        if best[1] >= 0 and best[0] >= 0:
            a, b, yy, tt = rest[best[1]]
            rest[best[1]] = (a, b, yy, t + tt)
        else:
            rest.append((x0, x1, y, t))
    return rest


def _pdf_column_pages(path: Path) -> list[Page]:
    args = ["pdftotext", "-bbox", str(path), "-"]
    out = subprocess.run(args, capture_output=True, text=True, check=True).stdout  # noqa: S603 -- fixed argv, no shell
    # A negating overlay right after a tag's ">" composes with it ("≯"), hiding the word from the
    # parser; decomposing splits it back into ">" and the overlay. Text is recomposed in normalise.
    out = unicodedata.normalize("NFD", out)
    pages = []
    for i, m in enumerate(re.finditer(r'<page width="([\d.]+)"[^>]*>(.*?)</page>', out, re.S)):
        words = [(float(a), float(c), float(b), html.unescape(t)) for a, b, c, t in
                 re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="[\d.]+">(.*?)</word>',
                            m.group(2))]
        pages.append(Page(f"pdf p. {i + 1}", columns_text(_attach_overlays(words), float(m.group(1)))))
    return pages


def _pdf_pages(path: Path, layout: bool) -> list[Page]:
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext not found (install poppler-utils)")
    args = ["pdftotext"] + (["-layout"] if layout else []) + [str(path), "-"]
    out = subprocess.run(args, capture_output=True, text=True, check=True).stdout  # noqa: S603 -- fixed argv, no shell
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]  # pdftotext ends the last page with a form feed
    return [Page(f"pdf p. {i + 1}", t) for i, t in enumerate(pages)]


_PAGEBREAK = re.compile(
    r'<[^>]*(?:epub:type="pagebreak"|role="doc-pagebreak"|id="page[-_]?\d+")[^>]*>', re.I
)
_PAGENUM_LABEL = re.compile(r'(?:aria-label|title)="\s*(?:page\s*)?(\d+|[ivxlc]+)\b[^"]*"', re.I)
_PAGENUM_ID = re.compile(r'id="(?:[^"]*?[-_ ])?(?:page[-_ ]?|p)?(\d+|[ivxlc]+)"', re.I)


def _html_to_pages(markup: str, start: str) -> tuple[list[Page], str]:
    """Split one (x)html document at page markers; returns pages and the label the next file starts on."""
    pages, label, pos = [], start, 0
    for m in _PAGEBREAK.finditer(markup):
        pages.append(Page(label, markup[pos:m.start()]))
        n = _PAGENUM_LABEL.search(m.group(0)) or _PAGENUM_ID.search(m.group(0))
        label = f"p. {n.group(1)}" if n else (label if label.startswith("after ") else f"after {label}")
        pos = m.end()
    pages.append(Page(label, markup[pos:]))
    for p in pages:
        p.text = html.unescape(re.sub(r"<[^>]+>", " ", p.text))
    return [p for p in pages if p.text.strip()], label


def _epub_pages(path: Path) -> list[Page]:
    with zipfile.ZipFile(path) as z:
        opf_name = next(n for n in z.namelist() if n.endswith(".opf"))
        opf = z.read(opf_name).decode("utf-8", "ignore")
        base = opf_name.rsplit("/", 1)[0] + "/" if "/" in opf_name else ""
        items = {}
        for tag in re.findall(r"<item\b[^>]*>", opf):
            i, h = re.search(r'id="([^"]+)"', tag), re.search(r'href="([^"]+)"', tag)
            if i and h:
                items[i.group(1)] = h.group(1)
        pages = []
        for idref in re.findall(r'<itemref[^>]*idref="([^"]+)"', opf):
            name = posixpath.normpath(base + urllib.parse.unquote(items.get(idref, "")))
            if name not in z.namelist():
                print(f"warning: spine item {idref!r} ({name}) not in the epub; skipped", file=sys.stderr)
            else:
                # Text before a file's first page marker is labelled by the file, never by the
                # previous file's last page; a book without markers is labelled file by file.
                start = f"{name.rsplit('/', 1)[-1]}, before its first page marker"
                new, _ = _html_to_pages(z.read(name).decode("utf-8", "ignore"), start)
                pages += new
        return pages


def load(path: Path) -> list[list[Page]]:
    """Every reading of the source worth trying, each a list of pages."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return [_pdf_pages(path, layout=False), _pdf_pages(path, layout=True), _pdf_column_pages(path)]
    if suffix == ".epub":
        return [_epub_pages(path)]
    if suffix not in TEXT_SUFFIXES:
        raise RuntimeError(f"unsupported file type {suffix or '(none)'}; convert it to .txt or .epub first")
    text = path.read_text(encoding="utf-8", errors="ignore")
    if suffix in (".html", ".xhtml", ".htm"):
        return [_html_to_pages(text, "page 1")[0]]
    return [[Page("text", text)]]


def has_text_layer(readings: list[list[Page]]) -> bool:
    """False when at least two thirds of pages carry almost no text: a scan, even with a text cover.

    A partial scan passes this test; its thin pages are then listed with any miss."""
    pages = readings[0]
    if not pages:
        return False
    thin = sum(len(normalise(p.text)) < MIN_CHARS_PER_PAGE for p in pages)
    return thin < (2 / 3) * len(pages)


def _search(target: str, pages: list[Page], lenient: bool) -> tuple[Page, str] | None:
    """Find target in the pages read as one text; return the page the match starts on."""
    norm = [(p, normalise(p.text, lenient)) for p in pages]
    norm = [(p, n) for p, n in norm if n]  # an empty page (a full-page figure) adds no gap
    joined = " " + " ".join(n for _, n in norm) + " "
    i = joined.find(" " + target + " ")
    if i < 0:
        return None
    offset = 1
    for page, n in norm:
        if i < offset + len(n):
            return page, n
        offset += len(n) + 1
    return None


def find(quote: str, readings: list[list[Page]]) -> Result:
    for lenient in (False, True):
        target = normalise(quote, lenient)
        if not target:
            return Result(quote, False, None, None)
        for pages in readings:
            hit = _search(target, pages, lenient)
            if hit:
                page = hit[0]
                flat = re.sub(r"\s+", " ", page.text).strip()
                words = sorted(re.findall(r"\w{4,}", quote), key=len, reverse=True)
                anchor = flat.lower().find(words[0].lower()) if words else -1
                at = max(0, anchor - 80) if anchor >= 0 else 0
                note = ("matched only leniently (a ':' read as '.', a footnote marker dropped, or"
                        " '11, 000' joined); check the page") if lenient else None
                return Result(quote, True, page.label, flat[at:at + 220], note)
    return Result(quote, False, None, None)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", type=Path)
    ap.add_argument("quotes", nargs="*")
    ap.add_argument("--quotes-file", type=Path, help="one quote per line; blank lines ignored")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    quotes = list(a.quotes)
    if a.quotes_file:
        try:
            lines = a.quotes_file.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as e:
            print(f"CANNOT READ {a.quotes_file}: {e}", file=sys.stderr)
            return 2
        quotes += [q.strip() for q in lines if q.strip()]
    if not quotes:
        ap.error("give at least one quote, or --quotes-file")
    short = [q for q in quotes if len(normalise(q).split()) < MIN_QUOTE_WORDS]
    if short:
        for q in short:
            print(f"TOO SHORT (fewer than {MIN_QUOTE_WORDS} words): {q}", file=sys.stderr)
        return 2
    try:
        readings = load(a.source)
    except (OSError, RuntimeError, subprocess.CalledProcessError, StopIteration, zipfile.BadZipFile) as e:
        print(f"CANNOT READ {a.source}: {e}", file=sys.stderr)
        return 2
    if a.source.suffix.lower() == ".pdf" and not has_text_layer(readings):
        print(f"NO TEXT LAYER in {a.source}: a scan; read the page images instead", file=sys.stderr)
        return 2
    results = [find(q, readings) for q in quotes]
    if a.json:
        print(json.dumps([asdict(r) for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            if r.found and r.note:
                print(f"CHECK    [{r.page}] {r.quote}  ({r.note})")
            elif r.found:
                print(f"FOUND    [{r.page}] {r.quote}")
            else:
                print(f"MISSING  {r.quote}")
        thin = [p.label for p in readings[0] if len(normalise(p.text)) < MIN_CHARS_PER_PAGE]
        if a.source.suffix.lower() == ".pdf" and thin and not all(r.found and not r.note for r in results):
            print(f"note: {len(thin)} page(s) have little or no text and may be scans, not searched in"
                  f" effect: {', '.join(thin[:12])}{' ...' if len(thin) > 12 else ''}")
        print(f"{sum(r.found and not r.note for r in results)} of {len(results)} found in {a.source.name}")
    return 0 if all(r.found and not r.note for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
