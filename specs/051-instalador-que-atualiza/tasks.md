# Tasks 051 — O instalador que atualiza

## Verification first
- [x] T0 — cenário de **upgrade** no `check-installed.sh`, escrito antes e visto vermelho:
  arquivo antigo refrescado · arquivo modificado preservado com a versão nova ao lado ·
  arquivo não mais enviado removido · nenhum diretório aninhado em si mesmo.

## Implementation
- [x] T1 — manifesto `.maestro/manifest.tsv` (hash por arquivo escrito).
- [x] T2 — `copy()` caminha arquivo a arquivo; fim do `cp -r` sobre diretório existente.
- [x] T3 — poda do que não é mais enviado, só quando inalterado.
- [x] T4 — caminho sem manifesto: não sobrescreve nada e diz por quê.
- [x] T5 — correções da revisão: manifesto só reivindica o que escrevemos · flags em qualquer
  ordem · caminho do manifesto validado contra travessia · `--force` guarda `.maestro-old` ·
  manifesto transacional · caminhos aposentados nomeados no upgrade pré-manifesto.
- [x] T6 — registrar: CHANGELOG, roadmap, índice de decisões; fechar o achado 050.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
