# Spec NNN — [TÍTULO]

- **Status**: Rascunho · **Raia**: [leve|plena|infra] · **Data**: [YYYY-MM-DD]
- **Origem**: [de onde vem esta demanda — pedido do Steward, roadmap, retro, bug]

<!--
  RAIA (modelo operacional §3): valor da spec ∝ ambiguidade × raio × irreversibilidade.
  - leve: dá para descrever o diff numa frase → NEM PRECISA desta spec (o PR é o artefato).
  - plena: feature ambígua, contrato, mudança cross-feature → este template inteiro.
  - infra: infra/migração/deploy → SEMPRE plena + gates de reversibilidade (§7).
  Na dúvida entre leve e plena → plena. Infra nunca é leve.
-->

## O quê e por quê

[O problema e o valor de negócio. O QUÊ e o PORQUÊ — nunca o COMO (isso é do plan).
Jornada(s) servida(s), se houver.]

## Requisitos funcionais

- **FR1**: [...]
- **FR2**: [...]

## Fora de escopo

<!-- Tão importante quanto o escopo: o que este ciclo NÃO faz, para ninguém "aproveitar". -->
- [...]

## Critérios de aceite (DoD)

<!--
  VERIFICÁVEL AUTONOMAMENTE (Princípio IV; skill dod-verificavel):
  - Comportamento → forma EARS: "QUANDO <condição> O SISTEMA DEVE <comportamento observável>"
    (vira teste quase 1:1: condição = arrange/act, comportamento = assert).
  - Estrutura/invariante → par (comando, esperado): grep/ls/teste com saída vazia/não-vazia/exit code.
  - Se não dá para responder "que comando prova isto?", o critério ainda está vago — reescreva.
  - Proibido: meta numérica gameável ("cobertura ≥ X%"), "está claro", "funciona bem".
-->
- [ ] QUANDO [condição] O SISTEMA DEVE [comportamento observável].
- [ ] `[comando]` → [esperado: vazio | = N | exit 0].

## Clarify

<!-- Ambiguidade NÃO se inventa — vira pergunta ao Steward. Resolvidas → registre a resposta aqui. -->
1. [pergunta] → [resposta/decisão, quando resolvida]

<!--
  GATE (DoR — indelegável): esta spec só vira plan após aprovação humana.
  Handoff: spec-agent → (aprovação) → plan-arquiteto.
-->
