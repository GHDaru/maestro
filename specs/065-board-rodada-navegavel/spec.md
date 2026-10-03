# Spec 065 — Board enxuto, rodada navegável e workflow por tarefa

- **Status**: Draft · **Lane**: full · **Date**: 2026-10-02
- **Origin**: Desejo 002 do Gilsiley, redigido pela Hindiana Assistente (.maestro/docs/desejo-002-board-e-rodada-navegavel.md). Depende da rodada 001 (spec 064). Desenho de referência: workflow-maestro.md.

## What and why

O board do painel hoje é poluído: roster, eventos crus de hook e textos longos com o mesmo peso. As rodadas não são navegáveis — cada artefato (spec, plan, tasks) vive solto, sem árvore que ligue requisito → teste → tarefa → workflow. E o estado de cada tarefa no workflow (red, green, runner2, crítica 1, crítica 2, integrada, VM, barra, produção) não aparece em lugar nenhum.

A proposta é um board enxuto com 3 exceções no topo e uma linha por sessão; cada tarefa carrega o próprio workflow visível; a rodada é navegável em árvore (spec → FR → testes, plan → artefatos, tasks → T → workflow, críticas → vereditos); e o roadmap mostra raias por ciclo com o gate do push no topo.

## Functional requirements

- **FR1**: O SISTEMA DEVE exibir o board com 3 exceções no topo: "precisam do Gilsiley" (prompts e gates humanos), "gate do push" (itens restantes) e "sem tarefa há 2 ciclos". Cada exceção só fica vermelha quando maior que zero.
- **FR2**: O SISTEMA DEVE exibir uma linha por sessão com 5 colunas: sessão, estado (pill), peça e passo do workflow, esperando quem, e há quanto tempo.
- **FR3**: O SISTEMA DEVE abrir o board no filtro "só exceções" por padrão. A lista completa está a um clique.
- **FR4**: O evento de hook DEVE aparecer como "última atividade há N min", não como uma linha separada.
- **FR5**: O SISTEMA DEVE exibir, para cada tarefa de uma rodada, o passo atual do workflow e o tempo nele.
- **FR6**: QUANDO o usuário clicar numa tarefa, O SISTEMA DEVE mostrar a linha do tempo dos passos (entrada, resumo, saída, sessão, hash, evidência) e a evidência que falta para o próximo passo.
- **FR7**: SE a evidência registrada não corresponder ao hash da tarefa, ENTÃO O SISTEMA DEVE marcar a divergência no card e na linha do tempo (chip amarelo).
- **FR8**: O SISTEMA DEVE exibir a rodada em árvore navegável: rodada › spec › cada FR/EARS › testes que o provam; › plan › artefatos; › tasks › cada T › workflow; › críticas › vereditos com link.
- **FR9**: QUANDO o usuário clicar num nó da árvore, O SISTEMA DEVE exibir o artefato à direita com breadcrumb (ex: `064 › spec › FR13`) e chips de evidência.
- **FR10**: ONDE um requisito não tiver teste ligado, O SISTEMA DEVE marcar o requisito como descoberto (chip amarelo).
- **FR11**: O SISTEMA DEVE exibir o roadmap em raias por ciclo (atual, próximo, depois), com um card por rodada. Cada card tem barra de progresso dos 15 passos, gates humanos pendentes destacados, e gate do push no topo.
- **FR12**: O SISTEMA DEVE derivar a árvore automaticamente das convenções: ID no spec.md (FR13), tarefa cita requisitos (T2 → FR13), commit cita tarefa (064 T2: …), teste cita requisito (test_fr13_…).

## Out of scope

- Edição de artefatos pela árvore (só leitura/navegação).
- Notificações push (fila outbox da 064 já existe; entregar notificação é outra rodada).
- Deploy do painel (instalação pela Assistente após APPROVE).

## Acceptance criteria (DoD)

- WHEN o board carrega THEN THE SYSTEM SHALL mostrar 3 exceções no topo, cada vermelha só se > 0.
- WHEN o board carrega THEN THE SYSTEM SHALL abrir no filtro "só exceções".
- WHEN o usuário clica numa tarefa THEN THE SYSTEM SHALL mostrar a linha do tempo com entrada, resumo, saída, sessão, hash, evidência e o que falta.
- WHEN a evidência ≠ hash da tarefa THEN THE SYSTEM SHALL marcar divergência (chip amarelo).
- WHEN o usuário clica num nó da árvore THEN THE SYSTEM SHALL exibir o artefato com breadcrumb e chips.
- WHERE requisito sem teste THEN THE SYSTEM SHALL marcar como descoberto.
- `python -m pytest tests/test_board_navegavel.py` → todos passam.
- `python -m pytest tests/test_workflow_tarefa.py` → todos passam.

## Clarify

1. O estado do workflow por tarefa vem da tabela `passos` da 064 ou de uma tabela nova? → da tabela `passos` existente, com `tarefa` como campo derivado do commit (convenção `064 T2: …`).
2. A árvore é gerada em tempo real ou no ingest? → no ingest, como as outras tabelas derivadas. A árvore é materializada numa tabela `arvore_rodrada` para a UI consultar.
3. O "sem tarefa há 2 ciclos" usa qual janela? → 2 ciclos do loop de status de 30 min (status = "sem tarefa" em dois ciclos consecutivos, ~60 min), NÃO 2 rodadas.

- **FR13**: SE o status de um worker for "sem tarefa" em dois ciclos de status consecutivos, ENTÃO O SISTEMA DEVE contá-lo na exceção "sem tarefa há 2 ciclos".

<!--
  GATE (DoR — not delegable): this spec only becomes a plan after human approval.
  Handoff: spec-agent → (approval) → plan-architect.
-->
