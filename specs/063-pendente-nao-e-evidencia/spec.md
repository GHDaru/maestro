# Spec 063 — "Pendente" não é evidência

- **Status**: Rascunho · **Raia**: plena · **Data**: 2026-08-23
- **Origem**: ao promover os ciclos 061 e 062, o `check-conformance.sh` imprimiu
  **`✓ TAIL:review evidence: pendente.`** — e promoveu. O portão que existe para impedir que
  uma caixa marcada valha por prova aceitou a palavra que **declara a ausência da prova**.

> **Raia**: plena. **Ambiguidade** baixa (o defeito é de uma função de quatro linhas);
> **raio** amplo — a função decide a evidência de **todos** os passos da cauda em **todos** os
> ciclos, e o portão que a usa passou a bloquear a CI no ciclo 061; **irreversibilidade** baixa.

## O quê e por quê

**Medido antes de escrever:**

| Fato | Como se sabe |
|---|---|
| `is_placeholder()` reconhece **três** coisas: vazio, `<`, `[` | `scripts/check-conformance.sh:135–138` |
| `pendente.` não é nenhuma das três, logo é aceito como evidência | os ciclos 061 e 062 saíram `✓` com exatamente esse texto |
| **Quatro** ciclos históricos escrevem ausência declarada no `TAIL:gate` | 042, 043, 044, 045: *"pendente: promoção `dev` → `main` aguardando"* |
| A revisão independente **não rodou** em 061 e 062 | dito no `qa-report` dos dois; rodou e reprovou em 053–060 |

### O defeito

`is_placeholder()` não reconhece *ausência de evidência*. Ele reconhece **a forma que o
`new-cycle.sh` gera** — um marcador entre `<` e `>`. Qualquer frase escrita por gente passa,
inclusive a frase cujo conteúdo é *"isto não foi feito"*.

É o anti-padrão 13 dentro do portão escrito para pegá-lo: mede a **presença de texto**, não a
presença de **fato**. E o custo já não é hipotético — dois ciclos foram promovidos com a
revisão independente ausente, e o portão marcou `✓` para ela nos dois.

### O que a correção não pode fazer

A palavra sozinha não decide. A evidência do `TAIL:gate` do ciclo 060 **contém** "pendente" no
meio de uma frase legítima. Uma busca solta reprovaria evidência boa — que é o defeito
espelhado, e foi exatamente o erro do ciclo 055, quando `grep -m1 "TAIL:x"` casou com a linha
errada e o remédio foi **ancorar**.

E ela não pode ser retroativa: os quatro ciclos de 042 a 045 escreveram a ausência **quando ela
era verdade**, e foram promovidos depois. Reprová-los hoje transforma o portão em ruído — o
precedente já está três vezes no próprio arquivo (`FLOOR`, `CRIT_FLOOR`, `MUT_FLOOR`).

## Requisitos funcionais

- **FR1**: `is_placeholder()` DEVERÁ tratar como não-evidência a **ausência declarada**, num
  vocabulário **fechado** e nos dois idiomas do repositório (`pendente`, `a fazer`,
  `aguardando`, `não executada`, `todo`, `tbd`, `pending`, `not run`, `n/d`).
- **FR2**: A regra DEVERÁ ser lida **do início** da evidência, nunca de qualquer posição —
  uma frase legítima que mencione a palavra no meio NÃO pode reprovar.
- **FR3**: A regra DEVERÁ valer a partir de um **piso** declarado (ciclo 061, o que a
  introduz). Os ciclos anteriores mantêm a dívida **declarada**, não apagada.
- **FR4**: O piso DEVERÁ **falhar** se for posto acima do ciclo mais novo ou se não for número
  — botão que desliga tudo e ainda imprime sucesso não é botão, é interruptor.
- **FR5**: Os achados da revisão independente dos ciclos 061 e 062 DEVERÃO ser tratados neste
  ciclo, e os que não forem, registrados no índice com o motivo.

## Critérios de aceite

- `TAIL:review` dos ciclos 061 e 062 **reprova** enquanto a revisão não tiver evidência real.
- Uma evidência legítima que **contenha** a palavra no meio continua passando.
- Um ciclo abaixo do piso com ausência declarada continua passando, e o piso está escrito.
- Piso acima do ciclo mais novo **reprova**, em vez de dispensar em silêncio.
