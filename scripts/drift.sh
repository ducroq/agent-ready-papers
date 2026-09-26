#!/usr/bin/env bash
# Session-start drift check. Mechanizes what /update-drift Steps 0-1 and 3 read by hand:
#   1. companion pin in CLAUDE.md vs the latest release tag in its clone, and the releases between
#   2. user-global skills byte-identical to the reference install AT THE PINNED TAG
#   3. this repo's stamp vs CHANGELOG.md; a TRACKED paper's pin behind it counts as drift,
#      an untracked sub-project's pin is only reported (a separate adopter's call)
# Triage stays with /update-drift; this only says whether there is anything to triage.
# Exit: 0 no drift · 1 drift · 2 cannot verify (no clone, fetch failed, pin tag missing, no stamp).
set -uo pipefail
R=$(git rev-parse --show-toplevel) || exit 2
FRAMEWORK=${FRAMEWORK:-$HOME/repos/agent-ready-projects}
rc=0
flag() { [ "$rc" -eq 2 ] || rc=$1; }
cant() { echo "CANNOT VERIFY: $*"; rc=2; }

P=$(command grep -oE 'agent-ready-projects\*\*: v[0-9]+\.[0-9]+\.[0-9]+' "$R/CLAUDE.md" | head -1 | command grep -oE 'v[0-9.]+$')
[ -n "$P" ] || { echo "CANNOT VERIFY: no companion stamp in CLAUDE.md"; exit 2; }
if [ ! -d "$FRAMEWORK/.git" ]; then
  cant "no companion clone at $FRAMEWORK (set FRAMEWORK=)"
else
  # Offline must not read as current: without a fetch the latest release is unknown.
  # Fetch BEFORE checking the pin, or a freshly bumped pin reads as missing.
  if ! git -C "$FRAMEWORK" remote get-url origin >/dev/null 2>&1; then cant "clone has no origin; the latest release is unknown"
  elif ! command -v timeout >/dev/null; then cant "timeout not on PATH; refusing an unbounded fetch"
  elif ! GIT_TERMINAL_PROMPT=0 timeout 30 git -C "$FRAMEWORK" fetch -q --tags 2>/dev/null; then
    cant "fetch failed; the latest companion release is unknown (comparing local tags only)"; fi
fi
if [ "$rc" -eq 2 ] && [ ! -d "$FRAMEWORK/.git" ]; then :
elif ! git -C "$FRAMEWORK" rev-parse -q --verify "refs/tags/$P" >/dev/null; then
  cant "pinned tag $P is not in the clone at $FRAMEWORK"
else
  tags=$(git -C "$FRAMEWORK" tag -l 'v[0-9]*' | sed '/-/d' | sort -V)
  latest=$(printf '%s\n' "$tags" | tail -1)
  gap=$(printf '%s\n' "$tags" | awk -v p="$P" 'f { printf "%s ", $0; n++ } $0 == p { f = 1 } END { printf "\n%d", n + 0 }')
  n=${gap##*$'\n'}; gap=${gap%$'\n'*}
  if [ "$n" -eq 0 ]; then echo "companion: pinned $P = latest local tag"
  else echo "companion: DRIFT pinned $P, latest $latest — $n release(s): $gap"
       echo "           triage with /update-drift"; flag 1; fi

  if ! inst=$(git -C "$FRAMEWORK" show "$P:scripts/install-global-skills.sh" 2>/dev/null); then
    cant "no installer at $P"
  else
    want=$(printf '%s\n' "$inst" | sed -n 's/^GLOBAL_SKILLS="\([^"]*\)".*/\1/p')
    set -f   # a `*` in the list must not glob
    k=0; same=0
    for s in $want; do
      k=$((k + 1)); i="$HOME/.claude/skills/$s/SKILL.md"
      if [ ! -f "$i" ]; then echo "skills: $s NOT INSTALLED"; flag 1; continue; fi
      if ! git -C "$FRAMEWORK" cat-file -e "$P:.claude/skills/$s/SKILL.md" 2>/dev/null; then
        cant "$s is not in $P"; continue; fi
      # Piped, not captured: $(...) strips trailing newlines and would hide a difference.
      if git -C "$FRAMEWORK" show "$P:.claude/skills/$s/SKILL.md" | cmp -s - "$i"; then same=$((same + 1))
      else echo "skills: DRIFT $s differs from $P"; flag 1; fi
    done
    set +f
    [ "$k" -gt 0 ] || cant "empty GLOBAL_SKILLS at $P"
    echo "skills: $same of $k global skills byte-identical to $P ($want)"
  fi
fi

S=$(command grep -oE 'agent-ready-papers\*\* \(this repo\): v[0-9]+\.[0-9]+\.[0-9]+' "$R/CLAUDE.md" | head -1 | command grep -oE 'v[0-9.]+$')
C=$(command grep -m1 -oE '^## v[0-9]+\.[0-9]+\.[0-9]+' "$R/CHANGELOG.md" | cut -c4-)
if [ -z "$S" ] || [ -z "$C" ]; then cant "self stamp '$S' or CHANGELOG top '$C' missing"
elif [ "$S" = "$C" ]; then echo "self: $S = CHANGELOG top"
else echo "self: DRIFT stamp $S, CHANGELOG top $C"; flag 1; fi

shopt -s nullglob
for f in "$R"/papers/*/CLAUDE.md; do
  d=${f#"$R"/}; d=${d%/CLAUDE.md}
  p=$(command grep -m1 -oE 'agent-ready-papers:\*\* v[0-9]+\.[0-9]+\.[0-9]+' "$f" | command grep -oE 'v[0-9.]+$')
  if git -C "$R" ls-files --error-unmatch "$f" >/dev/null 2>&1; then kind=tracked; else kind=sub-project; fi
  if [ -z "$p" ]; then echo "paper $d ($kind): NO STAMP"; flag 1
  elif [ "$p" = "$S" ]; then :
  elif [ "$kind" = tracked ]; then echo "paper $d (tracked): DRIFT pinned $p, framework $S"; flag 1
  else echo "paper $d (sub-project): pinned $p, framework $S — its own call"; fi
done
exit "$rc"
