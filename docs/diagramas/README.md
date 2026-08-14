# Diagramas do Maestro

Peças visuais que explicam o método — para apresentar a comitês, onboarding e consulta rápida.
As peças **01–05** existem em três formas: **markdown** (conteúdo textual, versionável e
diffável), **PDF** (para apresentar/imprimir) e **HTML** (a fonte visual que gera o PDF).
A **06** é a exceção declarada na nota abaixo da tabela.

| # | Peça | Markdown | PDF | Fonte HTML |
|---|---|---|---|---|
| 01 | **Definição** — o que é o Maestro em uma frame | [md](01-definicao.md) | [pdf](pdf/01-definicao.pdf) | [html](fontes/01-definicao.html) |
| 02 | **Problema → solução** | [md](02-problema-solucao.md) | [pdf](pdf/02-problema-solucao.pdf) | [html](fontes/02-problema-solucao.html) |
| 03 | **Fluxo** — o ciclo spec-driven (timeline) | [md](03-fluxo.md) | [pdf](pdf/03-fluxo.pdf) | [html](fontes/03-fluxo.html) |
| 04 | **SIPOC** — o ciclo de entrega como processo | [md](04-sipoc.md) | [pdf](pdf/04-sipoc.pdf) | [html](fontes/04-sipoc.html) |
| 05 | **BPMN** — o processo em raias, com os gates onde o fluxo para | [md](05-bpmn-processo.md) | [png](05-bpmn-processo.png) | [html](fontes/05-bpmn-processo.html) |
| 06 | **Fluxo v5** — ⚠️ **proposta, não vigente**: o ciclo comparado a um desenho externo de 13 passos | [md](06-fluxo-v5-proposta.md) | — | — |

> A peça **06 é uma proposta**; quem descreve o processo em vigor é a **05**. Ela nasce só em
> markdown — o desenho é Mermaid, que o GitHub renderiza e o `render-pdf.mjs` não resolve sem
> biblioteca externa. Ganha PDF se a proposta virar processo.

## Código de cores (peças 01–05)

- 🟣 **violeta** — agente de IA executa
- 🟡 **ouro ◆** — humano: decisão / gate indelegável
- 🟢 **verde ●** — verificado / mecânico (CI)

> A peça **06 usa um código próprio e conflitante** (lá o verde quer dizer "já existe hoje",
> não "verificado"), e o declara na própria página. O motivo é que ela responde a outra
> pergunta: as peças 01–05 colorem **quem executa**; a 06 colore **o que mudaria**. Duas
> perguntas, duas escalas — o que não pode é a segunda passar por continuação da primeira.

## Regenerar os PDFs

Os PDFs são renderizados dos HTML em `fontes/` com Chromium (Playwright). O HTML é a fonte de
verdade visual; ao editar um `fontes/*.html`, regenere o PDF correspondente:

```bash
# playwright-core + o Chromium já presente em /opt/pw-browsers (sem baixar navegador)
node render-pdf.mjs   # slides = 1280×720 (16:9); fluxo/sipoc = largura fixa, altura medida
```

> Slides (01, 02) são página única 16:9; fluxo (03) e SIPOC (04) são página única de altura
> ajustada ao conteúdo. Tema escuro (identidade "sala de concerto"), coerente com o handbook.
