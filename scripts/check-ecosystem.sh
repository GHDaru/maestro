#!/usr/bin/env bash
# check-ecosystem.sh — the ecosystem catalogue says what we decided about other people's
# work, and this gate says whether that is still true.
#
# Why it exists: ADR 0008 recorded four ideas as absorbed. Two of them — "isolated worktree
# per task" and "standards per layer" — never landed anywhere on disk, and stayed recorded
# as absorbed for 39 cycles. Nothing measured the difference between DECIDING to absorb and
# HAVING absorbed. Same family of defect as cycle 046 (a licence claim with no text) and
# cycle 042 (a norm with no forcing function): the record outlived the fact.
#
# What this actually measures (anti-pattern 13): NOT whether a verdict is wise — that is a
# human judgement and no script can make it. It measures that every judgement is anchored:
# a source with a licence, a dated card, a current state, and — for anything claimed as
# adopted or absorbed — a destination that EXISTS.
#
# The contract it reads: specs/047-catalogo-do-ecossistema/data-model.md
#
# Usage:  scripts/check-ecosystem.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DIR="docs/ecosystem"
SOURCES="$DIR/fontes.md"
CARDS="$DIR/ideias"
STATE="$DIR/estado.jsonl"

# Patterns matched against the catalogue, which is Portuguese (the installable surface is
# English — ADR 0014). Declared here so the marker sits on the line that carries the text.
CITE_ONLY_RE='citável, não copiável|citable, not copyable'          # PT-DATA (pattern)
TRIGGER_RE='Gatilho de reavaliação|Re-evaluation trigger'           # PT-DATA (pattern)

fail=0
ok()  { printf '  ✓ %s\n' "$1"; }
bad() { printf '  ✗ %s\n' "$1"; fail=1; }

echo "── Ecosystem: is every judgement about someone else's work still anchored? ──"

# A project that has never evaluated anything has no catalogue, and that is not a defect —
# it is a different state from "has a catalogue, and it is broken". Said out loud, never in
# silence: a gate that exits 0 without saying what it looked at is the failure this
# repository has already named twice (anti-pattern 16).
if [[ ! -d "$DIR" ]]; then
  # …unless THIS repository declares that it has one. Deleting the whole catalogue used to
  # exit 0, which made the escape hatch for new projects into an escape hatch for everyone.
  if [[ -f boundary.json ]] && grep -qF '"docs/ecosystem/"' boundary.json; then
    echo "  ✗ $DIR/ is declared in boundary.json and does not exist — the catalogue of this"
    echo "    repository was deleted, which is not the same as never having had one."
    exit 1
  fi
  echo "  · no $DIR/ in this repository — nothing external has been evaluated yet."
  echo "    (to start one: mkdir -p $DIR/ideias && touch $DIR/fontes.md $DIR/estado.jsonl,"
  echo "     then cp .specify/templates/evaluation-template.md $DIR/ideias/001-<slug>.md)"
  exit 0
fi

# From here on the catalogue exists, so a missing piece IS a finding. Cycle 046 shipped a
# gate whose blocks were bare `if [[ -f … ]]` with no else: deleting the file under test
# returned exit 0.
for f in "$SOURCES" "$STATE"; do
  [[ -f "$f" ]] || { bad "$f is missing — the catalogue cannot be checked"; }
done
[[ -d "$CARDS" ]] || bad "$CARDS/ is missing — there are no idea cards to check"
[[ $fail -eq 0 ]] || { echo "──"; echo "✗ the catalogue is not readable."; exit 1; }

# ---- 1. sources: owner/repo, a licence, and a date we observed it ---------------
# PT-DATA: the catalogue is Maestro's own memory and is published in the book, so its
# headings are Portuguese — like docs/adr/. Only the installable surface is English.
rows="$(grep -E '^\|' "$SOURCES" | grep -vE '^\|[[:space:]]*:?-{2,}' | grep -vE '^\|[[:space:]]*(Fonte|Source)\b' || true)"
n_src=0
src_names=""
if [[ -z "$rows" ]]; then
  bad "$SOURCES lists no source — an empty catalogue is not a clean one"
