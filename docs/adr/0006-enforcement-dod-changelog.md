# ADR 0006 — Enforcement da Definition of Done e forcing function do CHANGELOG

- **Status**: Aceito
- **Data**: 2026-07-22
- **Relacionado**: `docs/governance/operating-model.md` (v1.2.0, §7, §12); ADR 0004/0005;
  Constituição v1.4.0 (Princípio V)

## Contexto

O modelo operacional definia a Definition of Done como checklist verificável, mas a
**garantia de aplicação** ainda dependia de disciplina. O princípio do elemento `[8]`
diz que a garantia vem de **tornar os checks executáveis e bloqueantes** — aplicá-lo ao
próprio modelo. O CI existente (`ci.yml`) já cobria testes, fitness functions
(`architecture.test.ts` no web, `lint-imports` no api) e build/typecheck; faltavam a
superfície de checklist humano/agente e a forcing function do CHANGELOG.

## Decisão

Fechar o enforcement em quatro peças, dividindo mecânico (hard gate) de julgamento
(checklist + aprovação humana):

1. **PR template** (`.github/pull_request_template.md`) espelhando a DoD (§7): raia,
   rastreabilidade, DoD, bloco de ações irreversíveis e gate de risco.
2. **Gate de CHANGELOG na CI** (`ci.yml`, job `changelog`): a PR falha se o
   `CHANGELOG.md` não for alterado; bypass via label `skip-changelog`. Cria-se o
   `CHANGELOG.md` no formato Keep a Changelog.
3. **Comando `/dod`** (`.claude/commands/dod.md`): self-check do agente que roda os
   checks locais e exige evidência antes de "pronto".
4. **Seção §12 "Aplicação e enforcement"** no modelo, mapeando cada item da DoD ao seu
   mecanismo (hard gate CI · setting nativo · checklist PR · comando · templates spec-kit).

**Secret scanning** fica como **setting nativo do GitHub** (secret scanning + push
protection), não como job de CI — evita ferramenta e falso positivo (YAGNI).

Não adotado agora: **lint** (ruff/eslint) — não há tooling configurado; adicioná-lo
falharia sobre código existente. Fica como follow-up (a DoD mantém "lint" como item de
revisão até o tooling existir).

## Consequências

- O que é mecânico bloqueia o merge sozinho (CI); o que exige julgamento fica no
  checklist do PR + aprovação humana (`[9]`) — a mesma divisão R/C→máquina, A→humano do
  `[5]`.
- O CHANGELOG deixa de depender de memória: quebra se esquecido.
- `operating-model.md` sobe para **v1.2.0** (novo §12).
- Follow-up: habilitar o secret scanning nativo no repositório; avaliar lint (ruff/eslint).

## Fontes

- Claude Code — *Best practices* (dê ao agente um check que ele rode): https://code.claude.com/docs/en/best-practices
- Keep a Changelog: https://keepachangelog.com/pt-BR/1.1.0/
- `docs/handbook/09-definition-of-ready-done.md`; `docs/governance/operating-model.md` §12.
