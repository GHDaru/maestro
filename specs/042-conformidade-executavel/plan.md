# Plano 042 — Conformidade executável: a cauda sobrevive ao artefato

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-07

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec antes; os seis FR saíram do defeito medido, não de ideia. |
| II. Orquestração governada | O portão mede artefatos, nunca julga qualidade — e diz por escrito que não sabe se alguém leu a evidência. O gate humano continua do humano. |
| III. Reversibilidade / gates | Classe baixa: texto, tokens e um script. Portão novo entra **com piso** (`MAESTRO_MIN_CYCLE_CONFORMANCE=42`), então nada retroage. |
| IV. Test-first / DoD verificável | Portão escrito **antes** dos templates, e a primeira execução foi vermelha contra um esqueleto recém-gerado — que é a prova do defeito. |
| V. Economia de contexto / fronteira | Não escrevi template para `research`/`data-model`/`contracts`: o catálogo diz quando se aplicam; o formato nasce do primeiro uso real. |
| VI. Artefatos vivos | O catálogo entra na superfície instalável, que é onde faltava. Nenhuma função duplicada: o portão não re-checa raia (é do `check-cycle`) nem papéis (é do `check-roles`). |
| VII. Governança leve / YAGNI | Três tokens e uma tabela. Nenhuma ferramenta nova, nenhum artefato novo por ciclo. |
| VIII. Comunicação inteligível | Siglas por extenso na primeira ocorrência de cada artefato novo; *token*, *cauda* e *conformidade* definidos onde aparecem. |

## Artefatos deste ciclo (declarar os cinco — silêncio não é decisão)

| Artefato | Declaração | Por quê |
|---|---|---|
| `research.md` | `ART:research=no` | nenhuma incógnita técnica: o defeito e o remédio foram medidos no próprio repositório |
| `data-model.md` | `ART:data-model=no` | não há entidade nem relação — é método, não produto |
| `contracts/` | `ART:contracts=no` | nada atravessa fronteira entre partes; os tokens são convenção interna de arquivo |
| `checklist.md` | `ART:checklist=no` | a DoD da spec cobre; checklist próprio seria cerimônia |
| `ux-design.md` | `ART:ux-design=no` | nenhuma tela é tocada |

## Como

**O movimento é um só: transformar omissão em declaração.** Silêncio não é auditável;
"não se aplica porque X" é. Daí saem as duas famílias de token:

| Token | Onde vive | O que impede |
|---|---|---|
| `ART:<artefato>=yes|no` | `plan.md` | o autor nunca olhar para os cinco — e o `ux-design` sumir sem ninguém decidir |
| `TAIL:review` · `TAIL:security` · `TAIL:gate` | `tasks.md` | a cauda existir só na spec e na memória, e evaporar na compactação |

Token e não prosa, porque prosa é reescrita e traduzida — o portão passaria a medir a
palavra em vez do fato. Mesmo raciocínio do campo `fecha` e do marcador `PT-DATA`.

**A evidência mora no `qa-report.md`**, não no checkbox. Marcação prova que alguém marcou.

**O gerador de esqueleto é mais importante que o template.** `new-cycle.sh` é o que se roda
de fato — todos os 42 ciclos daqui nasceram dele. Template certo com gerador errado produz
quarenta esqueletos não-conformes, que foi exatamente o que aconteceu.

**A camada de axiomas** ganha o que faltava para os três mecanismos derivarem de algo:
**C12** (o que sobrevive à compactação é o que está em artefato consumido — o resto é
apagado, não degradado) e **C13** (pergunta respondível de memória será respondida de
memória, e memória relata intenção).

## Verificação (DoD)

```bash
scripts/check-conformance.sh        # FR1–FR4, com piso no ciclo 042
scripts/check-conformance.sh 042    # este ciclo, verboso
scripts/check-install.sh · check-language.sh · check-links.sh · check-roles.sh
node publicar/build.mjs · scripts/package-plugin.sh --verify
```

Prova de que o portão acusa: quatro injeções — artefato não declarado; `=yes` sem o arquivo;
`tasks.md` sem token da cauda; passo aplicável sem evidência no relatório. Mais a quinta,
achada durante a construção: `n/a:` com razão de placeholder.
