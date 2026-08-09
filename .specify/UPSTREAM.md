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
| `templates/spec-template.md` | upstream 0.4.3 | **Adaptado** (ciclo 009): PT, Raia, EARS, Fora de escopo, Clarify, gates — formato provado nos ciclos 003–008 |
| `templates/plan-template.md` | upstream 0.4.3 | **Adaptado** (009): Constitution Check I–VIII nomeado, Como por fronteira, Verificação executável |
| `templates/tasks-template.md` | upstream 0.4.3 | **Adaptado** (009): verificação primeiro, doc viva no mesmo PR, gate humano + registro automático |
| `.claude/commands/speckit.converge.md` | fork `0117a7b` | **Adaptado** (009): sem extension hooks (YAGNI); anexa, nunca reescreve |
| `templates/checklist-template.md` | upstream 0.4.3 | Verbatim (pouco uso; adaptar quando doer) |
| `templates/constitution-template.md` | upstream 0.4.3 | Verbatim (nossa constituição já existe em `.specify/memory/`) |
| `templates/agent-file-template.md` | upstream 0.4.3 | Verbatim |
| `.claude/commands/speckit.plan.md` | upstream 0.4.3 | **Adaptado** (ciclo 044): as fases 0 e 1 passam a **deferir à tabela de declaração** do plano (`ART:<artefato>=yes\|no`) em vez de gerar `research.md`, `data-model.md` e `contracts/` incondicionalmente; `quickstart.md` **não** é produzido |
| demais `.claude/commands/speckit.*` | upstream 0.4.3 | Verbatim (leem os templates adaptados — herdam o método por eles) |
| `scripts/bash/` | upstream 0.4.3 | Verbatim |

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
