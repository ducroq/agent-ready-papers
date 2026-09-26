#!/usr/bin/env bash
# List decision records grouped by the `status:` field in their frontmatter: the block between
# the first two `---` lines, opening before the first `## ` heading and closed.
# A status line in the body does not count; values are case-normalised (`accepted` = `Accepted`).
# Only Accepted DRs bind. Exit 1 if a DR has no frontmatter status, or none exist.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 2
shopt -s nullglob
files=(decisions/DR-*.md)
[ "${#files[@]}" -gt 0 ] || { echo "NO DRs found in decisions/"; exit 1; }
empty=0
for f in "${files[@]}"; do [ -s "$f" ] || { echo "NO STATUS (empty file): $f" >&2; empty=1; }; done
awk '
  # Portable (mawk, busybox): no ENDFILE, so a file is closed out when the next starts, and at END.
  # The frontmatter must OPEN before the first `## ` body heading and CLOSE; a status is committed only at the close.
  function done_file() { if (prev != "" && !ok) { print "NO STATUS: " prev > "/dev/stderr"; bad = 1 } }
  FNR == 1 { done_file(); prev = FILENAME; dashes = 0; ok = 0; s = ""; body = 0
             id = FILENAME; sub(/^.*\//, "", id); sub(/_.*/, "", id) }
  { sub(/\r$/, "") }
  /^## / { body = 1 }
  /^---[ \t]*$/ && dashes == 0 && !body { dashes = 1; next }
  /^---[ \t]*$/ && dashes == 1 { dashes = 2
    if (s != "") { ok = 1; v = toupper(substr(s, 1, 1)) tolower(substr(s, 2)); g[v] = g[v] (g[v] == "" ? "" : ", ") substr(id, 4) }
    next }
  dashes == 1 && s == "" && tolower($0) ~ /^status:/ {
    s = $0; sub(/^[^:]*:[ \t]*/, "", s); sub(/[ \t]*#.*$/, "", s); sub(/[ \t]+$/, "", s) }
  END { done_file(); for (v in g) printf "%-22s DR-%s\n", v, g[v] | "sort"; close("sort"); exit bad }
' "${files[@]}"
rc=$?; [ "$empty" -eq 0 ] || rc=1
echo "${#files[@]} DR files"
exit "$rc"
