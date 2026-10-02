# UX Design 065 — Board enxuto, rodada navegável e workflow por tarefa

- **Spec**: `spec.md` · **Date**: 2026-10-02 · **Author**: W03

## Visão geral

Três views novas no painel, cobrindo os 13 FRs da spec 065:

1. **Board enxuto** — 3 exceções no topo + linha por sessão (FR1, FR2, FR3, FR4, FR13)
2. **Árvore da rodada** — árvore navegável derivada de convenções (FR8, FR9, FR12)
3. **Workflow por tarefa** — passo atual, linha do tempo, evidência (FR5, FR6, FR7, FR10)
4. **Roadmap** — raias por ciclo com gate do push (FR11)

## 1. Board enxuto (FR1, FR2, FR3, FR4, FR13)

### FR1 — 3 exceções no topo

Barra no topo do board com 3 cards de exceção. Cada card só fica vermelho
quando o contador for maior que zero; caso contrário, cinza.

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚠ Precisam do Gilsiley (2)   ⚠ Gate do push (1)   ⚠ Sem tarefa 2 ciclos (0)  │
└──────────────────────────────────────────────────────────────────┘
```

- **Precisam do Gilsiley**: prompts e gates humanos pendentes (vem de
  `transicoes` onde `resultado IS NULL AND quem = 'Gilsiley'`)
- **Gate do push**: itens restantes no gate (vem de `passos` onde
  `passo = 'push' AND saida_em IS NULL`)
- **Sem tarefa há 2 ciclos** (FR13): workers com status "sem tarefa" em
  2 ciclos consecutivos do loop de status de 30 min (~60 min). Vem do
  `status_workers` comparando os últimos 2 ciclos. Não confundir com
  2 rodadas — são 2 ciclos de status (Clarify #3 da spec).

### FR2 — Linha por sessão com 5 colunas

Abaixo das exceções, uma linha por sessão ativa:

```
┌─────────────┬──────────┬────────────────────┬──────────┬─────────┐
│ Sessão      │ Estado   │ Peça / Passo       │ Esperando│ Há quanto│
├─────────────┼──────────┼────────────────────┼──────────┼─────────┤
│ W03         │ ● busy   │ 065 / ux-design    │ W13+W01  │ 15 min  │
│ W09         │ ● busy   │ 064 / T1 schema    │ —        │ 2 h     │
│ W13         │ ○ idle   │ —                  │ —        │ —       │
│ Gerente02   │ ● busy   │ 065 / despachar    │ W13,W01  │ 5 min   │
└─────────────┴──────────┴────────────────────┴──────────┴─────────┘
```

- **Sessão**: nome da sessão (W03, Gerente02, etc.)
- **Estado**: pill colorido (● busy = verde, ○ idle = cinza, ⚠ erro = vermelho)
- **Peça / Passo**: spec/tarefa atual e passo do workflow
- **Esperando**: quem a sessão está esperando (crítico, Gilsiley, ou —)
- **Há quanto**: tempo desde a última atividade

### FR3 — Filtro "só exceções" por padrão

O board abre no filtro "só exceções" — só mostra sessões com estado
de exceção (erro, esperando, sem tarefa). Um toggle "Mostrar todas"
no canto superior direito revela a lista completa.

```
[ ☑ Só exceções ]  [ Mostrar todas ]    ← toggle, abre em "Só exceções"
```

### FR4 — Hook event como "última atividade há N min"

Eventos de hook (tabela `eventos` da 064) não geram linha separada no
board. Eles atualizam a coluna "Há quanto" da sessão correspondente,
mostrando "última atividade há N min". O hook é ingerido em
`ingest.py` e atualiza `status_workers.ultima_atividade`.

## 2. Árvore da rodada (FR8, FR9, FR12)

### FR8 — Árvore navegável

Tree view da rodada com 4 ramos principais, conforme spec:

```
R001: Workflow painel
├── spec
│   ├── FR1 ✓  test_fr1_excecoes_topo
│   ├── FR2 ✓  test_fr2_linha_sessao
│   ├── ...
│   └── FR13 ✓ test_fr13_sem_tarefa_2_ciclos
├── plan
│   ├── ux-design.md ✓
│   └── tasks.md ✓
├── tasks
│   ├── T1 ✓  W09  schema_workflow.sql
│   ├── T6 ✓  W03  v_rodadas em server.py
│   └── T9 ✓  W03  erros_leitura em ingest.py
└── críticas
    ├── W13 RETURN → fix ✓  W03
    └── W08 APPROVE ✓
