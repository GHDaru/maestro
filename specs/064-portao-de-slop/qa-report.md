# QA report 064 — Portão de slop

- **Data**: 2026-08-13 · **Raia**: plena

## DoD — evidência

```
$ node publicar/verifica-slop.mjs
✓ prosa sem marcas de IA: 32 arquivos, 3914 linhas, 16 padrões (travessão fora, por decisão)

$ scripts/check-adr.sh
✓ 18 ADR(s): one row each, every row linked to a real file, and the status in the
  index agreeing with the status the ADR declares about itself.

$ scripts/check-language.sh
✓ (o portão mora em publicar/, fora da superfície instalável — ADR 0014 preservado)
```

## TAIL:mutation — o portão foi quebrado de propósito e visto recusando

Slop plantado no fim de `docs/handbook/03-spec-driven.md`, com uma linha coberta por
`slop-ok` para testar o escape na mesma passada:

```
✗ marcas de escrita de IA: 5 achado(s)
   docs/handbook/03-spec-driven.md:186: §1 significância inflada — "desempenha um papel\ncrucial"
   docs/handbook/03-spec-driven.md:187: §5 atribuição vaga — "especialistas afirmam"
   docs/handbook/03-spec-driven.md:187: §7 vocabulário de IA — "crucial"
   docs/handbook/03-spec-driven.md:187: §23 filler — "É importante ressaltar que"
   docs/handbook/03-spec-driven.md:186: §28 sinalização — "Vamos mergulhar"
```

Três coisas ficam provadas de uma vez: o portão acusa (FR1), a frase quebrada entre as
linhas 186 e 187 é acusada mesmo assim (FR4), e a linha coberta por
`<!-- slop-ok: exemplo citado de propósito -->` **não** aparece — sem o comentário ela
produz mais dois achados (§7 "Adicionalmente" e §25 "o futuro é promissor"), com ele,
nenhum (FR2). Capítulo revertido; `git status` limpo.

O autoteste (FR3) foi visto falhando duas vezes durante a construção, nos repositórios
irmãos, e as duas eram defeito real e não do teste: a primeira versão não casava frase
quebrada em duas linhas, e a regra §16 estava escrita em dois lugares com semânticas
diferentes. As duas foram corrigidas antes deste porte.

## TAIL:security — passagem proporcional à classe de risco

Classe: **leitura**. O portão lê `.md` de um escopo fixo, escreve em `stdout`/`stderr` e sai
0 ou 1. Sem rede, sem `exec`, sem escrita em disco, sem segredo.

- **ReDoS**: verificado padrão a padrão. As expressões são alternâncias de literais com
  `\s+` entre palavras; o único quantificador sobre classe é `[^.!?]{0,80}` em §9,
  **limitado**. Não há quantificador aninhado (`(a+)+`), que é a forma que produz
  retrocesso exponencial. O corpus roda em tempo constante perceptível (< 1s para 3.914
  linhas).
- **Travessia de caminho**: o escopo é uma lista literal de cinco diretórios, e a varredura
  desce a partir deles. Não há entrada do usuário no caminho.
- **Injeção**: nenhuma string do corpus é interpretada — só casada e impressa via
  `JSON.stringify`, que escapa o conteúdo antes de ir para o terminal.

## Dívidas em aberto

- **TAIL:review** — a revisão independente em contexto fresco **não foi feita**. Quem
  executou foi o agente, e o Princípio II diz que quem executa não verifica. Declarado
  também no Constitution Check do plan.
- **TAIL:gate** — o gate humano de merge é do autor, por definição.
- **Duplicação entre os três livros**: as três cópias do portão divergem em quais regras
  valem (cada corpus mediu uma coisa), e uma mudança na lista de padrões precisa ser feita
  três vezes. Registrado como consequência aceita no ADR 0021.
