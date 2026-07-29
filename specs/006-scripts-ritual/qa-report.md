# QA-report 006 — Scripts do ritual

- **Data**: 2026-07-29 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD) — todas executadas

| Check | Esperado | Resultado |
|---|---|---|
| `bash -n scripts/*.sh` | sem erro | ok (3/3) ✅ |
| `test -x scripts/*.sh` | executável | ok (3/3) ✅ |
| `verificar-agentes.sh` no estado atual | exit 0 | exit 0 (12 agentes, invariantes ok) ✅ |
| `novo-ciclo.sh 999 teste` | cria 4 artefatos | criou spec/plan/tasks/qa-report ✅ |
| `novo-ciclo.sh` 2ª vez | não sobrescreve | marcador preservado ✅ |
| `promover-main.sh` com árvore suja | aborta, main intacto | exit 1, hash de main inalterado ✅ |

## Cobertura dos requisitos

- **FR1** (`promover-main.sh`: confirmação + retry + aborts): ✅ — gate humano preservado.
- **FR2** (`novo-ciclo.sh`: scaffold, não sobrescreve): ✅.
- **FR3** (`verificar-agentes.sh`: invariantes, exit≠0 se quebra): ✅.
- **FR4** (`scripts/README.md` + limite do gate): ✅.

## Nota de segurança (Princípio II)

`promover-main.sh` executa só o **mecânico**; a **decisão** de promover continua humana
(confirmação obrigatória, aborta com árvore suja / sem avanço). A execução deste próprio
ciclo usará o script com `--yes` **após** o gate humano — dogfood do happy path.

## Estado da Fase 3

3 scripts no ar. Workflows pesados adiados até haver dor (YAGNI).
Próximo no roadmap: F4 — vendorizar spec-kit seletivo (spec 007).
