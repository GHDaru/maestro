# Passagem de sessão — Maestro, "o método se cobra sozinho e bate o ponto"

> **Onde está:** `specs/064-o-metodo-se-cobra-e-bate-o-ponto/handoff.md`, na branch
> `064-auto-checagem-e-livro-de-ponto`. Abra a sessão nessa branch e leia este arquivo primeiro.
>
> **Para a sessão que vai continuar:** leia a seção 1 inteira antes de qualquer ação. Há um
> problema de numeração **ainda não resolvido** (seção 8) que precisa de decisão do Darú
> antes de qualquer merge. Escrito em 12/10/2026 pela sessão que fez o trabalho; todos os
> números abaixo foram medidos rodando comandos, não lembrados.

---

## 1. Resumo em uma tela

| Item | Estado |
|---|---|
| Repositório | `GHDaru/maestro` (público). Versão do método: **v0.3.0** (confirmado: README, CHANGELOG; não existe 0.8 em nenhuma branch) |
| Branch do trabalho | `064-auto-checagem-e-livro-de-ponto`, **1 commit** sobre a `main`: `9d7f094` "O método se cobra sozinho e bate o ponto (ciclo 064)" — já no GitHub |
| Base | criada a partir da `main` (`534a088`, 23/08/2026) |
| Squash | feito a pedido do Darú; os 6 commits originais estão na tag **local** `backup-064-antes-do-squash` (`a08c731`) — só existe no container da sessão anterior, não no GitHub |
| Portões | todos verdes, exceto `check-evals.sh` e `check-chapters.sh`, que **já estavam vermelhos na `main`** antes deste trabalho |
| Merge / promoção | **não feitos** — o gate humano é do Darú. Nada foi para `dev` nem `main` |
| **Bloqueio** | o número **064**, o **ADR 0021** e a fase **F29** do roadmap colidem com trabalho já existente em outras branches (seção 8) |

**Próximo passo recomendado:** perguntar ao Darú qual número o ciclo recebe (065 ou 066), então
rebasear a branch sobre `origin/dev` e renumerar (roteiro na seção 8).

---

## 2. De onde veio o pedido

Conversa de 12/10/2026 com o Darú (dono do Maestro; prefere ser chamado assim; responde em
português; regra pessoal: **"prove, não declare"** — quer o comando rodado e a saída, nunca
resposta de memória).

A conversa começou como aula sobre **mods do Claude Code** (lançados na v2.1.287, em 1º/10/2026)
e **hooks clássicos**, e virou dois pedidos concretos:

1. *"Desejo que o método se auto cheque, e não que eu pergunte."*
2. *"Quero ver quanto estou gastando. Na minha arquitetura as sessões trocam mensagens e tem um
   gerente. Quando o gerente passa uma tarefa, a sessão que recebe registra um start task, e quando
   termina um stop task. A tarefa pode ser implement, test, audit, com tentativas e status
   (reprovada, aprovada…)."* Depois: *"e tokens, além do custo?"* — sim, tokens viraram a medida
   principal.

Depois: *"escreva as orientações para o Maestro implementar no instalador, mas quero testar"* e,
por fim, *"pode implementar tudo, seguindo o próprio Maestro, já usando os hooks e o mod"*.

---

## 3. O que foi construído

### 3.1 Autocobrança — hook `Stop` (hook clássico, em `.claude/settings.json`)

- `scripts/hooks/stop-conformance.py` roda no **fim de cada resposta** do agente.
- Mede `scripts/check-conformance.sh --ticked-only <NNN>` **só do ciclo mais novo** em `specs/`.
- Vermelho (caixa `TAIL` marcada sem evidência) → responde `{"decision":"block","reason":…}`: o
  Claude Code **não deixa o agente parar**; a razão traz as linhas ✗ reais.
- Segunda vez seguida (`stop_hook_active: true`) → não bloqueia de novo; manda `systemMessage` ao
  humano (evita laço que queima tokens).
