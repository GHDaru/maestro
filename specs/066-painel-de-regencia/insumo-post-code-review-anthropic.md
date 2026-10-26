# Insumo — "How the Claude Code team does code review" (anotado em 26/10/2026, a pedido do Darú)

- **Fonte**: [claude.dev/blog/solving-code-review-at-anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/), 15/10/2026, Addy Osmani, Morgan Westlee Lunt e Qing Wang. Números são dados internos da equipe, sem comparação controlada.
- **Para quê**: avaliar a metodologia do Maestro contra uma prática de revisão em escala (cerca de 30 mil mudanças por dia no monorepo; Claude escreve cerca de 90 % do código do Claude Code).

Siglas: PR (*pull request*, pedido de integração) · CI (*Continuous Integration*, integração contínua) · DoD (*Definition of Done*, definição de pronto) · ADR (*Architecture Decision Record*, registro de decisão de arquitetura).

## O que o post descreve

1. **Verificação antes do PR**: o agente roda testes, build, lint ou comparação de capturas e mostra a saída em vez de afirmar; um subagente revisa o diff em contexto fresco; skills de caça a defeitos, simplificação e checagem ponta a ponta.
2. **Arquivos de instrução**: `CLAUDE.md` com convenções; `REVIEW.md` escrito pelos donos do código dizendo o que é falha em cada parte do repositório, limitando nits, listando caminhos a pular e exigindo evidência arquivo e linha.
3. **Revisão por IA em todo PR**, com três profundidades; passagem de segurança separada; achado aberto bloqueia o merge.
4. **Vários agentes caçam defeitos em paralelo e um grupo separado de verificadores vota em cada achado**; só o achado com acordo suficiente é publicado. É o principal controle de falso positivo.
5. **Severidade e filtro**: estilo, diagnóstico e limpeza são descartados; o que sobra vira comentário Important, Nit ou Pre-existing; filtros testados por A/B.
6. **Convergência**: teto de três rodadas, re-revisão só do diff depois das primeiras passagens, apontar a classe do defeito e não cada instância, sem achado repetido. Resultado interno: PR aprovado em uma rodada de 65 % para 78 %; cinco ou mais rodadas de 8,9 % para 1,5 %; média de 2,08 para 1,32 revisões.
7. **Ruído medido**: comentários classificados pela resposta do autor (corrigido, errado, intencional, irrelevante); o revisor roda em PRs sabidamente limpos para medir alarme falso.
8. **Aprovação por classe de risco**: um classificador define o nível pela mudança, não pelo autor; nenhuma, uma ou duas pessoas; aprovação de agente nunca conta como humana; aprovação vale para um commit e cai com commit novo.
9. **Fila de merge, feature flags, lançamento por estágios, rollback rápido**; cada incidente vira caso de eval do revisor, pontuado diariamente.
10. **Papel humano**: decidir o que construir, revisar áreas de risco (cobrança, atualizador, CI, prompts de sistema) e arquitetura que vira padrão, ler a evidência, responder pelo resultado.
11. **Lacuna declarada**: ainda não há disjuntor que aperte a aprovação quando revert ou incidentes sobem.

## Leitura pelo Maestro (o que já temos, o que falta)

| Prática do post | No Maestro hoje | Veredito |
|---|---|---|
| Verificação antes do PR, saída mostrada | Princípio IV ("prove, don't claim"), `/dod`, fitness functions, qa-report com saída colada | Já é constituição. |
| Revisão em contexto fresco por quem não executou | Princípio II, `TAIL:review`, agentes `review` e `security` | Já é constituição. |
| `REVIEW.md` por dono de código (o que é falha, caminhos a pular, evidência arquivo e linha) | Não existe; o que há são `anti-patterns` e as fitness functions do ux-design, por ciclo | **Falta**: um `REVIEW.md` por domínio (`painel/`, `scripts/`, `docs/governance/`) dizendo o que é falha ali. Raia leve. |
| Vários caçadores em paralelo e verificadores que votam | Um revisor e um crítico por gate; a rodada 4 do 073 terá três juízes com nota mínima 9 | **Parcial**: adotar a votação de verificadores na cauda dos ciclos com código (dois caçadores, um verificador que confirma com arquivo e linha) quando a mudança for de classe média ou alta. |
| Teto de rodadas e convergência | Regra das duas rodadas sem mudança de diagnóstico (adotada em 24/10, ADR pendente); no 072 o Gerente parou laços quando o diagnóstico não mudava | **Parcial**: falta medir: rodadas por ciclo até o gate, achados corrigidos versus repetidos. Entra no painel de regência como métrica com fonte. |
| Ruído medido (achado classificado pela resposta do autor; revisor em PR limpo) | Não medimos ruído; só registramos achados e dívidas | **Falta**: classificar cada achado da cauda como corrigido, errado, intencional ou irrelevante no qa-report, e rodar o revisor num ciclo sabidamente limpo uma vez por retro. |
| Classe de risco pela mudança, aprovação de agente nunca conta como humana, aprovação cai com commit novo | Princípio III (reversibilidade × raio de impacto), ADR 0026 (gate por delegação com crítico), `TAIL:gate` | **Já temos** a classe de risco e a delegação escrita; **falta** amarrar a aprovação a um hash: o cabeçalho conferível do ADR 0024 faz isso e ainda não foi implementado (ciclo 072 rodada 2). |
| Cada incidente vira caso de eval | `evals/`, `/eval`, retro → regra versionada (Princípio VII) | Já existe o mecanismo; **falta** alimentá-lo com os achados do 070 e do 072 como casos. |
| Fila de merge, feature flags, rollback | `promote-main.sh` com conformance completa; `dev` → `main`; rollback por revert | Proporcional ao tamanho; sem flags, por YAGNI. |
| Disjuntor por revert e incidentes | Não temos; `check-retro.sh` mede dívida de achados, não reverts | Lacuna compartilhada com o post; candidata ao painel de regência (DORA já conta reverts). |

## Três coisas a levar para o método (propostas, não decididas)

1. **`REVIEW.md` por domínio** com "o que é falha aqui", caminhos a pular e exigência de arquivo e linha, lido pelos agentes `review` e `security`. Raia leve, um ciclo.
2. **Cauda com votação**: para mudança de classe média ou alta, dois caçadores em paralelo e um verificador que confirma cada achado antes de ele entrar no qa-report; achado sem confirmação vira "não confirmado", não some.
3. **Ruído e convergência como métricas do painel**: achados por resposta do autor, rodadas até o gate, e o cabeçalho conferível (ADR 0024) amarrando aprovação a hash.

O que não levar: três profundidades de revisão por repositório e fila de merge são escala que o Maestro não tem; entram se um dia o volume pedir (YAGNI).
