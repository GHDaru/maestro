# Proposta consolidada: painel de controle do Maestro

Consolidação: Hindiana Assistente, 01/10/2026, a partir do painel de especialistas (W01, W04, W06, W07, W11; crítico às cegas W08 e, depois do desvio do par 01, um crítico independente com visão). Decisão: Gilsiley.

## 1. O problema

O controle de um projeto feito por uma equipe de agentes de IA está espalhado. Decisões, retro, barra, quadro, relatório da manhã, página de progresso e mensagens entre sessões vivem em lugares diferentes. Toda rodada reescreve o controle à mão. O "Estado atual" de cada sessão é digitado pelo próprio agente e desatualiza.

O Maestro hoje recusa um painel de métricas: em `operating-model.md` §6 ele aparece como "Later / YAGNI", e o handbook 02 diz que DORA é "bússola, não painel". O YAGNI valia sem escala. Hoje são 16 sessões, 160 worktrees, 52 desvios registrados em três dias e decisões por hora. O custo de coordenação é medido, e o desvio mais caro (teste verde que não passa pelo caminho real) nasce justamente de controle disperso.

## 2. Princípios do desenho (não se discutem)

1. **Os arquivos são a fonte de verdade; o SQLite é uma projeção.** É um read-model CQRS (W04), reconstruível a qualquer momento (ADR 0008). Apagar o `.db` e reingerir não perde nada, exceto os eventos.
2. **Só entra direto no SQLite o que não existe em arquivo nenhum:** status de sessão, sinal de vida, transição de peça com evidência, deploy, incidente e recuperação. Esses registros vão para a tabela `eventos`, que só aceita inclusão: os triggers recusam UPDATE e DELETE.
3. **Sem prova, a peça não muda de coluna (W06).** Cada estado exige uma evidência, e o registro é recusado se faltar:
   - entregue: hash;
   - suítes aceitas: hash + runner2;
   - aprovada às cegas: hash + par montado por + descrição factual;
   - integrada: hash + merge;
   - em produção: hash + deploy.
4. **O gate é humano (Princípio II).** O app nunca promove nada sozinho; quem promove registra o próprio nome em `autor`.
5. **Merge não é deploy (W07, Office).** A frequência de deploy só conta deploy registrado. O merge na linha principal aparece apenas como proxy rotulado.
6. **Segurança da ingestão (W06):**
   - nunca abrir `.env` nem o conteúdo de `backups_producao`;
   - nunca escrever nos arquivos do projeto;
   - nada de host, IP, usuário ou token no SQLite.

   Há um teste para cada regra.
7. **Leveza:** Python stdlib (`sqlite3`, `http.server`, `subprocess git`) e um único `index.html` com JS puro. Sem build, sem dependência, só localhost.

## 3. O que foi construído (branch `painel-controle` do Maestro, `maestro/painel/`)

| Peça | O que mostra | Fonte |
|---|---|---|
| Board de agentes (tela inicial, W01) | Cada sessão em trabalhando, esperando, bloqueado, sem tarefa ou sem registro; o que faz; idade do último sinal; alerta de sem sinal | `eventos` tipo status + "Estado atual" de `equipe/*.md` |
| Fluxo de peças | Spec → red → entregue → suítes aceitas → aprovada às cegas → integrada → em produção, com selos de evidência | `eventos` tipo peça |
| Roadmap e specs | Specs por repositório: status, tasks feitas/total, plan, qa-report (falta destacada) | `specs/NNN-*`, `roteiro-ciclos.md` |
| Decisões e ADRs | Id, quando, decisão, contexto, como desfazer | `decisoes-*.md`, `adr/` |
| DORA | As 4 métricas com a fonte escrita ao lado; "—" com instrução quando falta registro | git (first-parent), `eventos`, `barra/execucoes` |
| Barra, defeitos e desvios | Voltas da barra; defeitos por volta; 52 desvios em 8 classes | `barra/execucoes`, `barra-v2-resultado.md`, `retro-anotacoes.md` |
| Tempo por fase | Horas por fase do método; fases abertas | `tempos/ponto.jsonl` (`ponto.py` do W04) |
| Higiene do git | Worktrees integradas, limpas e protegidas; branch com upstream na produção; lista de remoção para aprovação | `git worktree list`, `for-each-ref`, `branch --merged` |
| Relatório de lote (W11) | Material da retro: barra, DORA, desvios por classe, candidatos ao método, higiene, documentos parados, 3 perguntas | todas as acima |
| Documentos do projeto | Documentos por papel (constituição, linguagem, jornadas, plano, decisões, controle, barra, papéis, infraestrutura), com idade; parado > 7 d marcado | config `documentos` |
| Linguagem ubíqua | Termo, definição, evitar | `03-ddd.md` §A5 |
| Estado para a IA (W04) | `GET /api/estado-ia?sessao=W04`: o "activeContext" derivado da sessão (estado, peça, hash, próximo passo, desvios dela, riscos de git, decisões recentes, DORA) | todas as acima |

