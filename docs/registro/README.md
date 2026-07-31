# Registro de decisões — índice consultável por máquina

> Absorção do estudo `maestro-02` (Apêndice A do handbook; spec 008). Diferente do
> original, aqui o registro é **versionado** — é governança, não estado de sessão.

## O protocolo

- **A prosa mora no ADR** (`docs/adr/`): contexto, alternativas, racional, consequências.
- **`decisoes.jsonl` é o índice de máquina**: 1 JSON por linha, **append-only** — nunca
  edite linha passada; correção = nova linha (`status: "superada por ..."`). Assim um
  agente consulta "as últimas N decisões" sem carregar os ADRs inteiros no contexto.

## Formato de cada linha

```json
{"id":"adr-0008","data":"2026-07-31","titulo":"Avaliação do ecossistema SDD","status":"aceita","registro":"docs/adr/0008-avaliacao-ecossistema-sdd.md","ciclo":"007"}
```

| Campo | Obrigatório | Conteúdo |
|---|---|---|
| `id` | ✅ | `adr-NNNN` ou `gate-NNN-<slug>` (decisão de gate de ciclo) |
| `data` | ✅ | `YYYY-MM-DD` |
| `titulo` | ✅ | uma linha |
| `status` | ✅ | `aceita` · `proposta` · `superada por <id>` |
| `registro` | ✅ | caminho do documento em prosa (ADR, qa-report, spec) |
| `ciclo` | — | `NNN` quando nasce de um ciclo |

## Como registrar

```bash
scripts/registrar-decisao.sh '{"id":"gate-008-merge","data":"2026-07-31","titulo":"...","status":"aceita","registro":"specs/008-.../qa-report.md"}'
```

O script valida o JSON e os campos obrigatórios e **apenas anexa** — nunca reescreve.
Consulta rápida: `tail -5 docs/registro/decisoes.jsonl`.
