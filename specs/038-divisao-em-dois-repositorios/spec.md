# Spec 038 — Divisão em dois repositórios (fatia 1: a fronteira decidível)

- **Status**: Concluída · **Raia**: infra · **Data**: 2026-08-06
- **Origem**: decisão do Steward — "vamos dividir o projeto do maestro em dois. Um é o
  instalável, skills, scripts e orientações sobre seu uso. O livro ou guia/documentação
  vamos colocar em outro repositório."

> **Raia**: infra. **Ambiguidade** média (o corte tem derivação pronta no corolário C10;
> as duas incógnitas foram resolvidas no gate); **raio** total (todo arquivo do repositório
> é afetado); **irreversibilidade** alta — depois que 10.000 linhas mudam de repositório,
> o histórico não volta barato. Por isso este ciclo **não move nenhum arquivo**.

## O quê e por quê

O corte já estava derivado antes de ser pedido. O corolário **C10** diz: *o que é instalado
é lido por máquinas; o que é publicado é lido por pessoas*. O repositório mistura as duas
audiências desde a fundação, e a mistura já cobra preço — o `check-language.sh` existe
justamente para impedir que o inglês do instalável vaze para o português do livro, dentro
do mesmo repositório.

A medição do acoplamento, porém, mostrou que o corte **não é limpo**:

| Medida | Valor | Consequência |
|---|---|---|
| Páginas do site publicado | 37 | destas, **9 vêm do lado instalável** (governança, agentes, roadmap, índices) |
| Links do livro atravessando a fronteira | 35 | 15 → `research`, 15 → `governance`, 4 → `adr`, 1 → `agents` |
| Caminhos de código citados como evidência no livro | 22 | `scripts/…`, `.claude/…` — a evidência do livro é este repositório |

Mover arquivos antes de decidir isso produziria um livro cujos capítulos citam evidência
que ele não tem mais, e um site que perde 9 páginas sem ninguém perceber no dia. **A fatia 1
existe para que a fatia 2 seja mecânica.**

## Decisões do gate humano (2026-08-06)

1. **A memória fica toda no toolkit** — `specs/`, `docs/adr/`, `docs/records/`,
   `CHANGELOG.md`, `docs/roadmap.md`. Ela registra decisões sobre o método, e o método é o
   instalável. O guia cita por URL do GitHub.
2. **O site continua completo** — o guia **consome** do toolkit as páginas espelhadas, com
   forcing function própria. Cópia manual foi explicitamente rejeitada: é o modo de falha
   que o ciclo 021 já documentou (lista à mão que deriva sem ninguém ver).

## Requisitos funcionais

- **FR1**: QUANDO um arquivo rastreado existir, O SISTEMA DEVERÁ atribuí-lo a **exatamente
  um** repositório — órfão e dupla reivindicação são falha.
- **FR2**: QUANDO um caminho for declarado espelhado, O SISTEMA DEVERÁ exigir que o toolkit
  seja o dono — espelho sem fonte é fork, e fork diverge.
- **FR3**: QUANDO uma página entrar no sumário do site, O SISTEMA DEVERÁ falhar se a origem
  dela pertencer ao toolkit e não estiver espelhada — é o que impede o site de perder
  páginas silenciosamente no dia da divisão.
- **FR4**: QUANDO a fronteira for alterada, O SISTEMA DEVERÁ decidi-la a partir de **um
  arquivo só** (`boundary.json`), nunca de listas espalhadas por scripts.

## Fora de escopo (é a fatia 2, e ela tem gate próprio)

- Criar o repositório remoto do guia e mover qualquer arquivo.
- O mecanismo de espelhamento em si (submódulo git ou script de sincronização + portão).
- Tornar `GITHUB_BASE` do `build.mjs` configurável por origem, para link cross-repo.
- Dividir `check-links.sh` e `check-chapters.sh` entre os dois repositórios.
- Renomear qualquer coisa. O nome `maestro-guia` em `boundary.json` é uma proposta, não
  um fato — nada depende dele ainda.

## Critérios de aceite (DoD)

- [x] `boundary.json` classifica **100%** dos arquivos rastreados, sem órfão e sem dupla
      reivindicação.
- [x] `scripts/check-boundary.sh` cobre FR1, FR2 e FR3 e foi **visto acusar** em cada uma
      das três condições, com a saída no `qa-report.md`.
- [x] As 9 páginas do site que nascem no toolkit estão declaradas como espelhadas.
- [x] ADR 0017 registra o corte, as duas decisões do gate e o que ficou para a fatia 2.
- [x] Os nove portões existentes continuam no estado esperado.

## Clarify

1. `docs/research/` fica com o guia mesmo sendo citado 15 vezes pelo livro? **Sim** — é
   leitura para pessoas (pesquisa e diário), e a decisão 1 fala da *memória de decisão*
   (specs, ADR, índice), não de toda a prosa. O link vira externo como os outros 20.
