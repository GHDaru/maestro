# Plan 064 — Workflow do ciclo Maestro no painel

- **Spec**: `spec.md` · **Lane**: full · **Date**: 2026-10-02

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Spec 064 aprovada, originada do desejo-001 do Gilsiley. |
| II. Human-governed orchestration | ✅ O humano (Gilsiley) aprova a spec e o plan; o hook registra, não decide. |
| III. Reversibility / risk gates | ✅ SQLite append-only; reconstrução em transação; rollback = restaurar snapshot anterior. |
| IV. Test-first / verifiable DoD | ✅ Cada FR tem acceptance criterion em EARS ou comando verificável. |
| V. Context economy / boundary | ✅ Corta pelo boundary: backend SQLite+hooks (W09) e tela HTML+JS (W03), worktrees separadas. |
| VI. Living artifacts | ✅ Spec, plan, tasks e código no mesmo ciclo (specs/070-workflow-sqlite/). |
| VII. Light governance / YAGNI | ✅ SQLite em WAL, não Redis/RabbitMQ (19 sessões numa máquina). |
| VIII. Intelligible communication | ✅ Siglas expandidas na primeira ocorrência; legível para quem chega hoje. |

**No violations.**

## Artifacts of this cycle

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Sem unknown técnico; o desenho (workflow-maestro.md) já define a arquitetura. |
| `data-model.md` | `ART:data-model=yes` | Tabelas rodadas, passos, transicoes, fila — entidades e relações. |
| `contracts/` | `ART:contracts=no` | O contrato é o schema SQLite + hooks do Claude Code; sem API externa. |
| `checklist.md` | `ART:checklist=no` | A spec já tem acceptance criteria verificáveis. |
| `ux-design.md` | `ART:ux-design=yes` | Toca tela (painel HTML+JS); roadmap, decisões, equipe, aviso de leitura velha. |

## How

### Backend (W09): SQLite + hooks

1. **Schema** (data-model.md): tabelas append-only `rodadas`, `passos`, `transicoes`, `fila` em SQLite modo WAL. Coluna `evidencia_json` em `passos` guarda hash, número, veredito.

2. **Hooks** (.claude/settings.json): `SessionStart` mostra os passos abertos da sessão e o próximo permitido. `Stop` cobra resumo e saída do passo aberto. Hooks escrevem no SQLite via script Python.

3. **Ingest transacional**: reconstrói dados derivados num arquivo temporário e troca (rename) no fim. Se interrompido, a versão anterior continua servindo (FR5/FR12).

4. **Leitura velha**: o painel compara o timestamp do último ingest com agora; se >1h, exibe aviso no cabeçalho (FR11).

5. **Erros de leitura**: se um arquivo de decisões ou roadmap não pode ser lido, exibe o caminho e o motivo, não vazio calado (FR6).

### Tela (W03): HTML+JS

6. **Roadmap**: cada rodada com passo atual, tempo em cada passo, quem está nele (FR4).

7. **Equipe real**: 19 sessões (4 Desktop: Office, Assistente, Reescrita, Testes Dev; 15 Code: Gerente, Gerente02, W01–W13 sem W10) (FR10).

8. **Link por documento**: cada item do roadmap/decisões linka para o arquivo.

### Fila (outbox)

9. **Fila em SQLite** (modo WAL): tabela `fila` lida pelos hooks. Entrega o que um broker daria, sem serviço adicional (FR9). Redis Streams anotado como decisão no Clarify, revisitado quando multi-máquina.

## Verification (DoD)

- `sqlite3 painel.db ".tables"` → contém `rodadas`, `passos`, `transicoes`, `fila`
- `sqlite3 painel.db "SELECT count(*) FROM passos WHERE entrada_em IS NOT NULL AND saida_em IS NULL"` → ≥ 0
- `python -m pytest tests/test_hooks.py -k session_start` → 0 failed (hook registra entrada)
- `python -m pytest tests/test_hooks.py -k stop` → 0 failed (hook cobra saída)
- `python -m pytest tests/test_ingest.py -k transacional` → 0 failed (painel não fica vazio se interrompido)
- `python -m pytest tests/test_painel.py -k roadmap` → 0 failed (roadmap mostra rodada com passo atual)
- `python -m pytest tests/test_painel.py -k leitura_velha` → 0 failed (aviso >1h)
- `python -m pytest tests/test_painel.py -k erro_leitura` → 0 failed (exibe caminho e motivo)

<!--
  GATE (not delegable): the plan is approved by a human before it becomes tasks.
  Handoff: plan-architect → (approval) → tasks → dev-implementer.
-->