else
  while IFS= read -r row; do
    [[ -n "$row" ]] || continue
    n_src=$((n_src + 1))
    name="$(awk -F'|' '{print $2}' <<<"$row" | tr -d '`*' | sed 's/^ *//; s/ *$//')"
    lic="$(awk -F'|' '{print $4}' <<<"$row" | sed 's/^ *//; s/ *$//')"
    seen="$(awk -F'|' '{print $5}' <<<"$row" | sed 's/^ *//; s/ *$//')"
    [[ -n "$name" ]] || { bad "a source row has no identifier"; continue; }
    src_names+="${name}"$'\n'
    if [[ -z "$lic" ]]; then
      bad "source '${name}': no licence — 'no licence declared' is itself a value, and the worst one to copy from"
    else
      # A licence that does not allow redistribution must SAY it is citable-only, in the row.
      # Otherwise the row reads as permissive to whoever is deciding whether to copy — which
      # is the one decision this column exists to inform (FR6).
      case "${lic,,}" in                                                   # PT-DATA
        *"sem licença"*|*"no licence"*|*proprietá*|*proprietary*|*comercial*|*commercial*|*"cc by"*|*nc-sa*)
          grep -qiE "$CITE_ONLY_RE" <<<"$lic" \
            || bad "source '${name}': licence '${lic}' does not allow redistribution but the row does not mark it citable-only — the column exists to answer 'may I copy this?'" ;;   # PT-DATA
      esac
    fi
    grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}' <<<"$seen" \
      || bad "source '${name}': no observation date — an undated observation claims to be current forever"
  done <<<"$rows"
  ok "${n_src} source(s) read"
fi

# ---- 2. cards: the mandatory anatomy and the seven dimensions -------------------
VOCAB_RE='adotar|absorver|observar|descartar|adopt|absorb|observe|discard'   # PT-DATA
declare -A card_id_seen=()
declare -A card_src_seen=()
n_card=0
shopt -s nullglob
cards=("$CARDS"/*.md)
shopt -u nullglob
if [[ ${#cards[@]} -eq 0 ]]; then
  bad "no idea card in $CARDS/ — the unit of this catalogue is the IDEA, not the tool"
fi
for c in "${cards[@]}"; do
  n_card=$((n_card + 1))
  base="$(basename "$c")"
  # Both spellings, on purpose: Maestro's own catalogue is Portuguese because it is
  # published in the book, while the installable template is English (ADR 0014). Same
  # precedent as check-conformance.sh, which accepts either heading for the criteria.
  # The trailing `<!-- ... -->` is stripped because the TEMPLATE carries inline guidance on
  # each field line — without this, a catalogue started from the template failed the gate
  # and the message blamed the wrong thing.
  field() {  # $1 = field label, as an alternation; prints the value after the colon
    sed -nE "s/^- \\*\\*($1)\\*\\*:[[:space:]]*(.*)$/\\2/p" "$c" | head -1 \
      | sed 's/<!--.*//' | sed 's/[[:space:]]*$//'
  }
  has() { grep -qE "^- \\*\\*($1)\\*\\*:" "$c"; }
  id="$(field 'Id' | tr -d '`*' | sed 's/^ *//; s/ *$//')"
  src="$(field 'Fonte|Source' | tr -d '`*' | sed 's/^ *//; s/ *$//')"                     # PT-DATA
  seen="$(field 'Observado em|Observed')"                       # PT-DATA
  verdict="$(field 'Veredito no momento|Verdict at the time')"  # PT-DATA
  [[ -n "$id" ]] || { bad "${base}: no **Id** — the card cannot be tied to a state"; continue; }
  if [[ -n "${card_id_seen[$id]:-}" ]]; then
    bad "${base}: id '${id}' already used by ${card_id_seen[$id]} — a state line would be ambiguous"
    continue
  fi
  card_id_seen[$id]="$base"
  # The full anatomy the data-model declares, not half of it: removing Destino and Gatilho
  # used to pass, which made the two fields that carry the whole obligation optional.
  has 'Destino|Destination' || bad "${base}: no destination field — write the path, or '—'"          # PT-DATA
  has "$TRIGGER_RE" \
    || bad "${base}: no re-evaluation-trigger field — write the condition, or '—'"              # PT-DATA
  if [[ -z "$verdict" ]]; then
    bad "${base}: no verdict-at-the-time field — the card records what was judged THEN"
  elif ! grep -qE "^(${VOCAB_RE})$" <<<"$verdict"; then
    # "absorver parcial" was in two cards: expressive, and outside the closed vocabulary the
    # index is validated against, so card and index could never be compared.
    bad "${base}: verdict '${verdict}' is outside the closed vocabulary — nuance goes in the prose, not in the field"
  fi
  grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' <<<"$seen" \
    || bad "${base}: the observation field is not a bare date — an observation without a moment is not an observation"
  # The source must be one we actually listed, matched EXACTLY. A substring match let a card
  # cite 'MIT', or 'claude-code' — which matches two sources with different licences.
  if [[ -z "$src" ]]; then
    bad "${base}: no **Fonte** — an idea with no origin cannot be re-evaluated when the origin changes"
  elif ! grep -qxF -- "$src" <<<"$src_names"; then
    bad "${base}: source '${src}' is not a row in $SOURCES — its licence was never recorded"
  else
    card_src_seen[$src]=1
  fi
  # Exactly the set 1..7, once each, in ONE section. Counting lines let a card carry the
  # digit 1 seven times, or split the table in two, and lose dimensions 6 and 7 — the two
  # the catalogue says decide almost every card.
  dsec="$(sed -nE '/^## (Dimensões|Dimensions)/,/^## /p' "$c" || true)"   # PT-DATA
  nsec="$(grep -cE '^## (Dimensões|Dimensions)' "$c" || true)"           # PT-DATA
  if [[ "$nsec" -ne 1 ]]; then
    bad "${base}: ${nsec} '## Dimensões' section(s) — there must be exactly one"
  else
    got="$(grep -oE '^\|[[:space:]]*[0-9]+[[:space:]]*\|' <<<"$dsec" | tr -cd '0-9\n' | sort -u | tr '\n' ' ' | sed 's/ *$//')"
    [[ "$got" == "1 2 3 4 5 6 7" ]] \
      || bad "${base}: dimensions present are [${got}] — the seven must each appear exactly once"
  fi