- Raiz = `$CLAUDE_PROJECT_DIR` (nunca o `cwd` do evento — o `cwd` deixava executar o
  `check-conformance.sh` de outro repositório). Falha **aberta**, sempre com aviso em stderr.
- Provado **ao vivo**: uma sessão Haiku disse "terminei" num repositório com a mentira plantada;
  foi bloqueada, investigou, e na segunda tentativa o humano foi avisado. E no fechamento do
  ciclo, **o hook barrou a própria sessão gerente** (evidência de `TAIL:security` reprovada pelo
  portão) até ser corrigida.

### 3.2 Livro de ponto — mod `maestro-ledger` + scripts

| Peça | Papel |
|---|---|
| `mods/maestro-ledger/` | Mod (TypeScript, roda **dentro** do processo do Claude Code). Lê as etiquetas, soma os tokens de **cada requisição** ao modelo (`turn.step`), grava via o gravador |
| `scripts/record-task.py` | Gravador: valida vocabulário fechado e tipos, acrescenta uma linha JSON em `docs/records/tarefas.jsonl` com `O_APPEND`, repetindo a escrita até sair inteira |
| `scripts/report-tasks.py` | Relatório: tokens e custo por tipo, ciclo e modelo; aprovação de primeira; custo do retrabalho; taxa de cache; órfãs; "não medido"; vereditos de ciclo. `--cycle NNN`, `--json` |
| `scripts/check-ledger.sh` | Portão novo, hermético: 77 verificações do gravador, relatório, hook `Stop` e `merge-settings` |
| `docs/governance/task-ledger.md` | O protocolo, **instalável**, em inglês (ADR 0014) |

**Protocolo** — cada etiqueta **sozinha na linha**; vale a **primeira** `[[TASK]]` e a **última**
`[[DONE]]` (exemplos citados no meio do texto são ignorados):

```text
[[TASK id=064-T03 kind=implement attempt=2 cycle=064 redoes=064-T03#1]]
...trabalho...
[[DONE id=064-T03 outcome=delivered]]

[[DONE id=064-A01 outcome=delivered target=064-T03 verdict=rejected reason="sem evidência de mutação"]]
```

- `kind`: spec · plan · implement · test · review · audit · fix · docs · research
- `outcome`: delivered · blocked · failed (o mod grava sozinho `interrupted` e `superseded`)
- `verdict`: approved · approved_with_notes · rejected — **só tarefas `audit`/`review` julgam**
  (Princípio II); o relatório só conta o veredito se a sessão dele for a da auditoria
- `target=<NNN>-cycle` = veredito do ciclo inteiro
- Eventos: `assigned` (gerente envia) · `start` · `stop` (com `requests`, `tokens_in`,
  `tokens_out`, `tokens_cache_read`, `tokens_cache_write`, `tokens_subagents`, `tokens_by_model`,
  `cost_usd`, `duration_s`) · `verdict`
- Segurança: uma `[[TASK]]` vinda de **outra sessão** não substitui tarefa aberta nem volta a
  tentativa; só a pessoa (terminal, Remote Control, host do `claude -p`) substitui.

### 3.3 Instalador

- `scripts/hooks/merge-settings.py`: veredito novo **`UPGRADE`** — se os `hooks` do projeto forem
  **exatamente** os de uma versão anterior do Maestro (`PREVIOUS_HOOKS`, começa pela v0.3.0), troca
  só a chave `hooks`. Antes, quem tinha a v0.3.0 recebia `CONFLICT` do próprio instalador.
  Hooks de terceiro continuam `CONFLICT` (arquivo intacto, provado com `cmp`).
- `scripts/install-maestro.sh`: copia o hook `Stop`, `record-task.py`, `report-tasks.py`,
  `task-ledger.md`; `--dry-run` diz "would upgrade"; para Claude Code imprime um passo
  **opcional, não executado**: `claude plugin install maestro-ledger --marketplace GHDaru/maestro --scope project`
  (o instalador não instala o mod porque isso grava nas configurações do usuário, fora do projeto).
- `scripts/check-installed.sh`: exige que todo hook citado no `settings.json` instalado exista e
  seja executável (o defeito real do primeiro push: o `settings.json` chamava um arquivo que o
  instalador não copiava).
