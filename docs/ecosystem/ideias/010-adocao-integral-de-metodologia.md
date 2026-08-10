# 010 — Adotar uma metodologia agêntica inteira (papéis, cerimônias, artefatos)

- **Id**: `adocao-integral-de-metodologia`
- **Fonte**: `bmad-code-org/BMAD-METHOD`
- **Observado em**: 2026-07-30
- **Veredito no momento**: descartar
- **Destino**: —
- **Gatilho de reavaliação**: —

## A ideia

Adotar um framework completo: ~12 agentes organizados como time ágil (PM, arquiteto, dev,
QA, SM), artefatos ágeis (PRD, épicos, *stories*) e *handoffs* por arquivo.

## Por que atravessa (ou não)

Não é complementar: é **concorrente integral**. Adotá-lo substituiria o Maestro em vez de
somar — duas fontes de verdade de processo, que é a falha que o ADR 0005 já tinha nomeado. A
cerimônia scrum-like foi rejeitada no modelo operacional (§10, papel de Scrum Master
cortado). E a ideia boa que ele carrega — *story file* com contexto focado — já é o nosso
`tasks.md` por fronteira, com o Princípio V. **A dimensão 1 reprova sozinha.**

O mesmo veredito vale, pela mesma razão, para adotar o `obra/superpowers` por atacado: dele
absorvemos ideias ([002](002-iron-law.md), [013](013-root-cause-antes-do-fix.md),
[003](003-worktree-por-task.md)), nunca a metodologia.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | **sim, insanável**: segunda fonte de verdade de processo |
| 2 | Licença e redistribuição | MIT — não é a licença que reprova |
| 3 | Função já servida | sim, inteira: 13 agentes, constituição, raias |
| 4 | Custo de contexto | alto (o mais caro dos comparados nas análises de 2026) |
| 5 | Reversibilidade | baixa: sair depois de migrar os artefatos é caro |
| 6 | Maturidade e evidência | maduro; nossa evidência é a leitura da documentação, não uso |
| 7 | Dor real hoje | não |
