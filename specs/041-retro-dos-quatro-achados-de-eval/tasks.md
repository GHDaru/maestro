# Tarefas 041 — Retro: os quatro achados de eval viram regra

## Verificação primeiro
- [x] T0 — rodar `scripts/retro.sh` (o gatilho já estava vermelho) e ler o material apurado
- [x] T1 — descobrir que a própria ferramenta mentia: 20 gates pendentes falsos

## Implementação
- [x] T2 — corrigir a apuração de gate no `retro.sh` (fato, não formato de id)
- [x] T3 — corrigir a correção: `grep -q` no fim de pipe sob `pipefail` (segunda ocorrência)
- [x] T4 — anti-padrões 19, 20 e 21 na skill, cada um com o ciclo de origem
- [x] T5 — `check-evals.sh`: `Axis:` obrigatório, `Ablation:` e `Premise-checked:`
      obrigatórios, aposentadoria com motivo impresso e contada à parte
- [x] T6 — vê-lo acusar nas três condições novas
- [x] T7 — aposentar o caso 002 com motivo; `Axis:` no 001 e os dois campos na linha de base
- [x] T8 — pré-voo e ablação obrigatórios no `/eval`; `evals/README.md` acompanha
- [x] T9 — `docs/records/README.md`: forma para achado fechado no mesmo ciclo
- [x] T10 — fechar os quatro achados; gatilho da raia sobredeterminada no roadmap
- [x] T11 — `CHANGELOG.md`, `docs/roadmap.md`, `CLAUDE.md`

## Gate
- [x] T12 — DoD verde → `qa-report.md`
- [ ] T13 — gate humano de merge `dev` → `main`
