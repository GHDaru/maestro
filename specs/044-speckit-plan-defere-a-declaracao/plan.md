# Plano 044 — O `/speckit.plan` defere à tabela de declaração

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-07

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec antes; os quatro FR saíram do achado da revisão do 042. |
| II. Orquestração governada | Emendar peça vendorizada é decisão de proveniência — foi **do Steward**, escolhida entre três saídas apresentadas. |
| III. Reversibilidade / gates | Classe baixa: texto. Reverter é um commit; nada gerado, nada apagado, nada migrado. |
| IV. Test-first / DoD verificável | O critério é textual e verificável por leitura do arquivo instalado; a verificação real é a revisão independente lendo o comando emendado contra o template. |
| V. Economia de contexto / fronteira | Só o `speckit.plan.md`. Os outros comandos herdam o método pelos templates e não foram tocados. |
| VI. Artefatos vivos | É o princípio que decide o `quickstart.md`: função já servida pela jornada e pelas receitas, então não se duplica. |
| VII. Governança leve / YAGNI | Nenhum token novo, nenhum artefato novo. `quickstart` **não** entra no conjunto `ART:` só para poder ser declarado ausente. |
| VIII. Comunicação inteligível | Nenhuma sigla nova; `ART:` já definido em `docs/governance/artifacts.md`. |

## Artefatos deste ciclo (declarar os cinco — silêncio não é decisão)

| Artefato | Declaração | Por quê |
|---|---|---|
| `research.md` | `ART:research=no` | nenhuma incógnita: a contradição é textual e já estava medida no ciclo 042 |
| `data-model.md` | `ART:data-model=no` | não há entidade nem relação — é texto de comando |
| `contracts/` | `ART:contracts=no` | nada atravessa fronteira entre partes |
| `checklist.md` | `ART:checklist=no` | a DoD da spec cobre os quatro requisitos |
| `ux-design.md` | `ART:ux-design=no` | nenhuma tela é tocada |

Este plano é, ele próprio, o exemplo do que o comando emendado passa a ler.

## Como

**Três pontos do comando, um princípio.** O comando não deixa de saber gerar os artefatos —
ele passa a perguntar antes:

| Onde | Antes | Depois |
|---|---|---|
| passo 3 (roteiro) | "Phase 0: Generate research.md" · "Phase 1: Generate data-model.md, contracts/, quickstart.md" | preenche a tabela de declaração **primeiro**, e ela decide o que as fases produzem |
| saída da fase 0 | `research.md` sempre | `research.md` **só** com `ART:research=yes` |
| saída da fase 1 | `data-model.md, /contracts/*, quickstart.md, agent file` | os declarados `=yes` + arquivo do agente |

**O `quickstart.md` sai por princípio, não por gosto.** A função dele — "como alguém
experimenta isto" — já é servida pelo documento de jornada e pelas receitas. Duplicar
função servida é o que o princípio VI proíbe, e a razão fica escrita no comando **e** no
`UPSTREAM.md`, para quem vier do upstream entender por que o arquivo sumiu.

**A proveniência é o que torna isto legítimo.** A regra 1 do `UPSTREAM.md` nunca proibiu
adaptar — ela proíbe **absorver por acidente**, e exige que a adaptação entre por spec e
seja registrada. O que faltava era a regra que diz o que fazer quando a peça vendorizada
**contradiz** o método. Ela agora existe como regra 2, com este caso como precedente:
divergir sem registrar é o que transforma vendorizar em bifurcar.

## Verificação (DoD)

```bash
scripts/package-plugin.sh --verify   # editar comando vendorizado é o que este portão guarda
grep -n "ART:research=yes" .claude/commands/speckit.plan.md    # a fase 0 defere
grep -n "quickstart.md\` is not produced" .claude/commands/speckit.plan.md
grep -n "speckit.plan.md" .specify/UPSTREAM.md                 # estado: Adaptado
scripts/check-language.sh · check-install.sh · check-conformance.sh · check-links.sh
```

Mais a revisão independente lendo o comando emendado **contra** o `plan-template.md`, que é
o par que estava contraditório.
