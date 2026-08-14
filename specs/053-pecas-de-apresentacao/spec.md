# Spec 053 — Peças de apresentação: o fluxo v5 e o caderno de desenvolvimento

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-14
- **Origem**: pedido do Steward após comparar o Maestro com o fluxo de ciclo de vida
  desenhado por um arquiteto externo (13 passos), e depois pedir uma apresentação do método
  com foco em desenvolvimento.

> **Raia**: leve. **Ambiguidade** baixa — o conteúdo das duas peças já foi revisto e
> aprovado pelo Steward antes de virar arquivo; **raio** contido a `docs/` (nada da
> superfície instalável muda); **irreversibilidade** baixa — são páginas, e reverter é
> apagar. Leve, mas com revisão independente, que a raia leve mantém.

## O quê e por quê

Duas lacunas de **comunicação**, não de método:

1. O repositório desenha o processo **vigente** (peça 05, BPMN), mas não tinha onde guardar
   um desenho **proposto** — e a comparação com o fluxo do arquiteto externo produziu um:
   três caixas novas, uma movida, e três lacunas reais nomeadas. Sem lugar no repositório,
   a comparação vive numa conversa e evapora no próximo reset de contexto.
2. Existem duas apresentações do método — a **executiva** (o porquê) e o **caderno técnico**
   (os 12 elementos do handbook). Falta a que serve a quem vai **desenvolver dentro do
   método**: quais comandos existem, quais arquivos a IA lê, o que cada artefato do ciclo
   obriga, onde o fluxo para e quem destrava.

## Requisitos funcionais

- **FR1**: QUANDO alguém abrir a peça 06, O SISTEMA DEVERÁ identificá-la como **proposta não
  vigente** já no título e no primeiro parágrafo, e apontar a peça 05 como o processo em
  vigor — uma proposta indistinguível do vigente é pior que a ausência dela.
- **FR2**: A peça 06 DEVERÁ marcar, passo a passo, o que já existe hoje e o que seria novo,
  e nomear as lacunas com a **evidência** que as sustenta (caminho de arquivo ou comando).
- **FR3**: A apresentação de desenvolvimento DEVERÁ percorrer o ciclo do ponto de vista de
  quem executa — comandos, artefatos, portões, papéis — e todo número que ela citar
  (agentes, portões, comandos, skills) DEVERÁ conferir com o disco.
- **FR4**: As duas peças DEVERÃO estar ligadas a partir do índice de onde alguém as
  procuraria (`docs/diagramas/README.md` e `docs/handbook/README.md`).

## Fora de escopo

- PDF da peça 06: o desenho é um diagrama Mermaid, que o `render-pdf.mjs` não resolve sem
  biblioteca externa. A peça nasce em markdown (renderiza no GitHub) e no artefato
  publicado; PDF entra se e quando a proposta virar processo vigente.
- Adotar qualquer um dos três passos propostos. Esta spec **documenta** a proposta; adotar
  é decisão do Steward e vira ciclo próprio.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- A peça 06 existe, diz "proposta" no título e no primeiro parágrafo, e linka a 05.
- Todo número citado na apresentação de desenvolvimento é conferível por um comando, e o
  comando está no qa-report.
- `docs/diagramas/README.md` e `docs/handbook/README.md` listam as peças novas.
- A bateria completa de portões, o plugin e o build do livro seguem verdes.

## Clarify

1. A fila de intenções (passo 1 da proposta) é do Maestro ou de quem instala o método?
   — **fica em aberto na própria peça**, como pergunta que precede o ciclo de adoção.
