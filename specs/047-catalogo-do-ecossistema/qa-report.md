# QA report 047 — Catálogo do ecossistema

- **Date**: 2026-08-10 · **Lane**: plena · **Verdict**: aprovado após reprovação e correção

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `scripts/check-ecosystem.sh` | vermelho contra o conteúdo migrado, verde após a correção do conteúdo | ✅ ver abaixo |
| `scripts/check-boundary.sh` | verde com `docs/ecosystem/` como toolkit + shared | ✅ 324 toolkit / 79 guide · 6 shared · 38 páginas com origem |
| `scripts/check-language.sh` | verde (template instalável em inglês; catálogo em português) | ✅ |
| `scripts/check-links.sh` · `check-install` · `check-agents` · `check-roles` · `check-evals` · `check-chapters` · `check-licensing` · `check-cycle` | verdes | ✅ |
| `node publicar/build.mjs` | verde, com o índice publicado em "Bastidores" | ✅ 38 páginas |
| `scripts/package-plugin.sh --verify` | verde | ✅ |
| `scripts/check-conformance.sh 047` | verde | ✅ |

### O portão foi visto acusar — por mutação, em clone descartável

Primeira bateria, contra a versão inicial do portão: 12 mutações, todas acusadas. Depois da
revisão independente, o portão foi endurecido em seis pontos e a bateria refeita, incluindo
**as mutações que a revisão usou para reprová-lo**:

| Mutação | O que quebra | Portão |
|---|---|---|
| `absorver` apontando para `README.md` sem prova | absorção declarada em arquivo que não contém a ideia | ✗ `with a destination but no 'prova'` |
| prova que não existe no arquivo de destino | idem, com prova falsa | ✗ `the proof text is not there` |
| destino absoluto (`/etc/passwd`) | destino fora do repositório | ✗ `points outside the repository` |
| fonte do card = `MIT` | casamento por substring | ✗ `is not a row in fontes.md` |
| fonte do card = `claude-code` (casa duas, licenças diferentes) | licença irresolvível | ✗ idem |
| dimensão 1 repetida sete vezes, sem 6 e 7 | contagem de linhas em vez do conjunto | ✗ `dimensions present are [1]` |
| duas seções `## Dimensões` somando sete linhas | idem | ✗ `2 section(s) — there must be exactly one` |
| veredito `talvez` no card | vocabulário aberto no card | ✗ `outside the closed vocabulary` |
| card sem campo `Destino` | metade da anatomia opcional | ✗ `no destination field` |
| catálogo inteiro apagado | escape hatch virando porta dos fundos | ✗ `declared in boundary.json and does not exist` |
| fonte listada sem card nenhum | fonte sem veredito | ✗ `no card judges it` |
| licença `proprietária` sem a marca de não-copiável | FR6 não verificado | ✗ `does not mark it citable-only` |
| `data` inválida no índice (`ontem`) | card exigia data, índice não | ✗ `is not YYYY-MM-DD` |
| fonte sem licença · fonte sem data · card com 6 dimensões · card sem data · `observar` sem gatilho · estado fora do vocabulário · card sem estado · estado sem card | (primeira bateria) | ✗ cada um |
| controle — clone íntegro | — | ✓ exit 0 |

## Closing tail — the evidence

- TAIL:review — revisão independente em contexto fresco, por quem não executou. Veredito:
  **NÃO PROMOVER COMO ESTÁ**, com cinco bloqueantes. Os dois mais graves eram de **honestidade
  do registro**, não de código: (a) **seis vereditos foram trocados e retrodatados** — o
  índice afirmava, em linha datada de 2026-07-30 e marcada `ciclo 007`, um veredito que o
  ciclo 007 não deu; isto é exatamente o defeito que a spec acusa no ADR 0008, cometido pela
  spec que o acusa; (b) **a alegação central estava superdimensionada nas duas metades** — o
  ADR 0008 lista GSD e Agent OS em "observar com gatilho explícito" três linhas abaixo da
  coluna de absorção, e o Apêndice B diz literalmente "gatilho F3 inalterado" e "mantém ADR
  0008", que é deferência e não reclassificação contra o ADR. Os outros três: o invariante
  central **não discriminava** (qualquer arquivo existente satisfazia uma absorção — `README.md`
  passava); a fonte do card era casada por **substring** no arquivo inteiro (`MIT` passava); e
  **o template instalável não passava no próprio portão**, porque seus comentários em linha
  eram capturados como valor do campo. Mais quatro relevantes (contagem de dimensões por
  linha, FR6 sem verificação, vocabulário aberto no card, anatomia pela metade) e quatro
  menores. **Todos corrigidos**: os vereditos históricos foram restaurados e as
  reclassificações reescritas como linhas novas de 2026-08-10 / ciclo 047, com nota; a
  narrativa foi reescrita para dizer o que os arquivos originais dizem; o portão ganhou o
  campo `prova`; e a migração recuperou **10 cards e 5 fontes** que tinha perdido.
