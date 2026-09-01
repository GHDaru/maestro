# Tasks 064 — Portão de slop: o julgamento editorial vira checagem

## Verification first
- [x] T0 — definir as checagens da DoD antes do código: canário por padrão (o portão acusa
  o próprio exemplo), canário dobrado em duas linhas, escape com motivo, e piso de arquivos
  e linhas para que portão vazio não passe por verde.

## Implementation
- [x] T1 — `publicar/verifica-slop.mjs`: 16 padrões lexicais, escopo declarado, escape por
  linha, autoteste embutido.
- [x] T2 — calibrar contra o corpus e **remover** o que produz falso positivo: §14, §18, §16
  e a palavra "robusto". Cada remoção com a medição escrita no cabeçalho.
- [x] T3 — ligar ao build (`publicar/package.json`) e à CI (passo próprio, porque o job roda
  `node publicar/build.mjs` direto e não `npm run build`).
- [x] T4 — registrar: ADR 0021, linha em `decisoes.jsonl`, CHANGELOG, `CLAUDE.md`.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [ ] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [ ] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
