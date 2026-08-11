#!/usr/bin/env bash
# check-installed.sh — install Maestro into an empty directory and exercise the result.
#
# Why it exists: every other gate here measures the SOURCE repository, where every file the
# method mentions happens to exist. Nothing ever ran the installed copy. Two defects lived
# in that blind spot until a companion agent hit them in a real installation and reported
# them back:
#
#   * scripts/check-roles.sh shipped, and read docs/agents/README.md — which the installer
#     does not copy. Red on a clean install, for a file that was never sent.
#   * the vendored /speckit.* commands shipped, pointing at .specify/memory/constitution.md
#     — a path the installation does not create.
#
# Both are the same defect: WE SHIP A THING THAT POINTS AT SOMETHING WE DO NOT SHIP. That is
# anti-pattern 22 (the installed method as a lossy copy of the method), and no gate could
# see it, because every gate was looking at the repository where the target happens to exist.
#
# What this actually measures (anti-pattern 13): NOT that the method is good, and NOT that
# an AI will follow it. It measures that a fresh installation is COHERENT — every script it
# ships runs, and every path its shipped files name exists there.
#
# Usage:  scripts/check-installed.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
ok()   { printf '  ✓ %s\n' "$1"; }
bad()  { printf '  ✗ %s\n' "$1"; fail=1; }
note() { printf '  · %s\n' "$1"; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
TARGET="$TMP/projeto"
mkdir -p "$TARGET"

echo "── Installed copy: does the method work where it lands? ──"

# 1. The installation runs at all, into an empty directory.
if ! scripts/install-maestro.sh "$TARGET" >"$TMP/install.log" 2>&1; then
  bad "install-maestro.sh failed on an empty directory:"
  sed 's/^/      /' "$TMP/install.log" >&2
  echo "──"; echo "✗ the installation does not even run."; exit 1
fi
ok "installs into an empty directory"

# The installer prints the instruction block; a target without it is not installed at all
# (check-install.sh's own rule), so the fixture does what the next-steps text tells a human.
scripts/install-maestro.sh --block > "$TARGET/CLAUDE.md"
( cd "$TARGET" && git init -q 2>/dev/null || true )

# 2. Every script we shipped RUNS there. A gate that ships red is worse than one that does
#    not ship: it teaches the person who installed the method to ignore red.
shipped_scripts=()
while IFS= read -r s; do shipped_scripts+=("$(basename "$s")"); done \
  < <(find "$TARGET/scripts" -maxdepth 1 -name 'check-*.sh' 2>/dev/null | sort)
if [[ ${#shipped_scripts[@]} -eq 0 ]]; then
  bad "the installation shipped no check-*.sh — the ritual has no fitness function"
else
  for s in "${shipped_scripts[@]}"; do
    if ( cd "$TARGET" && "./scripts/$s" >"$TMP/$s.log" 2>&1 ); then
      ok "runs green on a fresh install: $s"
    else
      bad "ships red on a fresh install: $s"
      sed 's/^/      /' "$TMP/$s.log" | head -6 >&2
    fi
  done
fi

# 3. Every repository path named by a shipped file must EXIST in the installation.
#    This is the general form of both reported defects. Only paths that look like they
#    belong to this method are checked: an arbitrary path in prose is not a promise, but
#    `.specify/…`, `docs/governance/…`, `skills/…` and friends are.
# A file is "vendored verbatim" when .specify/UPSTREAM.md says so and does NOT list it as
# adapted. The provenance file is already the place where that is recorded (rule 2: declared
# divergence, never silent), so the gate reads it instead of keeping a second list.
UP="$ROOT/.specify/UPSTREAM.md"
is_vendored_verbatim() {  # $1 = path of the installed file
  local base row; base="$(basename "$1")"
  case "$1" in .specify/*|.claude/commands/speckit.*) ;; *) return 1 ;; esac
  # STRICT BY DEFAULT. The first version returned "verbatim" by ABSENCE, which handed a free
  # pass to every file Maestro itself wrote under .specify/ — including UPSTREAM.md, which
  # does not list itself, and every template of ours. A file earns the upstream's tolerance
  # only by SAYING SO in the provenance table (`UP:state=verbatim`); anything else is ours,
  # dangling citations included.
  row="$(grep -F "$base" "$UP" 2>/dev/null | head -1 || true)"
  [[ -n "$row" ]] || return 1
  grep -qF 'UP:state=verbatim' <<<"$row"
}

echo "── Paths promised by the shipped files ──"
mapfile -t shipped_files < <(cd "$TARGET" && find . -type f \
  \( -name '*.md' -o -name '*.sh' \) -not -path './.git/*' | sed 's|^\./||' | sort)
declare -A missing_by_path=()
for f in "${shipped_files[@]}"; do
  # Paths inside backticks, which is how this method writes them everywhere.
  while IFS= read -r p; do
    [[ -n "$p" ]] || continue
    case "$p" in
      .specify/*|.claude/*|docs/*|skills/*|evals/*|scripts/*) ;;
      *) continue ;;
    esac
    # A bare DIRECTORY under docs/ is a convention the method asks the project to follow —
    # `docs/adr/` is where THEIR decisions go, `docs/research/` is where their curator
    # writes. Promising a file is a promise; naming a folder they are meant to create is
    # not. The method's own machinery (.specify/, .claude/, skills/, scripts/, evals/) is
    # held to the strict rule, which is where `.specify/scripts/bash/` was caught.
    case "$p" in
      docs/*/) continue ;;
    esac
    # A directory reference (trailing slash) or a file: either must exist.
    [[ -e "$TARGET/${p%/}" ]] && continue
    # `specs/NNN-*/` and the cycle files are created per cycle, never by the installer.
    case "$p" in *'<'*|*'NNN'*|*'*'*) continue ;; esac
    # Two different defects, and the difference matters.
    #
    #  (a) The path exists HERE and not THERE: the installer did not send what its own files
    #      name. Always a defect — this is the reported one.
    #  (b) The path exists in NEITHER: the citation dangles everywhere. Tolerated ONLY when
    #      the file doing the citing is vendored VERBATIM — then it is the upstream CLI's
    #      artifact and belongs to .specify/UPSTREAM.md, not to us. In a file we wrote or
    #      adapted, a dangling citation is ours. Without this second rule, re-pointing a
    #      command back at `.specify/memory/constitution.md` would pass, which is the very
    #      defect this cycle fixed.
    if [[ ! -e "$ROOT/${p%/}" ]]; then
      # Declared upstream-optional paths are not our promise to keep, and the declaration
      # lives in the provenance file, in the open — never in a heuristic in here.
      grep -qF "UP:optional-path=${p%/}" "$UP" 2>/dev/null && continue
      is_vendored_verbatim "$f" && continue
    fi
    missing_by_path["$p"]+="$f "
  done < <(grep -oE '`[A-Za-z_.][A-Za-z0-9_./-]*\.(md|sh|json|jsonl|yml)`|`[A-Za-z_.][A-Za-z0-9_./-]*/`' "$TARGET/$f" 2>/dev/null | tr -d '`' || true)
done
if [[ ${#missing_by_path[@]} -eq 0 ]]; then
  ok "every method path named by an installed file exists there"
else
  for p in "${!missing_by_path[@]}"; do
    bad "installed files name '${p}', which the installation does not create — cited by: ${missing_by_path[$p]% }"
  done
fi

echo "──"
if [[ $fail -ne 0 ]]; then
  echo "✗ the installed copy is not coherent: it ships something that points at nothing."
  exit 1
fi
echo "✓ a fresh installation runs every gate it ships and names no path it does not create."
