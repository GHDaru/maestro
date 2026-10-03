# Spec 066 — Medição de tokens e controle de sessões pelo portal

- **Status**: Approved (GATE Gilsiley 02/10, ajuste 03/10: tokens em vez de R$) · **Lane**: full · **Date**: 2026-10-02
- **Origin**: Desejo 003 do Gilsiley, redigido pela Hindiana Assistente (.maestro/docs/desejo-003-custeio-e-controle-de-sessoes.md). Depende das rodadas 001 (spec 064: workflow em SQLite) e 002 (spec 065: board e rodada navegável). Ajuste 03/10: Gilsiley decidiu "Não precisa trazer custo, total de tokens é suficiente" — escopo reduzido, sem novo gate.

## What and why

O Maestro mede o fluxo (DORA, passos, evidências), mas não mede o consumo de tokens. Cada resposta do modelo nos transcripts `.jsonl` traz `message.usage` com os 4 contadores de tokens. Sem isso, não dá para saber quanto consumiu cada sessão, rodada ou melhoria — e o cache lido domina o volume.

Além dos tokens, há metadados das sessões que o painel não enxerga: tempo em cada estado, erros de ferramenta, negativas do classificador, padrão de despacho, compactações e desvios do método. Tudo derivável só de metadados, sem o texto das mensagens.

Finalmente, o Gilsiley quer subir e derrubar sessões do Claude Code pelo portal, com gates de confirmação. Sessões do Claude Desktop ficam só em leitura.

## Functional requirements

### Medição de tokens

- **FR1**: O SISTEMA DEVE ler os transcripts das pastas configuradas e gravar o consumo de tokens por sessão, modelo e hora, sem armazenar o conteúdo das mensagens. O SISTEMA NÃO DEVE gravar o texto de comandos Bash nem o input ou output de ferramenta — só a classificação do desvio (ex.: "commit sem runner2", "push tentado") e o hash ou nome do arquivo. O ingest DEVE ser incremental: guarda o arquivo + offset de cada `.jsonl` e lê só o que é novo a cada Stop, nunca relê o arquivo inteiro.
- **FR2**: O SISTEMA DEVE contar cada `message.id` uma única vez (deduplicação pelo streaming).
- **FR4**: O SISTEMA DEVE exibir os tokens (input, output, cache lido, cache escrito e total) por sessão, por papel, por rodada e por tarefa integrada.
- **FR5**: QUANDO uma rodada for fechada, O SISTEMA DEVE incluir os tokens da rodada no relatório.

### Metadados de sessão

- **FR8**: O SISTEMA DEVE exibir, por sessão, o tempo trabalhando, esperando permissão, esperando outra sessão e ocioso.
- **FR9**: O SISTEMA DEVE contar erros de ferramenta por ferramenta e os retrabalhos do mesmo arquivo.
- **FR10**: O SISTEMA DEVE registrar negativas do classificador e prompts de permissão (onde a sessão parou à espera do humano).
- **FR11**: O SISTEMA DEVE medir o padrão de despacho: quem manda mensagem para quem, com que frequência e quanto tempo até a resposta.
- **FR12**: O SISTEMA DEVE registrar compactações e o contexto médio por resposta.
- **FR13**: O SISTEMA DEVE contar subagentes por tipo e os tokens deles.
- **FR14**: O SISTEMA DEVE detectar desvios do método (commit sem runner2, push tentado por worker, APPROVE sem hash) a partir dos comandos Bash registrados, gravando SÓ a classificação do desvio e o hash ou nome do arquivo — nunca o texto do comando, nem o input ou output de ferramenta, para que tokens ou senhas no comando não vazem para nenhuma tabela.

### Controle de sessões

- **FR15**: QUANDO o usuário pedir para subir uma sessão de um papel, O SISTEMA DEVE pedir confirmação na tela, chamar o lançador (caminho configurado em `projetos/<projeto>.json`) com o `session_id` do mapa e registrar o evento. O lançador DEVE gravar o PID (e o `session_id` quando surgir) no lançamento; sem esse registro, o portal não oferece derrubar.
- **FR16**: QUANDO o usuário pedir para derrubar uma sessão, O SISTEMA DEVE sempre pedir confirmação na tela. SE a sessão tiver passo de workflow aberto, ENTÃO O SISTEMA DEVE mostrar os passos abertos e exigir confirmação dupla. O SISTEMA DEVE mostrar o PID e a linha de comando antes de confirmar, encerrar SÓ o processo cujo `session_id` case EXATAMENTE com o do registro de lançamento, nunca encerrar mais de um processo por ação, e nunca encerrar a sessão que fez o pedido.
- **FR17**: O SISTEMA NÃO DEVE oferecer subir ou derrubar sessões do Claude Desktop (Office, Assistente e demais sessões Desktop ficam só em leitura e não aparecem para derrubar).
- **FR18**: O SISTEMA DEVE avisar a Office de toda ação de subir ou derrubar.
- **FR19**: O SISTEMA DEVE registrar no histórico quem, quando, qual sessão e por quê subiu ou derrubou.

### Dashboard

- **FR20**: O SISTEMA DEVE exibir três big numbers: tokens do dia, tokens da rodada atual e tokens por tarefa integrada.
- **FR21**: O SISTEMA DEVE exibir uma série diária por papel (Office, Assistente, gerentes, workers) e uma lista "sessões com mais tokens" com contexto médio por resposta.

## Out of scope

- Custo em R$ e tabela de preço (Gilsiley 03/10: "Não precisa trazer custo, total de tokens é suficiente").
- Conferência com fatura.
- Estimativa de preço por worker.
- Edição de sessões do Claude Desktop (só leitura).
- Notificações push (fila outbox da 064 já existe).
- Deploy do painel (instalação pela Assistente após APPROVE).

## Acceptance criteria (DoD)

- WHEN o ingest lê os transcripts THEN THE SYSTEM SHALL gravar tokens (input, output, cache lido, cache escrito, total) por sessão, modelo e hora, sem conteúdo de mensagens.
- WHEN um `message.id` aparece 2x THEN THE SYSTEM SHALL contar uma única vez.
- WHEN rodada fechada THEN THE SYSTEM SHALL incluir tokens no relatório.
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
2. O lançador `multi-session.py` já existe — o portal só o chama? → sim, o portal chama o script existente com `--name` ou `--resume`. O portal não re-implementa o lançador.
4. Derrubar sessão: o portal mata o processo `claude.exe` pelo `session_id` na linha de comando? → sim, após aviso para commit/relatório. O `session_id` vem do mapa `contatos`/`sessoes.json`.
5. Os 4 contadores de tokens são `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`? → sim, todos de `message.usage`.
6. FR8 "esperando permissão": o `.jsonl` registra o prompt de permissão? → provar com transcript real no clarify. Se não registrar, o FR muda de fonte (hook) ou sai. Nada na tela sem fonte.
7. Sessão aberta com `--name` não leva `session_id` na linha de comando. Como derrubar? → o lançador grava o PID (e o `session_id` quando surgir) no lançamento. O FR16 usa esse registro. Sem registro, o portal não oferece derrubar.
8. O caminho do `multi-session.py` é fixo? → não, vira configuração em `projetos/<projeto>.json`.

<!--
  GATE (DoR — not delegable): this spec only becomes a plan after human approval.
  Handoff: spec-agent → (approval) → plan-architect.
-->
