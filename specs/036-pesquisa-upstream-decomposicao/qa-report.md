# QA-report 036 — Pesquisa do upstream

- **Data**: 2026-08-03 · **Raia**: plena · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Fontes primárias linkadas | ≥12 | ✅ 14 links, agrupados por família |
| Gap medido por comando | 34 specs, 20 de origem pontual | ✅ classificação feita sobre o campo `Origem` de cada spec |
| Cobertura upstream do toolkit | zero | ✅ `grep` em agentes e skills não acha decomposição |
| Licença incompatível declarada | CC BY-NC-SA do PM-Skills | ✅ tratada antes da proposta |
| Proposta contida | 1 objeto, 1 verbo, 1 portão, 1 gate | ✅ + seção "o que não faremos" |
| `check-links.sh`, `check-language.sh`, build | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ veredito explícito por família. **FR2**: ✅ gap medido, não afirmado.
- **FR3**: ✅ licença declarada. **FR4**: ✅ pirâmide explicitamente fora.
- **FR5**: ✅ três riscos, incluindo o desconfortável (o gap pode não se pagar aqui).

## Achados

1. **O Spec Kit não tem upstream — confirmado comando a comando**, não por impressão. Isso
   muda a leitura do ADR 0008: adotamos uma ferramenta que cobre metade do problema, e a
   outra metade nunca foi nomeada como lacuna até agora.
2. **A skill que faria o corte não existe pronta em lugar nenhum.** O que existe é (a) muito
   pesado (BMAD, sete papéis), (b) abaixo da spec (`decompose` → issues), ou (c) conhecimento
   de livro que ninguém empacotou como skill — os nove padrões de fatiamento e o SPIDR.
3. **Licença é critério de adoção, e quase passou batido.** O catálogo mais útil que
   encontrei (70 skills de produto) é CC BY-NC-SA: citar sim, copiar não. Fica como regra
   para futuras absorções — verificar licença **antes** de propor uso, não depois.
4. **Contra-evidência registrada**: 20 dos 34 ciclos deste repositório nasceram de conversa
   e entregaram. A pesquisa recomenda **não construir sem dor real** — o que é coerente com
   a regra de nascimento das skills e com o corolário C9.

## Pendência de gate

- **Decisão do Steward** sobre a proposta (seção 6 da pesquisa) — antes de qualquer
  implementação.
- promoção dev → main aguarda aprovação humana.
