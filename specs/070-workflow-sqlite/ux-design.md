# UX Design 064 — Wireframe do painel atualizado

- **Spec**: `spec.md` · **Date**: 2026-10-02 · **Author**: W03

## Layout geral

O painel mantém o layout de 232px (sidebar) + 1fr (main). As mudanças
de T6–T9b são aditivas: novos blocos dentro do conteúdo existente, sem
mudar a estrutura da página.

```
┌─────────────┬──────────────────────────────────────────────────┐
│ M Maestro   │  [aviso-velho: leitura velha: 2h3m desde o último]│
│ arquivos... │  [aviso-erro: Não leu esp/x.md: FileNotFoundError]│
│             │                                                  │
│ ▤ Board     │  Planejamento / Roadmap e specs                  │
│ ⇢ Roadmap   │  Do roadmap às tasks                             │
│ ⚖ Decisões  │                                                  │
│ ...         │  ┌─ Rodadas (1) ──────────────────────────────┐  │
│             │  │ ID  Desejo          Passo  Quem    Passos  │  │
│             │  │ R001 Workflow painel plan  Gerente spec:1h│  │
│             │  │                                  → plan:aberto│
│             │  └────────────────────────────────────────────┘  │
│             │                                                  │
│             │  ┌─ ola (15 specs) ───────────────────────────┐  │
│             │  │ #   Spec    Status   Tasks  Plan  QA       │  │
│             │  │ 064 Workflow Draft   0/12   ✓    falta     │  │
│             │  └────────────────────────────────────────────┘  │
│             │                                                  │
│             │  ┌─ Roadmap · Ciclo 1 ───────────────────────┐  │
│             │  │ P1  P2  P3  ...                            │  │
│             │  └────────────────────────────────────────────┘  │
└─────────────┴──────────────────────────────────────────────────┘
```

## T6 — Rodadas no roadmap

Nova seção no topo do roadmap, antes das specs. Tabela com colunas:
ID, Desejo, Passo atual (loz warn), Quem (avatar+nome), Passos (tempo),
Arquivo (link).

O passo atual é o último passo com `entrada_em` e sem `saida_em`.
O tempo de cada passo é `saida_em - entrada_em` em horas, ou "aberto"
se ainda sem saída.

## T7 — Equipe real (19 sessões)

A configuração `equipes` no `hindiana.json` passa a ter 4 grupos:

| Grupo | Sessões |
|---|---|
| Claude Desktop (4) | Office, Assistente, Reescrita, Testes Dev |
| Coordenação (3) | Gerente, Gerente02, Torre |
| Time do Gerente (6) | W02, W06, W07, W08, W09, W11 |
| Time do Gerente02 (6) | W01, W03, W04, W05, W12, W13 |

W10 saiu. O board de agentes mostra os 19 cards agrupados por raia.

## T8 — Aviso de leitura velha

Barra amarela entre a sidebar e o conteúdo, só visível quando
`ingerido_age_min > 60`:

```
┌─────────────────────────────────────────────────────┐
│ ⚠ leitura velha: 2h3m desde o último ingest         │
└─────────────────────────────────────────────────────┘
```

## T9 — Erro de leitura

Bloco entre o aviso de leitura velha e o conteúdo. Cada erro é uma
linha com o caminho (em `code`) e o motivo:

```
┌─────────────────────────────────────────────────────┐
│ Não leu esp/decisoes.md: FileNotFoundError: ...      │
│ Não leu ola/roteiro.md: PermissionError: ...         │
└─────────────────────────────────────────────────────┘
```

## T9b — Decisões aparecendo

A view de Decisões já existe (`vDecisoes`). A mudança é garantir que
o ingest lê os arquivos de decisões apontados pela config e a tabela
`decisoes` não fica vazia. Sem mudança de UI — só dados.
