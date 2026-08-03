# ADR 0010 — Princípio VIII: comunicação inteligível (sigla nunca nasce nua)

- **Status**: Aceito · **Data**: 2026-08-01 · **Origem**: pedido direto do Steward

## Contexto

O defeito nomeado desde o início — o "amontoado" — tem uma causa recorrente: **sigla sem
expansão**. Já havia a skill `fight-the-pile-up` (regra de documento) e o glossário, mas
faltava a regra para a **conversa**: cada resposta é lida isoladamente, e "já expliquei
antes" não ajuda quem entra agora. O Steward pediu que a regra subisse à constituição.

## Decisão

Novo **Princípio VIII — Comunicação inteligível**, com Iron Law: em cada resposta,
documento ou artefato, a **primeira ocorrência** de uma sigla vem por extenso, com a
abreviação entre parênteses; depois, abrevia-se livremente. **A contagem reinicia a cada
resposta/documento.** Brechas fechadas explicitamente ("todo mundo conhece", "já expliquei
antes", "é jargão do domínio"). Termo novo entra no glossário.

Constituição sobe para **1.1.0** (MINOR: novo princípio).

## Alternativas consideradas

- **Manter só na skill `fight-the-pile-up`**: a skill governa documentos; a lacuna era a
  resposta em conversa — e skill não tem a força de princípio inegociável.
- **Regra apenas no CLAUDE.md**: valeria para agentes deste repo, não para o método
  (o Maestro é o produto; a regra é do método, não da instância).

## Consequências

- (+) O leitor de qualquer resposta isolada entende sem histórico — reduz a barreira de
  entrada, que é a métrica-bússola do roadmap.
- (+) Alimenta o glossário por construção.
- (−) Leve verbosidade em respostas com muitas siglas; aceita — clareza paga.

## Registro

`docs/governance/principles.md` v1.1.0 (Princípio VIII); skill
`fight-the-pile-up` permanece como operacionalização em documentos.
