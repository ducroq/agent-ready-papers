#!/usr/bin/env bash
# Build Paper 1's arXiv source package: papers/perspective/arxiv/ (gitignored).
#
# The preprint differs from the journal build (Learned Publishing Opinion) in three ways,
# all switched by \preprintmode in manuscript.tex: single spacing, no line numbers, and
# the abstract from abstract.tex. The version stamp (DR-026) is baked into the source,
# because arXiv compiles the paper itself and has no git. arXiv does not run BibTeX,
# so the package ships the .bbl. Comment-only lines are stripped (the registry anchors
# stay in the repository source); inline comments are kept.
#
# Output: arxiv/src/ (upload these files, or the tarball), arxiv/paper1-arxiv.tar.gz,
# and arxiv/manuscript.pdf, the PDF built from the package, to check before uploading.
# Refuses a dirty working tree (the stamp would say -dirty) unless ALLOW_DIRTY=1.
# Exit: 0 built, 1 build failed or the tree is dirty.
set -euo pipefail

# The root from this script's own path, not git rev-parse: memory/ is its own repo.
root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." >/dev/null && pwd -P)
paper="$root/papers/perspective"
out="$paper/arxiv"
src="$out/src"

v=$(git -C "$paper" describe --tags --dirty --match 'paper1-*' 2>/dev/null) ||
  v="untagged $(git -C "$paper" describe --always --dirty --match 'paper1-*' 2>/dev/null)"
case "$v" in
  *dirty*)
    if [ "${ALLOW_DIRTY:-0}" = 1 ]; then echo "warning: dirty tree, the stamp says so ($v)" >&2
    else echo "refusing: the working tree is dirty ($v); commit first, or set ALLOW_DIRTY=1 for a test build" >&2; exit 1; fi ;;
esac

rm -rf "$out"
mkdir -p "$src"

strip_comments() { [ -s "$1" ] || { echo "missing or empty: $1" >&2; exit 1; }; grep -v '^[[:space:]]*%' "$1" || true; }

{
  printf '%% Paper 1 preprint, built by scripts/paper1-arxiv.sh from %s\n' "$v"
  printf '\\def\\preprintmode{}\n\\def\\paperversion{%s}\n' "$v"
  strip_comments "$paper/manuscript.tex"
} >"$src/manuscript.tex"
strip_comments "$paper/abstract.tex" >"$src/abstract.tex"
cp "$paper/references.bib" "$out/references.bib"

# Build once with BibTeX to make the .bbl. Each step is checked on its own line: set -e
# is off inside a subshell on the left of ||, so that form would hide a failed step.
fail() { echo "build failed: $1 (log: $src/manuscript.log)" >&2; exit 1; }
cp "$out/references.bib" "$src/references.bib"
cd "$src"
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex >/dev/null || fail "pdflatex, first pass"
bibtex manuscript >/dev/null || fail "bibtex"
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex >/dev/null || fail "pdflatex, second pass"
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex >/dev/null || fail "pdflatex, third pass"
rm -f references.bib
cd - >/dev/null
[ -s "$src/manuscript.bbl" ] || fail "no manuscript.bbl; arXiv cannot build the references without it"
if grep -q 'undefined' "$src/manuscript.log"; then
  grep 'undefined' "$src/manuscript.log" >&2
  fail "undefined references or citations"
fi

mv "$src/manuscript.pdf" "$out/manuscript.pdf"
(cd "$src" && rm -f ./*.aux ./*.log ./*.out ./*.blg ./*.toc)
tar -czf "$out/paper1-arxiv.tar.gz" -C "$src" .

echo "version: $v"
echo "package: $out/paper1-arxiv.tar.gz ($(cd "$src" && ls | tr '\n' ' '))"
echo "check:   $out/manuscript.pdf"
