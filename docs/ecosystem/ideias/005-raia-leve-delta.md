# 005 — Mudança descrita como *delta*, não como spec inteira

- **Id**: `raia-leve-delta`
- **Fonte**: `Fission-AI/OpenSpec`
- **Observado em**: 2026-07-29
- **Veredito no momento**: absorver
- **Destino**: `docs/governance/operating-model.md`
- **Gatilho de reavaliação**: —

## A ideia

Para mudança pequena, o artefato não é uma spec completa: é o **delta** — o que muda em
relação ao que já existe. Cerimônia proporcional ao tamanho da mudança.

## Por que atravessa (ou não)

A ferramenta foi descartada no ADR 0005 (uma ferramenta SDD só, e o Spec Kit já estava
adotado), mas a ideia virou a **raia leve**: na raia leve o *pull request* é o artefato.
Caso limpo de "descartar a ferramenta, absorver a ideia" — o primeiro do repositório, e o
que estabeleceu o critério.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | a **ferramenta** conflitava (duas fontes de verdade); a ideia reforça o Princípio VII |
| 2 | Licença e redistribuição | MIT na origem; nada copiado |
| 3 | Função já servida | não à época — o método tinha uma cerimônia só, para tudo |
| 4 | Custo de contexto | negativo: economiza |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | 12 ciclos rodaram na raia leve; `check-cycle.sh` mede a distribuição |
| 7 | Dor real hoje | sim, e imediata: spec plena para mudança de uma linha |
