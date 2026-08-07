# Relatório de QA 042 — Conformidade executável

- **Data**: 2026-08-07 · **Raia**: plena · **Veredito**: aprovado **depois de reprovado**

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/check-conformance.sh 042` | verde | ✅ (depois das correções da revisão) |
| `scripts/check-chapters.sh` | verde | ✅ — acusou o capítulo 07 atrás da skill; corrigido |
| `check-agents` · `check-roles` · `check-install` · `check-language` · `check-links` · `check-retro` · `check-evals` · `check-boundary` | verde | ✅ |
| `node publicar/build.mjs` · `package-plugin.sh --verify` | verde | ✅ |
| `scripts/check-cycle.sh` | vermelho herdado do ciclo 040 | ⚠️ ver ciclo 041; sai da janela na promoção |

## Closing tail — a evidência

- **TAIL:review** — revisão independente executada em contexto fresco por subagente com a
  instrução de `.claude/agents/review.md`, sobre o diff staged completo. **Veredito: "Do not
  promote."** Sete achados, dois bloqueadores. Todos corrigidos antes deste relatório; a
  lista e as correções estão na seção "A revisão me reprovou" abaixo. É a primeira vez que a
  cauda é cumprida em vez de marcada, e ela reprovou o ciclo que a criou.
- **TAIL:security** — n/a: o ciclo não toca superfície de risco. Nenhum segredo, credencial,
  rede ou permissão entra no diff; o que há de executável é um script `bash` somente-leitura
  que lê `specs/`, `docs/governance/principles.md` e `git log`.
- **TAIL:gate** — pendente: promoção `dev` → `main` aguarda aprovação humana. Três ciclos
  acumulados (040, 041, 042).

## A revisão me reprovou — os dois bloqueadores

**Bloqueador 1: um esqueleto vazio passava verde.** O portão testava se o token
`TAIL:<x>` **aparecia** no `qa-report.md` — e o `new-cycle.sh` escreve os três tokens em todo
relatório que gera. O gerador pré-satisfazia o check que deveria testá-lo. A revisão rodou:

```
$ scripts/new-cycle.sh 099 loophole-test && scripts/check-conformance.sh 099
✓ every case … EXIT=0        # zero trabalho, verde
```

Pior: era **a mesma falha** que eu já tinha corrigido onze linhas acima, no ramo do `n/a`.
Corrigi um ramo e não o irmão — anti-padrão 16, cometido dentro do ciclo que fala de cópia
com perda. Depois da correção, o mesmo teste:

```
✗ TAIL:review in qa-report.md is still the placeholder — nobody wrote what happened
✗ TAIL:security in qa-report.md is still the placeholder — nobody wrote what happened
✗ TAIL:gate in qa-report.md is still the placeholder — nobody wrote what happened
✗ research: declared ART:research=no with no reason — a declaration without a why is silence
   … 8 vermelhos, EXIT=1
```

**Bloqueador 2: o `qa-report.md` deste ciclo era esse esqueleto vazio** — título `<title>`,
veredito `<pending>`, tabela de fitness em branco — **com o `TAIL:review` marcado como
feito**. Ou seja: cometi o anti-padrão 22 no ciclo que o escreveu, e a `[x]` estava lá antes
de qualquer revisão existir. O arquivo que você está lendo é a correção.

## Os outros cinco achados

| # | Achado | O que fiz |
|---|---|---|
| 3 | `ART:research=banana` e `ART:data-model=` passavam; a coluna "Por quê" nunca era lida | valor restrito a `yes`/`no`; razão obrigatória e não-placeholder |
| 4 | o detector de placeholder conhecia `<...>` do gerador, mas não `[...]` dos templates — **que vencem na divergência** | predicado único `is_placeholder`, rejeita `<`, `[` e vazio |
| 5 | `T11` marcado com `CHANGELOG`, roadmap e índice ausentes do diff | os três entraram; o roadmap §3 virou **ponteiro** para `artifacts.md` em vez de segunda fonte |
| 6 | `/speckit.plan` instalado continua exigindo os quatro artefatos incondicionalmente | **não corrigido** — registrado como achado aberto, ver abaixo |
| 7 | `check-conformance.sh 42` (sem zero à esquerda) saía 0; piso alto desligava o portão com sucesso | comparação numérica com `10#`; zero ciclos verificados agora é **erro**, não sucesso |

A revisão também confirmou o que estava certo: nenhum `grep -q` termina pipe (anti-padrão
21), FR2 e FR3 são de fato aplicados, `bash -n` passa, e nada fora de escopo mudou.

## Cobertura dos requisitos

- **FR1** ✅ os cinco `ART:` declarados, com valor restrito e razão exigida.
- **FR2** ✅ `=yes` sem arquivo reprova.
- **FR3** ✅ token ausente no `tasks.md` reprova.
- **FR4** ✅ **agora** — era o bloqueador 1.
- **FR5** ✅ `check-conformance.sh` + a regra "não responda de memória" no `CLAUDE.md` e no
  bloco que o instalador gera.
- **FR6** ✅ catálogo e portão instaláveis — **com a ressalva do achado 6**.

## O que fica aberto, e por quê

**A contradição do `/speckit.plan` sobrevive.** Quem instala recebe um `plan-template.md`
que manda declarar (provavelmente `=no`) e um comando vendorizado que manda gerar os quatro
incondicionalmente, mais um sexto (`quickstart.md`) que nem está no catálogo. Metade do
defeito diagnosticado na spec continua de pé.

Não corrigi porque mexer num comando vendorizado é questão de proveniência
(`.specify/UPSTREAM.md`, regra 2: quando divergem, o upstream vence) e isso é decisão, não
implementação. Registrado como achado aberto.

## Lição para a retrospectiva

Duas, e a segunda é a que importa:

1. **Corrigi um ramo e deixei o irmão** — o `n/a` ganhou detector de placeholder e a
   evidência não. É o anti-padrão 16 (portão que cobre um formato e ignora a família), agora
   com terceira ocorrência. Se repetir, vira Iron Law em `verifiable-dod`.
2. **A cauda funcionou na primeira vez que foi cumprida.** Eu tinha marcado `TAIL:review`
   com `[x]` e o relatório vazio. Se a revisão não tivesse sido executada de verdade, este
   ciclo teria sido promovido com um portão que aprova esqueletos vazios — vendendo
   exatamente a garantia falsa que ele existe para impedir.

## Pendência de gate

- Promoção `dev` → `main`: aguarda aprovação humana.
