# Plan 064 — O método se cobra sozinho e bate o ponto

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-10-12

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Sete requisitos funcionais (FRs, de *functional requirements*) na spec, escritos **depois** de o protótipo ser medido; cada tarefa cita o FR que atende. |
| II. Human-governed orchestration | ✅ O hook `Stop` bloqueia **uma** vez e, na segunda, devolve a decisão ao humano (`systemMessage`); o veredito no livro de ponto vem de uma tarefa de auditoria, nunca de quem executou; o instalador **não** instala o plugin — imprime o passo e o humano decide. |
| III. Reversibility / risk gates | ✅ Remover a entrada `Stop` e desinstalar o plugin desfaz tudo; o livro só acrescenta; o `UPGRADE` substitui **apenas** hooks que são exatamente os de uma versão anterior do Maestro — hooks de terceiros continuam `CONFLICT`. |
| IV. Test-first / verifiable DoD | ✅ Cada peça tem teste executável (motor real via `claude plugin test`, stdin simulado, instalação em projeto novo) e cada portão criado ou alterado tem mutação; o ponto foi provado **ao vivo** contra o relatório da própria sessão. |
| V. Context economy / boundary | ✅ Quatro fatias com fronteira clara: hook (settings), gravador (script), mod (plugin), relatório (script). O mod não lê o livro; o relatório não conhece o mod — o contrato entre eles é o esquema da linha. |
| VI. Living artifacts | ✅ O protocolo vive **uma vez**, instalável, em `docs/governance/task-ledger.md`; o gravador o impõe (vocabulário fechado), o relatório o consome. CHANGELOG, roadmap e índice de scripts mudam no mesmo pull request. |
| VII. Light governance / YAGNI | ✅ Nenhum serviço, banco ou painel: um arquivo JSON Lines (JSONL) e dois scripts. O relatório imprime texto; gráfico fica para quando alguém pedir. |
| VIII. Intelligible communication | ✅ Spec com glossário; o documento instalável expande cada sigla na primeira ocorrência; as etiquetas usam palavras inteiras (`attempt`, `outcome`), não códigos. |

**No violations.**

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | As incógnitas (eventos do mod, tokens por requisição, concorrência do append) foram resolvidas medindo o protótipo; a evidência está no `qa-report.md`. |
| `data-model.md` | `ART:data-model=yes` | O ciclo introduz entidades — tarefa, tentativa, evento — e relações (`redoes`, `target`) das quais o relatório deriva métricas. |
| `contracts/` | `ART:contracts=yes` | Três interfaces entre partes: a entrada e saída do hook `Stop`, a linha de comando do gravador, e a linha do livro que o mod escreve e o relatório lê. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite da spec são todos executáveis e estão no DoD abaixo. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela; o mod usa só a linha de status e o log do transcript, sem componente desenhado. |

## How

**1. Atualizar não pode ser conflito (FR2).** `merge-settings.py` ganha uma lista versionada
`PREVIOUS_HOOKS` com o objeto `hooks` exato de cada versão já distribuída (começa pela v0.3.0,
extraída do git). Se o `hooks` do alvo for **igual** a um deles, o veredito é `UPGRADE` e só
a chave `hooks` é trocada. O instalador trata `UPGRADE` como `MERGED` (mesma escrita atômica)
e diz "upgraded". Qualquer outra coisa continua `CONFLICT`.

**2. O mod viaja pelo marketplace (FR4).** Segunda entrada em `.claude-plugin/marketplace.json`.
O instalador, quando o agente é o Claude Code, imprime no resumo final o comando de instalação
do plugin e as versões mínimas. Nunca o executa.

**3. O protocolo é instalável (FR5).** `docs/governance/task-ledger.md`, em inglês: etiquetas,
vocabulário, eventos, campos, limites. O instalador já copia `docs/governance/`; o bloco do
`CLAUDE.md` ganha uma linha apontando para ele.

**4. O relatório (FR6).** `scripts/report-tasks.py` lê o livro e imprime as métricas do
`data-model.md`. Pura leitura, sem dependência fora da biblioteca padrão do Python. Testado com
um livro sintético cujas respostas foram calculadas à mão.

**5. Portões (FR7).** `check-installed.sh` passa a exigir o hook `Stop` executável e o
gravador. A integração contínua (CI, de *continuous integration*) ganha um passo que roda `claude plugin validate` e
`claude plugin test` no mod **se** o `claude` existir no runner, e diz que pulou quando não
existir. Os testes do gravador e do relatório rodam sempre (Python puro).

**6. Ajustes da revisão independente.** O hook `Stop` mede só o ciclo mais novo (`--ticked-only NNN`), usa
`$CLAUDE_PROJECT_DIR` como raiz (o `cwd` do evento é só reserva) e monta o motivo do bloqueio a
partir das linhas ✗ reais do portão. **As etiquetas** só contam sozinhas na linha (primeira
`[[TASK]]`, última `[[DONE]]`); um `[[TASK]]` de outra sessão não substitui tarefa aberta; só
`audit`/`review` gravam veredito.

## Verification (Definition of Done, DoD)

| Comando | Esperado |
|---|---|
| `merge-settings.py <hooks v0.3.0> <hooks novos>` | `UPGRADE` (era `CONFLICT`) |
| `merge-settings.py <hooks de terceiro> <hooks novos>` | `CONFLICT` |
| instalar sobre um projeto v0.3.0 | hook `Stop` presente e executável; resto do `settings.json` intacto |
| `claude plugin test mods/maestro-ledger` | todos passam |
| `scripts/check-ledger.sh` (gravador, relatório, hook `Stop` e `UPGRADE`) | todos passam |
| `scripts/check-installed.sh <projeto novo>` | verde |
| **mutação**: `UPGRADE` aceita qualquer `hooks` | teste reprova |
| **mutação**: `check-installed.sh` sem a checagem do `Stop` · com o hook apagado | reprova |
| **mutação**: relatório conta a tentativa 2 como primeira | teste reprova |
| os portões de sempre: idioma, conformidade, links, instalação, plugin | verdes |
