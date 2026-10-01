#!/usr/bin/env bash
# The review profile's invariants (.claude/review-profile.md, gitignored, read by the
# user-global review-changes skill). Four checks, each a past review finding:
#   1. every guarantee path's winning tier is HIGH (else its lens can never fire);
#   2. every HIGH pattern has at least one guarantee beneath it (else the lens has nothing to check);
#   3. a tier pattern whose base path is gitignored is listed in the profile's "Ignored paths"
#      table (else the row is scoped to files Step 1 never enumerates: decide, fold in or remove);
#   4. every Makefile target and every scripts/* file is named, in backticks, in the guarantee section.
# Matching: `**` crosses directories, `*` does not, a leading `/` is dropped (all paths are
# repo-relative); `?` and `[` are literal. The winning tier is the most specific matching
# pattern (most literal characters), the highest tier on a tie, as the profile states.
# A guarantee written as a glob is tested as a sample path (`**` -> two levels, `*` -> one
# name), so a guarantee broader than its HIGH pattern is a finding.
# Limits: check 3 asks git about the base path only (the text before the first `*`), so a
# pattern whose files are only partly ignored is not flagged; a pattern starting with `*`
# has no base and is reported as unchecked; a guarantee glob is one sample path, so a
# lower-tier carve-out inside it (`tests/fixtures/**` under `tests/**`) is not seen.
# Bullets and `## ` headings inside code fences are skipped.
# Usage: check-profile.sh [ROOT]   (default: this repo)
set -euo pipefail
root="${1:-$(CDPATH='' cd -- "$(dirname -- "$0")/.." >/dev/null && pwd -P)}"  # not git rev-parse: memory/ is its own repo
# Exit: 0 all four hold · 1 a finding · 2 cannot verify: no or unreadable profile, no HIGH
# row, no or empty guarantee section, no Makefile or no targets in it, no scripts/ directory,
# an unclosed code fence, not a git work tree, a failed `git check-ignore`, no `python3`,
# or a crash.
python3 - "$root" <<'EOF' || { rc=$?; [ "$rc" -le 2 ] || rc=2; exit "$rc"; }
import os, re, subprocess, sys

TIERS = ("HIGH", "MEDIUM", "LOW")  # highest first

def cannot(msg):
    print(f"CANNOT VERIFY: {msg}", file=sys.stderr)
    sys.exit(2)

def glob_re(pat):
    out, i = "", 0
    while i < len(pat):
        if pat.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pat[i] == "*":
            out, i = out + "[^/]*", i + 1
        else:
            out, i = out + re.escape(pat[i]), i + 1
    return re.compile(out + r"\Z")

def norm(p):
    return p.lstrip("/")

def sample(p):  # a concrete path a glob reaches, so a broader guarantee cannot hide behind its text
    return p.replace("**", "\0").replace("*", "n").replace("\0", "d1/d2")

def key(p):  # `audits/`, `audits/**` and `audits` name the same population
    p = norm(p)
    while p.endswith("/**") or p.endswith("/"):
        p = p[:-3] if p.endswith("/**") else p[:-1]
    return p

def unfence(text):  # blank out fenced blocks, keeping line count
    out, fence = [], None
    for line in text.split("\n"):
        m = re.match(r" {0,3}(`{3,}|~{3,})", line)
        if fence is None and m:
            fence = m.group(1)
            out.append("")
        elif fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            out.append("")
        else:
            out.append(line)
    if fence is not None:
        cannot("an unclosed code fence: the rest of the profile would be skipped")
    return "\n".join(out)

