# Spec 042 — Conformidade executável: a cauda sobrevive ao artefato

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-07
- **Origem**: auto-avaliação de uma agente companheira num repositório vizinho (ciclo 029,
  PR #39). Perguntada "você seguiu o Maestro?", respondeu honestamente que não — e o
  diagnóstico dela é a spec deste ciclo.

> **Raia**: plena. **Ambiguidade** média (o defeito estava claro; o mecanismo não);
> **raio** amplo (mexe em três templates, no gerador de esqueleto, no instalador e na camada
> de axiomas); **irreversibilidade** baixa — nada é apagado, e o portão novo tem piso.

## O quê e por quê

A agente relatou: o `plan.md` listava a ordem de implementação e **parava em "docs e
fitness verdes"**. A cauda do método — revisão independente, security, gate humano — vivia
na spec e na memória de trabalho dela. A compactação de contexto então promoveu a versão
truncada a fonte de verdade, e ela dirigiu até o PR **obedecendo com fidelidade**.

Isso não é um acidente daquele repositório. Medido aqui:

| Medida | Valor |
|---|---|
| Ciclos cujo `tasks.md` perdeu o gate humano que o template carrega | **35 de 40** |
| Ciclos com `research.md` · `data-model.md` · `contracts/` · `checklist.md` · `ux-design.md` | **0 de 40** |
| Onde a regra de quando cada artefato se aplica está escrita | `docs/roadmap.md` §3 |
| O instalador copia o roadmap? | **não** |
| O comando `/speckit.plan` instalado manda gerar esses artefatos? | **sim, quatro deles** |

Quem instala o Maestro recebe um comando que exige quatro artefatos, template para um só, e
a regra de quando eles se aplicam guardada num documento que não é entregue.

**Os dois problemas são o mesmo defeito**: o método instalado é uma **cópia com perda** do
método, e o executor segue a cópia com fidelidade. Omissão não viola nada visível — o
Constitution Check pergunta se o plano *viola* um princípio, nunca se ele *omite* um passo.

## Requisitos funcionais

- **FR1**: QUANDO um plano for escrito, O SISTEMA DEVERÁ exigir que os cinco artefatos
  condicionais sejam **declarados** (`=yes`/`=no` com razão), nunca apenas ausentes.
- **FR2**: QUANDO um artefato for declarado `=yes`, O SISTEMA DEVERÁ falhar se o arquivo
  não existir no diretório do ciclo.
- **FR3**: QUANDO um `tasks.md` for escrito, O SISTEMA DEVERÁ exigir os três passos da cauda
  como **tokens legíveis por máquina**, sobrevivendo a tradução e reescrita.
- **FR4**: QUANDO um passo da cauda não for `n/a`, O SISTEMA DEVERÁ exigir a **evidência**
  no `qa-report.md` — marcação não é testemunha.
- **FR5**: QUANDO alguém perguntar "estou seguindo o Maestro?", O SISTEMA DEVERÁ oferecer um
  comando que responda pelos artefatos, e a instrução de **não responder de memória**.
- **FR6**: QUANDO o método for instalado noutro repositório, O SISTEMA DEVERÁ levar junto o
  catálogo de artefatos e o comando de conformidade.

## Fora de escopo

- Templates para `research.md`, `data-model.md` e `contracts/`. O catálogo diz **quando**
  cada um se aplica; o formato só vale a pena quando o primeiro ciclo precisar de um, e aí
  nasce do uso e não da imaginação (YAGNI).
- Retroagir os 35 ciclos sem cauda. O portão tem piso no 042; a dívida fica declarada.
- Portão que force o humano a **ler** a evidência. Não existe, e dizer o contrário seria
  promessa — o gate humano é do humano por axioma (A2).

## Critérios de aceite (DoD)

- [x] `docs/governance/artifacts.md` existe, é instalável e cobre os quatro obrigatórios,
      os cinco condicionais e os três da cauda.
- [x] `plan-template`, `tasks-template` e `qa-report-template` carregam os tokens.
- [x] `new-cycle.sh` gera esqueleto **conformante** — é ele que se usa de fato.
- [x] `scripts/check-conformance.sh` cobre FR1–FR4 e foi **visto acusar** em cada uma.
- [x] Corolários **C12** e **C13** na camada de axiomas; anti-padrão **22**; ADR 0019.
- [x] `install-maestro.sh` leva o catálogo, o portão e a regra da pergunta no bloco gerado.

## Clarify

1. Por que token (`TAIL:review`) e não prosa? Porque prosa é reescrita e traduzida, e o
   portão passaria a medir a palavra em vez do fato — anti-padrão 13. É o mesmo raciocínio
   do campo `fecha` no índice e do marcador `PT-DATA`.
