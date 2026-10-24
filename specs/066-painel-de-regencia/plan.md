# Plan 066 — Painel de regência: ciclo guarda-chuva da integração da linha paralela

- **Spec**: `spec.md` (intenção do painel de regência; o desenho dos papéis está em `ux-design.md`) · **Raia**: leve para o que é coordenação; o código que este ciclo abriu foi entregue pelos ciclos filhos · **Data**: 2026-10-19 (aberto) · 2026-10-24 (este plano, escrito depois, para o ciclo dizer o que foi)
- **O que este ciclo é**: a pasta de **coordenação** da integração da linha paralela do Hindiana no Maestro e da abertura do painel de regência. Não entrega código próprio além do lançador multi-sessão; o que produziu são insumos, planos, pareceres, o handoff do longrun, o desenho de UX e as decisões. Os ciclos que entregam código são os filhos: 066 painel v0, 067 trava de domínio, 068 chamados, 069 conferidor pela data, 070 workflow SQLite, e o 072 painel de regência (em curso).
- Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · DoD (*Definition of Done*, definição de pronto) · UX (*user experience*, experiência de uso) · CI (*Continuous Integration*, integração contínua).

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ A intenção está em `spec.md`; os ciclos filhos têm spec própria (066 v0 retroativa, 067, 068, 069, 070 retroativas; 072 escrita antes do código). |
| II. Human-governed orchestration | ✅ O Darú decidiu as cinco decisões do longrun e as decisões A, B, C registradas no `handoff-longrun.md`; em 24/10 delegou os gates por escrito (ADR 0026). |
| III. Reversibility / risk gates | ✅ Tudo o que este ciclo fez é reversível: branches, tags locais `arquivo/paralela/*`, worktrees; o lançador abre sessões, não altera o repositório. |
| IV. Test-first / verifiable DoD | ⚠️ Parcial, declarado: o lançador `scripts/multi-session.py` não tem teste; a prova foi o dry-run e a abertura real das sete sessões (andamento de 22/10 e 24/10). Dívida: teste do `gateway_url` e do `ps_for`. |
| V. Context economy / boundary | ✅ O ciclo existiu para cortar por fronteira: um ciclo filho por commit da linha paralela, cada um com a própria cauda. |
| VI. Living artifacts | ✅ `andamento.md` (diário), `handoff-longrun.md` (retomada), `plano-integracao-linha-paralela.md` (mapa), `ux-design.md` (papéis), insumos; nada duplica os ciclos filhos. |
| VII. Light governance / YAGNI | ✅ Nenhum artefato além dos consumidos; o `spec.md` do esqueleto não foi inflado para parecer ciclo de código. |
| VIII. Intelligible communication | ✅ Siglas expandidas neste plano e nos documentos do ciclo. |

**One declared partial: Principle IV** (lançador sem teste). No other violation.

## Artifacts of this cycle (declare all five — silence is not a decision)

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | A pesquisa deste ciclo foi feita como pareceres e insumos datados (`pareceres-sessoes-via-gateway.md`, `insumo-hindiana.md`, `insumo-prompt-setup-harness.md`), não como incógnita técnica a resolver antes de codificar. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade: o ciclo não escreve código de domínio; o modelo do painel está nos ciclos 068 (chamados) e 070 (workflow). |
| `contracts/` | `ART:contracts=no` | Nenhuma rota nem porta nova; o lançador só chama `claude --name --model`. |
| `checklist.md` | `ART:checklist=no` | A DoD abaixo cobre o que há para checar num ciclo de coordenação. |
| `ux-design.md` | `ART:ux-design=yes` | Toca tela por intenção: o desenho dos papéis semânticos do painel de regência (kanban por gate, jornada, fila de decisões, mapa de sessões) está aqui e é consumido pela spec do 072. |

## How

1. **Mapa de integração** (`plano-integracao-linha-paralela.md`): inventário das 42 branches, renumeração 066–072, estratégia de merge `--no-ff` por hash, decisões 1–9 para o Darú.
2. **Longrun e handoff** (`handoff-longrun.md`, `andamento.md`): cinco decisões fechadas com o Darú; ponto de retomada do 070; roteiro das sete sessões.
3. **Sessões construtoras**: `scripts/multi-session.py` adaptado da Hindiana (um modelo por sessão, uma worktree por Worker, sem segredo), correção do 401 por herança de `ANTHROPIC_BASE_URL` (`18d7223`).
4. **UX antes de componente**: `ux-design.md` pelo agente `ux-semantics`, insumo direto da spec do 072.
5. **Decisões de método nascidas aqui**: ADR 0024 (cabeçalho conferível), ADR 0026 (gate por delegação); ADR 0022 e 0023 pelos ciclos filhos 066 v0 e 067.

## Verification (DoD)

- `ls specs/066-painel-de-regencia/` → `andamento.md`, `handoff-longrun.md`, `plano-integracao-linha-paralela.md`, `ux-design.md`, `pareceres-sessoes-via-gateway.md`, `insumo-hindiana.md`, `insumo-prompt-setup-harness.md`, `spec.md`, `plan.md`, `tasks.md`, `qa-report.md`
- `python scripts/multi-session.py . --dry-run` → sete linhas (Gerente glm-5.3, Worker01–06 deepseek-v4.1-flash) e `[dry-run] nothing opened`
- `scripts/check-conformance.sh 066` → verde para `066-painel-de-coordenacao-v0` e para esta pasta
- `grep -c 'ciclo 066' CHANGELOG.md` → ≥ 1 (entrada do ciclo filho 066 v0; esta pasta não tem entrada própria porque não entrega função ao usuário)