- TAIL:security — passe proporcional à classe de risco (texto e um portão de leitura).
  Quatro superfícies. **(a) Injeção por prosa**: `.specify/templates/evaluation-template.md`
  passa a ser instalado em repositórios de terceiros; varredura por linha em forma de
  diretiva (`you must`, `ignore previous`, `execute`, `curl`, `bash`, URL executável):
  **nenhuma** — o arquivo é um formulário com comentários. **(b) Injeção de padrão**: o
  portão lê dados de arquivos do repositório (nome de fonte, id, destino, prova) e os usa em
  `grep`. Todos os casamentos com dado variável usam `-F`/`-xF`; o único `-E` é padrão fixo
  declarado no script. **(c) Leitura de caminho**: `destino` vem de arquivo e é aberto pelo
  portão — por isso caminho **absoluto** e `..` são recusados; o destino é um caminho neste
  repositório. **(d) Execução**: nenhuma. O JSON é lido com `json.loads`, sem `eval`, e
  nenhuma parte do catálogo vira comando.
- TAIL:gate — DoD verde (tabela acima), dez portões estruturais + plugin + build verdes,
  `check-conformance.sh 047` verde. **Aguarda o gate humano** de promoção `dev` → `main`, que
  não é delegável.

## Requirement coverage

- **FR1** — 23 fontes, cada uma com `owner/repo` (ou nome, quando não há repositório
  público), licença e data de observação. Portão: bloco 1.
- **FR2** — 40 cards imutáveis e datados, cada um com as sete dimensões, exatamente uma vez
  cada, em uma só seção. Portão: bloco 2.
- **FR3** — `estado.jsonl` append-only; o corrente é a última linha por id. As
  reclassificações deste ciclo são **linhas novas**, nunca edições. Portão: vocabulário
  fechado + amarração nos dois sentidos.
- **FR4** — `adotar`/`absorver` exigem destino que é **arquivo**, dentro do repositório, e
  uma **prova**: texto literal encontrado dentro dele. As 14 absorções correntes têm as duas
  coisas, verificadas uma a uma.
- **FR5** — `observar` exige gatilho não vazio: as 15 têm.
- **FR6** — licença que impede redistribuição precisa dizê-lo na própria linha; quatro
  fontes que só diziam "sem licença declarada" passaram a carregar a marca.
- **FR7** — `.specify/templates/evaluation-template.md`, instalável (o instalador copia
  `.specify/templates` inteiro) e **testado contra o próprio portão**: um catálogo mínimo
  gerado a partir dele, em inglês, passa verde.

## Achados registrados neste ciclo

- **Cinco ideias estavam como `absorver` com destino condicional e nenhuma chegou a um
  arquivo** (worktree por task, standards por camada, padrões de fatiamento, fatia vertical,
  contrato por fatia). Todas voltaram a `observar` com gatilho, em linha nova.
- **O portão não achou um defeito preexistente no disco**: as linhas com destino de pasta
  foram escritas nesta migração, ao tentar expressar em forma verificável o que o ADR dizia
  em prosa. É onde a promessa não sobreviveu à tradução — resultado mais fraco do que
  "o portão pegou uma mentira antiga", e é o que de fato aconteceu.
- **Eu retrodatei seis vereditos** e só a revisão independente viu. O ciclo que existe para
  impedir que registro sobreviva ao fato cometeu a versão mais direta desse defeito.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