```

Cada nó mostra: nome, status (✓/⏳/↻), e referência (teste, artefato, sessão).

### FR9 — Click no nó → artefato à direita com breadcrumb

Click num nó abre o artefato no painel direito com breadcrumb e chips
de evidência:

```
┌──────────────────────────────┬──────────────────────────────────┐
│ R001                         │ 064 › spec › FR13                │
│ ├── spec                     │                                  │
│ │   ├── FR1 ✓               │ FR13: SE status "sem tarefa"     │
│ │   ├── ...                  │ em 2 ciclos consecutivos,        │
│ │   └── FR13 ✓ ← click      │ THEN contar na exceção.          │
│ ├── plan                     │                                  │
│ ...                          │ Teste: test_fr13_sem_tarefa_...  │
│                              │ Hash: a145b07 ✓                  │
│                              │ [chip verde: evidência confere]  │
└──────────────────────────────┴──────────────────────────────────┘
```

Breadcrumb: `064 › spec › FR13`. Chips:
- Verde: evidência confere com hash
- Amarelo: evidência diverge do hash (FR7) ou requisito sem teste (FR10)

### FR12 — Árvore derivada de convenções

A árvore é montada automaticamente no ingest (não em tempo real),
materializada na tabela `arvore_rodada` (Clarify #2 da spec). As
convenções que guiam a derivação:

| Convenção | Exemplo | Deriva |
|------------|---------|--------|
| ID no spec.md | `FR13` | nó folha sob spec |
| Tarefa cita requisito | `T2 → FR13` | T2 filho de FR13 |
| Commit cita tarefa | `064 T2: …` | commit ligado a T2 |
| Teste cita requisito | `test_fr13_…` | teste filho de FR13 |

Query: `GET /api/rodadas?id=R001` retorna a árvore materializada de
`arvore_rodada` para a rodada.

## 3. Workflow por tarefa (FR5, FR6, FR7, FR10)

### FR5 — Passo atual + tempo por tarefa

Cada tarefa mostra o passo atual do workflow e o tempo nele:

```
T9  Erro de leitura    W03    Passo: crítica    20 min
```

Dados de `passos` onde `passo` começa com "T". Passo atual = último
passo com `entrada_em` preenchido e `saida_em` NULL.

### FR6 — Click na tarefa → linha do tempo

Click numa tarefa abre a linha do tempo dos passos:

```
T9: Erro de leitura (W03)
┌────────────┬──────────────┬────────────┬────────┬──────────┬──────────┐
│ Entrada    │ Resumo       │ Saída      │ Sessão │ Hash     │ Evidência │
├────────────┼──────────────┼────────────┼────────┼──────────┼──────────┤
│ 02/10 14:00│ T9 red test  │ 02/10 14:30│ W03    │ 58cf24e  │ ✓ teste   │
│ 02/10 14:30│ T9 green     │ 02/10 15:00│ W03    │ 2f57ec7  │ ✓ teste   │
│ 02/10 15:00│ T9+T9b+T11   │ 02/10 16:00│ W03    │ a145b07  │ ✓ runner2 │
│ 02/10 16:00│ fix W13      │ 02/10 16:20│ W03    │ 41f3b60  │ ✓ runner2 │
│ 02/10 16:20│ crítica W13  │ —          │ W13    │ —        │ ⏳ aguard  │
└────────────┴──────────────┴────────────┴────────┴──────────┴──────────┘

