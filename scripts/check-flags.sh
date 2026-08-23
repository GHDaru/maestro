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

# Any flag a script ACCEPTS, however it tests for it: a `case` arm (parser_flags) or a literal
# comparison such as `[[ "$MODE" == "--verificar" ]]`. The second form is how package-plugin.sh
# reads its only flag, and a detector that knew only `case` skipped that script entirely.
parser_flags_any() {  # $1 = script
  { parser_flags "$1"
    # Code lines only. Reading comments too made this function find the flag names quoted in
    # its OWN explanation and report check-flags.sh as a parser — a gate accusing itself of
    # what it was written to detect.
    grep -vE '^[[:space:]]*#' "$1" \
      | grep -oE '==[[:space:]]*"--[A-Za-z][A-Za-z0-9_-]*"' 2>/dev/null \
      | grep -oE -- '--[A-Za-z][A-Za-z0-9_-]*' || true
  } | sort -u
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

# Same comparison, reading every shape a script uses to accept a flag (see parser_flags_any).
gate_reference_check() { _reference_check any "$@"; }
reference_check()      { _reference_check case "$@"; }
_reference_check() {  # $1 = reader, $2 = script, $3 = human name, $4 = its reference text
  local reader="$1" script="$2" name="$3" doc="$4" have want missing extra
  [[ -f "$doc" ]] || { bad "${name}: reference text missing (${doc})"; return 0; }
  if [[ "$reader" == "any" ]]; then have="$(parser_flags_any "$script" || true)"
  else have="$(parser_flags "$script" || true)"; fi
  _reference_compare "$name" "$have" "$doc"
}
_reference_compare() {  # $1 = name, $2 = accepted set, $3 = reference text
  local name="$1" have="$2" doc="$3" want missing extra
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
# The gates themselves parse flags too, and this gate covered exactly two parsers — so
# `--ticked-only`, born in cycle 061 inside check-conformance.sh, was outside the rule whose
# motto is "a flag that exists is documented, and a documented flag exists". It happened to be
# coherent; coherent by accident is not covered. A new door, and the old guard never told —
# anti-pattern 23, found by the independent review of cycles 061-062.
# Every gate in scripts/, not just `check-*`: `package-plugin.sh` accepts `--verificar`, which
# no `# Usage` mentions, and it was outside the first version of this loop. And the detector
# now reads an ARM, alias included — `^\s*--flag)` missed `--strict|-s)` and `--ai=*)`, the very
# shapes parser_flags() had to learn, and skipped the whole script in silence.
for g in scripts/*.sh bin/maestro; do
  [[ -f "$g" ]] || continue
  case "$g" in scripts/install-maestro.sh|bin/maestro) continue ;; esac   # covered above
  # The detector is parser_flags() itself — the same reader used for the two parsers above.
  # A second, weaker detector was the bug: `^\s*--flag)` saw only `case` arms, so
  # `package-plugin.sh`, which compares with `[[ "$MODE" == "--verificar" ]]`, was skipped in
  # silence with an undocumented flag. One reader, one answer.
  [[ -n "$(parser_flags_any "$g")" ]] || continue
  # The header range must CLOSE. `sed -n '/^# Usage/,/^set -euo/p'` on a script that opens with
  # `set -eu` (no pipefail) never closes, so the whole file — parser included — became the
  # "documentation", and an undocumented flag matched itself. Two anchors, and a range that
  # did not close is a failure, never a pass.
  awk '/^# Usage/{u=1} u && /^[^#]/{exit} u{print}' "$g" > "$WORK/gusage"
  if [[ ! -s "$WORK/gusage" ]]; then
    bad "$(basename "$g") parses flags and has no '# Usage' header to compare them with"; continue
  fi
  if grep -qE '^[[:space:]]*(-[a-zA-Z-]+\|)*--[a-zA-Z]' "$WORK/gusage" && grep -qE '\)[[:space:]]*(;;|$)' "$WORK/gusage"; then
    bad "$(basename "$g"): the '# Usage' block runs into the code — the header never closed, so the parser would document itself"; continue
  fi
  gate_reference_check "$g" "$(basename "$g"), its own # Usage header" "$WORK/gusage"
done

for prose in docs/receitas/instalar-o-maestro.md README.md; do
  [[ -f "$prose" ]] && prose_check "${prose}" "$prose" scripts/install-maestro.sh bin/maestro
done

# ── The index of scripts × the scripts that exist (cycle 063) ─────────────────────────────
# `scripts/README.md` is INSTALLED, and the recipe presents it as "what each script is". It
# had drifted six scripts behind — check-conformance.sh among them, which the installer's own
# closing message tells you to run. Same family as everything else here: two places stating
# one set, with nothing comparing them.
echo ""
echo "── Every script is in the index that ships with it ──"
if [[ -f scripts/README.md ]]; then
  idx_missing=0
  for g in scripts/*.sh; do
    b="$(basename "$g")"
    grep -qF "$b" scripts/README.md || { bad "scripts/README.md never mentions ${b} — the installed index is behind"; idx_missing=1; }
  done
  # Only names the page presents as OURS — a backticked span or a relative link. A bare regex
  # over the prose cobrou `ci-helper.sh` inside a URL and `configure.sh` in a sentence about
  # autotools, turning a blocking gate red on legitimate text (review of cycle 063).
  while IFS= read -r named; do
    [[ -n "$named" ]] || continue
    [[ -f "scripts/$named" ]] || { bad "scripts/README.md documents ${named}, which does not exist"; idx_missing=1; }
  done < <(grep -oE '`[A-Za-z0-9][A-Za-z0-9._-]*\.sh`|\]\(\./[A-Za-z0-9][A-Za-z0-9._-]*\.sh\)' scripts/README.md \
             | tr -d '`' | sed -E 's|^\]\(\./||; s|\)$||' | sort -u)
  [[ "$idx_missing" -eq 0 ]] && ok "the index names every script, and every script it names exists"
else
  bad "scripts/README.md is missing — the installed index of scripts does not exist"
fi

# ── Subcommands: the same lie, on the door cycle 058 built ────────────────────────────────
# `check-flags` covered flags and stopped there, so the README could advertise `maestro deploy`
# and nothing would notice — the class of defect this gate exists for, one level up (cycle 059).
subcommands() {
  # ONLY the dispatch `case` at the bottom — the parser inside cmd_init has its own arms
  # (`--yes|-y)`), and stripping dashes from those invented subcommands called "yes" and "y".
  # The `case` line is matched loosely (trailing spaces used to produce twelve false
  # failures), and an arm is read whatever its FIRST alternative is: `""|-h|--help|help)` hid
  # a real subcommand — `help` — which the gate then called nonexistent (independent review).
  sed -n '/^case[[:space:]]*"\${1:-}"[[:space:]]*in[[:space:]]*$/,/^esac[[:space:]]*$/p' bin/maestro \
    | grep -oE '^[[:space:]]*[a-z"|*_-]+\)' \
    | tr -d ' )' \
    | awk -F'|' '{for(i=1;i<=NF;i++) if ($i ~ /^[a-z][a-z-]*$/) print $i}' \
    | sort -u
}
announced_in_usage() {
  # The command list inside usage(): five spaces, the name, then its description.
  # `maestro` itself is filtered: the examples at the end of usage() are indented the same
  # way as the command list, so the tool's own name came back as a subcommand.
  sed -n '/^usage() {/,/^}/p' bin/maestro \
    | grep -oE '^     [a-z][a-z-]*' | grep -oE '[a-z][a-z-]*' \
    | grep -vx 'maestro' | sort -u
}
announced_in_prose() {  # stdin
  # A subcommand is ANNOUNCED where a command is WRITTEN: inside a fenced code block, or
  # inside backticks. Anchoring on "start of line" both missed the commonest shape
  # (`cd /x && maestro deploy`, which the README itself uses) and turned ordinary Portuguese
  # that happens to begin a line with "maestro" into a build failure. Prose is prose; a code
  # fence is a promise (independent review of cycle 059).
  awk '/^```/ {inblock = !inblock; next} inblock {print}
       !inblock { while (match($0, /`[^`]*`/)) { print substr($0, RSTART+1, RLENGTH-2); $0 = substr($0, RSTART+RLENGTH) } }' \
    | grep -oE '(^|[^A-Za-z0-9_./-])maestro[[:space:]]+[a-z][a-z-]*' \
    | grep -oE 'maestro[[:space:]]+[a-z][a-z-]*' | sed -E 's/^maestro[[:space:]]+//' | sort -u
}

echo ""
echo "── Subcommands accepted × subcommands announced ──"
if [[ ! -f bin/maestro ]]; then
  bad "bin/maestro is missing — there is no door to compare"
else
  have_sub="$(subcommands || true)"
  # Reference: its own usage text, both directions.
  ref_sub="$(announced_in_usage || true)"
  miss="$(comm -23 <(echo "$have_sub") <(echo "$ref_sub") || true)"
  ghost="$(comm -13 <(echo "$have_sub") <(echo "$ref_sub") || true)"
  while read -r c; do [[ -n "$c" ]] && bad "maestro usage: '${c}' is accepted and never announced"; done <<<"$miss"
  while read -r c; do [[ -n "$c" ]] && bad "maestro usage: announces '${c}', which the dispatcher does not accept"; done <<<"$ghost"
  [[ -z "$miss$ghost" ]] && ok "maestro subcommands, its own usage text: announces exactly what it accepts ($(wc -w <<<"$have_sub"))"

  # Prose: one direction — everything it announces must exist.
  # Every place that ANNOUNCES the door, including the copy shipped inside the plugin and the
  # ADR that describes distribution. The first version watched two files, which is the very
  # anti-pattern (23: a new door, and the old guard never told) this cycle cites.
  for prose in README.md docs/receitas/instalar-o-maestro.md plugin/maestro/README.md \
               docs/adr/0012-distribuicao-em-tres-camadas.md; do
    [[ -f "$prose" ]] || continue
    said="$(announced_in_prose <"$prose" || true)"
    ghost="$(comm -13 <(echo "$have_sub") <(echo "$said") || true)"
    while read -r c; do [[ -n "$c" ]] && bad "${prose}: announces 'maestro ${c}', which does not exist"; done <<<"$ghost"
    [[ -z "$ghost" ]] && ok "${prose}: every 'maestro <cmd>' it announces exists"
  done
fi

echo "──"
if [[ $fail -ne 0 ]]; then
  echo "✗ the flags and the documentation disagree."
  exit 1
fi
echo "✓ every flag that exists is documented, and every documented flag exists."
