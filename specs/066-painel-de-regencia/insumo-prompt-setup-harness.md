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
| 4. Decisões determinísticas (escolha de ferramenta, caminho, retries) fora do modelo, via "JEV" | A postura já é esta: o que é determinístico vai para script, hook e fitness function, não para o modelo (Princípio V; `scripts/hooks/`). **"JEV" não está expandido em lugar nenhum** — viola o Princípio VIII e, sem saber o que é, não dá para avaliar a ferramenta. | Depende do que JEV é. A direção (determinismo fora do modelo) já é do método. |
| Mostrar cada mudança como diff antes; nada editado sem "go" | Princípio III: gate humano proporcional à irreversibilidade; alterar `CLAUDE.md` e `settings` é mudança de configuração com aprovação. | Nada: compatível. |

## Veredito curto

O prompt é sobre o **harness** (como o Claude Code é configurado); o Maestro é sobre o **método**. Dos cinco pontos, quatro já estão cobertos ou são parâmetro do lançador. O único que acrescentaria regra ao método é a **parada do laço de correção após duas rodadas sem progresso** (3b). "JEV" precisa ser expandido antes de qualquer decisão sobre o item 4.
