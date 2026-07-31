# Plan NNN — [TÍTULO]

- **Spec**: `spec.md` · **Raia**: [plena|infra] · **Data**: [YYYY-MM-DD]

## Constitution Check (principios-maestro.md)

<!--
  OBRIGATÓRIO e COMPLETO — uma linha por princípio, nunca pule (skill constitution-check).
  ✅ = conforme (uma frase de porquê). Violado = o plano SÓ funciona quebrando o princípio;
  desconforto ≠ violação. Violação real → reformule OU registre em Complexity Tracking
  (qual princípio, por que inevitável, o que a torna reversível) → gate humano decide.
-->

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | [nasce de spec aprovada?] |
| II. Orquestração humano-governada | [o A humano é preservado?] |
| III. Reversibilidade / gates de risco | [dá para desfazer? gate ∝ risco?] |
| IV. Test-First / DoD verificável | [sucesso verificável autonomamente?] |
| V. Economia de contexto / fronteira | [fatias estreitas, corte por fronteira?] |
| VI. Artefatos vivos | [doc e código no mesmo PR?] |
| VII. Governança leve / YAGNI | [só o necessário agora?] |

**[Sem violações. | Complexity Tracking: ...]**

## Como

<!--
  O COMO: arquitetura, corte por fronteira (bounded context — permite paralelizar com
  segurança), decisões (decisão arquitetural → ADR, imutável). Em feature de CÓDIGO,
  gere também data-model.md/contracts/; em docs, não se aplicam.
  Raia infra: inclua backup/dry-run/rollback AQUI (bloco de reversibilidade do §7).
-->

- [...]

## Verificação (DoD)

<!-- Os comandos que provam os critérios da spec, com o esperado de cada um.
     O comando /dod roda; aqui você ESCREVE (design-time — skill dod-verificavel). -->

- `[comando]` → [esperado]

<!--
  GATE (indelegável): plan aprovado por humano antes de virar tasks.
  Handoff: plan-arquiteto → (aprovação) → tasks → dev-implementador.
-->
