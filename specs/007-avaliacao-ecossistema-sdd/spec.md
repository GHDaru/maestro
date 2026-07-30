# Spec 007 — Avaliação do ecossistema SDD (Superpowers, BMAD e afins)

- **Status**: Aprovada · **Raia**: Plena · **Data**: 2026-07-30
- **Origem**: pergunta do Steward ("foi avaliado o OpenSpec? Spec Kit? Superpowers? que
  outros existem?"). O OpenSpec foi avaliado e descartado com racional (ADR 0005); o resto
  do ecossistema **nunca passou pelo crivo** — lacuna honesta do método.

## O quê e por quê

Pesquisar e fichar, **com fontes citadas**, as principais alternativas/complementos de
Spec-Driven Development e de toolkits de agentes, e decidir por ADR o que o Maestro
**adota / absorve como ideia / descarta** — como foi feito com o OpenSpec.

**Valor**: o Maestro afirma "trazemos conceito adaptado de todas as fontes" (roadmap §6).
Sem esta avaliação, a afirmação não é honesta: só olhamos 2 ferramentas (Spec Kit, OpenSpec).
A decisão também blinda contra re-litigar ("já avaliamos X? onde?") — resposta vira link.

## Requisitos funcionais

- **FR1**: ficha de pesquisa `docs/research/avaliacao-ecossistema-sdd.md` no padrão da casa
  (pergunta → avaliação crítica → fontes), executada pelo perfil `curador-pesquisa`, cobrindo
  no mínimo: **Superpowers** (obra/superpowers), **BMAD-Method**, **Kiro (AWS)**,
  **Taskmaster AI**, **Agent OS (Builder Methods)** — e registrando outras encontradas.
- **FR2**: para cada ferramenta, veredito explícito: **adotar** / **absorver ideia** (qual,
  vira o quê no Maestro) / **descartar** (por quê) / **observar** (reavaliar quando).
- **FR3**: **ADR 0008** com a decisão consolidada (imutável, como a 0005 do OpenSpec).
- **FR4**: seção "Ecossistema avaliado" no roadmap (ou link) — a resposta canônica para
  "isso foi avaliado?".

## Fora de escopo

- Instalar/vendorizar qualquer ferramenta nova (se algo merecer adoção, vira spec própria).
- Reavaliar OpenSpec (ADR 0005 já decidiu) e Spec Kit (adotado; vendorização é a F4).
- Templates de jornada/design (spec 008, F4).

## Critérios de aceite (DoD)

- [ ] `docs/research/avaliacao-ecossistema-sdd.md` existe com ≥5 ferramentas fichadas,
      cada uma com ≥1 fonte (link) e veredito de FR2.
- [ ] `docs/adr/0008-*.md` registra a decisão consolidada.
- [ ] Ideias absorvidas apontam artefato-destino concreto (skill/regra/spec futura).
- [ ] Roadmap/ADR linkados (resposta canônica de "já foi avaliado?").

## Clarify (resolvido)

1. **Profundidade**: fichamento por fontes primárias (repo/docs oficiais) — sem instalar
   e rodar cada uma (YAGNI; instalar só se o veredito for "adotar", em spec própria).
2. **Lista mínima**: as 5 nomeadas + o que a pesquisa revelar de relevante.
