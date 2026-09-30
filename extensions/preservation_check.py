"""Preservation check: did a rewrite keep the source's numbers and certainty?

STATUS: PROPOSED under DR-023. Staged in extensions/ (the DR-018 precedent);
it is not a tools/ surface until DR-023 is Accepted.

DR-023 puts a translation step between agent prose and a human reader: a fresh
context rewrites a report or CHANGELOG entry so it can be read once. Rewriting
for plainness can make claims stronger (ducroq/agent-ready-papers#41). This
script is the word-level half of the check that follows each translation. It
compares a source text with its translation and reports:

  numbers     A number in the source that is missing from the translation, and
              a number in the translation that is not in the source (a new
              number may be invented). Presence only: two numbers that swap
              places ("3 failed, 4 passed" -> "4 failed, 3 passed") pass; that
              is Prompt C's job. Digits inside identifiers do not count:
              DR-022, L86, #41, S2-2, v4.0.0, commit hashes, code spans, paths
              and file names (a rate such as 12GB/s is a number, not a path).
              A unit stays with its number: 5ms != 50ms and 12GB != 16GB;
              "5 ms" == "5ms" for units of two or more letters, while s, m, h,
              g and x count only when attached. A minus sign stays too.
              "34,521" equals "34521", "7%" equals "7" (the unit can be lost
              unnoticed), "three" equals "3", and in the translation "first"
              equals "1st". "1.0" and "1", "85k" and "85,000", or "25" and
              "twenty-five", count as different. A source "0 X" survives when
              a translation sentence has "no", "none", "nothing" or "zero"
              within three words before a word starting with X's first five
              letters ("0 blockers" -> "nothing blocks").
  dates       ISO dates (2026-09-30) missing from the translation or new in it.
              Other date formats are read as plain numbers.
  tiers       Tier words from the Language Calibration table in
              templates/writing-guide.md (DR-002), read from that file at run
              time, so the bands follow the guide. Reported: a tier phrase that
              occurs fewer times in the translation than in the source, and a
              translation sentence whose tier word sits in a higher band than
              its closest source sentence (a hedge added to a sentence that had
              no tier word is not a rise). Also a document-level count of the
              words at each band or above, which does not depend on sentence
              matching and which a move down never raises.
  hedges      Hedge words outside the table ("might", "likely", "unverified"),
              when the translation has fewer of one than the source. Not part
              of DR-023's specification: added because the 2026-09-30 rewrite
              of the maintainer's memory files dropped "may be" and
              "unverified" without touching a table word.
  absolutes   Absolute words ("every", "never", "only", "exactly"), when the
              translation has more of one than the source; "all" and "every"
              count together. Also outside DR-023's specification, for the
              same reason as hedges.
  link        With --link TEXT, whether the translation contains TEXT (DR-023
              requires the translation to link to its source).

What it cannot see: an added claim with no number and no tier word. Both
2026-09-30 cases in #41 were that shape ("fits the course" became "works like
an instructor"). DR-023's second half, the claim comparison in a fresh
context (extensions/translation-prompts.md, Prompt C), exists for it. Every
report says so.

Known limits (why it reports and never gates):
  - Sentence matching is by shared content words. A heavily restructured
    translation can match a sentence to the wrong source sentence; the
    document-level band count is the backstop.
  - "shows" and "supports" are also ordinary verbs ("the table shows"). An
    ESTABLISHED or SUPPORTED word closely after a negation ("does not show")
    is skipped, except after phrases that assert ("not only", "no doubt",
    "without question"; see NOT_NEGATING). Hedges count even after a negation.
  - "May" with a capital, other than at the start of a sentence, or before a
    digit, is read as the month. "maybe" is in neither word list.
  - Sentences split at ". " before a capital, so "e.g. Smith" splits too.
  - "one" is not counted as a number (it is usually a pronoun).
  - English only.

Exit codes: 0 when a report was produced, flagged or not; 2 when an input or
the writing guide cannot be read, or the guide's table yields no bands.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

DEFAULT_GUIDE = Path(__file__).resolve().parent.parent / "templates" / "writing-guide.md"
TIER_ORDER = ("ESTABLISHED", "SUPPORTED", "EMERGING", "SPECULATIVE")

NUMBER_WORDS = {
    "zero": "0",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
    "thirty": "30",
    "forty": "40",
    "fifty": "50",
    "hundred": "100",
}
ORDINALS = {"first": "1", "second": "2", "third": "3", "fourth": "4", "fifth": "5", "tenth": "10"}
HEDGES = (
    "might",
    "could",
    "likely",
    "unlikely",
    "possibly",
    "perhaps",
    "probably",
    "appears",
    "appear",
    "seems",
    "seem",
    "suggests",
    "suggest",
    "suggested",
    "roughly",
    "approximately",
    "partly",
    "partially",
    "tentative",
    "tentatively",
    "provisional",
    "unverified",
    "unmeasured",
    "not yet",
    "at least",
    "at most",
    "rough",
    "estimated",
)
ABSOLUTES = (
    "every",
    "all",
    "always",
    "never",
    "none",
    "only",
    "entirely",
    "completely",
    "exactly",
    "guaranteed",
    "proves",
    "proven",
    "cannot",
    "impossible",
    "certainly",
)
# Words that swap for each other in a rewrite ("all references" -> "every reference") count together.
ABSOLUTE_GROUPS = [("every", "all")] + [(w,) for w in ABSOLUTES if w not in ("every", "all")]
NEGATION = re.compile(r"\b(?:not|no|never|cannot|n't)\W+(?:\w+\W+){0,2}$", re.I)
# Phrases that open with a negation word but assert: "no doubt it shows", "not only shows".
NOT_NEGATING = re.compile(
    r"\b(?:not\s+(?:only|just|merely|simply)|no\s+(?:doubt|question)|without\s+(?:doubt|question)"
    r"|(?:cannot|can't|can\s+not)\s+(?:deny|help\s+but)|never\s+fails?\s+to)\W+(?:\w+\W+){0,2}$",
    re.I,
)
SPACED_UNITS = "ms|mins?|secs?|hz|khz|mhz|ghz|kb|mb|gb|tb|mm|cm|km|kg|px"  # "5 ms" == "5ms"
UNITS = SPACED_UNITS + "|s|m|h|g|x|st|nd|rd|th"  # single letters only when attached: "5m", "2x"
STOPWORDS = set(
    "that this with from have been were what when which their there they them than then "
    "also into only more most such each some will would should could about these those "
    "does done over under after before because while where your ours".split()
)


@dataclass
class Flag:
    kind: str
    detail: str
    source_line: int | None = None
    translation_line: int | None = None


@dataclass
class Report:
    source: str
    translation: str
    flags: list[Flag] = field(default_factory=list)
    counts: dict = field(default_factory=dict)
    examined_nothing: bool = False


class GuideError(Exception):
    pass


# --- reading ---------------------------------------------------------------


def read_bands(guide: Path) -> dict[str, list[str]]:
    """Tier -> phrases, from the Language Calibration table. Fails closed."""
    try:
        text = guide.read_text(encoding="utf-8")
    except OSError as e:
        raise GuideError(f"cannot read writing guide {guide}: {e}") from e
    m = re.search(r"^## Language Calibration\s*$(.*?)(?=^#|\Z)", text, re.M | re.S)
    if not m:
        raise GuideError(f"no '## Language Calibration' section in {guide}")
    bands: dict[str, list[str]] = {}
    for line in m.group(1).splitlines():
        row = re.match(r"^\|\s*([A-Z]+)\s*\|(.*)\|\s*$", line)
        if row and row.group(1) in TIER_ORDER:
            phrases = re.findall(r'"([^"]+)"', row.group(2).split("|")[0])  # the Language column
            if not phrases:
                raise GuideError(f"tier {row.group(1)} has no quoted phrases in {guide}")
            bands[row.group(1)] = phrases
    if len(bands) != len(TIER_ORDER):
        raise GuideError(f"read {len(bands)} of {len(TIER_ORDER)} tiers from {guide}")
    return bands


def _word_pattern(word: str) -> str:
    """A table word plus its inflections: shows -> show, showed, shown, showing."""
    if len(word) <= 3:
        return re.escape(word)
    stem = word
    if stem.endswith("ed"):
        stem = stem[:-2]
    elif stem.endswith("s"):
        stem = stem[:-1]
    if stem.endswith("e"):
        stem = stem[:-1]
    stem = re.escape(stem).replace("z", "[sz]")
    return stem + r"(?:e|es|s|ed|d|ing|n)?"


def phrase_regex(phrase: str) -> re.Pattern:
    words = phrase.split()
    return re.compile(r"\b" + r"\s+".join(_word_pattern(w) for w in words) + r"\b", re.I)


# --- units -----------------------------------------------------------------


def _clean(line: str) -> str:
    line = re.sub(r"`[^`]*`", " ", line)  # code spans: paths, commands
    line = re.sub(r"https?://\S+", " ", line)  # URLs
    line = re.sub(r"<!--.*?-->", " ", line)
    line = re.sub(r"\]\([^)]*\)", "]", line)  # markdown link targets
    line = re.sub(r"(?<!\S)(?!\d[\d.,]*[A-Za-z]{0,4}/[A-Za-z]{1,4}\b)(?=\S*[A-Za-z])\S*/\S+", " ", line)  # bare paths
    line = re.sub(r"(?<!\S)\S*\.(?:md|py|tex|bib|txt|json|ya?ml|sh|pdf|html?)\b\S*", " ", line)  # file names
    return line


def units(text: str) -> list[tuple[int, str]]:
    """(line number, sentence) pairs. Table rows and list items are units too."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for n, raw in enumerate(text.splitlines(), 1):
        if raw.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence or re.match(r"^\s*\|?[\s:|-]+\|?\s*$", raw) and "-" in raw:
            continue
        line = _clean(raw).strip()
        if not line:
            continue
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z*\"(\[])", line):
            if part.strip():
                out.append((n, part.strip()))
    return out


