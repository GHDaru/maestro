# Plano 045 — A quarta ocorrência vira forma, e a v0.1.0 é fechada

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-07

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec antes; a correção do FR1 foi **pré-comprometida** pelo achado-043, não improvisada agora. |
| II. Orquestração governada | O diagnóstico da quarta ocorrência e o corte de versão foram decisão do Steward; eu propus, ele escolheu. |
| III. Reversibilidade / gates | A tag é o item irreversível: uma vez empurrada, terceiros a veem. Mitigado por ela ser **anotada** (carrega a mensagem do que é) e por apontar para um `main` com onze portões verdes. |
| IV. Test-first / DoD verificável | O portão do FR2 foi escrito e **visto falhar** antes de o template mudar. |
| V. Economia de contexto / fronteira | A reorganização das subseções repetidas do changelog ficou **fora**, com razão escrita: edição em massa junto de corte de versão é o anti-padrão 18. |
| VI. Artefatos vivos | É o princípio que decide o FR1: caixa na spec duplica a função do `qa-report`. |
| VII. Governança leve / YAGNI | A correção **remove** forma em vez de acrescentar: uma caixa a menos, nenhum campo novo. |
| VIII. Comunicação inteligível | DoD e SemVer (*Semantic Versioning*, versionamento semântico) por extenso na primeira ocorrência. |

## Artefatos deste ciclo (declarar os cinco — silêncio não é decisão)

| Artefato | Declaração | Por quê |
|---|---|---|
| `research.md` | `ART:research=no` | nenhuma incógnita: o diagnóstico foi pré-comprometido e o corte é bookkeeping |
| `data-model.md` | `ART:data-model=no` | não há entidade nem relação |
| `contracts/` | `ART:contracts=no` | nada atravessa fronteira entre partes |
| `checklist.md` | `ART:checklist=no` | os cinco critérios da spec cobrem |
| `ux-design.md` | `ART:ux-design=no` | nenhuma tela é tocada |

## Como

**A correção é subtrativa.** Quatro ocorrências em dois tokens diferentes dizem que o
problema não é atenção — é uma forma que convida ao erro. Instruir já foi tentado no ciclo
043 e falhou no 044, noutro token. Então a caixa **sai**: o template e o gerador passam a
listar critérios como marcadores simples, e `check-conformance.sh` reprova uma spec ≥045 que
tenha caixa ali, nomeando a duplicação de função.

Piso em 045 (`MAESTRO_MIN_CYCLE_CRITERIA`), pelo mesmo motivo de sempre: retroatividade
transforma portão em ruído, e as 44 specs antigas mantêm suas caixas como estão.

**O corte é uma declaração, não uma cerimônia.** A `[0.1.0]` recebe uma nota de release que
diz **o que a versão é** (a linha de base: método instalável, doze portões, camada de
axiomas, corpus de evals com um caso provado) e **o que ela reconhecidamente não tem** (o
serviço do companion não publicado, um caso de eval aposentado sem substituto, e a dívida
declarada dos ciclos anteriores ao piso de cada portão). Versão que só lista conquistas é
release note de marketing.

**A tag é anotada e vem depois da promoção**, nesta ordem: ciclo verde → gate humano →
`promote-main.sh` → tag em `main`. Tag em `dev` apontaria para um commit que pode ser
reescrito; em `main`, ela identifica o que foi de fato aprovado.

## Verificação (DoD)

```bash
scripts/check-conformance.sh                 # inclui a regra nova, com piso em 045
grep -c '^- \[' specs/045-fechar-v0-1-0/spec.md   # → 0
grep -n '^## \[0.1.0\]' CHANGELOG.md
git tag -n9 v0.1.0                           # anotada, com a mensagem do que é
```

Mais a bateria completa dos onze portões e a revisão independente.
