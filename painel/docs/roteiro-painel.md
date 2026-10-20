# Painel de especialistas: app de controle do Maestro

Conduz: Hindiana Assistente. Aloca: Hindiana Office. Decide: Gilsiley. Data: 01/10/2026.

## O que se quer

Um app leve, em HTML e JavaScript com SQLite e só em localhost, incorporado ao Maestro (GHDaru/maestro) e aplicado primeiro ao projeto hindiana/ola. Ele deve mostrar:

1. **Board de agentes**: o que cada sessão (Office, Gerente, Gerente02, W01–W13) está fazendo agora, em que peça trabalha, há quanto tempo, e se está bloqueada e por quem.
2. **Roadmap → spec → plan → tasks → implementação** com rastreabilidade (spec ↔ hash ↔ testes ↔ jornada).
3. **Decisões e ADRs**, desvios de retro, defeitos e barra (vereditos com evidência).
4. **Indicadores**: DORA primeiro (frequência de deploy, lead time, taxa de falha, tempo de recuperação) e tempo por fase (ferramenta `ponto.py` do W04).
5. **Documentos do projeto em época de IA**: constituição, linguagem ubíqua, objetos semânticos, jornadas e os documentos que a própria IA precisa ler.

## A barra (contra o que se compara)

- **Jira**: board, timeline e backlog reais (atlassian.com/software/jira).
- **Cline Kanban e Agent Teams**. Clone em `C:\Users\ghdaru\DriveD\010_PROJETOS\cline`; ler `docs/usage/kanban.mdx`, `docs/kanban/core-workflow.mdx`, `docs/cli/agent-teams.mdx` e `sdk/packages/shared/src/team/types.ts`. O card mostra a última ação do agente e o diff. As tasks têm dependências, há um mission log (progress/handoff/blocked/decision/done/error), runs com sinal de vida e uma caixa de mensagens.
- **Parte medida**: DORA calculado do git real do hindiana e do ola, mais o tempo por fase.

## Restrições que não se discutem

- **Maestro** (levantamento de 01/10):
  - Os arquivos são a fonte de verdade (`specs/`, `docs/records/decisoes.jsonl`, ADR, CHANGELOG). O SQLite é **cópia derivada**, reconstruível a qualquer momento (ADR 0008, nada de segunda fonte de verdade).
  - Só o que não existe em arquivo entra direto no SQLite, sempre acrescentando e nunca reescrevendo: status de agente, sinal de vida, deploy registrado.
  - O gate é humano (Princípio II).
  - O painel de métricas está como YAGNI em `operating-model.md` §6, e incorporá-lo pede um ADR, que fica para o Gilsiley aprovar.
- **Hindiana**:
  - Nunca ler `hindiana/.env` nem o conteúdo de `backups_producao`; dos backups, só `backup.log` e `manifesto.json`.
  - Nada de host, IP, usuário ou token no repositório.
  - Merge na main não é deploy, e o push de 1e135b5 provou isso. A verdade do deploy é a lista de deploys do Railway, registrada pela Office.
- **Leveza**: um arquivo HTML, JS puro, sql.js ou Python stdlib (`sqlite3` + `http.server`), e nenhum build obrigatório.

## Fontes já existentes no hindiana (entram na ingestão)

- `ola/especificacao/`: `decisoes-madrugada-3009.md`, `retro-anotacoes.md`, `retro-maestro-2909.md`, `barra-v2.md`, `barra-v2-resultado.md`, `barra/execucoes/*/passos.json`, `relatorio-manha-3009.md`, `jornada-do-momento.md`, `equipe/*.md` ("Estado atual"), `equipe/indicadores-24h.json`, `tempos/`, `adr/`, `itens/`, `rastreabilidade/`, `modulos/`, `03-ddd.md` (glossário §A5, objetos B1–B8), `catalogo-provas-enganosas.md`.
- `git log` do hindiana e do ola: commits, merges, tags e hashes devolvidos.

## Papéis e perguntas (cada worker responde as das suas duas especialidades)

**W04: arquiteto DDD/hexagonal e engenharia de contexto para IA**

1. Quais são os agregados e as entidades do app? Mapeie a linguagem ubíqua: rodada, peça, hash, medição, barra, defeito, decisão, desvio, sessão, fase.
2. O que a IA precisa ler a cada sessão? Compare constituição, CLAUDE.md, memory bank do cline (`projectbrief`, `activeContext`, `progress`...) e o hook `session-state.sh` do Maestro. Como o app gera um "estado atual" que o agente lê, como JSON ou MCP?
3. Que documentos de projeto são obrigatórios em época de IA, e quais são derivados?

**W01: UX de painéis e jornadas, e produto e fluxo ágil**

1. Que telas, e em que ordem? O board de agentes é a tela inicial? Desenhe o wireframe em texto de board, roadmap, rastreabilidade, decisões e DORA.
2. Como o humano (Gilsiley) usa o app em 2 minutos de manhã e em 30 segundos durante o dia?
3. Que colunas e estados o board tem? Use o vocabulário fechado do hindiana: entregue, suítes aceitas, aprovada às cegas, integrada.

**W07: plataforma e DevOps (DORA), e dados e métricas em SQLite**

1. Como calcular as quatro métricas DORA com o que existe (git, gate-main, `barra/execucoes`, deploys registrados)? Defina a fórmula de cada uma.
2. Qual é o esquema SQLite? Tabelas, chaves, e o que é derivado e o que é acrescentado. Use como referência `sqlite-team-store.ts` do cline.
3. Como e quando a ingestão roda? Script, gatilho, idempotência.

**W06: qualidade (TDD, barra, evidência), e governança, segurança e risco**

1. Que evidência um card precisa para mudar de coluna (hash, runner2, tsc, barra)? Como o app impede um "✅ sem prova"?
2. Que regras de segurança a ingestão segue (segredos, dados de produção, append-only)? Que teste prova cada uma?
3. Como o app expõe os 12 desvios recorrentes da retro, para que deixem de se repetir?

**W11: documentação técnica e facilitador de método**

1. Que mudança no Maestro o app exige? Rascunhe o ADR que supera o YAGNI do painel e diga em que capítulo do livro o app entra.
2. Quais documentos do hindiana estão mortos (parados desde 21–22/09) e quais estão vivos? Proponha o conjunto mínimo.
3. Como o app alimenta a retro? Que relatório ele gera ao fim de um lote?

**W08: crítico às cegas** (não participa da discussão)

Julga as telas prontas contra a barra. O par sem rótulos e a descrição factual são montados por quem roda a barra; o crítico nunca escreve a descrição.

## Formato da contribuição

Mande à Hindiana Assistente (SendMessage), em até 1200 palavras, com as respostas numeradas e uma seção final **"Especialistas, skills e tools que o método deveria exigir"**. Não edite nada fora da sua worktree e não abra branch neste repositório; a consolidação é da Assistente.

Prazo: 60 minutos depois de receber o papel.
