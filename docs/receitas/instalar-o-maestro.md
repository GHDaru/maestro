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

## O caminho curto: `maestro init`

```bash
git clone https://github.com/GHDaru/maestro.git && cd maestro
./bin/maestro agents                              # quais IAs ele sabe servir
./bin/maestro init /caminho/do/seu-projeto --ai claude
```

`init` conduz os quatro passos — agente, destino, instalação, **verificação** — e **sai
diferente de zero se a verificação falhar**. Instalar sem provar não conta.

Toda pergunta também é flag (`--ai`, `--yes`, `--dry-run`, `--no-hooks`, `--force`), então ele
roda em CI (integração contínua, *continuous integration*) sem ninguém digitando. Sem terminal e sem `--yes`, ele **recusa** em vez de
responder por você.

O resto desta receita é o caminho longo — os mesmos passos, um comando por vez, para quem quer
ver o que acontece em cada um.

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
| `cursor-agent` | Cursor | `.cursor/rules/specify-rules.mdc` | — | não |
| `codex` | Codex CLI · Amp, opencode, Kiro, Bob, Pi | `AGENTS.md` | — | não |

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
{"ai": "claude", "instruction": "CLAUDE.md", "harness": true, "maestro_version": "0.3.0", "installed": "2026-08-22"}
```

O campo `harness` grava o **fato** desta instalação, não o que a tabela permite: com
`--no-hooks` num agente que os suporta, a tabela diz `yes` e o arquivo diz `false`.

## 1. Veja o que será instalado (sem escrever nada)

```bash
scripts/install-maestro.sh /caminho/do/seu-projeto --ai claude --dry-run
```

Troque `claude` pelo id que você escolheu no passo 0. **Omitir `--ai` instala para o
`claude`** — que é um padrão, não uma adivinhação, mas continua sendo uma escolha sua.

## 2. Instale

```bash
scripts/install-maestro.sh /caminho/do/seu-projeto --ai claude
```

**Instalar é também atualizar.** O que o método escreveu e você não tocou é renovado; o que
você modificou é **mantido**, com a versão nova ao lado como `*.maestro-new`; o que o método
deixou de enviar é removido só enquanto continuar intacto. Nada seu é sobrescrito em silêncio —
`--force` existe para forçar, e mesmo ele salva a sua versão como `*.maestro-old` antes.
Ele leva cinco camadas:

| Camada | O que vai | Para quê |
|---|---|---|
| `.claude/agents/` | 13 subagentes | **quem faz** cada papel |
| `skills/` | 6 skills | **como fazer** (cada uma com sua lei) |
| `scripts/` | 13 scripts + `hooks/` | o **ritual** e as verificações |
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

> **Se quem vai seguir isto é uma IA**, e não você: o repositório do Maestro tem uma seção
> escrita para ela — o que ler antes de agir, o comando que responde pelo estado (nunca a
> memória), o que um hook **recusa** reescrever, e que promover não é dela. Está no
> [README do Maestro](https://github.com/GHDaru/maestro#se-você-é-uma-ia-e-acabou-de-abrir-este-repositório),
> que é o arquivo que um agente abre — por isso ela mora lá e não aqui.

## 4. Prove que está instalado

**Dentro do seu projeto** — não no clone do Maestro. Rodar daqui devolve um verde que é
do repositório do método, não do seu:

```bash
cd /caminho/do/seu-projeto
scripts/check-install.sh      # camadas + instrução da IA + skills todas visíveis
scripts/check-agents.sh       # invariantes dos subagentes; exit 0 = ok
scripts/check-roles.sh        # todo papel do modelo tem agente; exit 0 = ok
scripts/new-cycle.sh 001 primeiro-ciclo
```

`check-install.sh` falha enquanto o `CLAUDE.md` não apontar para o método — e falha
de novo se amanhã entrar uma skill que ninguém citou na instrução. É assim que a instalação
continua verdadeira depois do primeiro dia.

## O que fica no seu projeto depois

Gerado de uma instalação real por **`maestro init --ai claude`**, num projeto que só tinha
`README.md`: **81 arquivos escritos** (82 no total, contando o seu). O comando importa: `init`
passa `--write-block`, e é ele que põe o `CLAUDE.md` no disco — `install-maestro.sh` sozinho
escreve 80 e deixa o bloco para você colar. Com outro agente a árvore é menor:
`maestro init --ai codex` escreve **53** e **nenhum `.claude/`**, porque aquele agente não lê
esse formato.

```
meu-app/
├── CLAUDE.md              a IA lê isto antes de trabalhar. É o que faz o método valer
├── README.md              seu, intocado
│
├── .claude/               formatos do Claude Code
│   ├── agents/            13 subagentes: spec, plan, dev, review, security, qa…
│   ├── commands/          12 comandos: /speckit.specify, /speckit.plan, /dod, /eval…
│   └── settings.json      liga os hooks abaixo
│
├── scripts/               o ritual e os portões
│   ├── new-cycle.sh       abre um ciclo (spec, plan, tasks, qa-report)
│   ├── promote-main.sh    dev → main, com o gate humano
│   ├── record-decision.sh a única via de escrita no índice de decisões
│   ├── check-*.sh         9 portões — os que fazem sentido fora daqui
│   ├── retro.sh           pré-computa o material da retrospectiva
│   ├── README.md          o que cada script é
│   └── hooks/             guard-immutables.py · session-state.sh
│
├── skills/                6 disciplinas que a IA consulta antes de agir
├── .specify/              12 templates (spec, plan, tasks, ADR — registro de decisão de arquitetura…) + o motor spec-driven
├── docs/governance/       a constituição, o modelo operacional, o catálogo de artefatos
├── docs/records/          decisoes.jsonl — índice append-only, começa vazio
├── evals/                 base para avaliar saída não-determinística
└── .maestro/              install-options.json (qual agente) · manifest.tsv (o que ele escreveu)
```

Duas coisas mudam **comportamento** no mesmo instante: o `CLAUDE.md`, que faz a IA seguir o
método, e o `.claude/settings.json`, que instala hooks que **recusam** reescrever o que é
história — corpo de ADR já commitado, o índice de decisões e os cards datados. O
`manifest.tsv` é o que torna reinstalar um **upgrade**: ele sabe o que escreveu, então
distingue arquivo nosso de arquivo seu.

## Livro de ponto (opcional)

Só para quem usa o Claude Code e quer saber **quanto cada tarefa gastou**. É um mod, distribuído
pelo marketplace do Maestro, que registra o início e o fim das tarefas etiquetadas
`[[TASK]]`/`[[DONE]]`, com os tokens de cada requisição, num livro append-only.

```bash
claude plugin install maestro-ledger --marketplace GHDaru/maestro --scope project
```

O instalador **imprime** este comando e **não o executa**: `claude plugin install` grava nas
configurações do usuário, fora do projeto-alvo, e o instalador só escreve dentro dele.

Limites, ditos de antemão:

- exige Claude Code **2.1.292 ou mais novo**;
- mods **não carregam** em sessões na nuvem (claude.ai/code) nem em sessões WSL (*Windows
  Subsystem for Linux*, o Linux dentro do Windows) do Desktop — nelas o livro simplesmente não
  registra nada;
- a etiqueta `[[TASK]]`/`[[DONE]]` precisa estar **sozinha na linha**: conta a primeira `[[TASK]]`
  e a última `[[DONE]]`, e um `[[TASK]]` vindo de outra sessão não substitui uma tarefa aberta;
- só tarefas `audit` e `review` registram veredito.

## Pronto quando

- [ ] `scripts/check-install.sh` sai com código 0
- [ ] `scripts/check-agents.sh` sai com código 0
- [ ] O `CLAUDE.md` do projeto aponta para os princípios e lista as skills
- [ ] `specs/001-*/` existe com os quatro artefatos

**Por quê?** → [Capítulo 13 — decisões de engenharia](../handbook/13-decisoes-de-engenharia.md)
