# Plan 013 — Livro: guia editorial, piloto e instalador

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 013 (decisões do Steward registradas no clarify) |
| II. Orquestração humano-governada | ✅ as 3 decisões (esqueleto, chat, piloto) foram do Steward |
| III. Reversibilidade / gates de risco | ✅ instalador não sobrescreve e tem `--dry-run`; migração de capítulos é gradual |
| IV. Test-First / DoD verificável | ✅ DoD por build, grep e teste de idempotência do instalador |
| V. Economia de contexto / fronteira | ✅ guia editorial = decisão empacotada; capítulo não re-deriva o formato |
| VI. Artefatos vivos | ✅ ADR 0011, índice, sumário, changelog no mesmo ciclo |
| VII. Governança leve / YAGNI | ✅ companion fica para ciclo próprio; capítulos migram um a um |
| VIII. Comunicação inteligível | ✅ siglas expandidas na 1ª ocorrência de cada documento novo |

**Sem violações.**

## Como

- **Guia editorial**: adaptar o padrão provado do `harness_engineering` (mesma família
  pedagógica) ao nosso contexto, acrescentando a seção §6 (ciclo real) — que lá não
  existe e aqui é possível porque temos 13 ciclos documentados.
- **Capítulo 13**: quadro-mestre com as 14 decisões (data + registro), depois uma
  subseção por decisão no formato **por quê / o que faz / o que provoca** (com o efeito
  indesejado explícito, que é o ponto do pedido).
- **Instalador**: bash puro, função `copiar` idempotente, seções por camada do toolkit
  (quem faz · como fazer · ritual · motor · governança) + próximos passos impressos.
- **Integração**: sumário via script Python (JSON), índice do handbook com nota de
  transição entre padrões.

## Verificação (DoD)

- `node publicar/build.mjs` → 25 páginas, links OK.
- `instalar-maestro.sh` em destino limpo → 47 arquivos; 2ª execução → todos "mantido".
- `grep -c "O que provoca"` ≥ 14; `grep -c "^## "` = 9 no capítulo 13.
- `ls docs/adr/0011-*.md`; `grep adr-0011 docs/registro/decisoes.jsonl`.