def section(text, heading):
    m = re.search(rf"^## (?:\W+\s*)?{heading}\b[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None

def main():
    root = sys.argv[1]
    prof = os.path.join(root, ".claude", "review-profile.md")
    try:
        with open(prof, encoding="utf-8") as h:
            text = unfence(h.read())
    except (OSError, UnicodeDecodeError) as e:
        cannot(f"{prof}: {e}")
    tiers = {}
    for t in TIERS:
        m = re.search(rf"^\| \*\*{t}\*\* \|([^|]*)\|", text, re.M)
        tiers[t] = [norm(p) for p in re.findall(r"`([^`]+)`", m.group(1))] if m else []
    if not tiers["HIGH"]:
        cannot("no HIGH row with backticked patterns in the tier table")
    gsec = section(text, "Guarantee surfaces")
    if gsec is None:
        cannot("no '## Guarantee surfaces' section")
    guarantees = [norm(p) for p in re.findall(r"^\s*[-*+] `([^`]+)`", gsec, re.M)]
    if not guarantees:
        cannot("the guarantee section lists no `- `path`` entries")
    findings = []
    rank = [(t, p, glob_re(p), len(re.sub(r"\*", "", p))) for t in TIERS for p in tiers[t]]

    def winner(path):
        hits = [(spec, -TIERS.index(t), t) for t, _, rx, spec in rank if rx.match(path)]
        return max(hits)[2] if hits else None

    for g in guarantees:
        w = winner(sample(g))
        if w != "HIGH":
            findings.append(f"guarantee `{g}` is tiered {w or 'nowhere'}, not HIGH: its lens can never fire")
    for t, p, rx, _ in rank:
        if t == "HIGH" and not any(rx.match(sample(g)) for g in guarantees):
            findings.append(f"HIGH pattern `{p}` has no guarantee beneath it: the lens has nothing to check")

    isec = section(text, "Ignored paths") or ""
    decided = {key(p) for p in re.findall(r"^\| `([^`]+)`", isec, re.M)}
    try:
        inside = subprocess.run(["git", "-C", root, "rev-parse", "--is-inside-work-tree"],
                                capture_output=True, text=True).stdout.strip()
    except OSError as e:
        cannot(f"git: {e}")
    if inside != "true":
        cannot(f"{root} is not a git work tree, so ignored patterns cannot be checked")
    ignored, unchecked = 0, []
    for t, p, _, _ in rank:
        base = key(p.split("*", 1)[0])
        if not base:
            unchecked.append(p)
            continue
        # Ask as a file and as a directory: a rule like `audits/` misses a bare `audits` that does not exist
        hit = False
        for q in ([base] if "*" not in p and not p.endswith("/") else []) + [base + "/"]:
            r = subprocess.run(["git", "-C", root, "check-ignore", "-q", "--", q])
            if r.returncode > 1:
                cannot(f"git check-ignore failed on `{q}` (pattern `{p}`)")
            hit = hit or r.returncode == 0
        if hit:
            ignored += 1
            if key(p) not in decided and base not in decided:
                findings.append(f"{t} pattern `{p}` is gitignored and not in the Ignored paths "
                                "table: decide, fold it into Step 1 or remove the row")

    try:
        with open(os.path.join(root, "Makefile"), encoding="utf-8") as h:
            mk = h.read()
    except (OSError, UnicodeDecodeError) as e:
        cannot(f"Makefile: {e}")
    mk = re.sub(r"^define\b.*?^endef\b", "", mk, flags=re.M | re.S)  # a define body is not a rule
    targets = sorted({n for line in re.findall(r"^([A-Za-z0-9][\w.-]*(?:[ \t]+[\w.-]+)*)[ \t]*::?(?![:=])", mk, re.M)
                      for n in line.split()})
    if not targets:
        cannot("no targets found in the Makefile")
    sdir = os.path.join(root, "scripts")
    if not os.path.isdir(sdir):
        cannot("no scripts/ directory")
    scripts = sorted(f for f in os.listdir(sdir)
                     if not f.startswith(".") and os.path.isfile(os.path.join(sdir, f)))
    for t in targets:
        if f"`{t}`" not in gsec:
            findings.append(f"Makefile target `{t}` is not named in the guarantee section")
    for s in scripts:
        if f"`{s}`" not in gsec and f"`scripts/{s}`" not in gsec:
            findings.append(f"scripts/{s} is not named in backticks in the guarantee section")

    print(f"profile: {len(tiers['HIGH'])} HIGH patterns, {len(guarantees)} guarantees, "
          f"{ignored} ignored patterns, {len(targets)} targets, {len(scripts)} scripts")
    for p in unchecked:
        print(f"UNCHECKED: `{p}` starts with a glob, so its ignore status was not asked")
    for f in findings:
        print(f"FINDING: {f}")
    if findings:
        print(f"{len(findings)} finding(s)")
        sys.exit(1)

try:
    main()
except SystemExit:
    raise
except Exception as e:  # a crash is "cannot verify", never exit 1 ("finding")
    cannot(f"crash: {type(e).__name__}: {e}")
EOF
