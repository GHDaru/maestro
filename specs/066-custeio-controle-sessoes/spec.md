# Spec 066 — Custeio da operação e controle de sessões pelo portal

- **Status**: Draft · **Lane**: full · **Date**: 2026-10-02
- **Origin**: Desejo 003 do Gilsiley, redigido pela Hindiana Assistente (.maestro/docs/desejo-003-custeio-e-controle-de-sessoes.md). Depende das rodadas 001 (spec 064: workflow em SQLite) e 002 (spec 065: board e rodada navegável).

## What and why

O Maestro mede o fluxo (DORA, passos, evidências), mas não mede o custo. Cada resposta do modelo nos transcripts `.jsonl` traz `message.usage` com os 4 contadores de tokens. Sem isso, não dá para saber quanto custou cada sessão, rodada ou melhoria — e o cache lido domina o volume.

Além do custo, há metadados das sessões que o painel não enxerga: tempo em cada estado, erros de ferramenta, negativas do classificador, padrão de despacho, compactações e desvios do método. Tudo derivável só de metadados, sem o texto das mensagens.

Finalmente, o Gilsiley quer subir e derrubar sessões do Claude Code pelo portal, com gates de confirmação. Sessões do Claude Desktop ficam só em leitura.

## Functional requirements

### Custeio

- **FR1**: O SISTEMA DEVE ler os transcripts das pastas configuradas e gravar o consumo por sessão, modelo e hora, sem armazenar o conteúdo das mensagens. O SISTEMA NÃO DEVE gravar o texto de comandos Bash nem o input ou output de ferramenta — só a classificação do desvio (ex.: "commit sem runner2", "push tentado") e o hash ou nome do arquivo.
- **FR2**: O SISTEMA DEVE contar cada `message.id` uma única vez (deduplicação pelo streaming).
- **FR3**: ONDE o preço de um modelo não estiver configurado, O SISTEMA DEVE exibir "preço não configurado" no lugar do valor, e não inventar.
- **FR4**: O SISTEMA DEVE exibir o custo por sessão, por papel, por rodada e por tarefa integrada.
- **FR5**: QUANDO uma rodada for fechada, O SISTEMA DEVE incluir o custo da rodada no relatório.
- **FR6**: SE a soma mensal divergir da fatura informada pelo Gilsiley (valor + mês, no mesmo arquivo de preço) em mais de 5%, ENTÃO O SISTEMA DEVE gerar um alerta. Nenhum worker digita fatura.
- **FR7**: O SISTEMA DEVE manter a tabela de preço por modelo e por tipo de token em `projetos/<projeto>.json`, com data de vigência, preenchida pelo Gilsiley.

### Metadados de sessão

- **FR8**: O SISTEMA DEVE exibir, por sessão, o tempo trabalhando, esperando permissão, esperando outra sessão e ocioso.
- **FR9**: O SISTEMA DEVE contar erros de ferramenta por ferramenta e os retrabalhos do mesmo arquivo.
- **FR10**: O SISTEMA DEVE registrar negativas do classificador e prompts de permissão (onde a sessão parou à espera do humano).
- **FR11**: O SISTEMA DEVE medir o padrão de despacho: quem manda mensagem para quem, com que frequência e quanto tempo até a resposta.
- **FR12**: O SISTEMA DEVE registrar compactações e o contexto médio por resposta.
- **FR13**: O SISTEMA DEVE contar subagentes por tipo e o custo deles.
- **FR14**: O SISTEMA DEVE detectar desvios do método (commit sem runner2, push tentado por worker, APPROVE sem hash) a partir dos comandos Bash registrados, gravando SÓ a classificação do desvio e o hash ou nome do arquivo — nunca o texto do comando, nem o input ou output de ferramenta, para que tokens ou senhas no comando não vazem para nenhuma tabela.

### Controle de sessões

