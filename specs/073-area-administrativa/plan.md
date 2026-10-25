# Plan 073 — Área administrativa do Maestro (rodada 1: pesquisa de plataformas)

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-10-24

> Ciclo de pesquisa em quatro rodadas; este plano cobre a **rodada 1**. As rodadas 2–4
> (confronto, wireframes, bar de três críticos) ganham os seus planos quando o regente der o
> "segue" — nada aqui decide arquitetura ou desenha tela.

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | Sim — a rodada 1 nasceu da spec (FR1–FR4 + tabela fixa de 26 funcionalidades em quatro grupos); nenhuma ficha foi escrita antes dela, e o vocabulário foi fixado antes de pesquisar. |
| II. Human-governed orchestration | Sim — o regente (sessão MAESTRO) definiu escopo, orçamento e divisão em três fatias; o Gerente despachou W03, W05 e W06 e integra; a verificação é por agente independente em contexto fresco (quem consolidou não verifica — Teorema 2). |
| III. Reversibility / risk gates | Sim — rodada documental: nada irreversível (nenhum software, nenhuma conta externa, nenhuma credencial real); os limites foram declarados no despacho e respeitados (exceção registrada: LiteLLM rodou local com chave descartável). |
| IV. Test-first / verifiable DoD | Sim — os critérios de aceite são verificáveis por contagem (colunas, linhas, células) e amostragem contra as fichas; a contagem medida está no qa-report, e a amostragem é repetida por quem não consolidou. |
| V. Context economy / boundary | Sim — três fatias por nicho (gateways e consoles de LLM; observabilidade e orquestração; processos e governança), cada worker com escopo limitado; a matriz é o índice, a prova fica na ficha — ninguém carrega 25 fichas no contexto. |
| VI. Living artifacts | Sim — `andamento.md` atualizado a cada DONE (é a página de progresso viva do Darú); `plataformas.md` consolidada por acréscimo, sem reescrever ficha alheia; nenhum artefato duplicou função já servida. |
| VII. Light governance / YAGNI | Sim — nenhuma ferramenta nova; plataformas extras de nicho (Cloudflare AI Gateway, Kong AI Gateway, Bifrost) foram deferidas ao regente, não incorporadas por conta própria; a normalização de notação entre gerações de ficha foi deferida para o preâmbulo da rodada 2, onde a força do veredito passa a importar. |
| VIII. Intelligible communication | Sim — siglas expandidas na primeira ocorrência em spec, fichas e matriz (RBAC — Role-Based Access Control; MCP — Model Context Protocol; A2A — Agent-to-Agent; LLM — Large Language Model). |

## Artifacts of this cycle (declare all five — silence is not a decision)

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | a pesquisa da rodada 1 vive em `pesquisa/` — 25 fichas de plataforma + a matriz `plataformas.md`; um research.md único duplicaria função já servida (Princípio VI) |
| `data-model.md` | `ART:data-model=no` | rodada documental: nenhuma entidade de software nasce antes da rodada 2 decidir o que entra |
| `contracts/` | `ART:contracts=no` | nada executável foi construído — não há rotas, portas ou eventos para contratar |
| `checklist.md` | `ART:checklist=no` | os critérios de aceite da rodada 1 (spec.md, seção Acceptance criteria) já são a lista de verificação; duplicá-la violaria o Princípio VI |
| `ux-design.md` | `ART:ux-design=no` | nenhuma tela nesta rodada; wireframes são a rodada 3, sobre contexto delimitado de DDD, e só depois da decisão da rodada 2 |

## Domain model (declared — research round)

- `DOM:aggregate=plataforma` — a raiz é a plataforma pesquisada: a ficha dela em pesquisa/ é a fonte de verdade e a coluna na matriz é projeção. A matriz é o índice; a prova está na ficha.
- `DOM:invariants=fonte_por_celula=domain | celula_sem_fonte_fica_vazia=domain`
  - As duas regras do artefato desta rodada: toda célula cita fonte na ficha (FR3) e célula
    sem fonte fica vazia (`—`), nunca "sim".
- `DOM:glossary=tabela-fixada` — o vocabulário da rodada é a tabela fixa de 26 funcionalidades em quatro grupos (spec.md); sigla nova entra expandida na primeira ocorrência, em spec, ficha e matriz.
- `DOM:ports=nenhuma` — a rodada 1 não tem software nem interfaces; as fontes web são lidas (URL por célula na ficha), não implementadas.

## How

1. **Spec primeiro** (`spec.md`): objetivo, tabela fixa de funcionalidades, critérios de aceite
   FR1–FR4, fora de escopo (nenhum software, nenhuma conta, nenhuma credencial real).
2. **Três fatias em paralelo**, cada worker com nicho próprio e a mesma tabela fixa:
   - W03 — gateways e consoles de LLM (LiteLLM, Portkey, OpenAI Platform, Helicone);
   - W05 — observabilidade e orquestração de agentes (AgentOps, Langfuse, LangSmith/LangGraph,
     CrewAI AMP, AutoGen Studio, Dify, Flowise + Arize Phoenix, Comet Opik);
   - W06 — controle de processos e governança (Temporal, Portainer, Prefect, Dagster, Copilot
     Studio, Agent 365, n8n, Claude Code, Maestri, Kiro Crew + AgentCore, Windmill).
3. **Busca na internet obrigatória** (WebSearch/WebFetch); ferramenta rodada local só em
   instalação oficial e sem credencial real — o LiteLLM do W03 é a exceção registrada, com
   capturas em `pesquisa/img/`.
4. **Consolidação por acréscimo** (`plataformas.md`): uma coluna por plataforma, 26 linhas na
   ordem da tabela fixa, fonte por célula (a ficha), `—` quando não há fonte. Quem termina
   primeiro publica a estrutura; os demais acrescentam colunas.
5. **Integração do Gerente**: merge das três fatias, `andamento.md` a cada DONE, decisão de
   notação (branco vira `—`; `não` transcrito como a ficha escreveu, divergência declarada na
   legenda; normalização deferida ao preâmbulo da rodada 2).
6. **Verificação em contexto fresco** (W03, que não consolidou): amostragem dirigida de 7
   células + recontagem independente + passagem de segurança sobre `pesquisa/`.

## Verification (DoD)

- `bash scripts/check-cycle.sh 073` → ok: lane justificada (ambiguidade × raio × irreversibilidade).
- Matriz: 27 colunas no cabeçalho (2 fixas + 25 plataformas), 26 linhas de dados, 0 linhas com
  contagem de células diferente de 27 — medido por script, evidência no qa-report.
- Amostragem: células sorteadas conferem contra as fichas (caminho:linha) — a do consolidador e
  a do revisor independente.
- `bash scripts/check-conformance.sh 073` → verde; `--ticked-only` → verde (TAIL:gate é do
  regente: o "segue" para a rodada 2).
- `andamento.md` com as quatro linhas da rodada 1 em **entregue** e o histórico datado.