def content_words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", s.lower()) if w not in STOPWORDS}


# --- numbers ---------------------------------------------------------------

_ID = re.compile(
    r"#\d+|\bv\d+(?:\.\d+)+\b|\b[A-Za-z]+[-_]?\d[\w-]*|\b\d+(?!(?i:"
    + UNITS
    + r")\b)[A-Za-z]{2,}\w*|\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,40}\b"
)
_DATE = re.compile(r"(?<![\w-])\d{4}-\d{2}-\d{2}(?![\w-])")  # not inside a file name
_NUM = re.compile(
    r"(?<![\w.])([-\u2212]?)(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?"
    r"(?:\s*(k\b|%)|\s?(" + SPACED_UNITS + r")\b|(" + UNITS + r")\b)?",
    re.I,
)


def numbers(s: str, words: bool = True) -> tuple[list[str], list[str]]:
    """(numbers, dates) in a cleaned unit. n=2 counts; k is kept (85k != 85)."""
    dates = _DATE.findall(s)
    s = _DATE.sub(" ", s)
    s = re.sub(r"\bn\s*=\s*(\d+)", r" \1 ", s)
    s = _ID.sub(" ", s)
    nums = []
    for m in _NUM.finditer(s):
        v = ("-" if m.group(1) else "") + m.group(2).replace(",", "") + (m.group(3) or "")
        if m.group(4) and m.group(4).lower() == "k":
            v += "k"
        unit = (m.group(5) or m.group(6) or "").lower()
        if unit and unit not in ("st", "nd", "rd", "th"):
            v += {"min": "mins", "sec": "secs"}.get(unit, unit)  # 5ms != 50ms, 12GB != 16GB
        nums.append(v)
    if words:
        nums += [NUMBER_WORDS[w] for w in re.findall(r"[a-z]+", s.lower()) if w in NUMBER_WORDS]
    return nums, dates


