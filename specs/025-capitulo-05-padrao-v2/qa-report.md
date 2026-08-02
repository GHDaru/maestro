# QA-report 025 — Capítulo 05 no padrão v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0 | ✅ 6 migrados · 7 pendentes |
| `ls .claude/commands/` | os 11 arquivos citados | ✅ idênticos |
| `grep -rli "prova.* falhando" specs/*/qa-report.md` | os 4 ciclos citados | ✅ 017, 018, 020, 021 |
| `node publicar/build.mjs` | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ uso real e não-uso declarados. **FR3**: ✅ comando
  reproduz a lista. **FR4**: ✅ o achado das raias é retomado, não maquiado.

## Achados

1. **O catálogo era maior que o uso.** Seis padrões documentados, um dominante
   (encadeamento), um relevante (avaliador-otimizador) e um nunca usado (autônomo). Isso
   não é defeito — é a regra da menor autonomia funcionando —, mas ficava invisível
   enquanto o capítulo só listava opções.
2. **Contagem de ocorrências ≠ contagem de arquivos.** A primeira medição do laço
   avaliador-otimizador usou `grep -rl` com uma redação só e achou 2 ciclos; a redação
   variava ("provado/provada/provados falhando"). Com o padrão certo, 4. Anti-padrão 13 de
   novo, pego na hora: o check media a frase, não o fato.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
