# Spec 017 — Retrospectiva executada: check-proxy vira regra + roadmap descongelado

- **Status**: Aprovada (auditoria do Steward) · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: três perguntas de auditoria do Steward sobre a própria metodologia — onde
  está o roadmap, onde ficam registrados os problemas encontrados (e se isso é
  **executado**), e por que um processo análogo falhou no FlowBuilder (spec 017/PR #20).

## O quê e por quê

A auditoria expôs **duas falhas de processo minhas**, não de conteúdo:

1. **Achado morrendo em "candidato"** — identifiquei o mesmo defeito duas vezes (ciclos
   015 e 016), escrevi "candidato a anti-padrão" nos relatórios e **nunca rodei a
   retrospectiva**. A regra `retro → regra versionada` só existe se for executada.
2. **Roadmap congelado** — `docs/roadmap.md` parou no ciclo 009; os ciclos 010–016
   aconteceram fora do mapa. Artefato de planejamento que não acompanha vira ficção
   (viola o Princípio VI).

Com o caso do FlowBuilder relatado pelo Steward, o padrão tem **três ocorrências** — o
gatilho de "erro recorrente vira regra" está mais que disparado.

## Requisitos funcionais

- **FR1**: retrospectiva **executada** (`scripts/retro.sh`) e o achado convertido.
- **FR2**: anti-padrão **13 — check que mede o proxy, não o fato** no catálogo, com os
  três sintomas reais (texto vs artefato · linhas vs itens · existe vs atualizado).
- **FR3**: anti-padrões **14** (achado que morre em candidato) e **15** (artefato de
  planejamento que congela) — as duas falhas desta auditoria, nomeadas.
- **FR4**: **segunda lei** na skill `dod-verificavel` — *um check que você nunca viu
  acusar não é um check, é uma esperança*; provar o check falhando antes de confiar.
- **FR5**: roadmap atualizado (F5, F6, F7, contínuos) + **regra de manutenção** no
  cabeçalho + tabela de **gatilhos abertos**.
- **FR6**: diagrama **BPMN** do processo (imagem + página no livro).

## Fora de escopo

- Migrar o capítulo 02 (próximo ciclo).
- Alterar a Constituição — os achados cabem em skill e roadmap (YAGNI).

## Critérios de aceite (DoD)

- [ ] `grep -c "^[0-9]*\. \*\*" skills/anti-padroes/SKILL.md` = 15.
- [ ] QUANDO alguém abrir a skill `dod-verificavel`, O SISTEMA DEVE apresentar as **duas**
      leis (a original e a de provar o check falhando).
- [ ] Roadmap contém F5/F6/F7 e a seção de gatilhos abertos.
- [ ] Diagrama BPMN existe como imagem e como página do livro; build verde.

## Clarify (resolvido)

1. **Vira princípio ou skill?** Skill + roadmap — a Constituição já cobre o fundamento
   (Princípios IV e VI); o que faltava era o **antídoto operacional**.
