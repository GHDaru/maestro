# Contracts 064 — as interfaces entre partes

O protocolo das etiquetas e o vocabulário vivem **uma vez**, instaláveis, em
`docs/governance/task-ledger.md`. Aqui ficam as interfaces internas que ninguém instala.

## 1. Hook `Stop` — `scripts/hooks/stop-conformance.py`

| Lado | Contrato |
|---|---|
| entrada (stdin) | o JSON (*JavaScript Object Notation*) do evento `Stop` do Claude Code: usa `hook_event_name`, `stop_hook_active` e, só como reserva, `cwd` |
| raiz do projeto | `$CLAUDE_PROJECT_DIR`; o `cwd` do evento só quando a variável não existe (o `cwd` anda com o agente, e rodar o `scripts/check-conformance.sh` de onde ele aponta executaria o script de outro repositório) |
| o que mede | `check-conformance.sh --ticked-only NNN`, **só do ciclo mais novo** (`specs/NNN-*/`) |
| saída, verde | nada; exit 0 |
| saída, vermelho, primeira vez | `{"decision":"block","reason":"…"}` em stdout; exit 0. O `reason` é feito das linhas ✗ reais do portão (até 6), sem remédio fixo |
| saída, vermelho, `stop_hook_active: true` | `{"systemMessage":"…"}` em stdout; exit 0 — **nunca** bloqueia duas vezes |
| sem o método no projeto | nada; exit 0 |
| erro interno ou tempo esgotado | falha **aberta**: aviso em stderr, exit 0 |

## 2. Gravador — `scripts/record-task.py`

| Lado | Contrato |
|---|---|
| chamada | `record-task.py '<um objeto JSON numa linha>'` — sem shell; o mod usa `$.process.run` com vetor de argumentos |
| destino | `docs/records/tarefas.jsonl`, ou `$MAESTRO_TASK_LEDGER` |
| exit 0 | gravado com `O_APPEND`, **repetindo a escrita até sair a linha inteira**; no Linux e no macOS linhas concorrentes não se misturam, **no Windows não há essa garantia** (o `O_APPEND` do Python lá é posicionar no fim e escrever) |
| exit 1 | recusado; o motivo em stderr, uma linha por problema |
| exit 2 | uso errado |
| regra de `verdict` | o evento `verdict` exige `by` (o id da tarefa `audit`/`review` que julgou); o relatório só conta vereditos dessas tarefas **e** só quando a `session` do veredito é a de um `start` da tarefa `by`. Um `task_id` terminado em `-cycle` é veredito de ciclo (seção *Cycle verdicts*) |

## 3. A linha do livro (escrita pelo mod e pelo gravador, lida pelo relatório)

Um objeto JSON por linha. Obrigatórios em toda linha: `ts` (data e hora no formato ISO 8601, da
*International Organization for Standardization*), `event`, `task_id`.
O conjunto completo de campos por evento e os vocabulários fechados estão em
`docs/governance/task-ledger.md`. Um campo novo pode ser **acrescentado** sem quebrar o
relatório, que ignora o que não conhece; renomear ou mudar o significado de um campo exige
uma nova versão do documento.

## 4. Etiquetas lidas pelo mod — `mods/maestro-ledger/hooks/tags.ts` e `register.ts`

O vocabulário está em `docs/governance/task-ledger.md`; aqui ficam as regras de leitura, que são
o contrato entre o texto das mensagens e o livro.

| Regra | Contrato |
|---|---|
| forma | a etiqueta fica **sozinha na linha**; texto antes ou depois anula. Valor entre aspas pode conter `]` |
| qual conta | a **primeira** `[[TASK]]` e a **última** `[[DONE]]` da mensagem; exemplos citados no meio do texto são ignorados |
| `[[TASK]]` de outra sessão | **não** substitui tarefa aberta: é recusada, com registro no log |
| quem substitui uma tarefa aberta | só a pessoa: terminal, Remote Control ou o anfitrião do `claude -p` |
| mesma tarefa, próxima tentativa | o mesmo id com `attempt` diferente fecha a anterior como `superseded` e abre a nova; o mesmo id e a mesma tentativa vistos duas vezes contam uma só |
| `[[DONE]]` de outro id | ignorado, com registro |
| veredito | só uma tarefa `audit` ou `review` grava; em qualquer outra espécie o veredito é descartado, com registro |
