# QA-report 008 — Absorções do estudo maestro-02

- **Data**: 2026-07-31 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD) — executadas

| Check | Esperado | Resultado |
|---|---|---|
| decisoes.jsonl parse linha a linha | ≥5 válidas | **6** ✅ |
| `bash -n` + `+x` nos 2 scripts novos | ok | ok ✅ |
| `registrar-decisao.sh` com id duplicado | recusa (exit 1) | recusou ✅ |
| `./scripts/retro.sh` | exit 0 | exit 0 (rodado ao vivo) ✅ |
| `ls skills/*/SKILL.md \| wc -l` | 4 | 4 ✅ |
| `anti-padroes`: frontmatter + gatilho | ok | ok ✅ |
| EARS em `dod-verificavel` | grep QUANDO | ok ✅ |
| caps. 04/10 com as subseções | grep | ok ✅ |
| ADR 0008 | Aceito | Aceito ✅ |
| CHANGELOG [Unreleased] | entrada | ok ✅ |

## Cobertura

FR1–FR7 todos entregues (ver tasks). Absorções do Apêndice A materializadas + EARS do
ciclo 007 fechado. Fora de escopo respeitado (telemetria de custo segue em observar).

## Insight de retro (achado pelo próprio retro.sh)

O primeiro run do `retro.sh` revelou uma lacuna real: **os qa-reports de ciclos já
promovidos mantêm a linha "aguarda aprovação" aberta** — o gate foi exercido no chat, mas
o artefato não foi atualizado. Regra candidata (próxima retro): ao promover, anexar a
decisão do gate via `registrar-decisao.sh` (`gate-NNN-merge`) — o registro consultável
passa a ser a fonte do estado do gate, sem editar qa-report histórico.

## Gate

- Aprovação prévia e explícita do Steward ("pode incorporar todas as sugestões") —
  registrada em `docs/registro/decisoes.jsonl` (`gate-008-absorcoes`). Promovido.
