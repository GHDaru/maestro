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
