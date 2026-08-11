# Spec 049 — O índice de decisões com portão

- **Status**: Em andamento · **Raia**: plena · **Data**: 2026-08-11
- **Origem**: achado `achado-046-indice-adr-congelado`, aberto no ciclo 046 e ainda em aberto.

> **Raia**: plena. **Ambiguidade** baixa (o fato a medir é conhecido); **raio** interno
> (o índice não é instalado); **irreversibilidade** baixa. Plena porque cria portão novo, e
> portão novo entra por spec.

## O quê e por quê

No ciclo 046, ao escrever um ADR, encontrei o índice `docs/adr/README.md` **congelado desde
o 0017**:

| Fato, verificado em 2026-08-10 | Consequência |
|---|---|
| ADRs **0018 e 0019** existiam e não estavam listados | duas decisões que ninguém acha pelo índice |
| **0017** constava "Aceito" desde o ciclo 039, superado pelo 0018 | **uma decisão revertida lida como corrente** |

O segundo é o grave. Um índice que lista uma decisão revertida como aceita não é um índice
incompleto: é um índice **errado**, e quem o consulta — humano ou agente — decide com base
nele. Foi corrigido à mão e registrado como achado **aberto**, porque a correção não impedia
a repetição: nada media a diferença entre o índice e os arquivos.

É a mesma forma do anti-padrão 15 (artefato de planejamento que congela) e a mesma que o
`check-roles.sh` já guarda para os perfis de agente — índice escrito à mão sobre arquivos
legíveis por máquina envelhece em silêncio. A diferença é que aqui não havia portão.

## Requisitos funcionais

- **FR1**: QUANDO um ADR existir em `docs/adr/`, O SISTEMA DEVERÁ falhar se ele não estiver
  listado no índice.
- **FR2**: QUANDO o índice listar um ADR, O SISTEMA DEVERÁ falhar se o arquivo apontado não
  existir.
- **FR3**: QUANDO um ADR declarar no próprio corpo que foi **superado**, O SISTEMA DEVERÁ
  falhar se o índice não disser o mesmo — e o inverso.
- **FR4**: QUANDO um ADR não declarar status nenhum, O SISTEMA DEVERÁ falhar: sem status no
  ADR, não há com o que o índice concordar.

## Fora de escopo

- **Gerar o índice a partir do disco.** Seria a lição do ADR 0013 aplicada aqui, e é
  tentador — mas o índice tem prosa em volta (nota de numeração, protocolo) e é página
  publicada do livro. Gerar exigiria fatiar a página; o portão custa menos e mede o mesmo
  fato. Fica como gatilho: **se o índice divergir uma segunda vez**, geramos.
- **Julgar o mérito de um ADR** ou a qualidade da prosa. O portão mede coerência entre índice
  e arquivos — anti-padrão 13.
- **Traduzir ou instalar o índice do Maestro.** Ele é português e é página do livro. O que
  viaja é o **portão**, não o conteúdo — decisão revista durante a execução: a primeira
  versão desta spec deixava o portão fora, e isso contradizia a lição do ciclo 048 (o método
  tem de funcionar onde cai). Um projeto que instalou o Maestro escreve ADRs porque o método
  manda, e o índice dele congelaria exatamente como o nosso. O portão vai junto, e diz
  explicitamente quando ainda não há ADR nenhum.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `scripts/check-adr.sh` cobre FR1 a FR4 e foi **visto acusar por mutação** em cada um.
- Entre as mutações está **o defeito real do ciclo 046** — índice sem 0018/0019 e 0017 como
  "Aceito" —, para provar que o portão o teria pego.
- Entrada ausente é falha, nunca aprovação.
- O portão entra na CI como bloqueante.
- O achado `achado-046-indice-adr-congelado` é **fechado** no índice de decisões, apontando
  para o relatório deste ciclo.

## Clarify

1. **Por que não estender o `check-roles.sh`?** Porque ele mede outro fato (papéis × agentes)
   e o Princípio VI proíbe duplicar função servida, não proíbe medir fatos diferentes em
   portões diferentes. Juntar os dois criaria um portão que falha por dois motivos sem
   nome — o oposto do que faz um portão ser lido.
2. **Por que ler o status por `grep` e não por número de linha?** Porque dois ADRs (0005 e
   0008) ganharam no ciclo 047 uma nota de migração acima do cabeçalho: uma leitura por
   linha fixa leria a nota. A forma tem de sobreviver ao que já aconteceu com os arquivos.