# --- tiers -----------------------------------------------------------------


def tier_hits(s: str, regexes: list[tuple[str, str, re.Pattern]]) -> list[tuple[str, str]]:
    """(tier, table phrase) for each non-negated, non-all-caps tier phrase in s."""
    hits = []
    for tier, phrase, rx in regexes:
        for m in rx.finditer(s):
            if m.group(0).isupper():
                continue  # a tier label, not language
            at_start = (
                re.fullmatch(r"[\s\-*+>#|_(\[\"']*(?:\d+[.)]\s*)?[*_]*", s[: m.start()].rsplit("|", 1)[-1]) is not None
            )
            if m.group(0) == "May" and (not at_start or re.match(r"\s*\d", s[m.end() :])):
                continue  # "in May", "May 2026": the month
            before = s[: m.start()]
            if _rank(tier) >= _rank("SUPPORTED") and NEGATION.search(before) and not NOT_NEGATING.search(before):
                continue  # "does not show" is no claim at that band; a hedge counts even after "not"
            hits.append((tier, phrase))
    return hits


def _rank(tier: str) -> int:
    return len(TIER_ORDER) - TIER_ORDER.index(tier)  # ESTABLISHED highest


def _count_words(units_: list[tuple[int, str]], vocab: tuple[str, ...]) -> Counter:
    c: Counter = Counter()
    for _, s in units_:
        low = s.lower()
        for w in vocab:
            c[w] += len(re.findall(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low))
    return c


# --- the check -------------------------------------------------------------


