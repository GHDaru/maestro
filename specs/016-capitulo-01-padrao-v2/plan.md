# Plan 016 — Capítulo 01 no padrão v2

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 016 |
| II. Orquestração humano-governada | ✅ o capítulo **é sobre** este princípio; migração aprovada pelo Steward |
| III. Reversibilidade / gates de risco | ✅ mudança textual, reversível por git; v1 preservado no histórico |
| IV. Test-First / DoD verificável | ✅ 9 seções por grep + **fitness function nova** do corpus (falha provada) |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo — lote pequeno, revisável |
| VI. Artefatos vivos | ✅ índice, sumário e corpus atualizados no mesmo ciclo |
| VII. Governança leve / YAGNI | ✅ só o 01; nenhum outro capítulo tocado |
| VIII. Comunicação inteligível | ✅ RACI, DoD, ADR expandidos na 1ª ocorrência do capítulo |

**Sem violações.**

## Como

- Migração fato-a-fato: cada bloco do v1 mapeado para a seção correspondente do v2
  (pergunta central → §2 problema; fundamentação → §5; frameworks → §5.4; recomendação →
  §4 regra vigente; conexões e fontes → rodapé).
- **Novo** no v2: objetivos (§1), ideia central em uma frase (§3), ciclo real (§6),
  anti-padrões (§7), verificação (§8) e "o que roubar" (§9).
- §6 usa o `promover-main.sh`: o script executa o mecânico e **aborta** sem decisão humana
  — a fronteira do princípio virando código, com saída real de comando.
- **Automação nascida do ciclo**: teste que compara as páginas do sumário com o corpus do
  companion, para o esquecimento de regenerar deixar de ser regra de papel.

## Verificação (DoD)

- `grep -c "^## "` = 9; greps dos frameworks e fontes preservados.
- `pytest` (11 testes) verde; falha provada com página fora do corpus.
- `node build.mjs` verde.
