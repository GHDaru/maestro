# Data model 057 — agente · escolha

> Duas coisas, porque **o que existe** e **o que este projeto escolheu** não são a mesma coisa.
> Este arquivo é o contrato que `scripts/install-maestro.sh` lê e `scripts/check-install.sh`
> confere; mudar um campo aqui é mudar o instalador.

## As entidades

```
AGENTE  1 ──── 0..1  ESCOLHA
(o que o método      (o que ESTE
 sabe instalar)       projeto usa)
```

| Entidade | Mutável? | Onde vive | Por quê |
|---|---|---|---|
| **Agente** | linha de tabela, editável | `scripts/install-agents.tsv` | é um catálogo do que sabemos instalar. Cresce por dor: alguém usar o agente. |
| **Escolha** | reescrita a cada instalação | `<alvo>/.maestro/install-options.json` | é o estado corrente daquele projeto; reinstalar com outro `--ai` é uma decisão nova, não um histórico. |

Deliberadamente **não** é append-only, ao contrário do índice de decisões: aqui não há
história a preservar — há um fato corrente, e o histórico dele é o git do projeto que instalou.

## Agente — a linha da tabela

Arquivo separado por **tabulação**, comentários começam com `#`.

| Campo | Obrigatório | Conteúdo |
|---|---|---|
| `id` | ✅ | identificador em minúsculas, o valor de `--ai` |
| `name` | ✅ | nome humano, o que aparece em `--ai list` |
| `instruction` | ✅ | caminho do arquivo que **aquele agente lê** no início da sessão |
| `commands` | ✅ | diretório de comandos, ou **`-`** quando o formato **não foi verificado** |
| `harness` | ✅ | `yes` \| `no` — se aquele agente executa hooks do Claude Code |

**Por que `-` e não um palpite**: derramar `.claude/commands` num repositório de Copilot envia
arquivo que ninguém lê. Enviar o que não é lido é a metade de despacho do anti-padrão 22, e um
palpite documentado como suporte é pior que um `-` honesto.

**Todo `instruction` foi lido do upstream vendorizado**
(`.specify/scripts/bash/update-agent-context.sh`) e **conferido linha a linha**:
`claude → CLAUDE.md`, `copilot → .github/copilot-instructions.md`,
`cursor-agent → .cursor/rules/specify-rules.mdc`, `codex → AGENTS.md`.

> A primeira versão desta tabela afirmava o mesmo e **duas das quatro linhas eram deduzidas**:
> o `generic` do upstream não mapeia arquivo nenhum (*"no predefined context file"*), e o id
> do Cursor lá é `cursor-agent`, não `cursor`. O parecer executou a conferência que eu tinha
> só afirmado. Os ids agora seguem o upstream, e a conferência virou parte do ciclo.

## Escolha — o arquivo gravado

Uma linha por campo, ao lado do manifesto do ciclo 051:

```json
{"ai": "claude", "instruction": "CLAUDE.md", "harness": true, "maestro_version": "0.2.0", "installed": "2026-08-17"}
```

| Campo | Obrigatório | Conteúdo |
|---|---|---|
| `ai` | ✅ | um `id` **que existe na tabela** |
| `instruction` | ✅ | copiado da linha do agente, para o projeto não precisar da tabela para saber onde está a instrução |
| `harness` | ✅ | `true` \| `false` — o que **de fato** aconteceu nesta instalação, não o que a tabela permite |
| `maestro_version` | ✅ | de onde veio, no formato do `init-options.json` do upstream |
| `installed` | — | data, `YYYY-MM-DD` |

`harness` grava o **fato** e não a permissão: com `--no-hooks` num agente que suporta, a tabela
diz `yes` e este campo diz `false`. Um arquivo de estado que registra a intenção em vez do
resultado é a mesma mentira que este método persegue desde o ciclo 042.

## Invariantes (o que o portão verifica)

1. Toda linha da tabela tem os cinco campos, id único, e `harness` no vocabulário fechado —
   **conferido pelo `check-installed.sh`**. Antes eram só estas frases: uma linha de quatro
   campos fazia o agente sumir de `--ai list` **e** de `--ai <id>` sem aviso, e `harness=YES`
   era silenciosamente tratado como `no`.
2. `--ai <id>` fora da tabela **recusa**, listando os válidos — nunca cai no padrão em silêncio.
3. `commands = -` ⇒ **nenhum** comando é instalado para aquele agente.
4. `harness = no` ⇒ a camada **não** é instalada, e o resumo diz por quê.
5. O bloco de método vive no `instruction` do agente escolhido — e o `check-install.sh` lê
   esse campo para saber **onde procurar**, em vez de supor `CLAUDE.md`.
6. O bloco **instalado** e o bloco que o instalador **gera para aquele agente** são o mesmo
   texto — comparado com `--ai <id>` e, quando o harness não está lá, com `--no-hooks`.
