# ADR 0014 — Inglês como idioma do método instalável

- **Status**: Aceito · **Data**: 2026-08-02
- **Ciclo**: 033 · **Decisor**: Steward

## Contexto

O Maestro nasceu em português: agentes, skills, scripts, templates e governança. Isso nunca
incomodou enquanto o método era operado aqui — mas o método passou a ser **instalável** em
outros repositórios (ciclos 018–021, ADR 0012) e a superfície instalável é lida por
**Inteligência Artificial (IA) em qualquer projeto**, não por um leitor específico.

Três forças empurraram a decisão agora:

1. O ecossistema em que o método se distribui é em inglês — o padrão de skills, o formato de
   plugin e os comandos vendorizados já vinham nesse idioma, produzindo um artefato híbrido.
2. Nomes de arquivo em português (`verificar-instalacao.sh`, `dod-verificavel/`) obrigam quem
   instala a escrever e ler acentos e convenções que não são as do próprio projeto.
3. O bloco de instrução gerado pelo instalador (`--block`) já era colado dentro de
   `CLAUDE.md` de projetos de terceiros: a instrução mais importante do método viajava em
   português para repositórios que não são nossos.

O Steward decidiu o escopo: **tudo que o instalador copia** vira inglês, incluindo
`docs/governance/` (constituição, modelo operacional, glossário).

## Decisão

1. **A superfície instalável é escrita em inglês**: `.claude/agents/`, `skills/`, `scripts/`,
   `.claude/commands/`, `.specify/templates/` e `docs/governance/` — nomes de arquivo,
   conteúdo, mensagens de saída e nomes de flag (`--verify`, `--block`, `--force`).
2. **O livro segue em português**: `docs/handbook/`, `docs/receitas/`, `docs/diagramas/`,
   `docs/livro/`, `docs/research/`, `docs/jornada/` e o site publicado. O livro tem público
   definido; a superfície instalável, não.
3. **O `CLAUDE.md` deste repositório segue em português** — ele é a instrução *deste*
   projeto, não parte do pacote. O bloco que o instalador gera para outros projetos é inglês.
4. **O índice de decisões mantém os nomes de campo originais** (`id`, `data`, `titulo`,
   `status`, `registro`). O arquivo é append-only e suas 38 linhas são imutáveis: traduzir as
   chaves exigiria reescrevê-las, que é exatamente o que o arquivo existe para impedir.
5. **`scripts/check-language.sh`** passa a ser a *fitness function* do idioma: falha quando
   há **resíduo de português** na superfície instalável. Linha que legitimamente carrega
   português (um padrão casado contra o livro, um rótulo de artefato português) declara o
   marcador `PT-DATA` na própria linha.

## Alternativas consideradas

- **Manter tudo em português**: coerente com o livro e com quem opera hoje, mas entrega um
  método instalável que fala uma língua diferente do ecossistema em que é instalado — e
  obriga o projeto de destino a conviver com nomes que ele não escolheu.
- **Traduzir só os nomes de arquivo**, mantendo o conteúdo em português: metade do caminho —
  a IA lê o conteúdo, não o nome. Produziria exatamente o híbrido que se quer evitar.
- **Traduzir tudo, inclusive o livro**: descartado pelo Steward nesta rodada. O livro tem
  público definido e treze capítulos recém-migrados; a tradução seria um projeto próprio, com
  benefício menor (o livro é lido por gente, não instalado em repositórios).
- **Não fazer nada**: o método continuaria se instalando em português em repositórios
  alheios, e cada arquivo novo escolheria o idioma pelo humor de quem digita.

## Consequências

- (+) O que a IA lê em qualquer repositório está no idioma do ecossistema em que ela opera.
- (+) O idioma deixa de ser escolha por arquivo: existe regra, e a regra é **verificada**.
- (+) Nomes de flag e de script ficam consistentes com o resto das ferramentas.
- (−) **O livro passa a citar documentos em inglês.** Um capítulo em português linkando
   `principles.md` é uma costura visível — aceita, e explicada no glossário.
- (−) A tradução tocou 60+ arquivos de uma vez: um diff grande, difícil de revisar linha a
   linha. Mitigado por serem mudanças mecânicas (renome + tradução) com portões verdes.
- (−) O `check-language.sh` mede **resíduo**, não "é inglês". Um texto escrito em espanhol
   ou em inglês ruim passa. É o limite honesto do check, declarado no seu cabeçalho.

## Registro

- Renomeados: 6 agentes, 5 skills, 9 scripts, 3 documentos de governança, `docs/registro/` →
  `docs/records/`
- Traduzidos: 13 agentes, 6 skills, 10 scripts, 7 templates, o comando `/dod`, a constituição,
  o modelo operacional (v1.4.0), o glossário, os dois `README` do toolkit e os metadados do
  plugin
- Novo: `scripts/check-language.sh` (provado falhando com resíduo injetado)
- Ciclo: `specs/033-ingles-no-instalavel/`
