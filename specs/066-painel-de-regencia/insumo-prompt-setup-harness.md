# Insumo — prompt de configuração do harness (anotado em 22/10/2026, a pedido do Darú)

Prompt recebido, transcrito sem edição:

```text
Rebuild my Claude Code setup around this tree:
1. Run the main session on Opus 5.5 with ultracode on.
2. In every workflow, run read-only scan stages on Haiku 5.5 and edit stages on Sonnet 5.5, each edit in its own isolated copy.
3. Add one rule to CLAUDE.md: every finding gets an independent verifier agent before it's reported, and fix loops stop after two rounds with no progress.
4. Route fast deterministic forks (tool choice, path selection, retries) through JEV.
Show me every change as a diff first. No edits until I say go."
```

## Leitura pelo Maestro (o que já existe, o que mudaria)

| Item do prompt | No Maestro hoje | Mudaria? |
|---|---|---|
| 1. Sessão principal em Opus, ultracode ligado | O método não fixa modelo; a decisão 066 põe o Gerente em glm-5.3 e os Workers em deepseek via gateway, e o lançador recebe `--gerente-model` / `--worker-model`. Ultracode é orquestração multiagente por opt-in explícito. | Não no método. Só a escolha de modelo no lançador, que já é parâmetro. Princípio V pede a menor autonomia que resolve: fluxo fixo antes de agente autônomo. |
| 2. Varredura só leitura em Haiku, edição em Sonnet, cada edição em cópia isolada | `review` e `security` já são agentes só leitura em contexto fresco; cada Worker já tem worktree própria (decisão 066, parecer de segurança). `scripts/check-roles.sh` já confere papel × agente. | Pouco: uma linha no perfil de papéis dizendo que papéis só leitura podem rodar em modelo mais barato. Não é princípio, é perfil. |
| 3a. Todo achado passa por verificador independente antes de ser reportado | Princípio II (quem executa não verifica) e `TAIL:review`. | Nada: já é constituição. |
| 3b. Laços de correção param após duas rodadas sem progresso | **Não existe.** O método não tem regra de parada para o laço corrigir → rodar portão → corrigir. Evidência de que falta: as evidências de cauda do 066 ao 069 custaram uma rodada cada pelo mesmo motivo (`is_placeholder`), e o archify traz "limite de reparo por diagnóstico" como contrato. | **Sim.** Candidata a regra no operating-model § 12 e a item 24 do `anti-patterns`: após duas rodadas sem mudar o diagnóstico, parar e reportar a lacuna em vez de insistir. Passa pelo YAGNI porque há evidência própria. |
| 4. Decisões determinísticas (escolha de ferramenta, caminho, retries) fora do modelo, via "JEV" | Pesquisado em 22/10: **Jev** é o modelo de decisão da TypeSafe AI (acesso antecipado em 15/09/2026; versão 1.14 em 14/10/2026; no OpenRouter como `typesafe/jev-1.14`). Não gera texto: recebe um `state` e perguntas tipadas e devolve **só a distribuição de probabilidade** sobre as opções declaradas (Choice, Score, Noul para sim/não, Box para imagem), com um valor de confiança que mede a concentração da distribuição, não o acerto. A própria documentação diz que **não** serve para regra determinística (regex ou consulta resolvem melhor), nem para chamada de ferramenta, nem para planejamento em vários passos. A postura do Maestro para o determinístico já é script, hook e fitness function (Princípio V). | O item do prompt aplica Jev ao lugar errado. Onde ele cabe no método é em **julgamento com incerteza explícita**: a classe de risco de uma mudança (Score sobre reversibilidade × raio de impacto, Princípio III), a raia (Choice leve/plena/infra), "este achado merece verificador?" (Noul), e a saúde dos evals (`/eval`, ADR 0016, teorema T7). Com piso de confiança: abaixo dele, cai no gate humano. A política allow/deny/ask continua declarativa e fora do modelo. É API externa paga (dado sai da máquina): mesma ressalva do gateway. Só entra com evidência (YAGNI), como piloto do 072, não como regra. |
| Mostrar cada mudança como diff antes; nada editado sem "go" | Princípio III: gate humano proporcional à irreversibilidade; alterar `CLAUDE.md` e `settings` é mudança de configuração com aprovação. | Nada: compatível. |

## Veredito curto

O prompt é sobre o **harness** (como o Claude Code é configurado); o Maestro é sobre o **método**. Dos cinco pontos, quatro já estão cobertos ou são parâmetro do lançador. O que acrescentaria regra ao método é a **parada do laço de correção após duas rodadas sem progresso** (3b). O Jev (item 4) não substitui o determinístico, que fica em script; cabe como **piloto de julgamento calibrado** (classe de risco, raia, "merece verificador?") com piso de confiança que devolve ao humano — a avaliar no 072 com evidência, não antes.

Fontes consultadas em 22/10/2026: [OpenRouter — What is Jev?](https://openrouter.ai/blog/insights/what-is-jev/) · [OpenRouter — Jev vs LLM-as-a-Judge](https://openrouter.ai/blog/tutorials/jev-vs-llm-as-a-judge/) · [arXiv 2609.30216 — Jev in the Wild](https://arxiv.org/pdf/2609.30216) · [AWS Builder — Jev as an LLM router](https://builder.aws.com/content/3JoJL1whRdHoUerKMxjg23g2rNe/jev-as-an-llm-router-fast-typed-decisions-for-model-selection) · [Towards Data Science — Jev vs LLMs](https://towardsdatascience.com/jev-vs-llms-when-ai-moves-from-generation-to-decision-making/). Boa parte é texto de fornecedor ou adjacente; as alegações de calibração e custo não foram verificadas por nós.
