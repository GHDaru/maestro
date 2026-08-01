# Diagramas do Maestro

Peças visuais que explicam o método — para apresentar a comitês, onboarding e consulta rápida.
Cada peça existe em três formas: **markdown** (conteúdo textual, versionável e diffável),
**PDF** (para apresentar/imprimir) e **HTML** (a fonte visual que gera o PDF).

| # | Peça | Markdown | PDF | Fonte HTML |
|---|---|---|---|---|
| 01 | **Definição** — o que é o Maestro em uma frame | [md](01-definicao.md) | [pdf](pdf/01-definicao.pdf) | [html](fontes/01-definicao.html) |
| 02 | **Problema → solução** | [md](02-problema-solucao.md) | [pdf](pdf/02-problema-solucao.pdf) | [html](fontes/02-problema-solucao.html) |
| 03 | **Fluxo** — o ciclo spec-driven (timeline) | [md](03-fluxo.md) | [pdf](pdf/03-fluxo.pdf) | [html](fontes/03-fluxo.html) |
| 04 | **SIPOC** — o ciclo de entrega como processo | [md](04-sipoc.md) | [pdf](pdf/04-sipoc.pdf) | [html](fontes/04-sipoc.html) |
| 05 | **BPMN** — o processo em raias, com os gates onde o fluxo para | [md](05-bpmn-processo.md) | [png](05-bpmn-processo.png) | [html](fontes/05-bpmn-processo.html) |

## Código de cores (comum a todas as peças)

- 🟣 **violeta** — agente de IA executa
- 🟡 **ouro ◆** — humano: decisão / gate indelegável
- 🟢 **verde ●** — verificado / mecânico (CI)

## Regenerar os PDFs

Os PDFs são renderizados dos HTML em `fontes/` com Chromium (Playwright). O HTML é a fonte de
verdade visual; ao editar um `fontes/*.html`, regenere o PDF correspondente:

```bash
# playwright-core + o Chromium já presente em /opt/pw-browsers (sem baixar navegador)
node render-pdf.mjs   # slides = 1280×720 (16:9); fluxo/sipoc = largura fixa, altura medida
```

> Slides (01, 02) são página única 16:9; fluxo (03) e SIPOC (04) são página única de altura
> ajustada ao conteúdo. Tema escuro (identidade "sala de concerto"), coerente com o handbook.
