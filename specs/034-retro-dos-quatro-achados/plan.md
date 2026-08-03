# Plan 034 — Retrospectiva dos quatro achados

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-03

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes dos scripts; requisitos em EARS |
| II. Orquestração humano-governada | ✅ os checks cobram; a retro e o julgamento da raia continuam humanos |
| III. Reversibilidade / gates de risco | ✅ tudo reversível; nenhum check bloqueia sem saída declarada |
| IV. Test-First / DoD verificável | ✅ os quatro checks **provados falhando** antes de valer |
| V. Economia de contexto / fronteira | ✅ um script por família de achado, não um "check tudo" |
| VI. Artefatos vivos | ✅ achados fechados no índice; catálogo de anti-padrões atualizado |
| VII. Governança leve / YAGNI | ✅ nenhum formato novo: os achados vivem no índice que já existia |
| VIII. Comunicação inteligível | ✅ QA, IA, ADR e EARS por extenso na primeira ocorrência |

## Como

1. **Registrar os achados antes de resolvê-los** — no índice de decisões que já existe
   (`achado-NNN-<slug>`, status `aberta`). Zero formato novo (YAGNI): o índice já é
   append-only, já tem script e já é consultado pela retro.
2. **`check-retro.sh`**: conta achados abertos e mede a idade do mais velho. Falha por
   **dívida**, não por calendário — cerimônia com data marcada vira teatro.
3. **`check-cycle.sh`**: junta os dois achados de disciplina de ciclo (raia justificada e elo
   de commit). Aplica a exigência de justificativa **a partir do ciclo 034** — histórico é
   evidência, não alvo.
4. **`check-links.sh`**: a versão "família inteira" do portão de links (anti-padrão 16),
   cobrindo todo o repositório e não só as páginas publicadas.
5. **`check-chapters.sh`** ganha a comparação data-da-skill × data-do-capítulo.
6. **Fechar os achados** com linha nova citando a regra que os fecha, e registrar `retro-034`.

## Verificação (DoD)

```bash
scripts/check-retro.sh      # 0 abertos ao fim (5 antes)
scripts/check-cycle.sh      # raia justificada + commits citando o ciclo
scripts/check-links.sh      # 242 links, todos resolvem
scripts/check-chapters.sh   # 13 capítulos + frescor das skills
scripts/check-language.sh ; scripts/check-install.sh ; scripts/check-agents.sh ; scripts/check-roles.sh
node publicar/build.mjs
```
