# Spec 010 — Estudo hands-on do Superpowers (Apêndice B)

- **Status**: Aprovada ("vamos avaliar este repositório primeiro") · **Raia**: Plena · **Data**: 2026-07-31
- **Origem**: fork `GHDaru/superpowers` (@`44c9b2d`, v6.2.0) adicionado pelo Steward.
  O ADR 0008 avaliou o Superpowers por fontes secundárias (veredito: absorver ideias +
  observar) e previu: "se um gatilho disparar, a reavaliação deve incluir hands-on".
  O gatilho disparou — o Steward trouxe o fork.

## O quê e por quê

Estudar o repositório real (14 skills, hooks, mecânica de enforcement) e produzir o
**Apêndice B** do handbook no padrão do Apêndice A: anatomia, ideias que contribuem,
onde não serve, e **vereditos propostos** (absorver/observar/descartar, com destino
concreto) para decisão do Steward. Valor: fechar a avaliação prometida no ADR 0008 com
evidência primária, e colher as práticas que o líder do ecossistema (~93k stars) provou.

## Requisitos funcionais

- **FR1**: `docs/handbook/apendice-b-superpowers.md` com: anatomia (skills/hooks/
  distribuição), ≥6 ideias avaliadas com veredito e destino, seção "onde não serve",
  tensões com o método (ex.: HARD-GATE universal × nossas raias) e data do estudo.
- **FR2**: apêndice entra no **livro** (sumário do site) e no índice do handbook.
- **FR3**: vereditos ficam como **proposta** até aprovação do Steward (gate de mérito,
  como no ciclo 008).

## Fora de escopo

- Incorporar qualquer absorção (ciclo seguinte, após aprovação — padrão 008).
- Instalar/rodar o Superpowers como plugin no maestro.

## Critérios de aceite (DoD)

- [ ] QUANDO o leitor abrir o sumário do site, O SISTEMA DEVE listar o Apêndice B na
      seção Apêndices (build verde com a página nova).
- [ ] `grep -c "Veredito" apendice-b-superpowers.md` ≥ 6.
- [ ] `grep -l "44c9b2d" apendice-b-superpowers.md` não-vazio (commit estudado citado).
- [ ] `grep -l "raia" apendice-b-superpowers.md` não-vazio (tensão registrada).

## Clarify (resolvido)

1. **Profundidade**: leitura das 14 skills (6 centrais na íntegra) + hooks + package —
   sem executar o plugin (fora de escopo).
