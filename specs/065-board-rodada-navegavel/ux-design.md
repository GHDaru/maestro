# UX Design 065 — Board da rodada navegável

- **Spec**: `spec.md` · **Date**: 2026-10-02 · **Author**: W03

## Visão geral

Three views novas no painel, todas derivadas das tabelas `rodadas` e `passos`
que W09 criou (spec 064) e que T6 (W03) já lê em `v_rodadas`:

1. **Board enxuto** — roadmap visual das rodadas (FR1)
2. **Árvore da rodada** — passos do workflow como árvore (FR2)
3. **Workflow por tarefa** — cada tarefa com worker, critério, crítico (FR3)

## 1. Board enxuto (FR1)

Kanban enxuto: uma coluna por estado do workflow, cards são rodadas.
Não substitui o board de agentes existente — é uma view nova acessível
pela sidebar (`⬚ Rodadas`).

```
┌─────────────┬──────────────────────────────────────────────────────┐
│ M Maestro   │  Rodadas                                             │
│             │                                                      │
│ ▤ Board     │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│ ⬚ Rodadas   │  │ spec    │  │ plan    │  │ implem  │  │ crítica │ │
│ ⇢ Roadmap   │  │         │  │         │  │         │  │         │ │
│ ⚖ Decisões │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │ │
│ ...         │  │ │R002 │ │  │ │R001 │ │  │ │R003 │ │  │ │R004 │ │ │
│             │  │ │Board│ │  │ │Workf│ │  │ │Impac│ │  │ │Porte│ │ │
│             │  │ │W03  │ │  │ │Gere │ │  │ │W08  │ │  │ │W13  │ │ │
│             │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │ │
│             │  │         │  │         │  │ ┌─────┐ │  │         │ │
│             │  │         │  │         │  │ │R005 │ │  │         │ │
│             │  │         │  │         │  │ │Excel│ │  │         │ │
│             │  │         │  │         │  │ │W11  │ │  │         │ │
│             │  │         │  │         │  │ └─────┘ │  │         │ │
│             │  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
│             │                                                      │
│             │  Legenda: spec=aberta · plan=planejando · implem=    │
│             │  implementando · crítica=em crítica · done=fechada    │
└─────────────┴──────────────────────────────────────────────────────┘
```

### Card da rodada

```
┌─────────────┐
│ R001        │  ← id (bold)
│ Workflow    │  ← desejo (truncado 1 linha)
│ painel      │
│ ▶ plan      │  ← passo atual (loz)
│ Gerente     │  ← quem está no passo (avatar)
│ 2h 30min    │  ← tempo total da rodada
└─────────────┘
```

Click no card → navega para Árvore da rodada (FR2).

### Cores dos estados

| Estado      | Cor do header | Ícone |
|-------------|---------------|-------|
| spec        | cinza         | 📄    |
| plan        | azul          | 📋    |
| implement   | verde         | 🔨    |
| crítica     | amarelo       | ⚖     |
| integrate   | roxo          | 🔀    |
| done        | verde escuro  | ✓     |

### Query

`GET /api/rodadas` (já existe de T6). Frontend agrupa por `passo_atual`:
- `spec`, `plan`, `implement`, `crítica`, `integrate` = colunas
- `fechada_em != null` = coluna "done" (ou oculta com toggle)

## 2. Árvore da rodada (FR2)

Tree view dos passos de uma rodada. Cada passo é um nó com:
- nome do passo (spec, plan, T1, T2, ..., crítica, integrate)
- quem executou (sessão)
- tempo (entrada_em → saida_em)
- resultado (ok, erro, skip, ou null se aberto)

```
┌─────────────┬──────────────────────────────────────────────────────┐
│ M Maestro   │  ← Rodadas > R001                                    │
│             │                                                      │
│ ▤ Board     │  R001: Workflow painel                               │
│ ⬚ Rodadas   │  Aberta por Gerente · 02/10 10:00                    │
│ ⇢ Roadmap   │                                                      │
│ ⚖ Decisões │  ├── spec ✓  Gerente    1h00   ok                     │
│ ...         │  ├── plan ✓  Gerente    0h30   ok                     │
│             │  ├── implement                                        │
│             │  │   ├── T1 ✓  W09       2h00   ok                    │
│             │  │   ├── T6 ✓  W03       1h00   ok                    │
│             │  │   ├── T7 ✓  W03       0h30   ok                    │
│             │  │   ├── T8 ✓  W03       0h15   ok                    │
│             │  │   ├── T9 ✓  W03       0h45   ok                    │
│             │  │   └── T11 ✓ W03       0h10   ok                    │
│             │  ├── crítica                                          │
│             │  │   ├── W13 RETURN → fix ✓  W03  0h20  ok            │
│             │  │   └── W08 APPROVE  ✓  W08  0h15  ok                │
│             │  ├── integrate ⏳  W07  —  aberto                     │
│             │  └── deploy                                           │
│             │                                                      │
│             │  Tempo total: 7h05 · Passos: 11/12 · Aberto: 1       │
└─────────────┴──────────────────────────────────────────────────────┘
```

