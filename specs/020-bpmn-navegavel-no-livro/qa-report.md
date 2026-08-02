# QA-report 020 — BPMN navegável no livro

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `node publicar/build.mjs` | exit 0, 35 páginas + sumário | ✅ `✓ Site gerado: 35 páginas + sumário em site/ (links internos OK)` |
| Imagem do BPMN publicada | `site/05-bpmn-processo.png` existe | ✅ copiada pelo motor |
| **Portão de imagem provado falhando** | exit 1 ao apontar imagem inexistente | ✅ `05-bpmn-processo.html -> [img] imagem-inexistente.png` |
| **Portão de `.md` cru provado falhando** | exit 1 com a reescrita desligada | ✅ `✗ 38 link(s) interno(s) quebrado(s)` — todos `[md cru]` |
| Links do bloco no HTML publicado | 38 links, 0 terminando em `.md` | ✅ medido no navegador: `links no bloco: 38 | .md restantes: 0` |
| Cliques em navegador real | 4 nós levam à página certa | ✅ Especificar→cap. 03 · Gate de merge→cap. 10 · DoD verde?→cap. 09 · npx skills add→receita de instalação |
| Largura | bloco não estoura o viewport (1280px) | ✅ `estoura a largura? false` |
| Temas | legível em claro e escuro | ✅ capturas nos dois temas; humano ganhou barra sólida porque a cor sozinha não o distinguia do agente |

## Cobertura dos requisitos

- **FR1** (copiar imagens): ✅ `build.mjs` varre `![...](...)` de cada página e copia o alvo relativo.
- **FR2** (portão de `<img src>`): ✅ implementado e provado falhando.
- **FR3** (reescrita em HTML bruto): ✅ `resolverHtmlBruto` aplica a mesma regra de `link_open`;
  o Markdown guarda `.md` (vale no GitHub), o site recebe `.html`.
- **FR4** (portão de `.md` cru): ✅ implementado e provado falhando.
- **FR5** (navegável + imagem): ✅ bloco de 6 raias no topo; PNG logo abaixo, rotulado
  "versão para apresentação".
- **FR6** (distinção visual): ✅ agente (ouro claro), automação (verde), humano (barra sólida),
  gate humano ◆ ouro, DoD ◆ verde, artefato tracejado — com legenda.

## Verificação no site publicado (após a promoção)

| Check | Resultado |
|---|---|
| `05-bpmn-processo.png` em `ghdaru.github.io/maestro/` | ✅ HTTP 200 |
| Raias renderizadas na página publicada | ✅ 6 |
| Destinos únicos do bloco, um a um por HTTP | ✅ 19/19 respondem 200 |
| `href` terminando em `.md` na página publicada | ✅ nenhum |

## Achados

1. **Terceira ocorrência da mesma classe de erro** (anti-padrão 13 — o check mede o proxy,
   não o fato): o portão de links validava `<a href>` e ignorava `<img src>`; depois de
   corrigido, ignorava também `.md` não reescrito. Cada vez que o portão ganhou um formato
   novo de link, o formato entrou sem cobertura. Registro para a retro: **portão de links
   deve enumerar todo atributo que vira requisição** (`href`, `src`, `srcset`, `poster`).
2. **Template de plano estava em I–VII** desde o ADR 0010 (princípio VIII, de 01/08). O
   Constitution Check dos ciclos 013–019 não tinha onde marcar o princípio VIII — norma sem
   forcing function de novo. Corrigido em `plan-template.md` e `novo-ciclo.sh` (T7).

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
