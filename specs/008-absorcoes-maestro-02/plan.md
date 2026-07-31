# Plan 008 — Absorções do estudo maestro-02

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-31

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 008; cada absorção veio de estudo + aprovação |
| II. Orquestração humano-governada | ✅ registro/retro **informam** o humano; nenhum artefato decide por ele |
| III. Reversibilidade / gates de risco | ✅ JSONL append-only (não reescreve história); scripts read-only exceto append |
| IV. Test-First / DoD verificável | ✅ DoD por parse JSON, bash -n, exit codes e greps |
| V. Economia de contexto / fronteira | ✅ FR5 dá **número** ao princípio; retro.sh evita recarregar contexto na cerimônia |
| VI. Artefatos vivos | ✅ apêndice anota incorporação; ADR muda status; CHANGELOG |
| VII. Governança leve / YAGNI | ✅ só as absorções aprovadas; telemetria de custo fica em observar |

**Sem violações.**

## Como

- **FR1**: JSONL = *índice de máquina*, ADR = *fonte em prosa* (não duplicar racional).
  Campos: `id, data, titulo, status, registro` (+ `ciclo` opcional). Script de append
  valida JSON com `python3 -m json.tool` e recusa edição (append-only por construção).
- **FR2**: `retro.sh` em bash puro (sem jq obrigatório): varre `specs/*/qa-report.md`
  (veredito, pendências), `tail` do decisoes.jsonl, contagens de inventário, e imprime
  as 3 perguntas-padrão da retro. Nunca escreve nada.
- **FR3**: skill no padrão da casa (frontmatter + gatilho + itens verificáveis), crédito
  ao maestro-02 na seção de fontes.
- **FR4/FR5**: subseções curtas nos caps. 10 e 04 (conceito + quando aplicar), sem
  reescrever os capítulos.
- **FR6**: seção "Sintaxe recomendada (EARS)" na skill `dod-verificavel` com 2 exemplos.
- **FR7**: editar status do ADR 0008 (Proposta→Aceito) + tabela do índice; nota no
  Apêndice A; entrada no CHANGELOG [Unreleased]; rebuild do site.

## Verificação (DoD)

- `python3 - <<< 'json.loads por linha'` sobre decisoes.jsonl → ok, ≥5 linhas.
- `bash -n scripts/{registrar-decisao,retro}.sh` + `test -x` + `./scripts/retro.sh` exit 0.
- `ls skills/*/SKILL.md | wc -l` = 4; grep frontmatter/gatilho em anti-padroes.
- `grep -l QUANDO skills/dod-verificavel/SKILL.md`; greps nos caps. 04/10; status do ADR.
