# Ciclo 074 — protótipo navegável do painel de regência (briefing da regente, 26/10/2026)

> Pedido do Darú (26/10, 20:25): "Vamos agora começar a construir os protótipos funcionais com
> telas e simulação da navegabilidade." Este arquivo é o **insumo** do ciclo — o Gerente o
> transforma em `spec.md` (spec-agent), `ux-design.md` (ux-semantics), `plan.md` com Constitution
> Check e `tasks.md`. Raia **plena**, com o **ramo de interface** (papel semântico antes do
> componente → gate de UX → jornada viva). Siglas (Princípio VIII): DoD (*Definition of Done*),
> ADR (*Architecture Decision Record*), DDD (*Domain-Driven Design*).

## 1. O que é (e o que não é)

- **É** um protótipo **clicável** de alta fidelidade do painel de regência inteiro: casca única,
  navegação por contexto delimitado, todas as telas dos cinco contextos, dados de exemplo e
  **ações simuladas** (clicar "reiniciar sessão" abre a confirmação desenhada no 073, confirma,
  muda o estado em memória e mostra o efeito). Serve para o Darú **andar pelo produto** antes de
  construir o backend de cada tela.
- **Não é** o produto: sem servidor novo, sem banco, sem chamada real ao harness. Toda ação de
  escrita é marcada `data-simulado="sim"` e produz efeito **só em memória** (recarregar a página
  volta às fixtures). O painel v0 (`painel/`) continua intacto; o protótipo **lê** dele o que já
  existe de verdade (`painel/projetos/exemplo.json`, `schema_workflow.sql`) para as fixtures.

## 2. Fundações (não se reinventa)

| Fundação | Onde | Como entra no 074 |
|---|---|---|
| 11 wireframes (Mensageria 4 · Administração 3 · Workflow 4), contrato `data-fonte / data-rotulo / data-referencia / data-exemplo`, regra 5 de identidade `nome · ref · projeto` | `specs/073-area-administrativa/prototipo/` | viram **telas do protótipo**, sem perder o contrato; o verificador do 073 continua a cobrá-las |
| Design system v1 (tokens medidos, 16 objetos → componente, navegação de 5 itens) | `specs/073-area-administrativa/design-system.md` | `tokens.css` + `amostra.html` (seção 5 do design system) são a **primeira** entrega |
| Mapa de contextos (Chamados e Gates · Workflow de sessões · Regência · Administração · Mensageria) e linguagem ubíqua por contexto | `specs/073-area-administrativa/confronto/mapa-de-contextos.md` | a **navegação** é por contexto; todo rótulo de menu, título e botão é termo do glossário |
| Telas da regência (kanban por gate, fila de decisões, ruling) com backend real | `painel/index.html` (`vKanban`, `vFila`), `specs/072-painel-de-regencia/ux-design.md` | reproduzidas no protótipo sobre os tokens novos, com os mesmos dados de exemplo |
| Jornada viva (capturas por script versionado + heurística datada) | `docs/jornada/072-painel-de-regencia.md`, `docs/jornada/scripts/captura-072.sh` | o 074 tem `docs/jornada/074-prototipo-navegavel.md` com capturas do protótipo rodando |

## 3. Decisões da regente (fixas para este ciclo)

1. **Onde mora**: `prototipo/` na raiz do repositório (é artefato do produto, não só do ciclo):
   `prototipo/index.html` (casca + roteador por `#/contexto/tela`), `prototipo/tokens.css`,
   `prototipo/amostra.html`, `prototipo/telas/<contexto>/<tela>.html` (fragmentos), `prototipo/fixtures/*.json`,
   `prototipo/app.js` (roteador, estado em memória, ações simuladas), `prototipo/verifica-navegacao.py`.
   Servido por `python -m http.server` (entrada em `.claude/launch.json`). Zero dependência externa:
   sem framework, sem build, sem CDN (o protótipo tem de abrir offline e ser capturável por script).
2. **Navegação**: lateral em desktop, inferior em largura estreita, com os cinco itens do design
   system (Regência · Chamados · Fila · Sessões · Administração) **mais** Mensageria; cada item é um
   contexto delimitado; a tela inicial é a **frase-chave do regente**. Toda tela é alcançável em
   **no máximo 3 cliques** a partir da inicial, e toda tela diz em que contexto está.
