# Data model 065 — tarefa, tentativa, evento

O livro de ponto não guarda entidades: guarda **eventos**. As entidades são derivadas na
leitura, pelo `scripts/report-tasks.py`. Por isso o livro nunca precisa ser reescrito.

## Entidades (derivadas)

| Entidade | Identidade | Nasce de | Atributos |
|---|---|---|---|
| **Tarefa** | `task_id` | o primeiro evento com aquele id | `kind`, `cycle`, tentativas, veredito final |
| **Tentativa** | `task_id` + `attempt` | um evento `start` | sessão, modelo, `outcome`, tokens, `cost_usd`, `duration_s` |
| **Atribuição** | `task_id` + sessão do gerente | um evento `assigned` | destinatário (`to`), hora |
| **Veredito** | `task_id` + `by` | um evento `verdict` | `verdict`, `reason`, a tarefa de auditoria que o emitiu (`by`) e a `session` dela |
| **Veredito de ciclo** | `<NNN>` + `by` | um evento `verdict` cujo `task_id` termina em `-cycle` (ex.: `064-cycle`) | `verdict`, `by`; o ciclo tem um histórico e o **último válido** é o atual (ex.: 064 `rejected` por 064-R1 → `approved_with_notes` por 064-R2) |

## Relações

```text
Tarefa 1 ──< Tentativa            (attempt = 1, 2, 3…)
Tentativa ──? Tentativa           (redoes = "<task_id>#<attempt>": a reprovada que esta refaz)
Tarefa(audit|review) ──> Tarefa   (target: a avaliada; gera um evento verdict nela)
Tarefa(audit|review) ──> Ciclo    (target = "<NNN>-cycle": o veredito do ciclo inteiro, não de uma tarefa)
Tentativa ── start ── stop        (pares por task_id + session + attempt; start sem stop = órfã)
```

## Regras de pareamento

1. Um `stop` fecha o `start` mais recente, ainda aberto, com o mesmo `task_id`, **a mesma
   sessão e a mesma tentativa** (a tentativa só é comparada quando os dois eventos a trazem).
   É o que o `report-tasks.py` faz.
   - **Por que a tentativa entra na chave**: o id de sessão não identifica um executor. Em
     sessões aninhadas ele pode se repetir — medido neste ciclo: as executoras herdavam o id do
     gerente, e o livro mostra T6 e T7 abertas ao mesmo tempo com o mesmo `session`, sem
     `superseded`. Só com `task_id` + `session`, duas tentativas abertas da mesma tarefa
     seriam indistinguíveis; com a tentativa, cada `stop` fecha a sua.
2. Um `start` sem `stop` é **órfã** — trabalho pago e não entregue. Nunca é completada por
   inferência.
3. O veredito de uma tarefa é o do **último** evento `verdict` com aquele `task_id`, e só conta
   se vier de uma tarefa `audit` ou `review` (`by`, obrigatório num `verdict`). Quem executou
   não dá veredito (Princípio II): o mod só grava veredito a partir dessas duas espécies, e o
   relatório descarta o que não vier delas.
   - **O `by` é declarado por quem escreve a linha**, então só ele não basta: o relatório exige
     também que a `session` do veredito seja a `session` de um `start` da tarefa `by` (quem
     julgou é quem rodou a auditoria). Limite: isso supõe ids de sessão distintos por executor
     (em sessões aninhadas eles se repetem), e a etiqueta não é autenticada.
4. Um `task_id` de veredito terminado em `-cycle` é o **veredito do ciclo**, não de uma tarefa:
   vale a mesma regra de quem pode julgar, o último válido é o atual, o histórico é mantido, e ele
   não entra na aprovação de primeira nem na lista "veredito sem `start`". Ids de tarefa
   terminados em `-cycle` ficam reservados.

## Métricas (o que o relatório calcula, e como)

| Métrica | Definição |
|---|---|
| tokens de uma tentativa | `tokens_in + tokens_out + tokens_cache_read + tokens_cache_write` do seu `stop` |
| custo por `kind` e ciclo | soma de `cost_usd` (e de tokens) dos `stop`, agrupada |
| tokens por modelo | soma de `tokens_by_model`; **sem custo** — o `cost_usd` é por tentativa, não por modelo, então a coluna fica `-` em vez de um rateio inventado |
| **aprovação de primeira** | tarefas cujo veredito final é `approved`/`approved_with_notes` **e** que só têm a tentativa 1 ÷ tarefas com veredito |
| **custo do retrabalho** | soma de tokens e custo das tentativas com `attempt ≥ 2` |
| **taxa de cache** | `tokens_cache_read ÷ (tokens_in + tokens_cache_read + tokens_cache_write)` |
| **órfãs** | `start` sem `stop` pareado (regra 1) |
