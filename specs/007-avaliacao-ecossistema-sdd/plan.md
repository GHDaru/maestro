# Plan 007 — Avaliação do ecossistema SDD

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-30

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 007 |
| II. Orquestração humano-governada | ✅ pesquisa propõe; a decisão de adotar/descartar é do ADR com gate humano |
| III. Reversibilidade / gates de risco | ✅ só leitura/pesquisa — nada instalado; adoção futura teria spec própria |
| IV. Test-First / DoD verificável | ✅ DoD por grep (nº de fichas, fontes, vereditos, ADR) |
| V. Economia de contexto / fronteira | ✅ papel `curador-pesquisa` — evidência externa, sem decidir nem implementar |
| VI. Artefatos vivos | ✅ ficha em `docs/research/`, decisão em ADR, link no roadmap |
| VII. Governança leve / YAGNI | ✅ fichamento por fontes primárias, sem instalar (instalar só se adotar) |

**Sem violações.**

## Como

- Executar o papel **`curador-pesquisa`**: WebSearch/WebFetch nas fontes primárias
  (repos e docs oficiais) das 5 ferramentas mínimas + varredura de "outras relevantes".
- Ficha no padrão da casa (`docs/research/`): **pergunta → por ferramenta:** o que é,
  mecânica central, o que faz bem, onde conflita com o Maestro, **veredito FR2** com
  destino concreto → **fontes** (links).
- Critério de veredito (mesmo da 0005): conflito com princípio = descarta; ideia boa
  sem a ferramenta = absorve (nomeando artefato-destino); complementar e maduro = adotar
  (spec própria); imaturo/incerto = observar (com gatilho de reavaliação).
- **ADR 0008** consolida; roadmap §6 ganha link "ecossistema avaliado".

## Verificação (DoD)

- `grep -c "^### " docs/research/avaliacao-ecossistema-sdd.md` ≥ 5 (fichas).
- `grep -c "Veredito" docs/research/avaliacao-ecossistema-sdd.md` ≥ 5.
- `grep -c "https://" docs/research/avaliacao-ecossistema-sdd.md` ≥ 5 (fontes).
- `ls docs/adr/0008-*.md` existe; roadmap linka a ficha/ADR.
