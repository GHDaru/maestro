# QA-report 033 — Inglês no método instalável

- **Data**: 2026-08-02 · **Raia**: plena · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `check-language.sh` **antes** | falhar com resíduo real | ✅ exit 1 — `skills/README.md` e `scripts/README.md` ainda em português |
| `check-language.sh` **provado falhando** | resíduo injetado é apontado | ✅ `.claude/agents/qa.md:19: Você não deve pular...` |
| `check-language.sh` depois | exit 0 nos 13 caminhos | ✅ |
| `check-agents.sh` | exit 0 com nomes novos | ✅ 13 agentes, read-only sem Write/Edit |
| `check-roles.sh` | exit 0 | ✅ 8 papéis, 2 templates, 8 princípios → 8 linhas |
| `check-install.sh` | exit 0 | ✅ camadas, instrução e 6 skills visíveis |
| `package-plugin.sh --verify` | sincronizado | ✅ 31 arquivos |
| `node publicar/build.mjs` | exit 0 | ✅ 35 páginas, links OK |
| `install-maestro.sh --block` | bloco em inglês | ✅ 6 skills lidas do disco |

## Cobertura dos requisitos

- **FR1**: ✅ 13 caminhos instaláveis em inglês. **FR2/FR3**: ✅ check com marcador `PT-DATA`.
- **FR4**: ✅ chaves do índice preservadas, motivo documentado no ADR e no `README`.
- **FR5**: ✅ build verde após corrigir dois renomes excessivos. **FR6**: ✅ `--block` gerado.

## Achados

1. **A varredura mecânica trocou demais, duas vezes.** `modelo-operacional.md` casou dentro
   de `0004-modelo-operacional.md` (um ADR que não foi renomeado) e
   `jornada-aprendizado-modelo-operacional.md` virou um caminho inexistente em catorze
   arquivos. **Quem acusou foi o portão de links do livro**, não a leitura — exatamente o
   papel dele. Substituição por texto é anti-padrão 13 esperando acontecer: casa o padrão,
   não o alvo.
2. **O próprio check achou o que a tradução esqueceu**: os dois `README` do toolkit
   (skills e scripts) tinham passado despercebidos porque ninguém os lê ao trabalhar. Um
   check que nasce vermelho por deriva real vale mais que um que nasce verde.
3. **Limite declarado, não escondido**: `check-language.sh` mede **resíduo de português**,
   não "está em inglês". Texto em espanhol ou em inglês ruim passaria. O cabeçalho do script
   diz isso — check honesto sobre o que mede é melhor que check que promete demais.
4. **Candidato para a retro do ciclo 034**: renome em massa precisa de um portão que
   compare *lista de arquivos citados* × *arquivos existentes* em todo o repositório, e não
   só nas páginas publicadas. Hoje um link quebrado dentro de `specs/` ou de um ADR passa.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
