# Plano 038 — Divisão em dois repositórios (fatia 1)

- **Spec**: `spec.md` · **Raia**: infra · **Data**: 2026-08-06

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec antes; FR1–FR3 viraram literalmente as três invariantes do portão. |
| II. Orquestração governada | As duas incógnitas do corte (onde fica a memória; o site continua completo) foram ao **gate humano** antes de qualquer linha de código — não eram minhas para decidir. |
| III. Reversibilidade / gates | **É o princípio que define este ciclo.** Divisão de repositório é alta irreversibilidade, então a reversibilidade foi *engenheirada*: a fatia 1 não move nada, e produz o critério que torna a fatia 2 mecânica. Custo de desfazer hoje: apagar dois arquivos. |
| IV. Test-first / DoD verificável | Portão escrito antes da classificação e visto acusar nas três condições (órfão, dupla reivindicação, página publicada sem espelho). |
| V. Economia de contexto / fronteira | O ciclo é a fronteira: decidir o corte, não executá-lo. A fatia 2 é outro ciclo, com gate próprio. |
| VI. Artefatos vivos | `boundary.json` é fonte única consumida pelo portão — não é lista em prosa. Falha alto quando um arquivo novo não é classificado. |
| VII. Governança leve / YAGNI | Um JSON e um script. Sem ferramenta de migração, sem submódulo ainda, sem renomear nada. |
| VIII. Comunicação inteligível | ADR, C10, DoD e FR por extenso na primeira ocorrência de cada artefato. |

## Como

**O corte deriva de C10**, não de gosto: `reader: machine` × `reader: human` é o campo que
decide cada linha de `boundary.json`. Onde o corolário não decide sozinho — a memória, que
máquinas e pessoas leem — a decisão foi ao gate.

**As três invariantes** são as três formas de uma divisão de repositório dar errado em
silêncio, e todas são verificáveis **enquanto os arquivos ainda estão juntos**:

| # | Invariante | O que ela impede |
|---|---|---|
| 1 | todo arquivo rastreado tem exatamente um dono | arquivo esquecido na origem; arquivo em duplicidade que passa a divergir |
| 2 | todo caminho espelhado é do toolkit | espelho sem fonte — que é um fork com outro nome |
| 3 | toda página do sumário vem do guia ou de um espelho | o site perder páginas no dia da divisão, sem ninguém notar |

A invariante 3 é a que justifica o ciclo. Sem ela, a divisão levaria embora nove páginas
publicadas — governança, agentes, roadmap, índices — e o sintoma apareceria semanas depois,
como link morto para um leitor.

**Longest prefix wins** na resolução de dono: `docs/adr/README.md` espelhado e `docs/adr/`
do toolkit não conflitam, porque o caminho mais específico decide. Um caminho reivindicado
por dois donos no **mesmo** comprimento é `AMBIGUOUS` e falha — ambiguidade silenciosa é
pior que erro.

## Verificação (DoD)

```bash
scripts/check-boundary.sh     # 3 invariantes; verde só quando a divisão é decidível
scripts/check-links.sh        # nada quebrou
scripts/check-language.sh     # o novo script é instalável, logo inglês
node publicar/build.mjs       # o site continua saindo
```

Prova de que o portão acusa: três injeções deliberadas (arquivo fora de toda classificação;
`docs/governance/` removido dos espelhados; `docs/governance/` reivindicado pelos dois
repositórios), cada uma com a saída vermelha no `qa-report.md`.
