# Capítulo 07 — Cerimônias e cadência (elemento `[6]`)

> Cadência **Shape Up + Kanban**, não Scrum: cerimônia é **função**, não reunião — e o
> WIP se mede em **atenção do humano**, não em capacidade de agentes.

## 1. Pergunta central

Quais cerimônias sobrevivem quando é **um humano + N agentes** — e, já que os agentes
paralelizam, **qual é o limite real do WIP**?

## 2. Fundamentação teórica

**Cerimônia é a função que entrega, não a reunião.** Para decidir o que cortar,
pergunte "essa **função** ainda existe no meu contexto?".

| Cerimônia | Função | Em solo+IA |
|---|---|---|
| Planning | comprometer escopo | vira **shaping/spec** (`[2]`) |
| Daily | sincronizar/destravar **entre pessoas** | **função some** → cortada |
| Review | inspecionar incremento | vira **checkpoint de ciclo** |
| Refinement | preparar backlog | **cortada** (sem backlog — Shape Up) |
| **Retro** | melhorar o processo | **amplificada** (ver abaixo) |

**Retro amplificada.** Num time humano, a melhoria da retro é um hábito mole que decai.
Com agentes, ela vira **instrução versionada** (`CLAUDE.md`/skill/constituição):
**durável e executável**, aplicada automaticamente na próxima. É a cerimônia de **maior
ROI** — cada erro recorrente de agente vira regra.

**Cadência = Shape Up + Kanban.** *Apetite* (tempo fixo, escopo variável — o oposto de
estimar prazo; casa com YAGNI e diffs pequenos), *cooldown* (dívida/manutenção/curadoria),
sem *backlog* formal (ideias importantes voltam via re-shaping), fluxo contínuo com **WIP
limitado**.

**O limite real do WIP é a atenção do humano.** Não é a capacidade dos agentes nem a
dependência entre tasks (essa limita o paralelo **dentro** de uma feature). Mesmo com 5
features de dependência zero, cada uma funila pelos **gates de decisão/aprovação/
verificação do humano** (`[5]`). Portanto:
- **paralelize DENTRO** de uma feature já decidida (subagentes por bounded context);
- **não paralelize ACROSS** features ambíguas (multiplicam os gates);
- para escalar, **barateie os gates** (DoD verificável `[8]`, reversibilidade `[1]`) — não
  abra mais frentes.

## 3. Frameworks / abordagens avaliados

| Framework | Papéis/eventos | Veredito para solo+IA |
|---|---|---|
| **Scrum** | PO/SM/Dev; planning, daily, review, retro, refinement | **Parcial** — mantém-se só a *função* de planning (→ spec) e retro; SM e daily são cerimônia de papel |
| **Kanban** | sem papéis/eventos; visualizar fluxo + limitar WIP | **Adotado** — WIP limitado (pela atenção humana) e fluxo contínuo |
| **Shape Up** | shapers/builders; apetite, ciclo 6sem + cooldown, betting, sem backlog | **Adotado (esqueleto)** — apetite + cooldown + sem backlog |
| **Scrumban** | híbrido | **Observado** — não precisamos do overhead do Scrum que ele carrega |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Cerimônias mínimas**: shaping/spec (planning real), execução por apetite,
  checkpoint de ciclo, cooldown, **retro** (→ regra versionada).
- **Cortar** daily e sprint planning (função de sincronização entre pessoas inexistente).
- **WIP baixo**, medido em **fluxos de decisão que o humano segura com qualidade**;
  paralelismo vai para **dentro** da feature.
- **Apetite** (tempo fixo, escopo variável): quando acaba, corta-se escopo — não se
  estende prazo.

## 5. Conexões

- **`[5]`** — o gargalo é o humano Accountable; o WIP é atenção humana.
- **`[4]`** — paralelizar *dentro* da feature (subagentes por bounded context).
- **`[2]`** — apetite = escopo variável = a raia certa por mudança.
- **`[8]` / `[1]`** — baratear os gates (DoD verificável, reversibilidade) é como se escala.

## 6. Insight da jornada e impacto no modelo

Insights do aprendiz: **cerimônia = função** (não reunião); **retro é a que fica mais
valiosa com agentes**; dependência de tasks limita o paralelo **dentro** da feature, mas
**o humano (atenção/decisão) é o gargalo do WIP através** de features. Sem impacto
normativo novo — fundamenta a cadência do `modelo-operacional.md` §5. Diário: `[6]`.

## 7. Fontes

- Basecamp — *Shape Up* (apetite, ciclo, cooldown, betting): https://basecamp.com/shapeup
- DORA — *four keys* (lote pequeno; velocidade×estabilidade): https://dora.dev/guides/dora-metrics-four-keys/
- `docs/governance/modelo-operacional.md` §5; Capítulos 01 (`[1]`), 06 (`[5]`).
