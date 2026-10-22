# Spec 070 — Workflow do ciclo Maestro no painel (escrita como 064 na linha paralela)

- **Status**: Implementado retroativamente (parcial: FR2 ausente, FR3 invertido, FR1 sem branch/hash — ver plan.md § Dívidas) · **Lane**: full · **Date**: 2026-10-02 (integrada em 2026-10-22, ciclo 070)
- **Origin**: Desejo 001 do Gilsiley, redigido pela Hindiana Assistente (.maestro/docs/desejo-001-workflow-painel.md). Desenho de referência: workflow-maestro.md.

## What and why

O ciclo Maestro hoje vive em mensagens. O painel só vê o que alguém lembra de registrar, e por isso o roadmap e as decisões aparecem vazios. Nenhuma rodada tem spec própria, e cada regra de método é texto que depende de memória — os 13 desvios vêm daí.

A proposta é que cada rodada seja uma execução de workflow registrada em SQLite, passo a passo. Cada passo tem entrada, resumo e saída, e o próprio hook da sessão faz o registro. O painel mostra o roadmap com as rodadas, as decisões aparecendo, a equipe real e um link de cada documento para o arquivo.

## Functional requirements

- **FR1**: QUANDO uma sessão iniciar um passo, O SISTEMA DEVE registrar a entrada com a rodada, o passo, a sessão, o branch e o hash de partida.
- **FR2**: SE o passo anterior da rodada não tiver saída com a evidência exigida, ENTÃO O SISTEMA DEVE recusar a entrada e informar o passo pendente.
- **FR3**: QUANDO uma sessão encerrar o turno com um passo aberto, O SISTEMA DEVE cobrar o resumo e a saída.
- **FR4**: O SISTEMA DEVE exibir no roadmap cada rodada com o passo atual, o tempo em cada passo e quem está nele.
- **FR5**: ENQUANTO o ingest reconstrói os dados, O SISTEMA DEVE continuar servindo a versão anterior completa.
- **FR6**: SE um arquivo de decisões ou de roadmap não puder ser lido, ENTÃO O SISTEMA DEVE exibir o arquivo e o motivo.
- **FR7**: O SISTEMA DEVE registrar cada passo três vezes: entrada (quem, quando, branch, hash de partida), resumo (1-3 linhas), saída (resultado e próximo passo liberado).
- **FR8**: O SISTEMA DEVE manter tabelas append-only: rodadas (id, desejo, criada_por, aberta_em, fechada_em), passos (rodada, passo, sessao, entrada_em, resumo, saida_em, evidencia_json, resultado), transicoes (passo → próximo, evidência exigida).
- **FR9**: O SISTEMA DEVE usar uma fila em SQLite (modo WAL) como outbox para mensagens entre sessões, sem serviço adicional.
- **FR10**: O SISTEMA DEVE exibir a equipe real: 4 sessões do Claude Desktop (Office, Assistente, Reescrita, Testes Dev) e 15 do Claude Code (Gerente, Gerente02, W01–W13).
- **FR11**: O SISTEMA DEVE avisar quando a leitura dos arquivos está velha (mais de 1 h desde o último ingest).
- **FR12**: O SISTEMA DEVE reconstruir os dados derivados num arquivo temporário e trocar (rename) no fim, para que o painel não fique vazio se o ingest for interrompido.
- **FR13**: ENQUANTO o ingest executa, O SISTEMA DEVE permitir escrita concorrente na tabela `eventos` sem "database is locked" (events em arquivo/DB separado ou WAL com transações curtas).
- **FR14**: SE o ingest for interrompido, ENTÃO O SISTEMA DEVE manter a versão anterior completa das tabelas derivadas (swap atómico, nunca tabelas vazias).

## Out of scope

- Redis Streams ou RabbitMQ (decisão registrada como "fila em SQLite agora; Redis Streams quando as sessões rodarem em mais de uma máquina").
- Mensageria entre máquinas.
- Deploy do painel (a instalação nova é feita pela Assistente depois do APPROVE).

## Acceptance criteria (DoD)

- WHEN uma sessão registra a entrada de um passo THEN THE SYSTEM SHALL criar um registro na tabela `passos` com `entrada_em` preenchido e `saida_em` nulo.
- WHEN o passo anterior não tem `saida_em` THEN THE SYSTEM SHALL recusar a entrada e retornar o passo pendente.
- WHEN uma sessão encerra com passo aberto THEN THE SYSTEM SHALL cobrar resumo e saída (hook `Stop`).
- WHEN o ingest reconstrói THEN THE SYSTEM SHALL servir a versão anterior até a reconstrução completar (sem painel vazio).
- WHEN um arquivo não pode ser lido THEN THE SYSTEM SHALL exibir o caminho e o motivo do erro.
- WHEN a leitura está velha (>1h) THEN THE SYSTEM SHALL exibir aviso no cabeçalho.
- `sqlite3 painel.db "SELECT count(*) FROM passos WHERE entrada_em IS NOT NULL AND saida_em IS NULL"` → ≥ 0 (passos abertos visíveis).
- `sqlite3 painel.db ".tables"` → contém `rodadas`, `passos`, `transicoes`, `fila`.

## Clarify

1. O hook `SessionStart` e `Stop` são do Claude Code ou do painel? → hooks do Claude Code (.claude/settings.json), escrevem no SQLite do painel.
2. A lista de sessões vem de onde? → configuração `equipes` atualizada com as 19 sessões (4 Desktop + 15 Code), sem W10 (saiu).
3. A migração dos dados existentes (eventos, decisões) para o novo schema é parte desta spec? → sim, o ingest reconstrói a partir dos arquivos existentes.

<!--
  GATE (DoR — not delegable): this spec only becomes a plan after human approval.
  Handoff: spec-agent → (approval) → plan-architect.
-->
