# Tasks 059 — "Clonei, e agora?"

## Verification first
- [x] T0 — executar as duas formas de instalar em outra pasta **antes** de documentá-las, e
      gerar a árvore de uma instalação real em vez de desenhá-la.

## Implementation
- [x] T1 — README: "o clone é a ferramenta, o alvo é outro projeto" + as duas direções.
- [x] T2 — README: a árvore depois da instalação, com o que cada camada é.
- [x] T3 — README: o bloco para uma IA que abre o repositório — apontando, nunca repetindo.
- [x] T4 — `agents` deixa de ser passo numerado: é consulta.
- [x] T5 — `check-flags.sh` confere **subcomandos**, nos dois modos do ciclo 058.
- [x] T6 — conferir no disco cada arquivo e comando citado no bloco para IA.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)

## Após o parecer — 19 achados
- [x] T7 — reempacotar o plugin (o `README.md` é empacotado, e o ciclo o editou).
- [x] T8 — o portão: comando é o que está em bloco de código ou crase; `help` deixou de ser
      chamado de inexistente; `plugin/maestro/README.md` e o ADR 0012 entraram nas fontes.
- [x] T9 — `readlink` no `BASH_SOURCE`: `maestro` por symlink no PATH voltou a funcionar.
- [x] T10 — quatro afirmações falsas minhas, corrigidas: promoção, `--ai`, anti-padrões, e o
      que o guarda **não** protege.
- [x] T11 — os números: árvore declarada como `--ai claude`, 81 escritos, dois scripts que
      faltavam, e a terceira contagem de portões removida.
