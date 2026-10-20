# Plano: integrar a linha paralela no Maestro (Opus, só leitura, medido em 19/10/2026)

**Base.** `origin/dev` = `origin/main` = `af6fd1b`. Desde a base antiga `534a088` são 9 commits (ciclos 064 capa e 065 livro de ponto). A linha paralela vive em `C:\Users\ghdaru\DriveD\010_PROJETOS\maestro` (42 branches, publicadas no GitHub em 19/10).

**O que mais pesa.** São duas linhagens irmãs, separadas em `7924ce2`, que só se tocam em `6e99bac`:
- **A (workflow/rodadas):** `064-workflow-painel` → `w07-064-integrate` `b33bb81` → `w09-065-reingerir` `6e9788f`.
- **B (painel-controle → chamados):** `painel-controle` `a1172a2` → `067-painel-chamados` `aa0efd1`.

`067-painel-chamados` **não contém** 064/065/066. `painel-controle` **não está** dentro de `064-workflow-painel`.

**O que a Hindiana roda.** `chamados.py`, `custo.py`, `server.py`, `index.html` em `180_HINDIANA\.maestro\painel` são idênticos aos de `067-painel-chamados` `aa0efd1`; `ingest.py` é o de `7924ce2`. A Hindiana roda a linhagem B sem a A. O `VERSAO` ("painel-controle, 7924ce2") está desatualizado.

## 1. Inventário

| Ciclo original | Ponta mais completa | Commits / tamanho | Entrega | Artefatos do método |
|---|---|---|---|---|
| base painel | `painel-controle` `a1172a2` (contém `7924ce2`, `43d652c`) | 12; 18 arquivos, +3579 | painel v0 (`painel/`: HTML+JS+SQLite, MCP); hook de veredito em `.maestro/controle/git-hooks/` | sem spec; rascunho "ADR 0021" em `painel/docs/adr-rascunho-painel.md` |
| trava de domínio | `trava-dominio-plan` `db6b89c` (já dentro do 067) | 3; 4 arquivos, +99 | tokens `DOM:*` no plan-template e no `check-conformance.sh` (`DOM_FLOOR=67`) | sem spec; **muda um portão** |
| 064 workflow | `w07-064-integrate` `b33bb81` | 14; 20 arquivos, +2192 | SQLite WAL, outbox, hooks `scripts/hooks/workflow_{session_start,stop}.py`, 5 testes | spec, plan (CC), data-model, ux-design; tasks com 4 TAIL `[ ]`; **sem qa-report** |
| 065 board | `w09-065-reingerir` `6e9788f` (contém 064) | 15; 15 arquivos, +2661 | board enxuto, árvore, rotas, testes de contrato | spec, plan, ux-design; **sem tasks/qa-report** |
| 066 custeio | `066-custeio-controle` `7eecbbc` | 4; só spec (84 linhas) | tokens por sessão; subir/derrubar PID | só spec |
| "067" chamados | `067-painel-chamados` `db6b89c..2796cbf` | 14; 12 arquivos, +3719 | `chamados.py`, `custo.py`, BPMN, `chamados-manuais-hindiana.json` (1133 linhas) | **nenhum specs/067** |
| 070 conferidor | `aa0efd1` + `699bddb`, `c625c42` (só em `w10/070-g3-codigo`) | 21; 12 arquivos, +485 | veredito vigente pela data | spec + G0–G3 (padrão Hindiana); sem plan/tasks/TAIL |
| 068 WhatsApp | spec em `fa6fc6a`; código só em `w09/068…` `8c30d79`, `w02/068-trilha-b` `33225a3`, `w08/068-p2` `5fb3557` — nunca unidos; conflito em `saida.py` | — | entrada WhatsApp (Evolution/n8n) | spec, plan, tasks (47 `[ ]`); GD classe C, LGPD pendente |
| 069 receptor | `069-receptor-grupo-ola` `c4eb58c` | 29; 40 arquivos | receptor HTTPS na LAN, `deploy/` (IP, sudoers) | spec, plan, tasks; sem TAIL |
| corpus | `fix/corpus-catalogo-ecossistema` `7bd7b72` | 1 | regenera `companion/backend/corpus.json` | raia leve |

Nenhuma branch toca `CHANGELOG.md`, `docs/roadmap.md`, `decisoes.jsonl`, `docs/adr/` ou `.claude/settings.json`.

## 2. Sobreposição e conflitos com `af6fd1b`

- **Textual com a dev:** só `scripts/check-conformance.sh` (dev: 1 linha PT-DATA; B: +62 linhas DOM). Trivial.
- **A × B** (a partir de `6e99bac`): `painel/index.html`, `painel/server.py`, `painel/projetos/hindiana.json`. Único conflito real; arbitrar pelos 13 testes da linhagem A.
- **Portões que vão reprovar:** `check-boundary` (`painel/`, `.maestro/`, `deploy/` sem domínio); `check-language` (hooks `workflow_*.py` em português dentro de `scripts`); `check-conformance` (nenhum ciclo importado tem qa-report); `check-cycle` (≈100 commits sem "ciclo NNN", consultivo).
- **ADR 0021 ocupado** na dev → próximo livre **0022**; roadmap **F30**.
- **066-custeio × 065 da dev:** FR1, 2, 4, 5, 13, 20 duplicam `mods/maestro-ledger`, `report-tasks.py` e `painel/custo.py`; FR8–12 e FR15–19 são complementares (metadados; subir/derrubar sessão = risco alto). Veredito: insumo do painel de regência, não ciclo.