Comandos:

```
python painel/server.py painel/projetos/hindiana.json          # http://127.0.0.1:8765
python painel/ingest.py painel/projetos/hindiana.json          # reconstrói o cache
python painel/registrar.py painel/projetos/hindiana.json status --sessao W04 --estado trabalhando --texto "..." --autor Assistente
python painel/registrar.py painel/projetos/hindiana.json peca --peca P6 --estado "suites aceitas" --evidencia '{"hash":"...","runner2":"..."}' --autor Office
python painel/registrar.py painel/projetos/hindiana.json deploy --estado SUCCESS --evidencia '{"hash":"..."}' --texto "railway" --autor Office
python -m unittest discover -s painel/tests                    # 11 testes
```

Um projeto novo entra com um arquivo `projetos/<nome>.json`. O hindiana é o primeiro.

## 4. Os documentos que um projeto precisa manter em época de IA

Critério do W04: um documento é **obrigatório** se carrega uma decisão humana ou um registro que só cresce. É **derivado** se pode ser apagado e regenerado sem perder informação.

| Documento | Classe | Para quem | Existe no hindiana? |
|---|---|---|---|
| Constituição (princípios, proibições) | obrigatório | humano e IA | `principles.md` fora da pasta + `00-fundacao.md` §8–11 + `LEIA-PRIMEIRO.md` (três lugares: consolidar) |
| CLAUDE.md / AGENTS.md (ponteiro curto) | obrigatório | IA | sim (raiz e `ola/`) |
| Arquivo de papel por sessão (regras e autorizações) | obrigatório | IA | `equipe/*.md`; o "Estado atual" deve virar derivado |
| Linguagem ubíqua (termo, definição, evitar) | obrigatório | humano e IA | `03-ddd.md` §A5, parado desde 22/09 |
| Objetos semânticos (agregados, invariantes, eventos) | obrigatório | humano e IA | `03-ddd.md` parte B + `modulos/*.md`, parados |
| Jornadas (passo a passo por papel, critério de erro) | obrigatório | humano, IA e barra | `barra-v2.md` E1–E8 (viva) |
| Spec EARS, plan, tasks, qa-report por peça | obrigatório | IA | `specs/`; 33 de 57 specs do hindiana sem qa-report |
| ADR e registro de decisões | obrigatório, só cresce | humano | `adr/` (5) e `decisoes-*.md` |
| Registro de desvios (retro) | obrigatório, só cresce | humano | `retro-anotacoes.md` |
| Execuções da barra | obrigatório, só cresce | humano e IA | `barra/execucoes/` (local) |
| Ponto (início/fim de rodada e fase) | obrigatório, só cresce | humano | `ponto.py` pronto, **zero marcações** |
| Registro de deploy | obrigatório, só cresce | humano | **não existe**: entra em `eventos` tipo deploy |
| Infraestrutura (ambientes, regras, sem segredos) | obrigatório | humano e IA | espalhado na memória da Office; `infraestrutura.md` proposto |
| Roadmap | obrigatório (vivo) | humano | `roteiro-ciclos.md`, parado desde 22/09 |
| Estado atual da sessão (activeContext) | **derivado** | IA | hoje escrito à mão; vira `/api/estado-ia` |
| Board, DORA, rastreabilidade, relatório de lote | **derivado** | humano | o painel |

Documentos mortos (W11): 28 arquivos parados desde 21–22/09, entre eles `plano-mestre.md`, `roteiro-ciclos.md`, `pendencias-cruzadas.md` e `decisoes_abertas.md`. A tela de Documentos marca os parados há mais de 7 dias. Arquivar ou reviver é decisão do Gilsiley.

## 5. Especialistas, skills e tools que o método deve exigir (entregável pedido)

### Especialistas (papéis permanentes num projeto feito por agentes)

| Papel | Responsabilidade | Hoje no hindiana |
|---|---|---|
| Regente humano (Product Steward / Orchestrator) | decide gate, prioridade, produção | Gilsiley |
| Coordenador de entrega | plano de tarefas, execução, conversa com gerentes, barra de produto | Hindiana Office |
| Controlador do método e auditor | board, sinal de vida, auditoria do método, retro, higiene, métricas | Hindiana Assistente |
| Gerentes de frente | distribuir blocos, cobrar evidência | Gerente, Gerente02 |
| Arquiteto DDD/hexagonal | linguagem ubíqua, agregados, mapa de contextos, ACL | W04 (painel), W12 |
| Engenheiro de contexto para IA | constituição, CLAUDE.md, estado derivado, skills, MCP | W04 (painel) |
| Engenheiro de qualidade | TDD, contrato pelo caminho real, prova verificável | W06 (painel) |
| Engenheiro de plataforma/DevOps | ambientes, runner, deploy registrado, DORA | W07 (painel) |
| Crítico às cegas independente | par sem rótulos, descrição factual conferida, veredito binário | **precisa ver imagem** (ver §6) |
| Documentador técnico e facilitador de retro | documentos vivos, relatório de lote, cerimônia | W11 (painel) |
| Governança, segurança e risco | segredos, dados de produção, append-only, classificador | W06 (painel) |
| UX de painéis e jornadas | jornada por papel, tela inicial, 30 segundos | W01 (painel) |

