# Receita — instalar o Maestro num projeto

> Objetivo: fazer a Inteligência Artificial (IA) seguir o método no **seu** repositório.
> Tempo: ~5 min. Pré-requisito: ter o repositório do Maestro clonado.
>
> **Instalar não é copiar arquivos.** Copiar é o passo 2; instalado é quando a IA sabe que
> deve segui-los (passo 3) — e `scripts/check-install.sh` (passo 4) só fica verde
> quando as duas metades existem.

## Escolha o caminho

| Caminho | Leva | Quando usar |
|---|---|---|
| **A. Script** (abaixo) | método **inteiro** | padrão — qualquer projeto, qualquer assistente |
| **B. Plugin** `/plugin marketplace add GHDaru/maestro` → `/plugin install maestro@ghdaru-maestro` | 13 agentes + 6 skills + comandos | usa Claude Code e quer atualização automática |
| **C. `npx skills add GHDaru/maestro`** | só as 6 skills | quer só as skills, em qualquer um dos 75+ agentes |

> B e C **não** trazem scripts nem governança. Para o método completo, siga o caminho A.

## 0. Diga qual agente você usa

O instalador **não adivinha**. Antes do ciclo 057 ele copiava `.claude/*` e imprimia um bloco
de `CLAUDE.md` fosse qual fosse a ferramenta — um método cujo instalador supunha um agente em
silêncio. Agora o agente é **escolha declarada**, no modelo do spec-kit (que grava a escolha
em `init-options.json` e mapeia cada agente ao seu arquivo de instrução).

```bash
scripts/install-maestro.sh --ai list
```

| `--ai` | Agente | Arquivo que ele lê | Comandos | Camada de hooks |
|---|---|---|---|---|
| `claude` *(padrão)* | Claude Code | `CLAUDE.md` | `.claude/commands` | **sim** |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` | — | não |
| `cursor` | Cursor | `.cursor/rules/specify-rules.mdc` | — | não |
| `generic` | Codex, Amp, opencode, Kiro… | `AGENTS.md` | — | não |

Três coisas que essa tabela diz de propósito:

- **`—` em comandos significa "não verificamos o formato"**, e por isso **nada** é instalado
  ali. Derramar `.claude/commands` num repositório de Copilot seria enviar arquivo que
  ninguém lê — a metade de despacho do anti-padrão 22.
- **A camada de hooks é mecanismo do Claude Code.** Para os outros agentes ela não é
  instalada, e o resumo **diz o motivo** em vez de omitir. O bloco escrito no arquivo de
  instrução também muda: sem hooks, ele diz que a regra vale *enquanto for seguida*, em vez de
  afirmar uma proteção que não existe ali.
- **Um `--ai` desconhecido recusa** e lista os válidos. Nunca cai no padrão calado: é assim
  que alguém instala para a ferramenta errada e descobre semanas depois.

Só quatro agentes, e não os 27 do upstream, porque o custo de um agente não é a linha da
tabela — é **testar** que a instalação funciona lá. Acrescentar é uma linha em
`scripts/install-agents.tsv` mais um teste; o gatilho é alguém usar.

A escolha fica gravada em `.maestro/install-options.json`, ao lado do manifesto:

```json
{"ai": "claude", "instruction": "CLAUDE.md", "harness": true, "maestro_version": "0.2.0", "installed": "2026-08-21"}
```

O campo `harness` grava o **fato** desta instalação, não o que a tabela permite: com
`--no-hooks` num agente que os suporta, a tabela diz `yes` e o arquivo diz `false`.

## 1. Veja o que será instalado (sem escrever nada)

```bash
scripts/install-maestro.sh /caminho/do/seu-projeto --dry-run
```

## 2. Instale

```bash
scripts/install-maestro.sh /caminho/do/seu-projeto
```

O script **não sobrescreve** arquivos existentes (use `--forcar` se quiser substituir).
Ele leva cinco camadas:

| Camada | O que vai | Para quê |
|---|---|---|
| `.claude/agents/` | 13 subagentes | **quem faz** cada papel |
| `skills/` | 6 skills | **como fazer** (cada uma com sua lei) |
| `scripts/` | 7 scripts | o **ritual** e as verificações |
| `.claude/commands/` + `.specify/templates/` | comandos e templates | o **motor** spec-driven |
| `docs/governance/` | princípios, modelo, glossário | a **fonte de verdade** |

## 3. Aponte a IA para o método

Por padrão o instalador **imprime** o bloco e você o acrescenta — o arquivo de instrução é do
dono do repositório. Para deixar que ele escreva:

```bash
scripts/install-maestro.sh /caminho/do/seu-projeto --ai claude --write-block
```

A regra é a mesma do `settings.json`: **acrescenta se não houver** bloco do Maestro, e
**recusa se já houver um diferente**, deixando o seu intacto e dizendo como comparar
(`--block`). E o `check-install.sh` passa a conferir que o bloco instalado é **exatamente** o
que o instalador gera hoje: um fato dito em dois lugares só continua igual se algo comparar.


O bloco é **gerado das skills que existem no disco** — lista escrita à mão envelhece
calada. Cole no `CLAUDE.md` do projeto:

```bash
scripts/install-maestro.sh --block >> /caminho/do/seu-projeto/CLAUDE.md
```

E mantenha **uma fonte só**, para as duas instruções não divergirem:

```bash
cd /caminho/do/seu-projeto && ln -s CLAUDE.md AGENTS.md
```

## 4. Prove que está instalado

```bash
scripts/check-install.sh    # camadas + instrução da IA + skills todas visíveis
scripts/check-agents.sh       # invariantes dos subagentes; exit 0 = ok
scripts/check-roles.sh        # todo papel do modelo tem agente; exit 0 = ok
scripts/new-cycle.sh 001 primeiro-ciclo
```

`check-install.sh` falha enquanto o `CLAUDE.md` não apontar para o método — e falha
de novo se amanhã entrar uma skill que ninguém citou na instrução. É assim que a instalação
continua verdadeira depois do primeiro dia.

## Pronto quando

- [ ] `scripts/check-install.sh` sai com código 0
- [ ] `scripts/check-agents.sh` sai com código 0
- [ ] O `CLAUDE.md` do projeto aponta para os princípios e lista as skills
- [ ] `specs/001-*/` existe com os quatro artefatos

**Por quê?** → [Capítulo 13 — decisões de engenharia](../handbook/13-decisoes-de-engenharia.md)
