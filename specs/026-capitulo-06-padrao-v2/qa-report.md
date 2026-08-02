# QA-report 026 — Capítulo 06 no padrão v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0 | ✅ 7 migrados · 6 pendentes |
| laço dos agentes sem `Write`/`Edit` | os três citados | ✅ `guardiao-processo`, `review`, `security` |
| `grep -c '"id": "gate-main' …decisoes.jsonl` | 21 | ✅ |
| `wc -l docs/registro/decisoes.jsonl` | 38 decisões | ✅ |
| `scripts/verificar-papeis.sh` | exit 0 | ✅ saída citada confere |
| `node publicar/build.mjs` | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ ferramentas negadas + `verificar-agentes.sh`.
- **FR3**: ✅ contagem por comando. **FR4**: ✅ caso do ciclo 018 no corpo do capítulo.

## Achados

1. **Três dos treze agentes são somente-leitura, e são exatamente os que julgam.** O dado
   não estava escrito em lugar nenhum do livro — vivia só na configuração. Agora o capítulo
   mostra o comando que o revela, o que torna a regra auditável por quem lê.
2. **Cadência confirmada**: com 026, sete dos treze capítulos estão no padrão v2 e seis
   pendentes, contados por script. A migração deixou de depender de memória no terceiro
   ciclo consecutivo.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