## 3. Mapa de renumeração (ordem de integração)

| Novo | Origem | Merge em | ADR / fase |
|---|---|---|---|
| **066** painel v0 + hook de veredito | base painel | `a1172a2` | ADR **0022** (rascunho promovido; supersede em parte "dashboard YAGNI" do operating-model §6); **F30** |
| **067** trava de domínio | trava-dominio-plan | `db6b89c` | ADR **0023**; F31 (`DOM_FLOOR=67` fica certo) |
| **068** chamados gate a gate + custo | trecho sem spec do 067 | `2796cbf` | F32 |
| **069** conferidor pela data | 070 | `aa0efd1` + `699bddb` | correção na F32 |
| **070** workflow SQLite + hooks | 064 | `b33bb81` | ADR **0024**; F33 |
| **071** board/rodada navegável | 065 | `6e9788f` | F33 |
| **072** painel de regência | esqueleto local `066-painel-de-regencia` + spec 066-custeio como insumo | — | F34 |
| fora | 068 WhatsApp, 069 receptor | — | repo da Hindiana |

B antes de A porque B é o que roda em produção; o conflito cai sobre a linhagem com testes.

## 4. Estratégia

- **Merge `--no-ff` por ciclo em hashes intermediários.** Sem rebase (reescreveria `7924ce2`/`aa0efd1` e o `VERSAO` da Hindiana ficaria órfão) e sem squash (apagaria os pares vermelho/verde do G2).
- Por ciclo: (1) merge `ciclo NNN: integra <origem> (<hash>) da linha paralela`; (2) commit no padrão `dda2225`: `git mv` do spec, plan com CC/ART/DOM, tasks com TAIL, qa-report real, CHANGELOG, roadmap, ADR; (3) `record-decision.sh` `ciclo-NNN-renumerado` (antigo → novo + hash original).
- **Uma PR por ciclo para a `dev`**, empilhadas, de `integra/linha-paralela-NNN`.
- **Branches de gate:** tag anotada `arquivo/paralela/<branch>` em cada uma das 42 pontas ANTES de qualquer deleção (obrigatório para as 9 do 068). Deleção só com aprovação.
- `check-cycle`: documentar a exceção no qa-report; não afrouxar.

## 5. Decisões humanas (com recomendação)

1. `painel/` e `.maestro/` no Maestro? **Sim**, em `toolkit.owns` do `boundary.json`, justificado no ADR 0022. `deploy/` não.
2. 068 e 069 são produto Hindiana (GD classe C, LGPD, IP, sudoers): **levar ao repo da Hindiana**, preservando tags; não importar.
3. Dados reais da Hindiana (`chamados-manuais-hindiana.json`, `hindiana.json`): **trocar por fixture**; o repo é público e as branches já foram publicadas.
4. 066-custeio: **não vira ciclo**; insumo do 072. Controle de PID em spec própria, depois.
5. Hooks do workflow: **`git mv` para `painel/hooks/`** (sai do instalador e do `check-language`).
6. TAIL retroativo: `TAIL:review` e `TAIL:mutation` executados de verdade agora, em contexto fresco; o que só existe nos G* da Hindiana não vale. `TAIL:gate` é do Darú, por ciclo.
7. Conflito A × B: **B prevalece**; A se adapta até os 13 testes ficarem verdes.
8. `VERSAO` da Hindiana: corrigir lá para `aa0efd1`, citando o `receptor_ola.py` (vem do 069).
9. Branches remotas: deleção só depois das tags e com o "sim" do Darú.

## 6. Execução

| # | Quem | Passo |
|---|---|---|
| 0 | Darú | decide 1–5 e 9 |
| 1 | Sonnet | `git fetch`; tags `arquivo/paralela/*` nas 42 pontas (push só com aprovação) |
| 2 | Opus | spec, plan, tasks retroativos do 066 + ADR 0022 a partir do rascunho |
| 3 | Sonnet | merge `a1172a2`; `boundary.json`; commit de renumeração; `record-decision.sh` |
| 4 | contexto fresco | `TAIL:review`, `TAIL:security`, `TAIL:mutation` (067: quebrar o bloco DOM e ver o portão recusar) → `qa-report.md` |
| 5 | Darú | `TAIL:gate` → PR para a `dev` |
| 6 | todos | repetir 2–5 para 067 (`db6b89c`, ADR 0023), 068 (`2796cbf`), 069 (`aa0efd1`+`699bddb`), 070 (`b33bb81` + mover hooks + ADR 0024), 071 (`6e9788f`, resolver conflito com `python -m pytest painel/tests`) |
| 7 | Sonnet | `promote-main.sh` |
| 8 | Opus | renumerar o esqueleto para `072-painel-de-regencia` e só então planejar o painel |

**Portões por PR** (Windows: Git Bash, shim `python3`, `PYTHONUTF8=1`, `core.autocrlf=false`): check-agents, check-roles, check-install, check-language, check-links, check-evals, check-boundary, check-chapters, check-licensing, check-ecosystem, check-installed, check-adr, check-version, check-flags; `check-conformance.sh NNN` e `--ticked-only`; check-ledger, check-cycle (`MAESTRO_TRACE_BASE=origin/dev`), check-retro; `package-plugin.sh --verify`; `node publicar/build.mjs`.
