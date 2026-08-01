# QA-report 019 — Distribuição em três camadas + templates

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Fonte alterada sem reempacotar | exit ≠ 0 nomeando o arquivo | **exit 1**, "agents/qa.md differ" ✅ |
| `ls .specify/templates/*.md \| wc -l` | 10 | 10 ✅ |
| `plugin/maestro/` | 13 agentes · 6 skills · 11 comandos | ✅ |
| `plugin.json` e `marketplace.json` | JSON válido | ✅ (parse) |
| Layout das skills p/ `npx skills add` | `skills/<nome>/SKILL.md` + name/description | ✅ 6/6 |
| `verificar-agentes` · `verificar-papeis` | exit 0 | ✅ |
| `pytest` · build do site | verdes | 11 testes · 35 páginas ✅ |

## O check funcionando em produção, no mesmo ciclo

Depois de editar o `README.md` (que vai dentro do pacote), rodei a bateria final e o
`--verificar` **acusou sozinho**: `README.md differ` → exit 1. Reempacotei e passou. O
check pagou-se antes mesmo de o ciclo fechar — exatamente o que a segunda lei prevê.

## Achado: a lacuna dos templates

`verificar-papeis.sh` (ciclo 018) cobria só os artefatos marcados "essencial" na tabela do
modelo — ADR e qa-report não estavam marcados assim, e passaram. **Nenhum check é
completo**: o do 018 fechou uma classe e deixou a vizinha aberta. Registrado como limite
conhecido, não como falha silenciosa.

## Pendência (do Steward)

Submeter ao marketplace comunitário da Anthropic (`claude-plugins-community`) exige
formulário e revisão — decisão de publicação, não de engenharia.

## Gate

- Aprovação do Steward; promovido via `promover-main.sh`.
