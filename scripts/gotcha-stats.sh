#!/usr/bin/env bash
# Entry count and size of the gotcha log, so no document has to restate them.
# An entry is a `### ` heading up to the next same-or-shallower heading; the
# `## Promoted` and `## Mechanized` tables are not entries; a `#` inside a code fence is
# not a heading. Unit: characters.
set -euo pipefail
f="${1:-$(CDPATH='' cd -- "$(dirname -- "$0")/.." >/dev/null && pwd -P)/memory/gotcha-log.md}"  # not git rev-parse: memory/ is its own repo
[ -f "$f" ] && [ -r "$f" ] || { echo "CANNOT READ: $f" >&2; exit 2; }
# Exit: 0 counted · 1 no entries found · 2 unreadable log.
python3 - "$f" <<'EOF' || { rc=$?; [ "$rc" -le 2 ] || rc=2; exit "$rc"; }
import re, statistics, sys
try:
    lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
except (OSError, UnicodeDecodeError) as e:
    print(f"CANNOT READ: {e}", file=sys.stderr); sys.exit(2)
sizes, cur, fence = [], None, None
for l in lines:
    f = re.match(r" {0,3}(`{3,}|~{3,})", l)
    if f and (fence is None or (f.group(1)[0] == fence[0] and len(f.group(1)) >= len(fence))):
        fence = None if fence else f.group(1)
    m = None if fence or f else re.match(r"(#{1,3}) ", l)
    if m:
        if cur is not None:
            sizes.append(cur)
        cur = len(l) + 1 if len(m.group(1)) == 3 else None
    elif cur is not None:
        cur += len(l) + 1
if cur is not None:
    sizes.append(cur)
if fence:
    sys.exit("UNCLOSED CODE FENCE: every entry after it was absorbed; counts are not trustworthy")
if not sizes:
    sys.exit("NO ENTRIES found: the heading shape changed, or the file is empty")
over = sum(s > 3000 for s in sizes)
print(f"{len(sizes)} entries, median {int(statistics.median(sizes))} chars, "
      f"max {max(sizes)}, {over} over 3,000")
EOF
