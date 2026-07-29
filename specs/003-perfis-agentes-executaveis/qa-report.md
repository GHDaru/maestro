# QA-report 003 — Perfis de agentes executáveis

- **Data**: 2026-07-29 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD verificável)

| Check | Comando | Esperado | Resultado |
|---|---|---|---|
| Contagem | `ls .claude/agents/*.md \| wc -l` | 8 | **8** ✅ |
| Frontmatter | `grep -L "^name:" .claude/agents/*.md` | vazio | vazio ✅ |
| Invariante read-only | `grep -lE "tools:.*(Write\|Edit)" review\|security\|guardiao-processo` | vazio | vazio ✅ |

## Cobertura dos requisitos

- **FR1** (8 subagentes-núcleo com frontmatter + system prompt): ✅ T1–T8.
- **FR2** (tools allowlist estreita; read-only sem Write/Edit): ✅ invariante verde.
- **FR3** (`docs/agents/README.md` índice): ✅ T9.
- **FR4** (`perfis.md` linka executáveis + regra de sincronia): ✅ T10.

## Fora de escopo (registrado, não regressão)

- 4 agentes de toolkit (Agent-Designer, Skill-Author, Curador, Didática) → próximo ciclo.
- Humanos e agentes de domínio → não são subagentes.

## Pendência de gate

- **T11**: promoção `dev → main` aguarda **aprovação humana** (gate indelegável).
