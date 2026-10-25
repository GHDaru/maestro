#!/usr/bin/env bash
# captura-072.sh — capturas da jornada viva do ciclo 072 (painel de regência, rodada 1)
#
# Iron Law (skill living-journey): uma jornada sem captura do build REAL é ficção.
# Este script sobe o servidor de verdade (`painel/server.py`) com a fixture de exemplo e
# fotografa as DUAS telas renderizadas — `#kanban` (Painel de regência) e `#fila` (Fila de
# decisões). Nada aqui é mock: o HTML é o que o painel serve, com o JavaScript que o navegador
# executa (é justamente o que F1/F9 NÃO cobrem — D-072-8).
#
# AQUECIMENTO (achado R1 da heurística): a derivação do painel é preguiçosa e assíncrona —
# na primeira consulta o servidor devolve a lista vazia enquanto calcula (varredura do git).
# Capturar sem esperar produz uma foto FALSA de "vazio". O script consulta `/api/chamados`
# até a derivação parar de estar vazia (ou estourar o limite) e só então fotografa.
#
# Uso:  bash docs/journeys/scripts/captura-072.sh
# Saída: docs/journeys/img/072-01-kanban.png, docs/journeys/img/072-02-fila.png
#
# Requisitos no host: python (3.x) com o pacote `playwright`; um navegador Chromium já
# instalado — usa o Edge do sistema via canal (`PW_CHANNEL=msedge`), então não precisa baixar
# binário do Playwright. Porta alta por padrão (8791); o servidor é derrubado no fim.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

PORTA="${PORTA:-8791}"
PY="${PY:-python}"
PW_CHANNEL="${PW_CHANNEL:-msedge}"
ESPERA_S="${ESPERA_S:-90}"
OUT="$ROOT/docs/journeys/img"
LOG="${TMPDIR:-/tmp}/captura-072-servidor.log"

mkdir -p "$OUT"

echo "== subindo o painel real em http://127.0.0.1:$PORTA (fixture exemplo) =="
PYTHONUTF8=1 "$PY" painel/server.py painel/projetos/exemplo.json --porta "$PORTA" >"$LOG" 2>&1 &
SRV_PID=$!
cleanup() { kill "$SRV_PID" 2>/dev/null || true; wait "$SRV_PID" 2>/dev/null || true; }
trap cleanup EXIT

# espera o servidor responder (máx. ~20 s)
for i in $(seq 1 40); do
  if "$PY" - "$PORTA" <<'PY' >/dev/null 2>&1
import sys, urllib.request
urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/api/meta", timeout=2).read()
PY
  then break; fi
  sleep 0.5
done

echo "== esperando a derivação aquecer (até ${ESPERA_S}s) =="
PORTA="$PORTA" ESPERA_S="$ESPERA_S" "$PY" - <<'PY'
import json, os, time, urllib.request
porta, limite = os.environ["PORTA"], float(os.environ["ESPERA_S"])
t0 = time.time()
n = 0
while time.time() - t0 < limite:
    try:
        d = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{porta}/api/chamados", timeout=30).read())
        n = len(d.get("chamados") or [])
    except Exception as e:
        print(f"  aviso: {e}")
    if n:
        break
    time.sleep(2.0)
print(f"  derivação estabilizada com {n} chamado(s) em {time.time() - t0:.1f}s"
      f"{' (ainda vazio — o fixture pode legitimamente não ter chamado)' if not n else ''}")
PY

echo "== capturando as duas telas com o navegador ($PW_CHANNEL) =="
PORTA="$PORTA" OUT="$OUT" PW_CHANNEL="$PW_CHANNEL" "$PY" - <<'PY'
import os
from playwright.sync_api import sync_playwright

porta, out = os.environ["PORTA"], os.environ["OUT"]
base = f"http://127.0.0.1:{porta}"
views = [("kanban", "072-01-kanban.png", "Painel de regência"),
         ("fila", "072-02-fila.png", "Fila de decisões")]

with sync_playwright() as p:
    b = p.chromium.launch(channel=os.environ.get("PW_CHANNEL", "msedge"), headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    for v, nome, titulo in views:
        pg.goto("about:blank")          # carga limpa por tela: nada de hashchange em página suja
        pg.goto(f"{base}/#{v}", wait_until="networkidle")
        pg.wait_for_timeout(2500)       # dá tempo ao fetch da tela e ao render
        destino = os.path.join(out, nome)
        pg.screenshot(path=destino, full_page=True)
        print(f"ok: {destino}  ({titulo})")
    b.close()
PY

echo "== pronto: capturas em $OUT =="
