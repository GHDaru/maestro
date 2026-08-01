# Receita — instalar o Maestro num projeto

> Objetivo: fazer a Inteligência Artificial (IA) seguir o método no **seu** repositório.
> Tempo: ~5 min. Pré-requisito: ter o repositório do Maestro clonado.

## 1. Veja o que será instalado (sem escrever nada)

```bash
scripts/instalar-maestro.sh /caminho/do/seu-projeto --dry-run
```

## 2. Instale

```bash
scripts/instalar-maestro.sh /caminho/do/seu-projeto
```

O script **não sobrescreve** arquivos existentes (use `--forcar` se quiser substituir).
Ele leva cinco camadas:

| Camada | O que vai | Para quê |
|---|---|---|
| `.claude/agents/` | 12 subagentes | **quem faz** cada papel |
| `skills/` | 5 skills | **como fazer** (cada uma com sua lei) |
| `scripts/` | 5 scripts | o **ritual** repetido |
| `.claude/commands/` + `.specify/templates/` | comandos e templates | o **motor** spec-driven |
| `docs/governance/` | princípios, modelo, glossário | a **fonte de verdade** |

## 3. Aponte a IA para o método

Cole no `CLAUDE.md` (ou `AGENTS.md`) do projeto — o script imprime este bloco no final:

```markdown
## Método: Maestro
- Leia `docs/governance/principios-maestro.md` e `docs/governance/modelo-operacional.md`
  antes de qualquer trabalho.
- **Skills primeiro**: antes de agir, verifique se uma skill de `skills/` se aplica;
  se houver chance razoável, siga-a.
- Fluxo: spec → plan (Constitution Check) → tasks → implement → DoD → revisão em
  contexto fresco → gate humano → merge.
- Raias: leve (o pull request é o artefato) · plena (spec completa) · infra (plena +
  reversibilidade).
```

## 4. Verifique

```bash
scripts/verificar-agentes.sh    # invariantes dos subagentes; exit 0 = ok
scripts/novo-ciclo.sh 001 primeiro-ciclo
```

## Pronto quando

- [ ] `scripts/verificar-agentes.sh` sai com código 0
- [ ] O `CLAUDE.md` do projeto aponta para os princípios
- [ ] `specs/001-*/` existe com os quatro artefatos

**Por quê?** → [Capítulo 13 — decisões de engenharia](../handbook/13-decisoes-de-engenharia.md)
