# Plan 018 — Instalação visível + UX e jornadas

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 018 |
| II. Orquestração humano-governada | ✅ o ramo de interface acrescenta um gate humano (aprovar UX), não remove |
| III. Reversibilidade / gates de risco | ✅ conteúdo e scripts; reversível por git |
| IV. Test-First / DoD verificável | ✅ **nova fitness function**, provada falhando (segunda lei da `dod-verificavel`) |
| V. Economia de contexto / fronteira | ✅ agente novo é estreito (semântica, não implementação) |
| VI. Artefatos vivos | ✅ README, índices, BPMN, perfis e instalador no mesmo ciclo |
| VII. Governança leve / YAGNI | ✅ 1 agente + 1 skill + 2 templates — exatamente o que a norma já exigia |
| VIII. Comunicação inteligível | ✅ IA, BPMN, DoR expandidos na 1ª ocorrência |

**Sem violações.**

## Como

- **README**: bloco de instalação antes de "Estrutura", escrito para dois leitores — o
  humano (comandos) e a IA (a nota de que instalar é copiar, não empacotar).
- **`ux-semantica`**: Iron Law "nenhuma tela nasce sem papel semântico declarado";
  produz `ux-design.md`; não implementa componente.
- **`jornada-viva`**: as três partes obrigatórias (documento · capturas do build real por
  script versionado · heurística datada) e o check que o caso do FlowBuilder revelou —
  regenerar captura **obriga** revisitar a heurística.
- **`verificar-papeis.sh`**: mapa papel-prescrito → arquivo-que-entrega; falha nomeando o
  que falta. Também cobre artefato essencial ↔ template.
- **BPMN**: raia própria (o ramo é condicional: "tem UI?"), com o gate de UX no lugar certo.

## Verificação (DoD)

- `verificar-papeis.sh` com o agente removido → exit 1 nomeando 'UX-agent' *(provado)*.
- `verificar-agentes.sh` → 13; `ls skills/*/SKILL.md` → 6.
- `grep` do instalador no README; raia no HTML do BPMN; `pytest` e build verdes.
