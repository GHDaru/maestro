# Plan 014 — Navegação em cinco trilhas

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 014, derivada do ADR 0011 |
| II. Orquestração humano-governada | ✅ decisão de ordem das trilhas foi do Steward |
| III. Reversibilidade / gates de risco | ✅ mudanças em conteúdo e motor — reversíveis por git |
| IV. Test-First / DoD verificável | ✅ **nova fitness function** de colisão de slug, testada com falha deliberada |
| V. Economia de contexto / fronteira | ✅ trilha declara o tipo — leitor (e agente) sabe o que esperar sem abrir |
| VI. Artefatos vivos | ✅ sumário, capa, motor e receitas no mesmo ciclo |
| VII. Governança leve / YAGNI | ✅ Jornada V1 é mapa; diálogo longo fica para quando o companion existir |
| VIII. Comunicação inteligível | ✅ siglas expandidas na 1ª ocorrência de cada receita |

**Sem violações.**

## Como

- **Sumário**: `partes` ganham `tipo` e `descricao`; novo bloco `cadencia` (nome, tempo,
  percurso, página inicial).
- **Motor** (`build.mjs`): renderiza tipo/descrição na barra lateral e no sumário; cartões
  de cadência no topo do sumário.
- **Correção de defeito encontrado durante o ciclo**: com cinco `README.md` no livro, o
  slug derivado só do nome colidia (`readme.html` cinco vezes, sobrescrevendo em silêncio).
  Causa raiz nas duas funções que derivam slug (item e resolvedor de links). Correção:
  slug de `README.md`/`index.md` usa o **diretório pai**; o resolvedor passa a resolver o
  caminho relativo antes de derivar. Mais a fitness function que teria pego o defeito.
- **Receitas**: quatro receitas curtas, cada uma com "Pronto quando" e link para o capítulo
  que explica o porquê (Diátaxis: como-fazer não explica).

## Verificação (DoD)

- `node publicar/build.mjs` → ≥34 páginas, links OK.
- Colisão injetada deliberadamente → build falha com código 1 e lista o conflito.
- `grep -c '"tipo"' sumario.json` = 5; cinco páginas de README distintas em `site/`.
- `grep -c 'blob/main' site/index.html` = 0 nos links de conteúdo.
