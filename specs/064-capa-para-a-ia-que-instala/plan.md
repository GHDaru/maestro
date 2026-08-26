# Plan 064 — Capa para a IA que instala

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-26

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | ok — spec antes da edição; o defeito foi medido antes de escrever |
| II. Orquestração governada por humano | ok — o Steward pediu; a promoção continua sendo dele |
| III. Reversibilidade / portões de risco | ok — texto e uma comparação a mais; reversível por `git revert` |
| IV. Test-first / DoD verificável | ok — o portão de ids passa a ler o README, com mutação e contraprova |
| V. Economia de contexto / fronteira | ok — a página encurta o caminho da IA: comando primeiro, leitura depois |
| VI. Artefatos vivos | ok — README e portão mudam no mesmo commit; contagens ficam sob portão |
| VII. Governança leve / YAGNI | ok — raia leve; nenhum portão novo, só o escopo de um existente |
| VIII. Comunicação inteligível | ok — o que a IA precisa (comando, flags, ids, prova) em blocos nomeados |

## Artefatos deste ciclo (declare os cinco — silêncio não é decisão)

| Artefato | Declaração | Porquê |
|---|---|---|
| `research.md` | `ART:research=no` | nada a descobrir: o comportamento foi medido rodando o instalador |
| `data-model.md` | `ART:data-model=no` | não há entidade nem relação; é documentação e um portão |
| `contracts/` | `ART:contracts=no` | nada cruza fronteira — a tabela de ids **é** o contrato, e já está sob portão |
| `checklist.md` | `ART:checklist=no` | o DoD da spec cobre |
| `ux-design.md` | `ART:ux-design=no` | não toca tela |

## Como

1. Medir o defeito antes de escrever: rodar `bin/maestro init` sem terminal e registrar
   código de saída, mensagem e quantos arquivos foram escritos.
2. Reescrever a seção de instalação do README na ordem em que uma IA precisa: o comando que
   funciona sem terminal → as flags → os ids → o que cai no projeto → como provar → atualizar
   → os dois caminhos menores.
3. Abrir a seção "Se você é uma IA" com a bifurcação: instalar em outro projeto × trabalhar
   no método aqui.
4. Estender o portão de ids de `check-installed.sh` para ler **as duas páginas**, com extração
   **escopada** ao cabeçalho `| \`--ai\` |` — ler "qualquer linha cuja primeira célula é um
   token entre crases" engoliria as outras tabelas da página e acusaria a primeira coluna
   delas como id fantasma.
5. Ausência da tabela = reprovação, nas duas páginas.
6. Corrigir "12 capítulos" para 13, que é o que `docs/handbook/` tem.

## Verificação (DoD)

```bash
scripts/check-installed.sh                    # ids das duas páginas + contagens do README
scripts/check-flags.sh                        # flags prometidas × flags que o parser aceita
scripts/check-links.sh scripts/check-language.sh scripts/check-boundary.sh
scripts/check-conformance.sh --ticked-only
```

Mutação obrigatória, no portão que este ciclo alterou — três formas, cada uma vista
reprovando, mais a contraprova antes e depois:

1. o README publica `cursor`, que o instalador recusa;
2. o README perde a tabela inteira;
3. o README esquece um id que o instalador aceita.
