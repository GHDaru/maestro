# Tasks 064 — Workflow do ciclo Maestro no painel

## Verification first

- [ ] **T0** — Define the executable DoD checks (see `plan.md § Verification`). Criar `tests/test_workflow_painel.py` com os 8 testes do plan, todos vermelhos. (Gerente)

## Implementation — Backend SQLite + hooks (W09)

- [ ] **T1** — Schema SQLite: tabelas `rodadas`, `passos`, `transicoes`, `fila` em modo WAL. Escrever `data-model.md` com entidades e relações. Migration cria o schema. (FR8, W09)
- [ ] **T2** — Hook `SessionStart`: mostra passos abertos da sessão e próximo permitido. Escreve entrada na tabela `passos` (rodada, passo, sessao, branch, hash, entrada_em). (FR1, FR7, W09)
- [ ] **T3** — Hook `Stop`: cobra resumo e saída do passo aberto. Se sem evidência exigida, recusa fechamento. (FR2, FR3, W09)
- [ ] **T4** — Ingest transacional: reconstrói dados derivados em arquivo temporário, troca (rename) no fim. Se interrompido, versão anterior continua servindo. (FR5, FR12, W09)
- [ ] **T5** — Fila outbox em SQLite: tabela `fila` lida pelos hooks. Entrega sem serviço adicional. (FR9, W09)

## Implementation — Tela HTML+JS (W03)

- [ ] **T6** — Roadmap: cada rodada com passo atual, tempo em cada passo, quem está nele. Link para o arquivo. (FR4, W03)
- [ ] **T7** — Equipe real: 19 sessões (4 Desktop + 15 Code sem W10). Atualizar configuração `equipes`. (FR10, W03)
- [ ] **T8** — Aviso de leitura velha: se último ingest >1h, aviso no cabeçalho. (FR11, W03)
- [ ] **T9** — Erro de leitura: se arquivo não pode ser lido, exibe caminho e motivo, não vazio. (FR6, W03)
- [ ] **T9b** — Decisões aparecendo: o painel mostra as decisões (hoje vazio). Ler do ingest e exibir no roadmap. (W03)

## Living documentation (same pull request)

- [ ] **T10** — `data-model.md` com entidades e relações. (W09)
- [ ] **T11** — `ux-design.md` com wireframe do painel atualizado. (W03)

## Closing tail — MANDATORY, one line each, never delete

- [ ] **TAIL:review** — independent review in fresh context, by whoever did not execute. Evidence: the verdict, in `qa-report.md`.
- [ ] **TAIL:security** — security pass proportional to the risk class. SQLite local, sem API externa; risk surface = permissão do hook escrever no db.
- [ ] **TAIL:mutation** — every gate this cycle created or changed was broken on purpose and seen refusing. Evidence: the mutation and its output, in `qa-report.md`.
- [ ] **TAIL:gate** — DoD green → guardian verdict → human merge gate (not delegable).
