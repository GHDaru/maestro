# Despachos do fechamento da rodada 3 — 26/10 (fallback do Gerente)

> **Registro:** este arquivo foi escrito como fallback enquanto o classificador da sessão do
> Gerente derrubava o SendMessage; os três despachos acabaram entregues por SendMessage
> (W01 em 26/10, W02 e W06 idem) e o texto abaixo é o que foi de fato enviado. Commitado como
> registro da cascata do fechamento, conforme a preferência da regente por fallback commitado.

## Para Worker01 [9a1b27]

[[TASK id=073-T3-readme-workflow kind=implement cycle=073 attempt=1]] — Mandato da regente
(fechamento da rodada 3). Antes de mexer: confere que tua branch está em `af81499` (a regente
avançou as worktrees; se não estiver, `git merge --ff-only af81499`).

Tarefa: o README do protótipo (`specs/073-area-administrativa/prototipo/README.md`) passa a
listar as 4 telas do Workflow pelos nomes novos — a regente renomeou na integração (`git mv`):
`workflow-01-sessao-de-agente.html`, `workflow-02-estado-do-agente-vivo.html`,
`workflow-03-tarefa-aberta.html`, `workflow-04-consumo-por-agente.html` (entrega do Worker05,
commit `365f59d`). Hoje o README diz "em entrega" com "*(arquivo a declarar pelo Worker05)*":

1. Linhas 32–35 da tabela tela × ENTRA: substituir o placeholder pelos nomes reais e o estado
   **em entrega** por **neste ramo** (`365f59d`, Worker05) — mantém ENTRA nº, nome ubíquo,
   contexto e juízes como estão.
2. Linha 78 (tabela por grupo): "Workflow de sessões | 4 esperadas | Worker05 | em entrega —
   nomes de arquivo ainda não declarados" → 4 telas, **neste ramo** — `365f59d`.
3. Bloco de medição (linhas 80–82): "São 7 telas na árvore hoje" → **11 telas** (4 + 3 + 4),
   com a data do retrato atualizada para 26/10 — a frase "quem listar a pasta vê o mesmo" tem
   de continuar verdadeira.

É o commit único que tu mesmo recomendaste (nomes + bloco de medição juntos, sem churn).
Commit citando "ciclo 073", [[DONE]] com hash + tokens (piso, soma do message.usage desde a
1ª ocorrência do [[TASK]]). Limites de sempre: sem push, sem merge, sem código de produto,
sem segredo.

## Para Worker02 [31f7bf]

[[TASK id=073-T3-revisao kind=review cycle=073 attempt=1]] — Mandato da regente (fechamento
da rodada 3). Antes de mexer: confere que tua branch está em `af81499` (ff-only se precisar).

Duas partes, NÃO executadas por ti até agora (contexto fresco — tu não escreveste tela nenhuma):

**Parte 1 — revisão fresca das 11 telas** de `specs/073-area-administrativa/prototipo/`
(4 `mensageria-*`, 3 `administracao-*`, 4 `workflow-*`) contra:
- `confronto/mapa-de-contextos.md` — cada tela respeita o contexto dono dela (§6) e os
  relacionamentos tipados (§ relacionamentos)?
- as **cinco colisões de nome** do §7 (:292–296): "fila" e "portão" nunca nus, "sessão" ×
  "agente" resolvida na tela, caixa de entrada ≠ fila de decisões, livro de mensagens ×
  livro de ponto;
- o **contrato de marcação** (docstring do `verifica-prototipo.py`): data-fonte por bloco,
  data-rotulo com termo do glossário, data-exemplo com "(exemplo)", `—` com motivo, citação
  sob data-fonte/data-referencia.
Tu NÃO corrige — relatas. Achado bloqueante ou não, cada um com arquivo:linha e a regra do
mapa/contrato que fere.

**Parte 2 — mutação do gate**: quebra DE PROPÓSITO uma regra do
`prototipo/verifica-prototipo.py` (ex.: cega a checagem de data-fonte, ou a de rótulo, ou a
de número-sem-exemplo), roda o script e mostra que um achado que o corpus
`prototipo/fixtures/tela-ruim.html` hoje acusa **deixa de ser acusado** — copia da saída o
nome do achado que sumiu. Depois **restaura o script byte a byte** (o teu trabalho não pode
deixar o gate alterado; confirma com `git diff` vazio ou hash igual ao de `af81499`).
Mecânica da corrida: o glob do script pega `prototipo/*.html` e pula `_`-prefixo e
subdiretórios — para incluir o fixture, copia-o temporariamente para `prototipo/` (sem
underscore), roda, e remove a cópia ao final; OU aponta o PROTO da cópia quebrada para o
diretório de fixtures. A escolha é tua, contanto que a saída mostre o antes (5 achados no
ruim) e o depois (achado sumindo).

Commit citando "ciclo 073" (a revisão pode ir em markdown dentro de
`specs/073-area-administrativa/` — sugestão: `revisao-073-rodada-3.md`; a mutação NÃO
commita o script quebrado, só a evidência textual). [[DONE]] com achados + evidência da
mutação + tokens (piso). Limites de sempre: sem push, sem merge, sem código de produto, sem
segredo.

## Para Worker06 [c85948]

[[TASK id=073-T3-seguranca kind=security cycle=073 attempt=1]] — Mandato da regente
(fechamento da rodada 3). Antes de mexer: tua branch está em `d71cee6` — `git merge --ff-only
af81499` primeiro (a regente avançou as worktrees; confirma o topo).

Duas partes:

**Parte 1 — segurança documental** sobre `specs/073-area-administrativa/` (foco no
`prototipo/` e no `confronto/`): nenhum segredo (chave, token, senha, connection string),
nenhum dado pessoal (nome real de pessoa, e-mail, caminho de usuário fora do padrão do repo),
nenhum nome real de sessão/agente não marcado como exemplo (as telas usam "Worker05
(exemplo)" — o marcador tem de estar presente em TODO valor que pareça real), e nenhuma URL
externa que vaze algo que não seja documentação pública. Achado = arquivo:linha + classe de
risco (taxonomy do Princípio III).

**Parte 2 — conformance**: `scripts/check-conformance.sh 073` nos dois modos (normal e
`TICKED_ONLY=1`), saídas coladas. Nota: `check-links.sh` e `check-boundary.sh` travam no
checkout principal desta máquina (fork por arquivo + worktrees em círculo; e o `python3` do
bash é stub da Microsoft Store) — se o conformance os invocar e pendurar, extrai o corpo
equivalente e roda com `python`, com timeout longo, e declara o que fez.

Commit citando "ciclo 073" (evidência em `specs/073-area-administrativa/qa-report.md`, por
acréscimo, ou arquivo próprio). [[DONE]] com saídas + tokens (piso). Limites de sempre: sem
push, sem merge, sem código de produto, sem segredo.
