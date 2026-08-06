# Relatório de QA 037 — Evals: linha de base para saída não-determinística

- **Data**: 2026-08-06 · **Raia**: plena · **Veredito**: aprovado **com vermelho declarado**

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/check-agents.sh` | verde | ✅ |
| `scripts/check-roles.sh` | verde | ✅ |
| `scripts/check-install.sh` | verde | ✅ |
| `scripts/check-language.sh` | verde, agora cobrindo `evals/` e `/eval` | ✅ (15 alvos) |
| `scripts/check-links.sh` | verde | ✅ |
| `scripts/check-retro.sh` | verde | ✅ (o achado novo entra dentro do teto) |
| `scripts/check-chapters.sh` | verde | ✅ |
| `scripts/check-cycle.sh` | verde, raia justificada | ✅ (`037 — lane 'plena' with rationale`) |
| `node publicar/build.mjs` | verde | ✅ (37 páginas, links internos OK) |
| `scripts/check-evals.sh` | **vermelho**, 2 linhas de base pendentes | ⚠️ **vermelho, como previsto na spec** |

## Prova de que o portão acusa (princípio IV, corolário C2)

O portão foi escrito **antes** dos casos e visto falhar em quatro condições distintas. Não
é a mesma falha quatro vezes: cada uma percorre um ramo diferente do script.

**1. Corpus inexistente** — o primeiro estado real, antes de `evals/` existir:

```
── Evaluation corpus (T7 / C11) ──
✗ evals/ does not exist — there is no corpus to keep honest.
exit=1
```

**2. Asserção que não discrimina** — caso `999-proof`, com `MUST-FIND` e sem `MUST-NOT-CLAIM`:

```
✗ expect.md has no MUST-NOT-CLAIM: — with no negative side the case does not discriminate
```

**3. Linha de base defasada** — `Target-commit: deadbee` gravado contra um alvo que já
tinha andado. O portão não só acusa: nomeia os dois lados da deriva.

```
✗ stale baseline — target moved deadbee → 7caefbc; re-run /eval
```

**4. Arquivo ausente** — `expect.md` removido:

```
✗ missing expect.md
```

O caso `999-proof` era descartável e foi removido depois da prova (`rm -rf evals/999-proof`).

## Cobertura dos requisitos

- **FR1** (teorema derivado, com evidência) — ✅ T7 em `axioms.md`, derivado de A2 e A4, com
  a evidência medida: treze agentes, trinta e seis ciclos, nenhuma linha de base; e o
  comentário de `check-cycle.sh:8` como prova de que o limite era conhecido. Corolário C11.
  Versão 1.0.0 → 1.1.0; ADR 0016 registra a emenda.
- **FR2** (alvo real + asserções que discriminam) — ✅ provado em (2) acima. Os dois casos
  declaram alvo existente: `review.md` e `process-guardian.md`.
- **FR3** (defasagem) — ✅ provado em (3). É a forcing function do corolário C11.
- **FR4** (nunca visto discriminando) — ✅ é o vermelho da entrega: `First-red: pending` nos
  dois casos, contados explicitamente (`pending baselines: 2`).
- **FR5** (comando para produzir a linha de base) — ✅ `.claude/commands/eval.md`, com a
  exigência de contexto fresco (T2) e a regra de que `First-red` só sai de `pending` quando
  o caso tiver **de fato** rejeitado uma resposta.

## O vermelho, explicado

`check-evals.sh` sai 1 na entrega. Isso é o estado verdadeiro, não uma falha do ciclo:

```
cases: 2 · pending baselines: 2
✗ evaluation corpus is not healthy (see above).
```

Executar os dois casos exige modelo no laço em contexto fresco, o que este ciclo não fez.
As alternativas eram piores: marcar `First-red` sem ter visto o caso reprovar nada seria
mentira gravada em arquivo; e afrouxar o portão para tolerar pendência seria o portão
medindo o proxy (anti-padrão 13). Precedente direto: `check-install.sh` nasceu vermelho no
ciclo 021 com deriva real de três ciclos — foi vermelho que revelou a deriva.

A dívida está no índice de decisões como `achado-037-linhas-de-base-pendentes` (status
`aberta`), ao alcance do gatilho da retro — ou seja, ela não depende de alguém lembrar.

## O que este ciclo NÃO entrega (limite honesto)

- **Nenhuma medida de qualidade ainda.** Entregamos a forma; a medida é a metade que custa
  execução. Um leitor apressado da linha "F13 ✅" concluiria que os agentes estão avaliados.
  Eles não estão — por isso a linha do roadmap diz ⚠️ e não ✅.
- **Dois casos, treze agentes.** Cobertura declarada, não estimada. Cresce por gatilho
  (regressão observada), registrado no roadmap.
- **O julgamento das asserções continua sendo leitura humana ou de agente.** O eval reduz o
  julgamento; não o elimina. Afirmar o contrário seria o anti-padrão 13 aplicado justamente
  ao mecanismo criado para evitá-lo.
- **`evals/` não entra na integração contínua.** Por decisão (ADR 0016): um portão que exige
  chave de interface deixa de ser portão.

## Gate pendente

- Promoção `dev` → `main` aguarda aprovação humana. O gate humano aqui tem uma pergunta
  extra além do de sempre: **aceitar um portão que entrega vermelho** — ou exigir as duas
  linhas de base antes do merge.