3. **Ações simuladas com contrato**: todo botão de escrita declara `data-acao` (verbo da
   linguagem ubíqua), `data-autoriza` (humano · regente por delegação · sessão dona — decisão 5
   da correção 1 do 073), `data-simulado="sim"` e `data-efeito` (o que muda na tela). Confirmações
   irreversíveis (derrubar, entregar a destino não resolvido, estourar teto) mostram o que se
   perde e como reverter, como desenhado no 073. O Gerente **nunca** é derrubável pela tela.
4. **Identidade e números**: regra 5 (`nome · ref · projeto`) vale em todas as telas; todo número
   é fixture marcada `(exemplo)` ou vem de `painel/projetos/exemplo.json` com `data-fonte`;
   `—` sempre com motivo. Sem dado pessoal real (fixtures são dos exemplos do repositório).
5. **DoD executável** (`verifica-navegacao.py`, além do verificador do 073 sobre as telas):
   (a) todo `href="#/…"` e todo `data-vai-para` resolve para um fragmento existente; (b) toda tela
   é alcançável em ≤ 3 cliques (grafo a partir da inicial); (c) todo botão de escrita tem os quatro
   atributos da decisão 3; (d) toda tela tem `data-contexto` em um dos cinco contextos;
   (e) nenhum `<link>`/`<script>` externo; (f) corpus de mutação com fixtures boa/ruim.
   Mais: `scripts/check-conformance.sh 074` verde nos dois modos, `check-language`, `check-links`.
6. **Barra do ciclo** (gate final, por delegação, ADR 0026): um crítico em contexto fresco **anda**
   pelo protótipo no browser (não lê HTML): cumpre as jornadas do `ux-design.md` clicando, e cada
   um dos 15 ENTRA do 073 + as 3 telas da regência tem de ser alcançado e sua ação simulada
   produzir o efeito declarado. Passa com nota ≥ 9 por jornada; regra das duas rodadas.

## 4. Fatias sugeridas (o Gerente decide a ordem; uma tarefa por dono, `[[TASK …]]`)

| Passo | Dono sugerido | Entrega |
|---|---|---|
| 0 · `spec.md` + `ux-design.md` (papel semântico de cada objeto e as jornadas por contexto) | Gerente com spec-agent e ux-semantics (ou Worker01) | gate de spec e gate de UX por delegação |
| 1 · `plan.md` (Constitution Check) + `tasks.md` + `data-model.md` das fixtures (um JSON por agregado do mapa: sessão, tarefa, chamado, pedido de decisão, mensagem, política, orçamento, catálogo) | Gerente | gate de plano |
| 2 · `tokens.css` + `amostra.html` + casca `index.html` + `app.js` (roteador, estado, toasts "simulado") + `verifica-navegacao.py` com fixtures de mutação | Worker02 | base sobre a qual os outros constroem; só depois disto as fatias 3–6 |
| 3 · Regência (frase-chave, kanban por gate, fila, ruling) a partir do `painel/index.html` e do `ux-design.md` do 072 | Worker01 | 3 telas |
| 4 · Mensageria (4 telas do 073 → fragmentos + ações: endereçar por ref, recusa de ambiguidade, drenar outbox) | Worker03 | 4 telas |
| 5 · Administração (3 telas → fragmentos + ações: cadastrar no catálogo, propor regra até a fila, ajustar teto com efeito) | Worker04 | 3 telas |
| 6 · Workflow de sessões (4 telas → fragmentos + ações: reiniciar com confirmação, derrubar com gate, cancelar/reatribuir tarefa) | Worker05 | 4 telas |
| 7 · Fixtures coerentes entre contextos (a mesma sessão `Worker03 [ad66d6] · maestro` em todas as telas), `launch.json`, `docs/jornada/074-*.md` + `captura-074.sh`, segurança documental, conformance | Worker06 | jornada viva + caudas |
| 8 · Integração, verificador 073 (11 telas, 0 achados) + verificador 074 verdes, `[[DONE 074]]` | Gerente | gate final com crítico que anda pelo protótipo |

## 5. Relação com o 073

O 073 segue em julgamento (rodada 4, segunda rodada de juízes, da regente). O 074 constrói sobre
o HEAD integrado da correção 1; se os juízes do 073 pedirem mudança numa tela, a mudança entra
na tela do 073 **e** no fragmento do 074 pelo mesmo dono. O verificador do 073 nunca fica vermelho.

## 6. Orçamento e canal

Workers no gateway (fora do teto); a regente só lê, decide gates e roda os críticos. DONE sempre
com cópia a `MAESTRO [7c8d05]`; fallback por arquivo `specs/074-prototipo-navegavel/done-*.md`.
