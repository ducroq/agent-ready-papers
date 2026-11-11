#!/usr/bin/env bash
# Entry count and size of the gotcha log, so no document has to restate them.
# An entry is a `### ` heading up to the next same-or-shallower heading; the
# `## Promoted` and `## Mechanized` tables are not entries; a `#` inside a code fence is
# not a heading. Unit: characters. Entries without a `**Problem**` line are counted
# (thinned entries keep only `**Fix / rule**`), so /curate need not reconcile by hand.
# Only a `**Problem**` at the start of a line, outside a code fence, counts.
set -euo pipefail
f="${1:-$(CDPATH='' cd -- "$(dirname -- "$0")/.." >/dev/null && pwd -P)/memory/gotcha-log.md}"  # not git rev-parse: memory/ is its own repo
[ -f "$f" ] && [ -r "$f" ] || { echo "CANNOT READ: $f" >&2; exit 2; }
# HTML comments are skipped (a fence marker inside one is text); an inline comment is stripped before matching.
# Exit: 0 counted · 0 on zero entries only when the `## Promoted` heading is there AND nothing
#   suggests entries in another shape (outside a `### ` entry: no `####`+ heading, no `## ` heading
#   but Promoted / Mechanized / Lessons kept, no `**Problem` line in any punctuation or case) ·
#   1 otherwise on zero entries (the heading shape changed) · 2 unreadable log.
python3 - "$f" <<'EOF' || { rc=$?; [ "$rc" -le 2 ] || rc=2; exit "$rc"; }
import re, statistics, sys
try:
    lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
except (OSError, UnicodeDecodeError) as e:
    print(f"CANNOT READ: {e}", file=sys.stderr); sys.exit(2)
sizes, cur, fence = [], None, None
noprob, has_prob = 0, True
# Zero entries reads as a clean log only with evidence that no entry hides in another shape.
SECTIONS = re.compile(r"## (Promoted|Mechanized|Lessons kept\b.*)\s*")  # this log's known `## ` sections
PROBLEM = re.compile(r"\*\*problem\b", re.I)   # `**Problem**`, `**Problem.**`, `**Problem:**`
anchored = False  # a `## Promoted` heading: the file still has its known structure
stray = 0         # outside a `### ` entry: a `####`+ heading, an unknown `## ` heading, a Problem line
comment = False
for l in lines:
    if comment:  # inside an HTML comment everything is text, fence markers included
        comment = "-->" not in l
        continue
    vis = l
    if fence is None:
        vis = re.sub(r"<!--.*?-->", "", l)
        if "<!--" in vis:  # opens here, closes on a later line
            vis, comment = vis.split("<!--")[0], True
            if not vis.strip():
                continue
    f = re.match(r" {0,3}(`{3,}|~{3,})", vis)
    if f and (fence is None or (f.group(1)[0] == fence[0] and len(f.group(1)) >= len(fence))):
        fence = None if fence else f.group(1)
    m = None if fence or f else re.match(r"(#{1,3}) ", vis)
    if not fence and not f and cur is None and (
            re.match(r"#{4,} ", vis) or PROBLEM.match(vis)
            or (m and len(m.group(1)) == 2 and not SECTIONS.fullmatch(vis.rstrip()))):
        stray += 1
    if m:
        anchored = anchored or re.fullmatch(r"## Promoted\s*", vis) is not None
        if cur is not None:
            sizes.append(cur)
            noprob += not has_prob
        cur = len(l) + 1 if len(m.group(1)) == 3 else None
        has_prob = False
    elif cur is not None:
        cur += len(l) + 1
        has_prob = has_prob or (not fence and PROBLEM.match(vis) is not None)
if cur is not None:
    sizes.append(cur)
    noprob += not has_prob
if fence:
    sys.exit("UNCLOSED CODE FENCE: every entry after it was absorbed; counts are not trustworthy")
if not sizes and anchored and not stray:
    print("0 entries (clean log: every entry retired or promoted)")
    sys.exit(0)
if not sizes:
    sys.exit("NO ENTRIES: no `## Promoted` heading, or %d line(s) look like entries in another shape "
             "(a `####` or unknown `## ` heading, or a Problem line, outside a `### ` entry); "
             "the heading shape changed" % stray)
over = sum(s > 3000 for s in sizes)
print(f"{len(sizes)} entries, median {int(statistics.median(sizes))} chars, "
      f"max {max(sizes)}, {over} over 3,000, {noprob} without a **Problem** line")
EOF
