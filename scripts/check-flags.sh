#!/usr/bin/env bash
# check-flags.sh — a flag that exists is documented, and a documented flag exists.
#
# Why it exists: asked "how do I install the Maestro?", the recipe answered with `--forcar`,
# a flag that does not exist (it is `--force`), and the installer's own `# Usage` header —
# the first thing anyone reads when opening the file — never learned about `--ai`,
# `--no-hooks` or `--write-block`, added two cycles earlier. Three lies, all of the family
# this method chases: one fact in two places with nothing comparing them (cycle 058).
#
# What this actually measures (anti-pattern 13): NOT that the documentation is good. It
# measures that the SET of flags the parser accepts and the SET of flags the prose promises
# are the same set. Both directions fail, because both directions hurt: an undocumented flag
# is invisible, and a documented flag that does not exist is an error someone will type.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
ok()  { printf '  ✓ %s\n' "$1"; }
bad() { printf '  ✗ %s\n' "$1"; fail=1; }

# Flags a `case` arm accepts: `--foo)` and `--foo=*)`, alone or in a `|` list. Never `-*)`,
# which is the catch-all that REFUSES unknown flags, and never `-h`-style short aliases of a
# long flag already listed.
parser_flags() {  # $1 = script
  # Any `case` arm that starts with a dash and ends in `)`, minus the `-*)` catch-all (which
  # REFUSES unknown flags rather than accepting one). Every `--long` on the line counts, so an
  # arm like `--yes|-y)` is read correctly — the first version of this regex missed it and
  # reported `--yes` as documented-but-not-accepted, which was the gate lying about itself.
  # A REAL case arm has no spaces in the pattern: `--ai)`, `--yes|-y)`, `--ai=*)`. Allowing
  # anything up to the first `)` matched PROSE inside the usage heredoc — lines like
  # "--ai <id>   which agent (see `maestro agents`)" were read as parser arms, so any invented
  # flag documented on a parenthesised line cancelled itself out and the gate stayed green
  # (independent review of cycle 058).
  grep -oE '^[[:space:]]*["a-zA-Z0-9|=*_-]+\)' "$1" \
    | grep -v -- '-\*)' \
    | grep -oE '\-{1,2}[A-Za-z0-9][A-Za-z0-9_-]*' | sort -u
}

# Flags the prose promises, inside a given range of a file.
# Flags that belong to OTHER commands quoted in our documentation. A prose document cannot be
# parsed for "which command does this flag belong to", so the exception is DECLARED here — one
# line each, visible — instead of being hidden in a looser regex. The list growing is itself a
# signal: it means the docs are quoting more foreign commands than they explain our own.
#   -s   → `ln -s CLAUDE.md AGENTS.md`, the one-source tip in the recipe
FOREIGN_FLAGS='^(-s)$'

documented_flags() {  # stdin = text
  # A flag in prose starts a WORD. Matching a dash anywhere turned `instá-los`, `qa-report`,
  # `comece-por-aqui` and `set -euo` into "documented flags that do not exist" — the gate
  # drowning in its own false positives. Short flags count (`-y`, `-h`), which is why the
  # boundary has to be explicit rather than "two dashes".
  grep -oE '(^|[[:space:]`"'"'"'(])-{1,2}[A-Za-z][A-Za-z0-9_-]*' \
    | grep -oE '\-{1,2}[A-Za-z][A-Za-z0-9_-]*' | grep -vE "$FOREIGN_FLAGS" | sort -u
}

# Two directions, and they do not apply to the same documents.
#
#   REFERENCE text (`# Usage`, `usage()`) is the command's own contract: BOTH directions —
#   a flag it accepts must be listed, and a flag it lists must exist.
#
#   PROSE (the recipe, the front page) shows a SUBSET on purpose, and legitimately mentions
#   more than one command. Demanding that a front page document every flag would force it to
#   become the reference. So prose is checked in ONE direction: every flag it names must
#   exist somewhere. That is the direction that produced lie #1 — `--forcar`, in prose, in a
#   parser nowhere — and it is the one that costs a reader an error message.
#
# Splitting them is not a weakening: the first version demanded both directions everywhere,
# which forced either a bloated front page or an exception list nobody would maintain.

reference_check() {  # $1 = script, $2 = human name, $3 = its reference text
  local script="$1" name="$2" doc="$3" have want missing extra
  [[ -f "$doc" ]] || { bad "${name}: reference text missing (${doc})"; return 0; }
  have="$(parser_flags "$script" || true)"
  want="$(documented_flags <"$doc" || true)"
  missing="$(comm -23 <(echo "$have") <(echo "$want") || true)"
  extra="$(comm -13 <(echo "$have") <(echo "$want") || true)"
  while read -r f; do [[ -n "$f" ]] && bad "${name}: '${f}' is accepted and never documented — an invisible flag is a flag nobody uses"; done <<<"$missing"
  while read -r f; do [[ -n "$f" ]] && bad "${name}: '${f}' is documented and NOT accepted — whoever follows the docs types it and gets an error"; done <<<"$extra"
  [[ -z "$missing$extra" ]] && ok "${name}: accepts and promises the same set ($(wc -w <<<"$have") flags)"
  return 0
}

prose_check() {  # $1 = human name, $2 = prose file, $3.. = every parser it may quote
  local name="$1" doc="$2"; shift 2
  local known="" want ghosts script
  [[ -f "$doc" ]] || { bad "${name}: missing (${doc})"; return 0; }
  for script in "$@"; do known+="$(parser_flags "$script" || true)"$'\n'; done
  known="$(sort -u <<<"$known" | grep -v '^$' || true)"
  want="$(documented_flags <"$doc" || true)"
  ghosts="$(comm -13 <(echo "$known") <(echo "$want") || true)"
  while read -r f; do [[ -n "$f" ]] && bad "${name}: names '${f}', which no command here accepts — whoever follows it types a flag that does not exist"; done <<<"$ghosts"
  [[ -z "$ghosts" ]] && ok "${name}: every flag it names exists ($(wc -w <<<"$want") named)"
  return 0
}

echo "── Flags accepted × flags documented ──"

# The installer: documented in its own header AND in the recipe people actually follow.
# mktemp + trap: the first version wrote a guessable name in a world-writable directory with
# `>` (which follows a planted symlink) and cleaned up only on success.
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

for src in scripts/install-maestro.sh bin/maestro docs/receitas/instalar-o-maestro.md README.md; do
  [[ -f "$src" ]] || bad "missing: $src — the gate cannot compare what is not there"
done

if [[ -f scripts/install-maestro.sh ]]; then
  # `set -euo pipefail` closes the range and would be read as a documented flag.
  sed -n '/^# Usage/,/^set -euo/p' scripts/install-maestro.sh | sed '/^set -/d' > "$WORK/usage"
  reference_check scripts/install-maestro.sh "install-maestro.sh, its own # Usage header" "$WORK/usage"
fi
if [[ -f bin/maestro ]]; then
  sed -n "/^usage() {/,/^}/p" bin/maestro > "$WORK/cli"
  reference_check bin/maestro "maestro, its own usage text" "$WORK/cli"
fi
for prose in docs/receitas/instalar-o-maestro.md README.md; do
  [[ -f "$prose" ]] && prose_check "${prose}" "$prose" scripts/install-maestro.sh bin/maestro
done

echo "──"
if [[ $fail -ne 0 ]]; then
  echo "✗ the flags and the documentation disagree."
  exit 1
fi
echo "✓ every flag that exists is documented, and every documented flag exists."
