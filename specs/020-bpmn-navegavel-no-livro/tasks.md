# Tasks 020 — BPMN navegável no livro

## Verificação primeiro
- [x] T0 — portão de `<img src>` no motor de publicação, **provado falhando** com imagem inexistente
- [x] T1 — portão de `.md` cru no HTML publicado, **provado falhando** com a reescrita desligada

## Implementação
- [x] T2 — copiar para `site/` as imagens referenciadas por cada página
- [x] T3 — extrair `resolverHref()` e aplicá-la ao HTML bruto embutido (`resolverHtmlBruto`)
- [x] T4 — classes `.bpmn*` no tema, derivadas por `color-mix` das variáveis existentes
- [x] T5 — bloco navegável em `docs/diagramas/05-bpmn-processo.md`: 6 raias, 38 links
- [x] T6 — distinguir humano (barra sólida), DoD mecânica (verde) e ramos paralelos ("ou")
- [x] T7 — template de plano e `novo-ciclo.sh` com a linha do princípio VIII (estavam em I–VII)

## Gate
- [x] T8 — DoD verde (build, portões provados, cliques em navegador real, capturas)
- [ ] T9 — gate de merge humano → `promover-main.sh`
