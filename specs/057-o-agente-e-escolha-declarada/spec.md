# Spec 057 — O agente é escolha declarada, não suposição do instalador

- **Status**: Rascunho · **Raia**: infra · **Data**: 2026-08-17
- **Origem**: pedido do Steward — "veja como o spec-kit faz, temos que configurar conforme o
  modelo; precisamos da documentação que explica isto e do instalador que permite escolher".
  E, na mesma conversa, a condição que **dispara gatilhos registrados**: o método vai passar a
  reger **desenvolvimento de software**, não só o próprio repositório.

> **Raia**: infra, e infra nunca é leve. **Ambiguidade** média — o modelo do upstream foi
> medido, o conjunto de agentes a suportar não é dedutível. **Raio**: todo repositório que
> instala, e o ciclo 056 acabou de aumentá-lo (hooks mudam o comportamento de todos os agentes
> de lá). **Irreversibilidade**: média — escrever no arquivo de instrução de terceiro.

## O quê e por quê

**O modelo do upstream, medido antes de desenhar.** O spec-kit resolve isto com escolha
gravada em arquivo, não com prosa: `.specify/init-options.json` guarda `"ai": "claude"`,
`"script": "sh"`, `"ai_commands_dir"` e a versão; e `update-agent-context.sh` suporta **26
agentes** (contados no `case`; um deles, `generic`, **não tem arquivo de instrução**), cada um com o **seu arquivo de instrução** — `claude → CLAUDE.md`,
`copilot → .github/copilot-instructions.md`, `cursor-agent → .cursor/rules/specify-rules.mdc`,
e uma família inteira (`codex`, `amp`, `opencode`, `kiro-cli`, `bob`, `pi`) que compartilha
`AGENTS.md`. O que varia entre agentes é **onde a instrução mora**.

**O nosso instalador supõe um agente e não declara.** Ele copia `.claude/agents`,
`.claude/commands` e imprime um bloco de `CLAUDE.md`. Quem instalar com outro agente recebe
arquivos que aquele agente nunca vai ler, sem um aviso sequer.

**E o ciclo 056 piorou isso.** A camada de harness — `PreToolUse`, `SessionStart`,
`.claude/settings.json` — é mecanismo do Claude Code. Instalá-la para um agente que não a
executa é enviar arquivo inerte: anti-padrão 22 na direção contrária, e o instalador diria
"harness: installed" mentindo.

**Terceiro fato, achado ao instalar o Maestro nele mesmo (ciclo 056).** O bloco que o
instalador gera e o bloco que vive no arquivo de instrução podem **divergir em silêncio**.
Hoje nada compara os dois. É a mesma família do `check-version.sh`: um fato dito em dois
lugares, mantido igual por memória.

## Requisitos funcionais

- **FR1**: O SISTEMA DEVERÁ aceitar `--ai <id>` e gravar a escolha num arquivo de opções,
  ao lado do manifesto, nos moldes do `init-options.json` do upstream.
- **FR2**: Os agentes suportados DEVERÃO viver numa **tabela declarada** — id, nome, arquivo
  de instrução, diretório de comandos, suporta harness — e acrescentar um agente DEVERÁ ser
  **uma linha**, não um ramo de código.
- **FR3**: QUANDO `--ai` receber um id fora da tabela, O SISTEMA DEVERÁ **recusar** e listar
  os válidos. Entrada desconhecida é reprovação, nunca escolha silenciosa do padrão.
- **FR4**: O SISTEMA DEVERÁ instalar comandos e bloco de instrução **nos caminhos do agente
  escolhido**, e não nos do Claude por omissão.
- **FR5**: QUANDO o agente escolhido não suportar a camada de harness, O SISTEMA DEVERÁ
  **não instalá-la** e dizer no resumo **por que** — "hooks são mecanismo do Claude Code".
  Silêncio aqui é indistinguível de esquecimento.
- **FR6**: O SISTEMA DEVERÁ oferecer `--ai list`, imprimindo a tabela — quem escolhe precisa
  ver as opções sem ler o código.
- **FR7**: QUANDO o arquivo de instrução do agente já contiver um bloco do Maestro, o portão
  DEVERÁ comparar o bloco **instalado** com o que o instalador **gera hoje** e reprovar a
  divergência. Um fato dito em dois lugares só continua igual se algo comparar.

## Fora de escopo

- Suportar os 26 agentes do upstream. A tabela nasce com **quatro** — `claude`, `copilot`,
  `cursor-agent`, `codex` (`AGENTS.md`) — com os **ids do upstream**, para os dois nunca
  discordarem sobre como uma coisa se chama — porque o custo real de um agente não é a linha da
  tabela: é **testar** que a instalação funciona lá. Acrescentar é uma linha e um teste, e o
  gatilho é alguém usar.
- Traduzir os agentes e skills do Maestro para o formato de cada ferramenta. O que muda aqui
  é **onde o arquivo é escrito**, não o conteúdo dele.
- `script: sh|ps` (PowerShell) do upstream. Nenhum uso, nenhuma dor — YAGNI declarado.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `--ai list` imprime a tabela; `--ai inexistente` **recusa** nomeando os válidos.
- Instalar com cada um dos quatro agentes põe comandos e bloco nos caminhos daquele agente.
- Com agente sem suporte a harness, a camada **não** é instalada e o resumo diz o motivo.
- A escolha fica gravada e é legível depois da instalação.
- O portão reprova quando o bloco instalado diverge do que o instalador gera.
- Cada uma dessas recusas é **vista falhando** (`TAIL:mutation`).
- A receita `docs/receitas/instalar-o-maestro.md` explica o modelo, com a tabela.
- Bateria completa, plugin e build verdes.

## Clarify

1. Quais agentes entram? → **Quatro**, listados acima. É a resposta que dá para defender hoje;
   o Steward pode acrescentar, e o custo é uma linha mais um teste.
2. O instalador passa a **escrever** o bloco no arquivo de instrução? → Continua **imprimindo**
   por padrão (copiar arquivo não é instalar, e o arquivo é do dono do repositório), com
   `--write-block` que **acrescenta se não houver** e **recusa se já houver outro** — a mesma
   regra que o `settings.json` ganhou no 056.

## Gatilhos que a mesma conversa disparou (registrar antes de tratar)

Não são escopo deste ciclo; ficam nomeados aqui porque a condição deles é **esta**:

- `contexto-na-spec` (PRP) — gatilho: *"primeiro ciclo regendo código de produção"*.
- Testes de caracterização — lacuna 02 da peça 06, gatilho: *"quando o método sair para
  código de produto"*.
- `achado-055` (linguagem ubíqua) — o roadmap a condiciona a *"se/quando houver domínio"*.