### Nó da árvore

```
├── {passo} {status} {sessao} {tempo} {resultado}
```

- **status**: `✓` = saida_em preenchido, `⏳` = aberto, `↻` = reaberto
- **tempo**: `saida_em - entrada_em` em horas, `—` se aberto
- **resultado**: `ok`, `erro`, `skip`, ou vazio

### Ramificação

Passos paralelos (múltiplos workers no mesmo passo) ficam como filhos
do mesmo pai. A árvore é montada pela ordem de `entrada_em` dentro de
cada passo. Transições (tabela `transicoes` do W09) definem a ordem
esperada; desvios aparecem com `↻`.

### Query

`GET /api/rodadas?id=R001` retorna a rodada com `passos[]` (já existe
de T6). Frontend monta a árvore agrupando passos por nome do passo pai
(usar campo `passo` como chave, transicoes para hierarquia).

## 3. Workflow por tarefa (FR3)

Tabela detalhada de cada tarefa dentro de uma rodada. Colunas:
Task, Descrição, Worker, Critério de aceite, Crítico, Status.

```
┌─────────────┬──────────────────────────────────────────────────────┐
│ M Maestro   │  ← Rodadas > R001 > Tarefas                          │
│             │                                                      │
│ ▤ Board     │  R001: Workflow painel — Tarefas                     │
│ ⬚ Rodadas   │                                                      │
│ ⇢ Roadmap   │  ┌─────┬───────────────┬───────┬──────────────────┐  │
│ ⚖ Decisões │  │Task │ Descrição     │Worker │ Critério         │  │
│ ...         │  ├─────┼───────────────┼───────┼──────────────────┤  │
│             │  │ T1  │ Schema WAL   │ W09   │ Tabelas + WAL    │  │
│             │  │     │              │       │ Crítico: W13     │  │
│             │  │     │              │       │ Status: ✓ ok     │  │
│             │  ├─────┼───────────────┼───────┼──────────────────┤  │
│             │  │ T6  │ Roadmap      │ W03   │ v_rodadas retorna│  │
│             │  │     │ rodadas      │       │ passo+quem+tempo │  │
│             │  │     │              │       │ Crítico: W13     │  │
│             │  │     │              │       │ Status: ✓ ok     │  │
│             │  ├─────┼───────────────┼───────┼──────────────────┤  │
│             │  │ T7  │ Equipe 19   │ W03   │ 19 sessões sem   │  │
│             │  │     │ sessões     │       │ W10 no JSON      │  │
│             │  │     │              │       │ Crítico: W08     │  │
│             │  │     │              │       │ Status: ✓ ok     │  │
│             │  ├─────┼───────────────┼───────┼──────────────────┤  │
│             │  │ T9  │ Erro de     │ W03   │ erros_leitura com │  │
│             │  │     │ leitura     │       │ caminho+motivo   │  │
│             │  │     │              │       │ Crítico: W13     │  │
│             │  │     │              │       │ Status: ✓ ok     │  │
│             │  └─────┴───────────────┴───────┴──────────────────┘  │
│             │                                                      │
│             │  4/12 tarefas · 4 ok · 0 erro · 8 pendentes         │
└─────────────┴──────────────────────────────────────────────────────┘
```

### Linha da tarefa

Cada tarefa ocupa 3 linhas na tabela:
1. **Task + Descrição + Worker + Critério** (resumo)
2. **Crítico:** quem critica + veredito (APPROVE/RETURN/PENDING)
3. **Status:** ✓ ok / ✗ erro / ⏳ pendente / ↻ reaberto

### Query

Dados vem de `passos` onde `passo` começa com "T" (tarefa).
O critério e o crítico são lidos do `tasks.md` da spec (campo
`evidencia_json` pode conter o hash e o veredito do crítico).

Alternativa: `GET /api/rodadas?id=R001` + join com `specs.tasks`
para o critério. O crítico vem do `tasks.md` (campo "Crítico:").

## Navegação

```
Board (FR1) ──click card──→ Árvore (FR2) ──click tarefa──→ Tarefas (FR3)
     ↑                                              │
     └────────────── ← Voltar ←────────────────────┘
```

- **Board**: `#view=rodadas` (novo item na sidebar)
- **Árvore**: `#view=rodada&id=R001`
- **Tarefas**: `#view=rodada-tarefas&id=R001`

## Dependências

- Tabelas `rodadas` e `passos` (W09, spec 064 — já existem)
- `v_rodadas` (W03, T6 — já existe em `server.py`)
- `transicoes` (W09, spec 064 — para hierarquia da árvore)
- `tasks.md` da spec (para critério e crítico na view de tarefas)

## Não inclui

- Drag-and-drop no board (FR4 — futura)
- Edição de tarefas pela UI (FR5 — futura)
- Filtros por worker ou data (FR6 — futura)
