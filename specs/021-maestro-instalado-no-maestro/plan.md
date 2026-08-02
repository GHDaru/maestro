# Plan 021 — Maestro instalado no próprio Maestro

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes do código; requisitos em EARS (*Easy Approach to Requirements Syntax*) |
| II. Orquestração humano-governada | ✅ o check reporta; corrigir a instrução continua decisão humana |
| III. Reversibilidade / gates de risco | ✅ tudo reversível por `git revert`; o instalador não sobrescreve |
| IV. Test-First / DoD verificável | ✅ os dois checks **provados falhando** — um deles com deriva real, não simulada |
| V. Economia de contexto / fronteira | ✅ um script novo, de responsabilidade única; nada acoplado ao build |
| VI. Artefatos vivos | ✅ o alvo do ciclo é exatamente isto: instrução que não envelhece calada |
| VII. Governança leve / YAGNI | ✅ 70 linhas de shell; nenhum framework de instalação |
| VIII. Comunicação inteligível | ✅ IA, ADR, DoD e EARS por extenso na primeira ocorrência de cada texto |

## Como

1. **Verificação primeiro**: escrever `verificar-instalacao.sh` e rodá-lo **antes** de
   arrumar nada. Se um check nasce verde, não se sabe o que ele mede (skill
   `dod-verificavel`, segunda lei). Este nasceu vermelho, com deriva real.
2. **Causa raiz antes do fix** (skill `diagnostico-antes-do-fix`): os três achados não são
   três bugs, são um só — lista à mão sem comparação com o disco. Por isso a correção é
   estrutural (fonte única + bloco gerado), não "atualizar o texto".
3. **Fonte única**: `AGENTS.md` → link simbólico para `CLAUDE.md`. `grep` segue o link,
   então o próprio check continua verificando os dois nomes sem tratamento especial.
4. **Bloco gerado**: `instalar-maestro.sh --bloco` lê `skills/*/SKILL.md` e monta a
   instrução com nome + primeira frase da descrição.
5. **Contagem de princípios** em `verificar-papeis.sh`: `### N.` na constituição × linhas
   `| N.` no template de plano.
6. **Prova ponta a ponta** num repositório vazio, seguindo a receita ao pé da letra.

## Verificação (DoD)

```bash
scripts/verificar-instalacao.sh          # exit 0 neste repo (nasceu em 1, com 2 achados)
scripts/verificar-papeis.sh              # exit 0; falha se o template perder um princípio
scripts/verificar-agentes.sh             # invariantes dos 13 subagentes
scripts/instalar-maestro.sh --bloco      # bloco gerado das 6 skills do disco
# ponta a ponta, em repositório vazio:
#   instalar -> check FALHA (7) -> --bloco >> CLAUDE.md + symlink -> check PASSA -> novo-ciclo
```
