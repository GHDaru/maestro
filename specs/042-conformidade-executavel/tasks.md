# Tarefas 042 — Conformidade executável

## Verificação primeiro
- [x] T0 — medir o defeito antes de propor (35/40 sem cauda · 0/40 artefatos condicionais ·
      roadmap não instalado · `/speckit.plan` instalado exigindo quatro deles)
- [x] T1 — escrever `check-conformance.sh` **antes** de tocar em qualquer template
- [x] T2 — vê-lo vermelho contra um esqueleto recém-gerado (a prova do defeito)

## Implementação
- [x] T3 — `plan-template.md`: tabela obrigatória com os cinco `ART:` 
- [x] T4 — `tasks-template.md`: bloco da cauda com os três `TAIL:`, não removível
- [x] T5 — `qa-report-template.md`: seção de evidência por token
- [x] T6 — `new-cycle.sh` gera esqueleto conformante (é ele que se roda de fato)
- [x] T7 — fechar a brecha do placeholder: `n/a: <razão>` de exemplo satisfazia o portão
- [x] T8 — `docs/governance/artifacts.md` (novo, instalável)
- [x] T9 — corolários C12 e C13; anti-padrão 22; ADR 0019
- [x] T10 — `install-maestro.sh` leva catálogo, portão e a regra da pergunta no bloco gerado
- [x] T11 — `CLAUDE.md`, `CHANGELOG.md`, `docs/roadmap.md`, índice de decisões

## Closing tail — obrigatória, uma linha cada, nunca apagar
- [x] **TAIL:review** — revisão independente em contexto fresco, por quem não executou
  (teorema T2). Evidência: o veredito, no `qa-report.md`.
- [x] **TAIL:security** — n/a: o ciclo não toca superfície de risco. Nenhum segredo,
  credencial, rede ou permissão entra no diff; os arquivos novos são texto e um script
  `bash` somente-leitura que apenas lê `specs/` e `docs/governance/principles.md`.
- [ ] **TAIL:gate** — DoD verde → veredito do guardião → gate humano de merge (indelegável);
  promoção via `scripts/promote-main.sh`.
