# Plan 053 — Peças de apresentação: o fluxo v5 e o caderno de desenvolvimento

- **Spec**: `spec.md` · **Lane**: leve · **Date**: 2026-08-14

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Quatro FRs curtos; cada um verificável por leitura ou por comando. |
| II. Human-governed orchestration | ✅ O conteúdo das duas peças foi revisto pelo Steward antes de virar arquivo; a adoção da proposta continua sendo decisão dele, e a peça diz isso. |
| III. Reversibility / risk gates | ✅ Só adiciona páginas em `docs/`; reverter é apagar dois arquivos e duas linhas de índice. |
| IV. Test-first / verifiable DoD | ✅ Os números da apresentação são conferidos por comando (`ls .claude/agents \| wc -l` etc.) antes de serem escritos, e os comandos ficam no qa-report. |
| V. Context economy / boundary | ✅ Tudo cai no domínio `guide` (`docs/diagramas/`, `docs/handbook/`), ambos já declarados em `boundary.json`. Nenhum caminho novo a classificar. |
| VI. Living artifacts | ✅ A peça 06 é datada e declarada **proposta**: não envelhece fingindo ser a regra vigente, e a 05 continua sendo a única que descreve o processo. |
| VII. Light governance / YAGNI | ✅ Raia leve, dois arquivos e dois índices. Sem portão novo: não há invariante mecânica aqui que um portão consiga medir sem virar contagem de frase (anti-padrão 13). |
| VIII. Intelligible communication | ✅ É o ponto do ciclo — as duas peças existem para serem lidas por humanos, uma por quem decide e outra por quem desenvolve. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | A comparação com o fluxo externo já foi feita e revista antes do ciclo; não sobrou incógnita. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface. |
| `checklist.md` | `ART:checklist=no` | Quatro critérios de aceite, dois deles conferíveis por comando. |
| `ux-design.md` | `ART:ux-design=no` | Não toca a interface de nenhum produto: são documentos, e o visual reusa a identidade já vigente das peças existentes. |

## How

**Peça 06** — `docs/diagramas/06-fluxo-v5-proposta.md`. Markdown com o diagrama em Mermaid
(renderiza no GitHub, é diffável, e não puxa biblioteca externa), a tabela passo a passo
marcando *temos / novo / movido*, as três lacunas com a evidência de cada uma, e as duas
perguntas em aberto. Rótulo de proposta no título, no primeiro parágrafo e na linha do
índice — três lugares, porque é o tipo de rótulo que some quando alguém copia um trecho.

**Apresentação de desenvolvimento** — `docs/handbook/apresentacao-desenvolvimento-maestro.html`.
Mesmo esqueleto (CSS, navegação por trilho, tema claro/escuro) das duas apresentações que já
existem: a identidade visual do método é uma só, e reimplementá-la seria a versão de sala de
apresentação do anti-padrão que a Constituição VIII combate no frontend. O conteúdo é novo e
percorre o ciclo do ponto de vista de quem executa.

**Índices** — uma linha em cada README.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `ls .claude/agents \| wc -l` · `ls .claude/commands \| wc -l` · `ls -d skills/*/ \| wc -l` · `ls scripts/check-*.sh \| wc -l` | conferem com os números escritos nas peças |
| `scripts/check-links.sh` | verde — as linhas novas de índice apontam para arquivos que existem |
| `scripts/check-boundary.sh` | verde — nenhum arquivo órfão |
| bateria completa · plugin · build do livro | verdes |