- **FR15**: QUANDO o usuário pedir para subir uma sessão de um papel, O SISTEMA DEVE pedir confirmação na tela, chamar o lançador com o `session_id` do mapa e registrar o evento.
- **FR16**: QUANDO o usuário pedir para derrubar uma sessão, O SISTEMA DEVE sempre pedir confirmação na tela. SE a sessão tiver passo de workflow aberto, ENTÃO O SISTEMA DEVE mostrar os passos abertos e exigir confirmação dupla. O SISTEMA DEVE mostrar o PID e a linha de comando antes de confirmar, encerrar SÓ o processo cujo `session_id` case EXATAMENTE com o do mapa, nunca encerrar mais de um processo por ação, nunca encerrar a sessão que fez o pedido, e nunca encerrar Office ou Assistente sem confirmação dupla.
- **FR17**: O SISTEMA NÃO DEVE oferecer subir ou derrubar sessões do Claude Desktop.
- **FR18**: O SISTEMA DEVE avisar a Office de toda ação de subir ou derrubar.
- **FR19**: O SISTEMA DEVE registrar no histórico quem, quando, qual sessão e por quê subiu ou derrubou.

### Dashboard

- **FR20**: O SISTEMA DEVE exibir três big numbers: custo do dia, custo da rodada atual e custo por tarefa integrada.
- **FR21**: O SISTEMA DEVE exibir uma série diária por papel (Office, Assistente, gerentes, workers) e uma lista "sessões mais caras" com contexto médio por resposta.

## Out of scope

- Estimativa de preço por worker (o preço é configuração do Gilsiley a partir da fatura).
- Edição de sessões do Claude Desktop (só leitura).
- Notificações push (fila outbox da 064 já existe).
- Deploy do painel (instalação pela Assistente após APPROVE).

## Acceptance criteria (DoD)

- WHEN o ingest lê os transcripts THEN THE SYSTEM SHALL gravar consumo por sessão, modelo e hora, sem conteúdo de mensagens.
- WHEN um `message.id` aparece 2x THEN THE SYSTEM SHALL contar uma única vez.
- WHERE preço não configurado THEN THE SYSTEM SHALL exibir "preço não configurado".
- WHEN rodada fechada THEN THE SYSTEM SHALL incluir custo no relatório.
- WHEN soma mensal divergir > 5% da fatura THEN THE SYSTEM SHALL gerar alerta.
- WHEN usuário pede para subir sessão THEN THE SYSTEM SHALL pedir confirmação, chamar lançador e registrar evento.
- WHEN usuário pede para derrubar sessão THEN THE SYSTEM SHALL sempre pedir confirmação na tela.
- WHEN usuário pede para derrubar sessão com passo aberto THEN THE SYSTEM SHALL mostrar passos abertos e exigir confirmação dupla.
- WHEN dois processos claude.exe têm session_id parecido THEN THE SYSTEM SHALL encerrar SÓ o de session_id exato.
- WHEN sessão é Claude Desktop THEN THE SYSTEM SHALL não oferecer subir/derrubar.
- `python -m pytest tests/test_consumo.py` → todos passam.
- `python -m pytest tests/test_controle_sessoes.py` → todos passam.
- `python -m pytest tests/test_contrato_rotas_066.py` → todos passam.
- `python -m pytest tests/test_seguranca_derrubar.py` → todos passam (inclui teste com dois processos parecidos: só o de `session_id` exato é encerrado).
- `python -m pytest tests/test_dados_sensiveis.py` → todos passam (um transcript com uma string de token não deixa essa string em nenhuma tabela).

## Clarify

1. O ingest dos transcripts roda no hook Stop da 064 (assíncrono via fila outbox) ou num cron? → no hook Stop, assíncrono, como as outras tabelas derivadas. O transcript de cada sessão está em `~/.claude/projects/<pasta>/<session-id>.jsonl`.
2. A tabela de preço lê `projetos/<projeto>.json` em que momento? → no ingest, lê o arquivo de preço vigente na data do consumo. Se não houver, marca "preço não configurado".
3. O lançador `multi-session.py` já existe — o portal só o chama? → sim, o portal chama o script existente com `--name` ou `--resume`. O portal não re-implementa o lançador.
4. Derrubar sessão: o portal mata o processo `claude.exe` pelo `session_id` na linha de comando? → sim, após aviso para commit/relatório. O `session_id` vem do mapa `contatos`/`sessoes.json`.
5. Os 4 contadores de tokens são `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`? → sim, todos de `message.usage`.

<!--
  GATE (DoR — not delegable): this spec only becomes a plan after human approval.
  Handoff: spec-agent → (approval) → plan-architect.
-->
