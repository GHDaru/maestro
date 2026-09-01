# ADR 0021 — Portão de slop no livro, sem travessão e sem emoji

- **Status**: Aceito · **Data**: 2026-08-13
- **Ciclo**: 064 · **Decisor**: Gilsiley Darú (gate humano)

## Contexto

O livro do Maestro é escrito com apoio de IA — é o próprio método em uso. Nenhum portão
olhava a **prosa**: `check-chapters.sh` mede as nove seções e a datação, `check-links.sh`
mede link, `build.mjs` mede slug e imagem. Um capítulo inteiro no registro "esta prática
desempenha um papel crucial no cenário em evolução da engenharia" passa com tudo verde.

Isto é o Princípio IV aplicado à prosa: o trabalho é **transformar julgamento em checagem**.
"Este capítulo soa gerado" era julgamento editorial, disponível só quando alguém lia com
atenção — e memória de revisor relata intenção, não fato (C13).

O portão vem dos dois livros irmãos do mesmo autor (ADR 0006 do *Teoria das Restrições*,
ADR 0009 do *Engenharia de Harness*). A pergunta deste ciclo não é se vale ter o portão, é
**quais regras sobrevivem ao contato com este corpus**.

## Decisão

1. **Adotamos** `publicar/verifica-slop.mjs`: 16 padrões lexicais de "Signs of AI writing"
   (Wikipédia) sobre o livro em português, cada um com uma amostra-canário que o autoteste
   roda a cada build.
2. **Descartamos §14 (travessão)**, como nos dois repositórios irmãos: a regra nasceu do
   inglês, onde o em dash é ornamento; em português é pontuação (aposto, intercalação, fala).
   O próprio guia lista "em dashes alone" entre seus falsos positivos conhecidos.
3. **Descartamos §18 (emoji)** — e esta é a decisão nova deste repositório, medida aqui.
4. **Descartamos §16 (listas com rótulo em negrito)**, herdando a medição dos irmãos: acusa
   lista de definição, que é o caso que o guia isenta. Livro de método vive disso.
5. **Escopo**: handbook, receitas, diagramas, `docs/livro` e `docs/jornada`. Fora ficam
   `docs/governance/` (inglês, e norma), `docs/research/` (notas que citam fonte externa
   literalmente) e `docs/adr/`, `docs/records/`, `docs/ecosystem/`.

## Alternativas consideradas

- **Aplicar §18 com whitelist**: a regra foi implementada e acusou **90 vezes, com 15
  símbolos distintos, e nenhum era decoração** — ⭐ marca a seção 6 do esqueleto editorial
  (o `check-chapters.sh` a remove do título ao comparar), ✨ marca capítulo migrado para a
  v2, 🔬 👁 ⛔ é a triagem do panorama de templates, 🟣 🟡 🟢 🔵 🟠 é a legenda dos
  diagramas, ✅ ❌ 🔄 é coluna de status, 📄 🎼 📐 distingue formato de download. Uma
  whitelist de 15 símbolos não é regra, é **inventário**: precisaria de manutenção toda vez
  que um diagrama ganhasse uma cor, e sobraria quase nada para pegar. — descartada.
- **Aplicar §14 e cortar os travessões**: reescreveria pontuação correta de português com
  base numa heurística de outra língua. — descartada.
- **Portar o portão para `scripts/` como as outras funções de aptidão**: `scripts/` é
  superfície instalável e tem de ser inglês (ADR 0014), enquanto as expressões são
  português por natureza. Marcá-las com `PT-DATA` linha a linha funcionaria, mas colocaria
  um portão específico do **livro** dentro do que viaja para outros repositórios. Em
  `publicar/`, ao lado do `build.mjs` (que também é português), ele fica onde o livro está e
  fora do que se instala. — descartada.
- **Não fazer nada**: o próximo capítulo continua sem rede, e o custo de auditar depois é
  uma varredura por capítulo, para sempre. — descartada.

## Consequências

- **Positivas**: o portão passa limpo hoje (32 arquivos, 3.914 linhas, zero achados), então
  qualquer achado futuro é sinal e não ruído. O autoteste roda os 16 canários a cada build,
  também dobrados em duas linhas — Markdown quebra parágrafo onde quiser, e a primeira
  versão deixava passar todo slop que caísse na dobra. Custo por capítulo novo: zero.
- **Negativas / custos aceitos**: dois tells conhecidos (travessão e emoji decorativo) ficam
  sem cobertura automática, e voltam a depender da revisão editorial humana. As três cópias
  do portão — aqui, no *Teoria das Restrições* e no *Engenharia de Harness* — divergem em
  quais regras valem, porque cada corpus mediu uma coisa diferente. A divergência é
  deliberada e está documentada nos três cabeçalhos, mas é duplicação: uma mudança na lista
  de padrões precisa ser feita três vezes.
- **Reversibilidade**: alta. Cada regra descartada é uma entrada a mais na tabela `PADROES`,
  e quem a acrescentar terá de argumentar contra o cabeçalho do arquivo, que é onde a
  justificativa mora.

## Critério que une os descartes

**Portão com falso positivo conhecido é portão que se aprende a ignorar** — a mesma razão
pela qual a CI mantém `check-cycle`, `check-retro` e `check-conformance` como advisory em
vez de bloqueantes. Zero achado no texto limpo é o que faz um achado futuro significar
alguma coisa.
