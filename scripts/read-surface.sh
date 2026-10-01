#!/usr/bin/env bash
# The read surface: characters in every `*.md` under memory/ and docs/work-items/,
# outside any archive/ folder. This is the set /curate Step 0 measures, so no document
# has to restate the number. Prints the total and each file over 10,000 characters,
# largest first. Budget: READ_SURFACE_BUDGET (default 100,000, the P25 target).
# Unit: Unicode characters, line endings kept, as `wc -m` in a UTF-8 locale.
# Usage: read-surface.sh [ROOT]   (default: this repo)
set -euo pipefail
root="${1:-$(CDPATH='' cd -- "$(dirname -- "$0")/.." >/dev/null && pwd -P)}"  # not git rev-parse: memory/ is its own repo
budget="${READ_SURFACE_BUDGET:-100000}"
case "$budget" in ''|*[!0-9]*) echo "CANNOT VERIFY: budget '$budget' is not a whole number" >&2; exit 2;; esac
[ -d "$root/memory" ] || [ -d "$root/docs/work-items" ] ||
  { echo "CANNOT VERIFY: neither memory/ nor docs/work-items/ under $root" >&2; exit 2; }
# Exit: 0 at or under budget · 1 over budget · 2 cannot verify (no surface or no files,
# an unreadable directory or file, a non-UTF-8 file, a bad budget, or a crash).
# Only regular files count, as with `find -type f`: symlinks, FIFOs and sockets are skipped.
python3 - "$root" "$budget" <<'EOF' || { rc=$?; [ "$rc" -le 2 ] || rc=2; exit "$rc"; }
import os, stat, sys

def cannot(msg):
    print(f"CANNOT VERIFY: {msg}", file=sys.stderr)
    sys.exit(2)

def walk_error(e):
    cannot(f"{e.filename}: {e.strerror}")

def main():
    root, budget = sys.argv[1], int(sys.argv[2])
    sizes = {}
    for top in ("memory", "docs/work-items"):
        t = os.path.join(root, top)
        if os.path.islink(t) or not os.path.isdir(t):
            continue  # as `find` without -L: a symlinked start point is not descended
        for d, dirs, files in os.walk(t, onerror=walk_error):
            dirs[:] = [x for x in dirs if x != "archive"]
            for f in files:
                p = os.path.join(d, f)
                if not f.endswith(".md"):
                    continue
                try:
                    if not stat.S_ISREG(os.lstat(p).st_mode):
                        continue  # as `find -type f`: no symlink, FIFO (open() would block), socket
                except OSError as e:
                    cannot(f"{p}: {e}")
                try:
                    with open(p, encoding="utf-8", newline="") as h:
                        sizes[os.path.relpath(p, root)] = len(h.read())
                except (OSError, UnicodeDecodeError) as e:
                    cannot(f"{p}: {e}")
    if not sizes:
        cannot("no *.md files outside archive/: nothing was measured")
    total = sum(sizes.values())
    print(f"read surface: {total:,} characters in {len(sizes)} files (budget {budget:,})")
    for p, n in sorted(sizes.items(), key=lambda kv: -kv[1]):
        if n > 10000:
            print(f"  {n:>7,}  {os.fsencode(p).decode('utf-8', 'replace')}")
    if total > budget:
        print(f"OVER BUDGET by {total - budget:,}")
        sys.exit(1)

try:
    main()
except SystemExit:
    raise
except Exception as e:  # a crash is "cannot verify", never exit 1 ("over budget")
    cannot(f"crash: {type(e).__name__}: {e}")
EOF
