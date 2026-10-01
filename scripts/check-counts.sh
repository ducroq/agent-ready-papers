#!/usr/bin/env bash
# Checks the counts the top CHANGELOG section states against the repo, so a stale
# number is caught before release instead of by a reader. Two claim shapes:
#   `path` … A → B characters   B must equal the file's character count now; the path
#                               is the nearest backticked token before the numbers
#   N tests                     a total: in an item where exactly one named `foo.py` has
#                               tests/test_foo.py, that file's collected tests;
#                               "suite went from A to N": all collected tests
# A number before "characters" or "tests", or after an arrow, that fits neither shape
# (an ASCII arrow, "added 5 tests", two files in one sentence) is UNPARSED: exit 2, so a
# reworded claim is caught in the shapes measured. Counts marked ~ are approximate.
# Limit: this narrows the class, it does not close it; a count in a shape neither scan
# knows (spelled out, a table cell) can still pass. The shapes were seeded by hand in
# review (2026-10-01); they are not yet a test file.
# Only the top `## ` section is read: older sections describe files that have moved on.
# Unit: Unicode characters, line endings kept, as `wc -m` in a UTF-8 locale.
set -euo pipefail
root="$(CDPATH='' cd -- "$(dirname -- "$0")/.." >/dev/null && pwd -P)"  # not git rev-parse: memory/ is its own repo
f="${1:-$root/CHANGELOG.md}"
[ -f "$f" ] && [ -r "$f" ] || { echo "CANNOT READ: $f" >&2; exit 2; }
# Exit: 0 every claim matches · 1 a claim is stale · 2 cannot verify (unreadable,
# no section, no claims, an unparsed claim, pytest collection failed, or a crash).
python3 - "$f" "$root" <<'EOF' || { rc=$?; [ "$rc" -le 2 ] || rc=2; exit "$rc"; }
import os, re, subprocess, sys
from collections import Counter

def cannot(msg):
    print(f"CANNOT VERIFY: {msg}", file=sys.stderr)
    sys.exit(2)

def main():
    path, root = sys.argv[1], sys.argv[2]
    p = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q", "--collect-only"],
                       cwd=root, capture_output=True, text=True)
    if p.returncode != 0:
        cannot("pytest collection failed")
    per_file = Counter(l.split("::")[0] for l in p.stdout.splitlines()
                       if re.match(r"tests/\S+\.py::", l))
    total = sum(per_file.values())
    if not total:
        cannot("no tests collected")

    lines = open(path, encoding="utf-8").read().split("\n")
    fence, comment, heads = None, False, []
    for i, l in enumerate(lines):
        m = re.match(r" {0,3}(`{3,}|~{3,})", l)
        if m and not comment and (fence is None or (m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence))):
            fence = None if fence else m.group(1)
        elif fence is None and not comment and l.startswith("## "):
            heads.append(i)
        if fence is None:
            s = re.sub(r"<!--.*?-->", "", l)
            if comment and "-->" in s:
                comment = False
            elif not comment and "<!--" in s:
                comment = True
    if not heads:
        cannot("no `## ` section")
    end = heads[1] if len(heads) > 1 else len(lines)
    title = lines[heads[0]][3:]

    # Items: a bullet with its continuation lines, or a paragraph.
    items, cur = [], []
    for l in lines[heads[0] + 1:end]:
        head = re.match(r"#{1,6} ", l)
        if not l.strip() or re.match(r"\s*([-*]|\d+\.) ", l) or head:
            if cur:
                items.append(" ".join(cur))
            cur = [l.strip()] if l.strip() and not head else []
        else:
            cur.append(l.strip())
    if cur:
        items.append(" ".join(cur))

    N = r"\d[\d,]*"
    B = r"(?<![\w.~,-])"  # not inside DR-021, v1.2, ~5, 1,2
    LABEL = re.compile(r"\b[A-Z][\w-]*\s+$")  # "Paper 1", "Step 0": a label, not a count
    items = [re.sub(r"(\*\*|__|\*|_|`)(~?\d[\d,.]*k?)\1", r"\2", it) for it in items]
    num = lambda s: int(s.replace(",", ""))
    loose = re.compile(B + r"\d[\d,.  ]*k?\s+(?:[A-Za-z+-]+\s+)?(?:characters|chars|tests?)\b"
                       r"|(?:→|->)\s*(?!~)\d")
    stale = checked = unparsed = 0
    for it in items:
        spans = []
        for m in re.finditer(rf"`([^`\s]+)`[^`]*?(?<![~\d,])({N}) → ({N}) characters", it):
            spans.append(m.span(2) + m.span(3)); checked += 1
            p_, b = m.group(1), num(m.group(3))
            fp = os.path.join(root, p_)
            if not os.path.isfile(fp):
                print(f"STALE  {p_}: claims {b:,} characters, not a file"); stale += 1; continue
            n = len(open(fp, encoding="utf-8", newline="").read())
            if n != b:
                print(f"STALE  {p_}: claims {b:,} characters, has {n:,}"); stale += 1
            else:
                print(f"ok     {p_}: {n:,} characters")
        for m in re.finditer(rf"\bsuite\b(?:[^.;]|\.(?=\d))*?\bfrom ({N})\b(?:[^.;]|\.(?=\d))*?\bto ({N})\b", it):
            spans.append(m.span()); checked += 1
            n = num(m.group(2))
            if n != total:
                print(f"STALE  test suite: claims {n}, collected {total}"); stale += 1
            else:
                print(f"ok     test suite: {total} tests")
        pys = {os.path.basename(x)[:-3] for x in re.findall(r"`([^`\s]+\.py)`", it)}
        targets = [f"tests/test_{x}.py" for x in pys if f"tests/test_{x}.py" in per_file]
        for m in re.finditer(rf"{B}({N}) tests\b", it):
            if any(a <= m.start(1) < b for s in spans for a, b in zip(s[::2], s[1::2])):
                continue
            if LABEL.search(it[:m.start(1)]):
                continue
            if len(targets) != 1 or re.search(r"(added|new|more|further|\+)\s*$", it[:m.start(1)]):
                continue  # left for the unparsed scan below
            spans.append(m.span(1)); checked += 1
            n, have = num(m.group(1)), per_file[targets[0]]
            if n != have:
                print(f"STALE  {targets[0]}: claims {n} tests, collected {have}"); stale += 1
            else:
                print(f"ok     {targets[0]}: {have} tests")
        for m in loose.finditer(it):
            d = re.search(r"\d", it[m.start():]).start() + m.start()
            if m.group(0)[0] in "→-" and not re.search(r"`[^`\s]+`", it):
                continue  # an arrow with no file named ("1 of 8 → 3 of 6")
            if LABEL.search(it[:d]):
                continue
            if not any(a <= d < b for s in spans for a, b in zip(s[::2], s[1::2])):
                print(f"UNPARSED  \"{it[max(0, m.start() - 30):m.end()].strip()}\"")
                unparsed += 1
    print(f"{title}: {checked} claims checked, {stale} stale, {unparsed} unparsed")
    if stale:
        sys.exit(1)
    if unparsed:
        cannot("reword each UNPARSED count into a checked shape, or mark it ~")
    if not checked:
        cannot("no count claims in the top section")

try:
    main()
except SystemExit:
    raise
except Exception as e:
    cannot(f"{type(e).__name__}: {e}")
EOF
