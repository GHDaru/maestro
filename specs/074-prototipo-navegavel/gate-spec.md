# Gate de spec do ciclo 074 — decidido por delegação (ADR 0026), 26/10/2026, sobre c09e01f

**Decisão da regente: APROVADA COM AJUSTES** — o Gerente aplica os ajustes abaixo no `spec.md`
no mesmo commit em que entrega o `ux-design.md`; não há nova rodada de gate de spec. Crítico em
contexto fresco: `process-guardian` (Sonnet). As sete interpretações do "Clarify" ficam
**aceitas**, com a correção da 2 (B1) e o reforço da 4 (B2).

## Ajustes obrigatórios (bloqueantes do crítico, aceitos)

- **B1 — Clarify 2.** Os cinco contextos são os do mapa (Chamados e Gates · Workflow de sessões ·
  Regência · Administração · Mensageria). Os seis itens de navegação são **vistas**: Regência →
  tela inicial (frase-chave); Chamados → kanban por gate com `data-contexto="chamados-e-gates"`
  (é o core domain; não esvaziar); Fila e ruling → `regencia`; Sessões → `workflow-de-sessoes`;
  Administração; Mensageria. O verificador (d) aceita exatamente esses cinco valores; cada item de
  menu resolve para um fragmento existente.
- **B2 — NFR1 ganha (g), (h), (i).** (g) os fragmentos de `prototipo/telas/` passam nas cinco
  regras (seis, depois da correção 2 do 073) do `verifica-prototipo.py`, invocado sobre essa pasta
  ou importando suas regras, com 0 achados; (h) nenhum botão com `data-acao="derrubar"` tem como
  alvo o Gerente; (i) todo botão irreversível aponta para uma confirmação com os atributos
  `data-perde` e `data-reverte` (nome final no `ux-design.md`). Clarify 4 passa a citar o item (g).

## Secundários aceitos

- **S1** definição de "botão de escrita": todo `<button>`, `<form>` ou `[role=button]` sem
  `href="#/…"` e sem `data-vai-para`.
- **S2** o grafo de cliques inclui as arestas dos seis itens da casca e tem a tela inicial como raiz.
- **S3** as fixtures são **derivadas na autoria** a partir de `painel/projetos/exemplo.json`, com
  `data-fonte` apontando a origem; o servidor roda em `prototipo/` (offline, sem `../painel`).
- **S5** tabela ENTRA → tela → elemento alcançado (15 linhas + as 3 telas da regência) no `ux-design.md`.
- **S6** o projeto nas fixtures é `maestro` em toda tela (valor de `exemplo.json`).
- **S4** e **S7** registrados como aviso ao plano: "abre offline" e "recarregar restaura" são
  julgados pelo crítico que anda; cauda `TAIL:*` e segurança documental vão ao `tasks.md`.

## Parecer do crítico (íntegra)

Veredito: APROVAR COM AJUSTES. Dois achados bloqueantes, ambos corrigíveis por texto na spec.

(1) A spec cobre as seis decisões fixas e não contradiz nenhuma explicitamente; a decisão 2 é
transcrita com o problema "seis itens × cinco contextos", mas a resolução do Clarify 2 está errada
(B1); a decisão 5 é enfraquecida pelo Clarify 4 (B2).

B1. Clarify 2 (linhas 155-161) contradiz o mapa de contextos: o mapa (linhas 101, 214, 245) tem
Chamados e Gates como contexto próprio e core domain; declarar o kanban como `regencia` esvazia o
core domain e deixa o item "Chamados" órfão (nenhum dos 14 fragmentos é "Chamados").

B2. Sem verificação por máquina do contrato do 073 nos fragmentos: FR3 exige os atributos e a
regra 5, mas as verificações (a)–(f) do NFR1 não os cobrem; 14 telas podem perder o contrato com o
DoD verde (Princípio IV). Faltam também as checagens da decisão 3 (Gerente nunca derrubável;
confirmação irreversível com "o que se perde e como reverter").

Secundários: S1 "botão de escrita" não definido (circular); S2 raiz e arestas do grafo de cliques
indefinidas; S3 `../painel` não é servível com `http.server` em `prototipo/`; S4 "offline" e
"recarregar restaura" sem verificação por máquina (aceitável se declarado como critério do
crítico); S5 Clarify 3 exige tabela ENTRA → elemento no `ux-design.md` ou `plan.md`; S6 projeto
`maestro` × `410_MAESTRO`; S7 cauda `TAIL:*` e segurança documental são do `tasks.md`.

Escopo: sem scope creep. Princípio VIII e idioma: corretos; `DoR`, `HTTP`, `CI`, `CSS` expandidos
sem uso no corpo (podar). Lidos: briefing, spec, README do protótipo do 073, mapa de contextos,
design system, `painel/projetos/exemplo.json`. Não leu o ADR 0026 nem rodou scripts.
