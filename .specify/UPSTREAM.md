# Proveniência do Spec Kit vendorizado

> Ciclo 009 (F4). **Vendorizar** = o conteúdo passa a ser fonte NOSSA, adaptado ao
> método; o upstream é consultado por decisão, nunca por acidente.

## Origens

- **Upstream oficial**: github/spec-kit — instalado via speckit **0.4.3**
  (`init-options.json`).
- **Fork da casa**: `GHDaru/spec-kit` @ **`0117a7b`** (2026-07-27) — origem do comando
  `converge`.

## Estado de cada peça

| Peça | Origem | Estado |
|---|---|---|
| `templates/spec-template.md` | upstream 0.4.3 | **Adaptado** (ciclo 009): PT, Raia, EARS, Fora de escopo, Clarify, gates — formato provado nos ciclos 003–008 · `UP:state=adapted` |
| `templates/plan-template.md` | upstream 0.4.3 | **Adaptado** (009): Constitution Check I–VIII nomeado, Como por fronteira, Verificação executável · `UP:state=adapted` |
| `templates/tasks-template.md` | upstream 0.4.3 | **Adaptado** (009): verificação primeiro, doc viva no mesmo PR, gate humano + registro automático · `UP:state=adapted` |
| `.claude/commands/speckit.converge.md` | fork `0117a7b` | **Adaptado** (009): sem extension hooks (YAGNI); anexa, nunca reescreve · `UP:state=adapted` |
| `templates/checklist-template.md` | upstream 0.4.3 | Verbatim (pouco uso; adaptar quando doer) · `UP:state=verbatim` |
| `templates/constitution-template.md` | upstream 0.4.3 | Verbatim, **não usado** (ciclo 048): o Maestro tem uma constituição só, `docs/governance/principles.md`. Preenchê-lo criaria a segunda · `UP:state=verbatim` |
| `templates/agent-file-template.md` | upstream 0.4.3 | Verbatim · `UP:state=verbatim` |
| `.claude/commands/speckit.plan.md` | upstream 0.4.3 | **Adaptado** (044 e 048): as fases 0 e 1 passam a **deferir à tabela de declaração** do plano (`ART:<artefato>=yes\|no`) em vez de gerar `research.md`, `data-model.md` e `contracts/` incondicionalmente; `quickstart.md` **não** é produzido; no 048 a citação da constituição foi reapontada · `UP:state=adapted` |
| `.claude/commands/speckit.constitution.md` · `speckit.analyze.md` | upstream 0.4.3 | **Adaptado** (ciclo 048): as 8 citações da constituição do upstream (sob o diretório de memória dele) passam a apontar para `docs/governance/principles.md`. O caminho do upstream **nunca existia numa instalação**, e mantê-lo criaria uma segunda constituição (anti-padrão 22) · `UP:state=adapted` |
| `.claude/commands/speckit.specify.md` · `speckit.tasks.md` · `speckit.implement.md` · `speckit.clarify.md` · `speckit.checklist.md` · `speckit.taskstoissues.md` | upstream 0.4.3 | Verbatim (leem os templates adaptados — herdam o método por eles) · `UP:state=verbatim` |
| `.specify/scripts/bash/` | upstream 0.4.3 | Verbatim · `UP:state=verbatim` |

> **`UP:state=verbatim|adapted`** — token legível por máquina em cada linha, lido pelo portão
> da cópia instalada (no repositório do Maestro). A coluna em prosa é para quem lê; o token é para o portão,
> pela mesma razão do `fecha`, do `PT-DATA` e dos `ART:`/`TAIL:`: renomear a coluna para
> "Ajustado" mudaria silenciosamente o comportamento do portão (achado da revisão do 048).

> **`UP:optional-path=<caminho>`** — caminho que o CLI do speckit cria **se** o projeto o
> usar, e que o Maestro deliberadamente não usa. Declarado aqui, um por linha, para que o
> portão da cópia instalada não o cobre e para que a exceção fique **visível** em vez de
> escondida numa heurística:
>
> - `UP:optional-path=.specify/extensions.yml` — extension hooks. Fora desde o ciclo 009
>   (YAGNI, mesma decisão do `speckit.converge.md`). As citações permanecem nos comandos
>   porque são honestas: o próprio texto diz "se não existir, pule em silêncio". Enfraquecê-las
>   para calar o portão seria trocar uma instrução acionável por prosa vaga — foi o que a
>   revisão do 048 pegou.

## Regras

1. **Sync deliberada**: novidade do upstream/fork só entra por **spec** (nunca
   reinstalar por cima — apagaria as adaptações). Compare, escolha, adapte, registre aqui.
2. **Divergência declarada, nunca silenciosa**: quando uma peça vendorizada contradiz o
   método, a contradição é resolvida **por spec** e a peça muda de estado nesta tabela.
   Precedente e motivo: até o ciclo 044 o `/speckit.plan` mandava gerar quatro artefatos
   incondicionalmente enquanto o `plan-template.md` mandava declará-los — quem instalava o
   Maestro recebia as duas ordens e nenhuma explicação de qual vencia. Divergir sem
   registrar é o que transforma vendorizar em bifurcar.

3. **`quickstart.md` não é produzido no Maestro**: a função "como alguém experimenta isto" é
   servida pelo documento de jornada (`templates/journey-template.md`) e pelas receitas.
   Princípio VI proíbe duplicar função já servida. Nota precisa: o `speckit.tasks` e o
   `speckit.implement` ainda **leem** o arquivo se ele existir (`IF EXISTS`), o que é
   inofensivo e não foi tocado — a divergência é sobre **produzir**, não sobre ler.

4. **Hierarquia de scaffolds**: estes templates são a **referência completa** (é o que os
   comandos `/speckit.*` leem); o esqueleto do `scripts/new-cycle.sh` é o atalho mínimo
   derivado. Se divergirem, **os templates mandam** — atualize o script.