Próximo passo: aguarda veredito W13.
Evidência faltante: veredito APPROVE de W13.
```

### FR7 — Evidência ≠ hash → chip amarelo

Se `evidencia_json.hash` não bater com o hash do commit da tarefa,
o card e a linha do tempo mostram chip amarelo:

```
┌─────────────┐
│ T9  ⚠       │  ← chip amarelo
│ hash diverge│
│ 41f3b60     │
│ ≠ a145b07   │
└─────────────┘
```

### FR10 — Requisito sem teste → chip amarelo "descoberto"

Onde um requisito (FR) não tem teste ligado (nenhum `test_fr*_…` na
árvore), o nó mostra chip amarelo "descoberto":

```
├── FR7 ⚠ descoberto    ← sem teste ligado
├── FR8 ✓ test_fr8_arvore
```

Query: `GET /api/rodadas?id=R001` + join com `arvore_rodada` onde
`tipo = 'teste' AND pai = FR_id`. Se vazio, marca como descoberto.

## 4. Roadmap (FR11)

Raias por ciclo (atual, próximo, depois) com um card por rodada.
Cada card tem barra de progresso dos 15 passos, gates humanos
pendentes destacados, e gate do push no topo.

```
┌──────────────────────────────────────────────────────────────┐
│ Ciclo atual              │ Próximo ciclo    │ Depois          │
├──────────────────────────┼──────────────────┼─────────────────┤
│ ┌──────────────────────┐ │ ┌──────────────┐ │ ┌─────────────┐ │
│ │ ⚠ Gate push (1)     │ │ │ R003 Impacto │ │ │ R004 Excel  │ │
│ │ R001 Workflow        │ │ │ W08 60%      │ │ │ —  0%       │ │
│ │ ████████████░░░ 80%  │ │ │ ░░░░░░░░░░░░ │ │ │ ░░░░░░░░░░░ │ │
│ │ W03/W09/W13/W08     │ │ └──────────────┘ │ └─────────────┘ │
│ │ Gates: Gilsiley (2)  │ │                  │                 │
│ └──────────────────────┘ │                  │                 │
│ ┌──────────────────────┐ │                  │                 │
│ │ R002 Board nav       │ │                  │                 │
│ │ ██████░░░░░░░░░ 40%  │ │                  │                 │
│ │ W03/W13/W01          │ │                  │                 │
│ └──────────────────────┘ │                  │                 │
└──────────────────────────┴──────────────────┴─────────────────┘
```

- **Gate do push no topo** do card (FR1): contador de itens restantes
- **Barra de progresso**: passos concluídos / 15 passos do workflow
- **Gates humanos pendentes**: destacados com ícone ⚠

## Navegação

```
Board (FR1-FR4,FR13) ──click sessão──→ Árvore (FR8,FR9,FR12)
                                    │
                                    └──click tarefa──→ Workflow (FR5-FR7,FR10)

Roadmap (FR11) ──click card──→ Árvore
```

- **Board**: `#view=board` (novo item na sidebar)
- **Árvore**: `#view=rodada&id=R001`
- **Tarefas**: `#view=tarefa&id=R001&task=T9`
- **Roadmap**: `#view=roadmap`

## Estados de erro e vazio

- **API falha**: mensagem "Não foi possível carregar os dados. [Tentar novamente]"
  no lugar da view. Não mostra dados parciais; a view inteira fica com o erro.
- **Sem rodadas**: "Nenhuma rodada encontrada." no centro da view, com ícone.
- **Rodada sem passos**: "Esta rodada ainda não tem passos registrados." na
  view de Árvore. O nó raiz aparece, mas sem filhos.
- **Tarefa sem passos**: "Esta tarefa ainda não começou." na view de Workflow.
- **Sessão sem peça**: colunas "Peça / Passo", "Esperando" e "Há quanto"
  mostram "—" (em-dash não; traço simples, regra R11).

## Dependências

- Tabelas `rodadas`, `passos`, `transicoes` (W09, spec 064 — já existem)
- Tabela `arvore_rodada` (nova, materializada no ingest — Clarify #2)
- Tabela `status_workers` (para FR13 — sem tarefa há 2 ciclos)
- `v_rodadas` (W03, T6 — já existe em `server.py`)
- `tasks.md` da spec (para critério e crítico na view de tarefas)

## Out of scope (alinhado com a spec)

- Edição de artefatos pela árvore (só leitura/navegação)
- Notificações push (fila outbox da 064 já existe)
- Deploy do painel (instalação pela Assistente após APPROVE)