def check(
    source: str,
    translation: str,
    bands: dict[str, list[str]],
    link: str | None = None,
    source_name: str = "source",
    translation_name: str = "translation",
) -> Report:
    rep = Report(source=source_name, translation=translation_name)
    su, tu = units(source), units(translation)
    regexes = [(t, p, phrase_regex(p)) for t in TIER_ORDER for p in bands[t]]

    # numbers
    s_nums: dict[str, int] = {}
    s_dates: dict[str, int] = {}
    for n, s in su:
        nums, dates = numbers(s)
        for v in nums:
            s_nums.setdefault(v, n)
        for d in dates:
            s_dates.setdefault(d, n)
    t_all: set[str] = set()
    t_new: dict[str, int] = {}
    t_dates: dict[str, int] = {}
    for n, s in tu:
        nums, dates = numbers(s)
        t_all.update(nums)
        t_all.update(ORDINALS[w] for w in re.findall(r"[a-z]+", s.lower()) if w in ORDINALS)
        for d in dates:
            t_dates.setdefault(d, n)
        for v in nums:
            t_new.setdefault(v, n)
    zero_nouns = [m.group(1)[:5].lower() for _, s in su for m in re.finditer(r"(?<![\w.])0\s+([A-Za-z]{3,})", s)]
    for stem in zero_nouns:  # "0 blockers" -> "nothing blocks"
        if any(re.search(r"\b(?:no|none|nothing|zero)\b\W+(?:\w+\W+){0,2}" + re.escape(stem), s, re.I) for _, s in tu):
            t_all.add("0")
    for v, n in s_nums.items():
        if v not in t_all:
            rep.flags.append(Flag("number-missing", f"{v} is in the source but not the translation", source_line=n))
    for d, n in s_dates.items():
        if d not in t_dates:
            rep.flags.append(Flag("date-missing", f"{d} is in the source but not the translation", source_line=n))
    for d, n in t_dates.items():
        if d not in s_dates:
            rep.flags.append(Flag("date-new", f"{d} is in the translation but not the source", translation_line=n))
    for v, n in t_new.items():
        if v not in s_nums:
            rep.flags.append(
                Flag(
                    "number-new",
                    f"{v} is in the translation but not the source: check it is not invented",
                    translation_line=n,
                )
            )

    # tiers: phrase counts (missing), sentence bands (moved up), band totals (backstop)
    s_hits = {i: tier_hits(s, regexes) for i, (_, s) in enumerate(su)}
    t_hits = {i: tier_hits(s, regexes) for i, (_, s) in enumerate(tu)}
    s_phr = Counter(p for h in s_hits.values() for _, p in h)
    t_phr = Counter(p for h in t_hits.values() for _, p in h)
    for p, c in s_phr.items():
        if t_phr[p] < c:
            line = next(su[i][0] for i, h in s_hits.items() if any(q == p for _, q in h))
            rep.flags.append(
                Flag(
                    "tier-missing", f'"{p}" occurs {c}x in the source, {t_phr[p]}x in the translation', source_line=line
                )
            )
    s_words = [content_words(s) for _, s in su]
    for i, hits in t_hits.items():
        if not hits:
            continue
        tw = content_words(tu[i][1])
        best, score = None, 0.0
        for j, sw in enumerate(s_words):
            if tw and sw:
                sc = len(tw & sw) / min(len(tw), len(sw))
                if sc > score:
                    best, score = j, sc
        t_top = max(hits, key=lambda h: _rank(h[0]))
        if best is None or score < 0.2:
            if _rank(t_top[0]) >= _rank("SUPPORTED"):
                rep.flags.append(
                    Flag(
                        "tier-unmatched",
                        f'"{t_top[1]}" ({t_top[0]}) is in a sentence with no clear source sentence',
                        translation_line=tu[i][0],
                    )
                )
            continue
        src = s_hits[best]
        s_rank = max((_rank(t) for t, _ in src), default=0)
        if _rank(t_top[0]) > s_rank and (src or _rank(t_top[0]) >= _rank("SUPPORTED")):
            was = max(src, key=lambda h: _rank(h[0])) if src else None
            before = f'"{was[1]}" ({was[0]})' if was else "no tier word"
            rep.flags.append(
                Flag(
                    "tier-up",
                    f'"{t_top[1]}" ({t_top[0]}) where the closest source sentence has {before}',
                    source_line=su[best][0],
                    translation_line=tu[i][0],
                )
            )
    s_band = Counter(t for h in s_hits.values() for t, _ in h)
    t_band = Counter(t for h in t_hits.values() for t, _ in h)
    for k, t in enumerate(TIER_ORDER[:3]):  # words at this band or above: a move down never raises it
        s_n = sum(s_band[u] for u in TIER_ORDER[: k + 1])
        t_n = sum(t_band[u] for u in TIER_ORDER[: k + 1])
        if t == "EMERGING" and t_band["SPECULATIVE"] >= s_band["SPECULATIVE"]:
            continue  # more "may" with no fewer SPECULATIVE words is a new hedge, not a rise
        if t_n > s_n:
            rep.flags.append(
                Flag("band-count", f"words at {t} or above: {s_n} in the source, {t_n} in the translation")
            )

    # hedges and absolutes
    sh, th = _count_words(su, HEDGES), _count_words(tu, HEDGES)
    for w in HEDGES:
        if th[w] < sh[w]:
            rep.flags.append(Flag("hedge-missing", f'"{w}": {sh[w]}x in the source, {th[w]}x in the translation'))
    sa, ta = _count_words(su, ABSOLUTES), _count_words(tu, ABSOLUTES)
    for group in ABSOLUTE_GROUPS:
        s_n, t_n = sum(sa[w] for w in group), sum(ta[w] for w in group)
        if t_n > s_n:
            name = " / ".join(f'"{w}"' for w in group)
            rep.flags.append(Flag("absolute-added", f"{name}: {s_n}x in the source, {t_n}x in the translation"))

    if link is not None and link not in translation:
        rep.flags.append(Flag("link-missing", f"the translation does not contain the source link {link!r}"))

    rep.counts = {
        "source_numbers": len(s_nums),
        "source_dates": len(s_dates),
        "source_tier_words": sum(s_phr.values()),
        "source_hedges": sum(sh.values()),
        "source_units": len(su),
        "translation_units": len(tu),
    }
    rep.examined_nothing = not (s_nums or s_dates or s_phr or sum(sh.values()))
    return rep