- `.claude-plugin/marketplace.json`: segunda entrada, `maestro-ledger`.
- `boundary.json`: `mods/` pertence ao domínio `toolkit`.
- CI (`.github/workflows/ci.yml`): roda `check-ledger.sh` sempre; o passo do mod (`claude plugin
  validate/test`) imprime `skipped` quando o runner não tem o Claude Code — que é o caso do GitHub.

### 3.4 Artefatos do ciclo e memória

`specs/064-o-metodo-se-cobra-e-bate-o-ponto/` (spec, plan com Constitution Check 8/8, data-model,
contracts/interfaces.md, tasks, qa-report com toda a evidência), `docs/adr/0021-…`, linha
`adr-0021` em `docs/records/decisoes.jsonl`, fase F29 no `docs/roadmap.md`, entradas no
`CHANGELOG.md`, glossário, receita `docs/receitas/instalar-o-maestro.md` (seção "Livro de ponto").

---

## 4. Como o trabalho foi executado (o próprio livro em uso)

- A sessão principal atuou como **gerente**; cada tarefa foi despachada a uma **sessão executora**
  (`claude -p`, Sonnet) com a etiqueta `[[TASK]]`, o mod (`--plugin-dir mods/maestro-ledger`) e o
  hook `Stop` ativos. O mod bateu o ponto sozinho. O gerente **verificou rodando** cada entrega
  antes de registrar o veredito.
- O despachante era um script no scratchpad da sessão anterior (não está no repositório). A forma:
  ```bash
  python3 scripts/record-task.py '{"ts":"…","event":"assigned","task_id":"064-T2",…}'
  env -u CLAUDE_CODE_SESSION_ID claude -p "[[TASK id=064-T2 kind=implement attempt=1 cycle=064]]
  <instruções>" --model sonnet --plugin-dir mods/maestro-ledger --permission-mode acceptEdits \
    --allowedTools "Read,Edit,Write,Glob,Grep,Bash(python3:*),Bash(scripts/*),…" \
    --disallowedTools "Bash(git commit:*),Bash(git push:*),…" --output-format stream-json --verbose
  ```
- **Revisões independentes** (Opus, contexto fresco, sem permissão de escrita):
  - **R1 reprovou**: 3 bloqueantes (o hook cobrava trabalho em andamento de ciclos antigos e
    mandava "desmarcar a caixa"; o teste do `UPGRADE` era tautológico; `--cycle` descartava todos
    os vereditos) + 10 importantes + 7 menores. Tratados nas tarefas F1–F5.
  - **R2 aprovou com ressalvas** (N1–N7: roteiro de teste da spec quebrado pela regra da linha
    própria; `by` do veredito autodeclarado; veredito de ciclo fora do modelo; regras sem teste).
    Tratadas em F6–F7.
  - Os textos completos de R1 e R2 ficaram no scratchpad da sessão anterior (efêmero); o
    resumo e o mapa achado → correção estão em `tasks.md` e `qa-report.md`.
- **Mutações** (`TAIL:mutation`): todo portão criado ou alterado foi quebrado de propósito e visto
  reprovando. No mod, 19 mutações, 18 mortas; a que sobrevive (`origin?.kind`) é equivalente.

---

## 5. Custo do ciclo — medido pelo livro que ele construiu

`python3 scripts/report-tasks.py --cycle 064`:

| | Tokens | US$ |
|---|---|---|
| implement (5 tentativas) | 6,37 M | 2,15 |
| docs (2) | 4,42 M | 1,31 |
| fix (4 + 3 não medidas) | 6,59 M | 2,56 |
| review (2 — R1 e R2) | 12,07 M | 6,34 |
| **Total (13 medidas)** | **29,45 M** | **12,36** |

