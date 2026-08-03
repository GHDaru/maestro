# Tasks 033 — Inglês no método instalável

## Verificação primeiro
- [x] T0 — `scripts/check-language.sh`: resíduo de português na superfície instalável
- [x] T1 — provar falhando: resíduo injetado em `.claude/agents/qa.md` → exit 1 com arquivo e linha

## Implementação
- [x] T2 — renomear 6 agentes, 5 skills, 9 scripts, 3 documentos de governança e `docs/registro/`
- [x] T3 — traduzir os 13 agentes e as 6 skills (Iron Laws incluídas)
- [x] T4 — traduzir os 10 scripts (comentários, mensagens e flags: `--verify`, `--block`, `--force`)
- [x] T5 — traduzir os 7 templates nossos e o comando `/dod`
- [x] T6 — traduzir constituição (v1.2.0), modelo operacional (v1.4.0), glossário e `docs/records/README.md`
- [x] T7 — varredura de referências (59 arquivos) + correção das duas trocas excessivas
      (`0004-modelo-operacional.md`, `jornada-aprendizado-modelo-operacional.md`)
- [x] T8 — marcador `PT-DATA` nas três linhas que legitimamente carregam português
- [x] T9 — `README` de skills e de scripts em inglês (achados pelo próprio check)
- [x] T10 — metadados do plugin e do marketplace em inglês; reempacotar
- [x] T11 — ADR 0014 + registro no índice; `CLAUDE.md` com a regra de idioma

## Gate
- [x] T12 — DoD verde: seis portões + build do livro
- [ ] T13 — gate de merge humano → `promote-main.sh`
