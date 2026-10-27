# [[TASK 073-correcao-2]] — despacho da regente ao Gerente (26/10/2026, 21:00; fallback por arquivo)

> A sessão regente reiniciou: o ref novo é **`MAESTRO [5d2fba]`**. Todo DONE e GATE vai para ele
> (confira no `ListAgents`). Os refs antigos `7c8d05`/`163f25` não resolvem mais.

## 1. Ciclo 073 — correção 2 da rodada 4 (prioridade)

Os três juízes da segunda rodada (contexto fresco, sobre `faca232`) devolveram **barra não
atingida com diagnóstico mudado**. Pela regra das duas rodadas há **uma única correção 2**,
consolidada com as decisões da regente em
`specs/073-area-administrativa/rodada-4/correcao-2.md` (commit `cda6d91`), com a tabela de
fatias por dono (Worker01 a Worker06). Despache uma `[[TASK …]]` por dono, com o conteúdo da
tabela e a instrução "leia a correção 2 inteira antes de tocar na sua fatia; as decisões são
fixas". Integre, rode o verificador (11 telas, 0 achados, **seis** regras), conformance 073 nos
dois modos, atualize `andamento.md` e mande `[[DONE 073-correcao-2]]` a `MAESTRO [5d2fba]` com
HEAD e tokens. **Não despache juízes**: a terceira leitura é da regente.

## 2. Ciclo 074 — em paralelo, sem bloquear o 073

- Gate de spec **aprovado com ajustes** por delegação (`specs/074-prototipo-navegavel/gate-spec.md`,
  commit `82f0ee8`): aplique B1 (kanban declara `chamados-e-gates`; os seis itens são vistas
  sobre os cinco contextos), B2 (NFR1 g/h/i) e S1, S2, S3, S5, S6 no `spec.md`, **no mesmo
  commit** do `ux-design.md`.
- Próximo: `ux-design.md` (agente `ux-semantics`: papel semântico de cada objeto, jornadas por
  contexto, tabela ENTRA → tela → elemento com 18 linhas) → `[[GATE 074-ux]]` a `MAESTRO [5d2fba]`;
  depois `plan.md` com Constitution Check + `tasks.md` + `data-model.md` → `[[GATE 074-plan]]`.
- Só depois do aceite do plano começa a fatia 2 (Worker02). Workers ocupados com a correção 2 do
  073 têm prioridade nela.

## 3. Canal

DONE/GATE sempre com cópia a `MAESTRO [5d2fba]`; se o `SendMessage` falhar, commite
`specs/NNN-*/done-*.md` ou `gate-*.md` na branch `066-painel-de-regencia` e eu leio.
