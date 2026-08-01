# Plan 017 — Retrospectiva executada e BPMN

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 017 |
| II. Orquestração humano-governada | ✅ a auditoria foi do Steward; o gate humano funcionou como rede |
| III. Reversibilidade / gates de risco | ✅ mudanças textuais, reversíveis por git |
| IV. Test-First / DoD verificável | ✅ **é o tema**: a segunda lei ataca exatamente o check não-provado |
| V. Economia de contexto / fronteira | ✅ anti-padrão numerado = referência curta ("isso é o 13") |
| VI. Artefatos vivos | ✅ **é o outro tema**: roadmap descongelado + regra de manutenção |
| VII. Governança leve / YAGNI | ✅ vira skill/roadmap, não princípio novo |
| VIII. Comunicação inteligível | ✅ BPMN, DoD e DoR expandidos na 1ª ocorrência |

**Sem violações.**

## Como

- Rodar `retro.sh` (a cerimônia que faltava) e responder as três perguntas padrão.
- Converter: pergunta 1 (erro recorrente) → anti-padrões 13/14/15 + segunda lei da skill.
- Descongelar o roadmap com as fases reais + **regra no cabeçalho** para não repetir.
- BPMN em quatro raias (Steward · agentes · automação · artefatos) com os losangos nos
  gates; imagem renderizada por navegador real, página no livro na trilha Bastidores.

## Verificação (DoD)

- Contagem de anti-padrões = 15; duas leis na `dod-verificavel`.
- Roadmap com F5–F7 e gatilhos; build do site verde (35 páginas).
