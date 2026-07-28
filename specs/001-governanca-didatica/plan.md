# Plan 001 — Governança didática

- **Spec**: `spec.md` (aprovada — gate DoR) · **Raia**: Plena · **Data**: 2026-07-28

## Constitution Check (principios-maestro.md I–VII)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 001; sem código sem spec |
| II. Orquestração humano-governada | ✅ humano aprovou a spec e aprovará o merge |
| III. Reversibilidade / gates de risco | ✅ mudança de docs, 100% reversível (git); baixo risco |
| IV. Test-First / DoD verificável | ✅ critérios de aceite são verificáveis por `grep` (siglas, referências) |
| V. Economia de contexto / fronteira | ✅ escopo cortado por fronteira (entrada/governança agora; capítulos incrementais) |
| VI. Artefatos vivos / rastreabilidade | ✅ glossário e guia são consumidos (linkados); PDFs regenerados da fonte |
| VII. Governança leve / YAGNI | ✅ camada nova, sem reescrever o que funciona |

**Sem violações.** Nenhuma justificativa de Complexity Tracking necessária.

## Refinamento de escopo (plan-time)

A abordagem **híbrida** (clarify) delimita o FR3 (expansão de siglas): **neste ciclo**,
expansão-na-1ª-ocorrência nos **documentos de entrada e governança** (`README.md`,
`comece-por-aqui.md`, `principios-maestro.md`, `modelo-operacional.md`) + o glossário
cobrindo 100% das siglas de todos os docs. A expansão dentro dos **12 capítulos** entra na
**reescrita incremental** (ciclos futuros, um capítulo por vez) — mantém o apetite.

## Como (arquitetura da mudança)

- **Guia narrativo** `docs/comece-por-aqui.md`: dor → jornada → sistema → como usar → mapa
  de leitura. Sem jargão sem expansão. Linkado no `README.md`.
- **Glossário** `docs/governance/glossario.md`: tabela ordenada; verbete = sigla · expansão
  · significado no Maestro · elemento/capítulo. Cobre todas as siglas coletadas por varredura.
- **Rebasing (FR4)**: varredura `grep` por `Constituição`/`Princípio (IV|V|VII)` nos docs
  migrados → apontar para `principios-maestro.md` (mapa de linhagem).
- **PDFs (FR5)**: regenerar `maestro-handbook.pdf` e `maestro-compendio-governanca.pdf`
  incluindo guia (abertura) e glossário (apêndice), via o pipeline Playwright já existente.

## Verificação (fecha a DoD)

- `grep` de siglas nos docs × glossário → cobertura 100%.
- `grep -rn "Constituição\|Princípio \(IV\|V\|VII\)"` nos docs migrados → só `principios-maestro.md`.
- guia existe e linkado; PDFs regenerados; CHANGELOG atualizado.
