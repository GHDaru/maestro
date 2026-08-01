# Spec 012 — Apêndice C: panorama exploratório de templates

- **Status**: Aprovada (pedido direto do Steward) · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: "assim como avaliamos SDD do git, superpowers, maestro — temos outros; gere
  um apêndice com uma pesquisa exploratória destes templates".

## O quê e por quê

Varredura **exploratória** (diferente do hands-on dos apêndices A/B) do resto do
ecossistema de templates/frameworks, com **triagem** (🔬 hands-on com gatilho / 👁
observar / ⛔ fora do problema) — formalizando o **funil de avaliação**: exploratório →
gatilho → hands-on → absorção por gate. Valor: garimpo sistemático sem re-litigar o já
decidido, e gatilhos explícitos em vez de FOMO.

## Requisitos funcionais

- **FR1**: `docs/handbook/apendice-c-panorama-templates.md` — ≥8 itens novos (não
  repetir os já julgados; linkar ficha 007 e apêndices A/B), cada um com fonte,
  "o que ensina" e triagem; síntese com gatilhos.
- **FR2**: no livro (sumário + índice do handbook).

## Fora de escopo

- Hands-on de qualquer item (só por gatilho, ciclo próprio).
- Importação de skills/templates de marketplaces (garimpo por dor, via curador).

## Critérios de aceite (DoD)

- [ ] QUANDO o build rodar, O SISTEMA DEVE gerar 23 páginas com links OK.
- [ ] `grep -c "Triagem" apendice-c` ≥ 8 · `grep -c "https://" apendice-c` ≥ 8.
- [ ] Nenhuma repetição de veredito dos já julgados (apêndice remete à ficha/A/B).

## Clarify (resolvido)

1. **Profundidade**: fontes secundárias + repos (varredura); hands-on fica para gatilho.
