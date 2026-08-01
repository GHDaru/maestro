# Plan 019 — Distribuição em três camadas + templates

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 019 |
| II. Orquestração humano-governada | ✅ decisão de distribuição registrada em ADR com gate do Steward |
| III. Reversibilidade / gates de risco | ✅ pacote é gerado (regenerável); nada destrutivo |
| IV. Test-First / DoD verificável | ✅ check de sincronia **provado falhando** (segunda lei) |
| V. Economia de contexto / fronteira | ✅ camadas separadas: quem quer só skills não carrega o método inteiro |
| VI. Artefatos vivos | ✅ ADR, README, receita, índices e corpus no mesmo ciclo |
| VII. Governança leve / YAGNI | ✅ **CLI próprio descartado** com racional; camada C saiu de graça |
| VIII. Comunicação inteligível | ✅ IA, ADR, CLI expandidos na 1ª ocorrência dos documentos |

**Sem violações.**

## Como

- **Templates**: ADR com alternativas e consequências negativas obrigatórias; qa-report
  com a coluna "Resultado" preenchida da execução real ("prove, não declare").
- **Pesquisa** (curador): vercel-labs/skills (`npx skills add`, 75+ agentes, **só skills**),
  plugin do Claude Code (manifesto + marketplace, agentes+skills+comandos) e Spec Kit
  (CLI Python, assets no wheel, ~6.900 linhas).
- **Empacotador**: reconcilia os layouts — o plugin quer `agents/`/`commands/` na raiz,
  nossas fontes vivem em `.claude/`. Gera e sabe **verificar**.
- **Ordem de apresentação**: A (completo) → B (plugin) → C (skills), cada um declarando o
  que **não** leva, para ninguém achar que instalou o método tendo instalado 1/5 dele.

## Verificação (DoD)

- Fonte alterada sem reempacotar → exit 1 nomeando o arquivo *(provado)*.
- 10 templates; plugin com 13/6/11; JSON válido nos dois manifestos.
- `pytest`, build do site, `verificar-agentes`, `verificar-papeis` verdes.
