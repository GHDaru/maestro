# Tasks 057 — O agente é escolha declarada

## Verification first
- [x] T0 — ler o modelo do upstream no que está vendorizado (`init-options.json`,
      `update-agent-context.sh`) e extrair os arquivos de instrução **do disco**, não de memória.

## Implementation
- [x] T1 — `scripts/install-agents.tsv`: a tabela, com `-` onde o formato não foi verificado.
- [x] T2 — `data-model.md`: agente e escolha gravada, com o que o portão exige de cada campo.
- [x] T3 — `--ai <id>` e `--ai list`; id inválido recusa listando os válidos.
- [x] T4 — comandos e bloco nos caminhos do agente; nada instalado onde a célula é `-`.
- [x] T5 — harness só quando a tabela permite; resumo diz o motivo quando não.
- [x] T6 — `.maestro/install-options.json` com a escolha.
- [x] T7 — `--write-block`: acrescenta se não houver, recusa se houver outro.
- [x] T8 — `check-install.sh`: bloco instalado × bloco gerado (FR7).
- [x] T9 — `docs/receitas/instalar-o-maestro.md` explica o modelo, com a tabela.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)

## Após o parecer — 16 achados
- [x] T10 — o guarda de symlink do ciclo 052, que o `--write-block` e o arquivo de opções não
      tinham: os dois escreviam **fora** do alvo através de um link.
- [x] T11 — extração do bloco reescrita (era um `sed` de faixa que nunca terminava): a
      comparação "já está atual" era inalcançável e o portão reprovava a própria saída do
      instalador.
- [x] T12 — `check-install.sh` passa a ler o agente do `install-options.json`: instalação
      correta de Copilot/Cursor ficava vermelha para sempre, e as camadas exigiam
      `.claude/agents` de quem não o lê.
- [x] T13 — CRLF na tabela deixou de desligar a camada inteira; `.claude/agents` deixou de ir
      para todo agente; `init-options.json` passa a levar o agente escolhido.
- [x] T14 — estado do harness diz o **motivo** certo, e declara quando a camada continua
      **viva** de uma instalação anterior; o campo `harness` grava o fato.
- [x] T15 — `copy_as` com subdiretório deixou de matar a instalação sem manifesto.
- [x] T16 — a tabela e o ciclo ganharam **teste**: validação de linhas, `--ai list`, recusa de
      id inválido, instalação não-Claude sem formato do Claude, opções gravadas e
      `--write-block` idempotente.
