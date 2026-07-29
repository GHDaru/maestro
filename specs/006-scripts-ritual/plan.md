# Plan 006 — Scripts do ritual

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-29

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 006 |
| II. Orquestração humano-governada | ✅ **crítico**: script executa o mecânico; o *gate* (decidir promover) continua humano — `promover-main.sh` exige confirmação e aborta |
| III. Reversibilidade / gates de risco | ✅ aborta com árvore suja / sem confirmação; `novo-ciclo` não sobrescreve |
| IV. Test-First / DoD verificável | ✅ DoD por exit code e efeito no FS (testável a seco) |
| V. Economia de contexto / fronteira | ✅ tira passo mecânico da atenção do Orquestrador (o gargalo) |
| VI. Artefatos vivos | ✅ `scripts/README.md`; roadmap atualizado |
| VII. Governança leve / YAGNI | ✅ só 3 scripts de dor provada; workflows pesados adiados |

**Sem violações.**

## Como

- Bash portável: `#!/usr/bin/env bash`, `set -euo pipefail`, mensagens claras, `chmod +x`.
- `promover-main.sh`:
  1. `git diff --quiet` + `git diff --cached --quiet` → aborta se sujo.
  2. Confere que `dev` está à frente de `main` (`git rev-list --count main..dev` > 0).
  3. Ecoa os commits que vão para main; pede confirmação (`read`, ou `--yes` explícito).
  4. `git branch -f main dev` + `git push origin main` com retry exponencial (2/4/8/16s).
- `novo-ciclo.sh <NNN> <slug>`: valida args; `mkdir -p specs/NNN-slug`; escreve os 4
  artefatos-esqueleto se não existirem (`set -C`/teste `-e`); ecoa o que criou.
- `verificar-agentes.sh`: roda as 3 asserções (contagem=12, frontmatter, read-only sem
  Write/Edit); acumula falhas; `exit 1` se houver.
- Função de retry compartilhada inline em cada script (sem lib externa — YAGNI).

## Verificação (DoD)

- `bash -n scripts/*.sh` (sintaxe) ok; todos com bit +x (`test -x`).
- `scripts/promover-main.sh` sem confirmação → exit ≠ 0, main intacto (dry-run com env).
- `scripts/novo-ciclo.sh 999 teste` cria 4 arquivos; rodar 2ª vez não sobrescreve.
- `scripts/verificar-agentes.sh` → exit 0 agora.