### Skills (no formato do Maestro: `skills/<nome>/SKILL.md`)

| Skill | O que garante | Origem |
|---|---|---|
| `prova-verificavel` / `evidence-gate` | só muda de estado com prova parseável (hash, runner2, barra); recusa "✅" | W06, W07, W01 |
| `catalogo-provas-enganosas` como validador | qa-report com forma enganosa é bloqueado | W06 (o catálogo já existe) |
| `critica-as-cegas` | par montado por quem roda a barra; descrição factual conferida; **teste de visão do crítico** antes | W06, W11 e o desvio do par 01 |
| `dora-from-git` | as 4 métricas do git e do deploy registrado; merge ≠ deploy | W07, W11 |
| `sqlite-derive` / `append-only-audit` | projeção idempotente; eventos só crescem; reingestão idêntica | W07, W11 |
| `estado-atual-derivado` | "Estado atual" gerado e não digitado; a sessão chama `get_estado_atual` | W04 |
| `ingestao-segura` | lista de caminhos permitidos; canário de segredo | W06, W11 |
| `ears-scenario` + `text-wireframe` | spec EARS antes do código; wireframe em texto antes da UI | W01 |
| `higiene-git` | upstream ≠ main, worktree integrada removida, nunca amend após hash | Assistente (achado de 01/10) |

### Tools

| Tool | Estado |
|---|---|
| `painel/ingest.py`, `server.py`, `registrar.py` | **feito** (esta proposta) |
| `ponto.py`, `tempo_ativo.py`, `relatorio_tempo.py` | feito (W04); falta usar |
| `barra_v2.py` | feito (Office) |
| detector de desvios (12 padrões, W06) | parcial: upstream na produção e worktree com risco já detectados; faltam qa-report sem runner2, amend após hash e migração fora de P3/P4 |
| MCP `get_estado_atual(papel)` | próximo passo (W04); hoje é `GET /api/estado-ia?sessao=` |
| `rito-hash.sh` (bundle, clone limpo no runner2, suítes, relatório) | proposto (W01) |

## 6. Desvios de método encontrados nesta rodada (para a retro)

1. **Crítico sem visão (W08, par 01). Confirmado em teste controlado pela Office (W12, 01/10): 2 de 2.** O W08 chamou de "tema escuro" duas telas claras e não transcreveu texto. No teste da Office, o W12 inventou título, frase e contador de uma captura da banca. As sessões de worker não leem imagem.
   - **Regra para o Maestro:** a crítica de imagem exige prova de leitura antes de valer. São três textos literais por imagem, conferidos por quem montou o par.
   - **Na prática:** a crítica de imagem é feita só por um subagente de contexto novo no modelo da sessão principal. Os workers criticam código, texto e dados. Worker que recebe imagem responde "não consigo ler a imagem".
2. **Assistente: testes da v0 escritos depois do código.** Princípio IV. Registrado; a v1 incluiu o teste do detector junto com o detector. A partir da v2, teste vermelho antes.
3. **Dez branches com upstream em origin/main** (achado do painel, corrigido pela Office com `--unset-upstream`). A regra já estava na memória e não era verificada. Agora é detector.
4. **Ponto sem uso.** `ponto.py` está pronto desde 30/09 e tem zero marcações. A ordem do Gilsiley ainda não virou hábito; o painel mostra o vazio na tela de Tempo.

## 7. Decisões pedidas ao Gilsiley

1. **ADR que supera o YAGNI do painel** (rascunho em `painel/docs/adr-rascunho-painel.md`). Aprovar, mudar ou recusar.
2. **Onde o painel mora:** proposta é o diretório `painel/` do Maestro, no domínio toolkit do `boundary.json`, aplicado a cada projeto por `projetos/<nome>.json`.
3. **Status de sessão:** quem grava, o loop da Assistente a cada 30 min ou cada sessão ao mudar de estado? Recomendo as duas coisas: a sessão grava ao mudar e o loop cobra quem ficou sem sinal.
4. **Remoção de worktrees:** são 60 candidatas (integradas, limpas, fora da lista protegida), com a lista pronta na tela Higiene do git. Remover só com a sua ordem.
5. **Documentos parados:** arquivar os 28 mortos ou revivê-los (linguagem ubíqua e roadmap são obrigatórios e estão parados).
