# Maestro — o método em um fluxo

> Fluxo/timeline do ciclo spec-driven. Fonte visual: [`fontes/03-fluxo.html`](fontes/03-fluxo.html)
> · PDF: [`pdf/03-fluxo.pdf`](pdf/03-fluxo.pdf)

**Um humano rege, muitos agentes de IA executam.** A intenção vive na especificação; o
humano segura os pontos de decisão; cada passo é verificável e reversível.

**Legenda:** ● agente de IA executa · ◆ humano (decisão / gate indelegável) · ● verificado/entregue.

## O ciclo — cada mudança nasce de uma spec

| Passo | Etapa | Quem / agente | Produz |
|---|---|---|---|
| — | **Intenção** | 🟡 Steward (humano) | o quê e por quê + apetite |
| 1 | **Especificar** | `spec-agent` | `spec.md` (critérios testáveis) |
| ◆ | **Porta: spec pronta (DoR)** | 🟡 humano aprova | *indelegável* |
| 2 | **Planejar** | `plan-arquiteto` | `plan.md` + Constitution Check + ADR |
| 3 | **Fatiar** | (plan) | `tasks.md` por fronteira |
| 4 | **Implementar** | `dev-implementador` | código + testes (diffs pequenos) |
| 5 | **Verificar** | `review` (fresco) · `security` · `qa` | veredito + evidência |
| ◆ | **Porta: pronto (DoD)** | checks mecânicos | verde local ≠ certo global |
| ◆ | **Gate de merge** | 🟡 humano decide | *indelegável* |
| ● | **Entregue → main** | `tech-writer` | docs vivas no mesmo PR; rastreável spec ↔ PR ↔ teste |

## Quem rege e o que sustenta

- **Regência (o humano, indelegável)** — *Steward*: decide o quê/por quê, aprova spec e
  merge. *Orquestrador*: sequencia agentes, gerencia contexto, para o que é caro reverter.
  Responde pela **política** (os trilhos), não por cada item — escala sem virar gargalo.
- **Guardião de processo** (agente, read-only) — vigia o ciclo, barra o que não passa no
  **Constitution Check**. Julga, não conserta.
- **Reversibilidade** — backup, dry-run e rollback tornam o erro barato; gate proporcional
  ao risco.
- **Toolkit (meta-agentes)** — `agent-designer`, `skill-author`, `curador-pesquisa`,
  `didatica-editor` constroem e evoluem o próprio método.

## Governança — tudo evolui sob

**Constituição · Princípios I–VII · ADRs (decisões imutáveis) · YAGNI.**
Retro → regra versionada: o método se corrige a si mesmo.