Taxa de cache 96,7%. Três tentativas aparecem como **não medidas** (064-T7#2, 064-F3#1, 064-F7#1):
foram feitas pela sessão gerente, que não tinha o mod carregado — o relatório as mostra assim,
nunca como zero. `cost_usd` em assinatura é o equivalente em preço de API.

---

## 6. Como verificar o estado (rode, não confie neste texto)

```bash
git clone https://github.com/GHDaru/maestro && cd maestro
git checkout 064-auto-checagem-e-livro-de-ponto
scripts/check-ledger.sh                         # ✓ 77 checks
(cd mods/maestro-ledger && claude plugin validate . && claude plugin test .)   # 16 pass
scripts/check-installed.sh                      # ✓
scripts/check-conformance.sh 064                # ✓
scripts/check-conformance.sh --ticked-only      # ✓
for g in check-install check-language check-links check-flags check-boundary check-version check-adr check-agents check-roles check-retro; do scripts/$g.sh | tail -1; done
scripts/package-plugin.sh --verify
python3 scripts/report-tasks.py --cycle 064
```

Requer Claude Code ≥ 2.1.287 para mods (2.1.292 para `--marketplace` no shell). Verificado em 2.1.296.

---

## 7. Limites declarados (estão no `task-ledger.md`; não são defeitos esquecidos)

- O mod **não carrega em sessões na nuvem** (`claude.ai/code`) nem em sessões WSL (Windows
  Subsystem for Linux) do Desktop. **Importante para o Darú**: se o gerente e as sessões dele rodam
  em `claude.ai/code`, o livro de ponto não funciona lá — precisa de outro caminho.
- As etiquetas não são autenticadas; a checagem de sessão do veredito assume ids de sessão
  distintos por executor (em sessões aninhadas eles se repetem — medido neste ciclo).
- No Windows, `O_APPEND` do Python não é atômico entre processos.
- Hot reload do mod perde a tarefa ativa (vira órfã visível); `session.end` tem 1,5 s.
- Uma tarefa ativa por sessão.
- Criar um `specs/NNN-*` novo e vazio faz o hook medir o ciclo novo e silenciar uma caixa sem
  evidência no anterior (a CI ainda pega).
- **Não testado ao vivo**: a troca de mensagens **entre duas sessões** (gerente → executor via
  `SendMessage`). Testado só no kit de testes do motor. Roteiro na spec, passos 4–5.

---

## 8. O PROBLEMA ABERTO — colisão de numeração (resolver antes do merge)

O ciclo foi aberto olhando só a `main`. Ao conferir a versão, descobriu-se que a `dev` e outra
branch já usavam os mesmos números:

| Branch | Ciclo 064 | ADR 0021 | Roadmap F29 |
|---|---|---|---|
| `origin/dev` (3 commits à frente da `main`, 26/08–01/09) | `064-capa-para-a-ia-que-instala` | livre | livre (vai até F28) |
| `origin/claude/educational-material-toc-ai-naotqe` | `064-portao-de-slop` | `0021-portao-de-slop-no-livro` | F29 usada |
| **esta branch** | `064-o-metodo-se-cobra-e-bate-o-ponto` | `0021-o-metodo-se-cobra…` | F29 usada |

Consequência: o pull request para a `dev` dá conflito, e os registros (livro de ponto com
`cycle: "064"` e ids `064-*`, `decisoes.jsonl` com `adr-0021`, CHANGELOG) apontam para números
errados.

**Decisão pendente do Darú:** o número do ciclo — **065** (se a branch educacional ainda não entra
na `dev`) ou **066** (se entra antes) — e a ordem entre as duas branches.

**Roteiro proposto (depois da decisão):**
1. `git fetch origin dev` (o clone raso não traz a `dev`; use
   `git fetch origin '+refs/heads/dev:refs/remotes/origin/dev'`) e rebasear a branch sobre ela.
2. Renomear `specs/064-o-metodo-…` → `specs/0NN-o-metodo-…`; atualizar referências a "ciclo 064"
   na spec, plan, tasks, qa-report, CHANGELOG, roadmap, `task-ledger.md`, comentários de código.
3. ADR: renumerar para o próximo livre (0021 se a educacional não entrar; 0022 se entrar),
   atualizar `docs/adr/README.md`. **O ADR ainda não foi para a `dev`**, então renumerar o arquivo
   é permitido; mas cuidado: o guard `PreToolUse` recusa editar ADR **já commitado** — use `git mv`
   e edição via Bash consciente, ou crie o novo e remova o antigo na mesma mudança.
4. `docs/records/decisoes.jsonl` é **append-only**: não editar a linha `adr-0021`; acrescentar com
   `scripts/record-decision.sh` uma linha nova que a supersede, explicando a renumeração.
5. `docs/records/tarefas.jsonl` também é append-only: não reescrever os ids `064-*`; acrescentar
   uma nota/decisão registrando que os eventos `064-*` desta branch pertencem ao ciclo 0NN.
6. Rodar toda a bateria da seção 6 e `scripts/check-cycle.sh` (os commits precisam citar
   `ciclo 0NN`).
7. Abrir PR para a **`dev`** (o fluxo do Maestro é branch → `dev` → `main`; a promoção para a
   `main` é `scripts/promote-main.sh`, que registra o gate humano). Merge e promoção: Darú.

---

## 9. Armadilhas operacionais aprendidas (economizam horas)

- **Sandbox das executoras**: `claude -p` com `--permission-mode acceptEdits` **não consegue
  escrever fora do repositório** (nem em `/tmp`, mesmo com `--add-dir`) e **não consegue editar os
  arquivos de hook do mod** (`mods/*/hooks/*.ts`, tratados como sensíveis). Essas partes foram
  feitas pela sessão gerente. Não contornar.
- **Id de sessão aninhado**: executoras lançadas de dentro de uma sessão herdam o id dela
  (`env -u CLAUDE_CODE_SESSION_ID` não resolveu). Por isso o pareamento usa tarefa + sessão +
  tentativa.
- **Clone raso**: o clone traz só a `main`. Sempre buscar `dev` e as outras branches antes de
  escolher número de ciclo/ADR.
- **`is_placeholder`** do `check-conformance.sh` trata qualquer `[` na evidência como esqueleto não
  preenchido — evidência que cita `[[TASK]]` reprova. Observação registrada no qa-report para um
  ciclo futuro.
- O `check-conformance.sh` corta linhas por **bytes** (parte acentos ao meio): quem lê a saída
  precisa decodificar com `errors="replace"`.
- `check-cycle.sh` só reconhece `spec NNN`, `ciclo NNN`, `cycle NNN` ou `ADR NNNN` na mensagem de
  commit; o prefixo `064:` sozinho não vale.
- Guards ativos no repositório: `PreToolUse` recusa reescrever ADR commitado,
  `decisoes.jsonl` e `docs/ecosystem/ideias/*`; `SessionStart` imprime o estado medido; e agora o
  `Stop` cobra a conformidade.

---

## 10. Achados herdados, ainda abertos (de ciclos anteriores, não deste)

Do `scripts/check-retro.sh` (dívida sob controle, 3 de 4):
- `achado-062-nenhuma-tag-existe-no-remoto` — o GitHub não tem nenhuma tag de versão.
- `achado-063-quatro-skills-sem-capitulo` — causa o vermelho do `check-chapters.sh`.
- `achado-063-anti-padrao-21-sobrevive-a-sete-fechamentos` — falta um portão que procure
  `| grep -q`, `| grep -m1`, `| head -1` no fim de pipe.

`check-evals.sh` vermelho: linha de base defasada (`target moved 7caefbc → 534a088; re-run /eval`).

---

## 11. Regras de conduta com o Darú (observadas nesta sessão)

- Português; chamar de **Darú**; ele não é especialista em JavaScript — explicar devagar, com
  vocabulário antes do fluxo, quando ele pedir explicação.
- **"Prove, não declare"**: colar comando e saída.
- O **gate humano é dele**: não fazer merge, não promover, não fazer `push --force` sem pedido
  explícito (o squash foi pedido e feito com `--force-with-lease`).
- Seguir o próprio Maestro em tudo que for do repositório: ciclo, Constitution Check, cauda de
  fechamento com evidência, revisão independente em contexto fresco.