done
[[ $n_card -gt 0 ]] && ok "${n_card} card(s) read"

# Every source must be judged by at least one card. Without this, a source could sit in the
# list forever with no verdict — which is the state the whole catalogue exists to end.
while read -r sname; do
  [[ -n "$sname" ]] || continue
  [[ -n "${card_src_seen[$sname]:-}" ]] \
    || bad "source '${sname}' is listed but no card judges it — a source with no verdict is an open question pretending to be an answer"
done <<<"$src_names"

# ---- 3-6. state: vocabulary, both directions, destination on disk, trigger -------
# Current state is the LAST line per id (append-only, same protocol as decisoes.jsonl).
if ! python3 - "$STATE" <<'PY'
import json, os, re, sys
path = sys.argv[1]
# Closed vocabulary, in both spellings — the installable template is English (ADR 0014)
# while Maestro's own catalogue is Portuguese, because it is published in the book.
# Keys likewise: a project writing its catalogue in English must not need a translator.
VOCAB = {"adotar": "absorb-like", "absorver": "absorb-like", "observar": "observe",
         "descartar": "discard", "adopt": "absorb-like", "absorb": "absorb-like",
         "observe": "observe", "discard": "discard"}
KEYS = {"ideia": ("ideia", "idea"), "estado": ("estado", "state"), "data": ("data", "date"),
        "destino": ("destino", "destination"), "gatilho": ("gatilho", "trigger"),
        "prova": ("prova", "proof")}
def get(d, key):
    for k in KEYS[key]:
        if k in d:
            return d[k]
    return None
