# ADR 0021 — O método se cobra sozinho e bate o ponto

- **Status**: Aceito · **Data**: 2026-10-12 · **Ciclo**: 065
- **Supersede**: nada. **Superado por**: —

## Contexto

Dois fatos medidos em 12/10/2026:

1. **O corolário C13** ("estou seguindo o método?" não se responde de memória) era cumprido
   por texto no `CLAUDE.md` e por um hook `SessionStart` que mede **uma vez**, no início. No
   momento em que o trabalho é entregue — o fim da resposta —, nada media nada. O dono do
   método pediu: *"desejo que o método se auto cheque, e não que eu pergunte"*.
2. **Não havia registro do custo de cada tarefa** numa arquitetura de um gerente e várias
   sessões executoras. Não se sabia quanto custava implementar versus auditar, nem quanto se
   gastava em retrabalho.

Os mods do Claude Code (2.1.287+) tornaram o segundo mensurável: um mod observa as mensagens
entre sessões (`session.receive`/`session.send`) e recebe os tokens de **cada requisição** ao
modelo (`turn.step`), coisa que um hook clássico não recebe.

## Decisão

1. **Um hook `Stop`** (`scripts/hooks/stop-conformance.py`) mede `check-conformance.sh
   --ticked-only` **do ciclo mais novo** no fim de cada resposta. Vermelho → não deixa o agente
   parar, **uma vez**; na segunda, deixa e avisa o humano (Princípio II: o humano decide; e um
   portão que vira laço queima tokens sem decidir nada). Falha aberta, sempre com aviso.
2. **Um livro de ponto** (`docs/records/tarefas.jsonl`), só acrescentado, recebe eventos
   `assigned`, `start`, `stop` e `verdict`, escritos pelo mod `maestro-ledger` a partir de
   duas etiquetas, cada uma sozinha na linha: `[[TASK ...]]` e `[[DONE ...]]`. O protocolo
   instalável está em `docs/governance/task-ledger.md`.
3. **Tentativa, resultado e veredito são campos distintos**, e o veredito **só** vem de uma
   tarefa `audit` ou `review` — o mod impõe e o relatório só conta esses (Princípio II: quem
   executa não verifica).
4. **Tokens são a medida principal**; `cost_usd` é o equivalente em preço de API.
5. **O instalador não instala o mod**: `claude plugin install` grava nas configurações do
   usuário, fora do projeto-alvo. Ele imprime o passo, e o humano decide.

## Consequências

- O ciclo 065 foi **executado pelo próprio livro**: cada tarefa distribuída com `[[TASK]]` a
  uma sessão executora, e o relatório respondeu quanto o ciclo custou. A revisão independente
  reprovou a primeira versão com 3 achados bloqueantes — dois deles no próprio mecanismo de
  cobrança (o hook cobrava trabalho em andamento de ciclos antigos) — e todos foram tratados.
- **Limites aceitos**, declarados no documento instalável: o mod não carrega em sessões na
  nuvem nem em sessões WSL (*Windows Subsystem for Linux*) do Desktop; no Windows a escrita
  concorrente não é atômica; o trabalho de uma sessão sem o mod fica "não medido", nunca zero.
- O instalador ganhou o veredito `UPGRADE`: projetos com hooks de uma versão anterior do
  Maestro são atualizados, em vez de recusados como se fossem de terceiro.