# --- output ----------------------------------------------------------------

LABELS = {
    "number-missing": "Numbers that went missing",
    "date-missing": "Dates that went missing",
    "date-new": "Dates that appeared",
    "number-new": "Numbers that appeared",
    "tier-up": "Certainty that went up",
    "tier-unmatched": "Confident words without a matching source sentence",
    "band-count": "More confident words overall",
    "tier-missing": "Tier words that went missing",
    "hedge-missing": "Hedges that went missing",
    "absolute-added": "Absolute words that appeared",
    "link-missing": "Link to the source",
}
CLAIM_NOTE = (
    "This script cannot see an added claim that has no number and no tier word. "
    "Run the claim comparison (extensions/translation-prompts.md, Prompt C) as well."
)


def to_markdown(rep: Report) -> str:
    out = [f"# Preservation check: {rep.translation} against {rep.source}", ""]
    if rep.flags:
        out.append(
            f"**{len(rep.flags)} item(s) to check before the translation goes out.** "
            "Each is a possible change in meaning, not a verdict."
        )
    elif not rep.examined_nothing:
        out.append(
            "**Nothing flagged.** The script found no missing number, date, tier word or hedge, "
            "and no rise in certainty of the kinds it can detect."
        )
    if rep.examined_nothing:
        out.append(
            "The source has no numbers, dates, tier words or hedges, so the source-side checks examined nothing. "
            "Only the claim comparison can say whether the translation is faithful."
        )
    out += ["", CLAIM_NOTE, ""]
    for kind, label in LABELS.items():
        fl = [f for f in rep.flags if f.kind == kind]
        if not fl:
            continue
        out.append(f"## {label}")
        for f in fl:
            where = []
            if f.source_line:
                where.append(f"source line {f.source_line}")
            if f.translation_line:
                where.append(f"translation line {f.translation_line}")
            out.append(f"- {f.detail}" + (f" ({', '.join(where)})" if where else ""))
        out.append("")
    c = rep.counts
    out.append(
        f"Examined: {c['source_numbers']} numbers, {c['source_dates']} dates, {c['source_tier_words']} tier "
        f"words and {c['source_hedges']} hedges in {c['source_units']} source sentences."
    )
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Advisory preservation check for a translation (PROPOSED, DR-023).")
    ap.add_argument("source")
    ap.add_argument("translation")
    ap.add_argument("--guide", default=str(DEFAULT_GUIDE), help="writing guide holding the Language Calibration table")
    ap.add_argument("--link", help="text the translation must contain, such as the source's path or URL")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = ap.parse_args(argv)
    try:
        bands = read_bands(Path(args.guide))
        src = Path(args.source).read_text(encoding="utf-8")
        trn = Path(args.translation).read_text(encoding="utf-8")
    except (GuideError, OSError, UnicodeDecodeError) as e:
        print(f"preservation_check: {e}", file=sys.stderr)
        return 2
    rep = check(src, trn, bands, args.link, args.source, args.translation)
    if args.json:
        print(json.dumps(asdict(rep), indent=2))
    else:
        print(to_markdown(rep), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