cur, bad = {}, []
with open(path, encoding="utf-8") as fh:
    for n, line in enumerate(fh, 1):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError as e:
            bad.append(f"line {n}: invalid JSON ({e.msg})")
            continue
        for f in ("ideia", "estado", "data"):
            if not get(d, f):
                bad.append(f"line {n}: missing required field '{f}' (or '{KEYS[f][1]}')")
        if get(d, "data") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(get(d, "data"))):
            bad.append(f"line {n}: date {get(d, 'data')!r} is not YYYY-MM-DD — the card is checked for this and the index was not")
        st = get(d, "estado")
        if st and st not in VOCAB:
            bad.append(f"line {n}: state '{st}' is outside the closed vocabulary {sorted(VOCAB)}")
        if get(d, "ideia"):
            cur[get(d, "ideia")] = (n, d)     # last line wins
if not cur and not bad:
    bad.append("the state index is empty — an empty catalogue is not a clean one")
for idea, (n, d) in sorted(cur.items()):
    kind = VOCAB.get(get(d, "estado") or "")
    if kind == "absorb-like":
        dest = (get(d, "destino") or "").strip()
        # isfile, not exists: a destination like `scripts/` is satisfied by a directory that
        # exists for other reasons, which is how "absorbed into scripts/ when the pain
        # appears" survived 39 cycles looking like a fact. Absorption lands in an ARTIFACT.
        st = get(d, "estado")
        proof = (get(d, "prova") or "").strip()
        if not dest:
            bad.append(f"'{idea}' is '{st}' with no destination — absorbing into nowhere is an intention recorded as a fact")
        elif os.path.isabs(dest) or ".." in dest.split("/"):
            bad.append(f"'{idea}' points outside the repository ('{dest}') — a destination is a path in THIS repository")
        elif os.path.isdir(dest):
            bad.append(f"'{idea}' is '{st}' pointing at the directory '{dest}' — name the file that proves the absorption, not the folder it might live in")
        elif not os.path.isfile(dest):
            bad.append(f"'{idea}' is '{st}' pointing at '{dest}', which does not exist on disk — this is the defect the catalogue exists to catch")
        # A file that merely EXISTS proves nothing: `README.md` would satisfy any absorption
        # ever declared. The proof is a literal string that has to be found inside the
        # destination — the sentence, law or field where the idea actually landed.
        elif not proof:
            bad.append(f"'{idea}' is '{st}' with a destination but no 'prova' — name the literal text in '{dest}' where the idea landed")
        else:
            try:
                body = open(dest, encoding="utf-8", errors="replace").read()
            except OSError as e:
                bad.append(f"'{idea}': cannot read '{dest}' ({e.strerror})")
                body = ""
            if proof not in body:
                bad.append(f"'{idea}' claims '{st}' into '{dest}', but the proof text is not there: {proof!r} — the destination does not contain the idea")
    if kind == "observe" and not (get(d, "gatilho") or "").strip():
        bad.append(f"'{idea}' is 'observar/observe' with no trigger — observing without a trigger is forgetting with ceremony")
for b in bad:
    print(f"  ✗ {b}")
if not bad:
    print(f"  ✓ {len(cur)} idea(s) with a current state: destinations exist, observations have triggers")
sys.exit(1 if bad else 0)
PY
then
  fail=1
fi

# Both directions: a card with no state is undecided; a state with no card is unexplained.
ids_state="$(python3 -c "
import json,sys
seen=[]
for l in open('$STATE',encoding='utf-8'):
    l=l.strip()
    if not l: continue
    try: d=json.loads(l)
    except Exception: continue
    k=d.get('ideia') or d.get('idea')
    if k and k not in seen: seen.append(k)
print('\n'.join(seen))
")"
for id in "${!card_id_seen[@]}"; do
  grep -qxF -- "$id" <<<"$ids_state" \
    || bad "card ${card_id_seen[$id]} (id '${id}') has no line in $STATE — judged and never stated"
done
while read -r id; do
  [[ -n "$id" ]] || continue
  [[ -n "${card_id_seen[$id]:-}" ]] \
    || bad "state '${id}' has no card in $CARDS/ — a verdict nobody can re-read is not auditable"
done <<<"$ids_state"

echo "──"
if [[ $fail -ne 0 ]]; then
  echo "✗ the catalogue records judgements that the repository no longer supports."
  exit 1
fi
echo "✓ every source has a licence, every idea a dated card, every state a card — and every"
echo "  adopted or absorbed idea has a destination that actually exists."
