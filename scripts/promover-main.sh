#!/usr/bin/env bash
# promover-main.sh — promove dev -> main (o "gate de merge" do Maestro).
#
# O GATE É HUMANO (Princípio II): este script só executa o passo MECÂNICO depois
# da sua decisão. Ele exige confirmação e aborta se algo estiver fora do lugar.
# Não decide por ninguém — só evita erro de digitação no ritual repetido.
#
# Uso:  scripts/promover-main.sh            # pergunta antes de promover
#       scripts/promover-main.sh --yes      # pula a pergunta (você já decidiu)
set -euo pipefail

DEV="${MAESTRO_DEV_BRANCH:-dev}"
MAIN="${MAESTRO_MAIN_BRANCH:-main}"
ASSUME_YES=0
[[ "${1:-}" == "--yes" ]] && ASSUME_YES=1

# 1. Árvore limpa (não promover trabalho não commitado).
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "abortado: árvore de trabalho suja — commite ou limpe antes de promover." >&2
  exit 1
fi

# 2. dev precisa estar à frente de main.
git rev-parse --verify --quiet "$DEV" >/dev/null || { echo "abortado: branch '$DEV' não existe." >&2; exit 1; }
git rev-parse --verify --quiet "$MAIN" >/dev/null || { echo "abortado: branch '$MAIN' não existe." >&2; exit 1; }
AHEAD=$(git rev-list --count "$MAIN".."$DEV")
if [[ "$AHEAD" -eq 0 ]]; then
  echo "nada a promover: '$MAIN' já está em '$DEV'." >&2
  exit 1
fi

# 3. Mostrar o que vai para main.
echo "vão para '$MAIN' ($AHEAD commit(s) de '$DEV'):"
git --no-pager log --oneline "$MAIN".."$DEV"
echo

# 4. Gate humano: confirmação explícita.
if [[ "$ASSUME_YES" -ne 1 ]]; then
  read -r -p "promover '$DEV' -> '$MAIN' e dar push? [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]] || { echo "cancelado."; exit 1; }
fi

# 5. Registrar o gate no índice de decisões (regra do ADR 0009 — automático,
#    para o registro consultável ser a fonte do estado do gate).
SHORT=$(git rev-parse --short "$DEV")
ATUAL=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")
if [[ "$ATUAL" == "$DEV" && -f docs/registro/decisoes.jsonl ]] && command -v python3 >/dev/null; then
  TITULO=$(git log -1 --format=%s "$DEV" | tr '"' "'")
  HOJE=$(date +%Y-%m-%d)
  LINHA=$(python3 -c "import json;print(json.dumps({'id':'gate-main-$SHORT','data':'$HOJE','titulo':'Gate de merge: $TITULO','status':'aceita','registro':'commit $SHORT'},ensure_ascii=False))")
  if scripts/registrar-decisao.sh "$LINHA" >/dev/null 2>&1; then
    git add docs/registro/decisoes.jsonl
    git commit -q -m "chore(registro): gate de merge gate-main-$SHORT"
    echo "gate registrado: gate-main-$SHORT"
  else
    echo "aviso: não registrou o gate (id já existe?); seguindo." >&2
  fi
else
  echo "aviso: registro indisponível (docs/registro/ ou python3 ausente); seguindo." >&2
fi

# 6. Executar o passo mecânico com retry exponencial no push (dev + main juntos).
git branch -f "$MAIN" "$DEV"
delay=2
for attempt in 1 2 3 4 5; do
  if git push origin "$DEV" "$MAIN"; then
    echo "ok: '$MAIN' promovido para $(git rev-parse --short "$DEV")."
    exit 0
  fi
  if [[ "$attempt" -lt 5 ]]; then
    echo "push falhou (tentativa $attempt); retry em ${delay}s..." >&2
    sleep "$delay"; delay=$((delay * 2))
  fi
done
echo "erro: push de '$MAIN' falhou após 5 tentativas." >&2
exit 1
