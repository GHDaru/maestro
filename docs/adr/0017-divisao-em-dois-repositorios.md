# ADR 0017 — Divisão em dois repositórios: toolkit e guia

- **Status**: **Superado pelo [ADR 0018](0018-fronteira-interna-em-vez-de-divisao.md)**
  (2026-08-06) — a divisão em dois repositórios foi revertida antes de qualquer arquivo se
  mover; a fronteira permaneceu, como fronteira **interna**. O corpo abaixo fica intacto:
  ADR é imutável, e o par 0017 → 0018 registra que a medição mudou a decisão.
- **Data**: 2026-08-06
- **Ciclo**: 038 · **Decisor**: Steward
- **Escopo deste ADR**: o corte e suas invariantes. A mudança física dos arquivos é a
  **fatia 2**, com gate humano próprio.

## Contexto

O repositório serve duas audiências desde a fundação: **agentes**, que leem o instalável
para executar o método, e **pessoas**, que leem o livro para entender por que ele é assim.
A mistura já cobrava preço antes desta decisão — o `check-language.sh` existe exatamente
para impedir que o inglês do instalável vaze para o português do livro, *dentro do mesmo
repositório*. Um portão que separa duas coisas dentro de uma caixa é a evidência de que são
duas caixas.

O corte tem derivação pronta: o corolário **C10** (`docs/governance/axioms.md`) já diz que
*o que é instalado é lido por máquinas e o que é publicado é lido por pessoas*. Faltava
executá-lo.

**A medição impediu o corte ingênuo.** Levantamento antes de qualquer proposta:

- o site publica **37 páginas**, das quais **9 nascem no lado instalável** (4 de governança,
  2 de agentes, roadmap, e os índices de ADR e de decisões);
- o livro atravessa a fronteira em **35 links** (15 para `research`, 15 para `governance`,
  4 para `adr`, 1 para `agents`);
- o livro cita **22 caminhos de código** (`scripts/…`, `.claude/…`) como *evidência*, que é
  a característica que o torna diferente de um livro genérico de metodologia.

Mover arquivos primeiro produziria um livro citando evidência que ele não tem mais e um site
perdendo nove páginas — com o sintoma aparecendo semanas depois, como link morto.

## Decisão

**1. Dois repositórios, cortados pelo leitor** (C10):

| | `maestro` (toolkit) | `maestro-guia` (proposto) |
|---|---|---|
| Leitor | máquina | pessoa |
| Conteúdo | agentes, skills, scripts, evals, templates, plugin, governança | handbook, receitas, diagramas, pesquisa, motor do site, companion |
| Idioma | inglês (ADR 0014) | português |
| Arquivos hoje | 282 | 79 |

**2. A memória fica toda no toolkit** — `specs/`, `docs/adr/`, `docs/records/`,
`CHANGELOG.md`, `docs/roadmap.md`. Decisão do Steward no gate. Razão: a memória registra
decisões **sobre o método**, e o método é o instalável; quem instala precisa poder responder
"por que esta regra existe?" sem clonar um segundo repositório. O guia cita por URL.

**3. O site continua completo, por consumo — nunca por cópia manual.** Decisão do Steward
no gate. As 9 páginas que nascem no toolkit entram no guia como **espelho com direção**:
o guia consome, jamais edita. Cópia à mão foi rejeitada explicitamente por ser o modo de
falha já documentado no ciclo 021 (lista mantida à mão que deriva sem ninguém ver).

**4. A fronteira é um arquivo só** (`boundary.json`), consumido por
`scripts/check-boundary.sh`, com três invariantes:

| # | Invariante | O que impede |
|---|---|---|
| 1 | todo arquivo rastreado tem **exatamente um** dono | arquivo esquecido na origem; arquivo duplicado que passa a divergir |
| 2 | todo caminho espelhado é **do toolkit** | espelho sem fonte, que é um fork com outro nome |
| 3 | toda página do sumário vem do guia **ou** de um espelho | o site perder páginas no dia da divisão |

Resolução de dono por **prefixo mais longo**; empate no mesmo comprimento é `AMBIGUOUS` e
falha — ambiguidade silenciosa é pior que erro.

**5. Nada se move neste ciclo.** A fatia 1 entrega o critério; a fatia 2 executa a mudança
com o portão verde como pré-condição.

## Alternativas consideradas

- **Mover primeiro e consertar os links depois.** Rejeitada por III: alta irreversibilidade
  sem reversibilidade engenheirada. O anti-padrão 18 (renome em massa por substituição de
  texto) nasceu de uma versão menor deste mesmo erro, no ciclo 033.
- **Um repositório com pastas bem separadas** (status quo). Já é o que existe, e é o que
  produziu a necessidade de um portão de idioma interno. Não resolve a audiência dupla.
- **Três repositórios** (toolkit · livro · memória). Rejeitada por YAGNI: a memória não tem
  ciclo de vida próprio nem leitor próprio; seria fronteira sem função.
- **Cópia manual da governança para o guia.** Rejeitada pelo Steward no gate, com precedente
  documentado (ciclo 021).

## Consequências

**Boas.** Cada repositório passa a ter um leitor só, o que torna o `check-language.sh`
desnecessário como fronteira interna. O instalável fica pequeno o suficiente para ser
auditável de uma vez. E a divisão vira **mecânica**: com o portão verde, mover é `git mv`
guiado por um manifesto, não julgamento arquivo a arquivo.

**Ruins, e assumidas.**

- **Os 35 links do livro viram externos.** Resolvem por URL do GitHub — o `resolverHref()`
  do `build.mjs` já tem esse fallback desde o ciclo 020 —, mas link externo não é validado
  pelo mesmo portão que hoje confere 252 links relativos. A cobertura de link **cai** com a
  divisão, e isso é uma perda real, não um detalhe de implementação.
- **A evidência do livro fica em outro repositório.** Um capítulo que diz "oito fitness
  functions em `scripts/`" passa a ser uma afirmação que nenhum portão do repo do guia
  consegue conferir. Nenhuma solução está desenhada ainda; é a dívida a nomear na fatia 2.
- **O espelho é infraestrutura nova**, com sua própria forma de defasar. Ele troca um
  problema conhecido (audiência dupla) por um problema novo (sincronia), e só compensa se
  nascer com forcing function — que é requisito da fatia 2, não promessa.
- **`maestro-guia` é nome proposto**, não decidido. Nada depende dele ainda.

## Referências

- `boundary.json` · `scripts/check-boundary.sh` · `specs/038-divisao-em-dois-repositorios/`
- Corolário C10 em `docs/governance/axioms.md` · ADR 0014 (inglês no instalável)
- Ciclo 021 (lista à mão que deriva) · anti-padrão 18 (renome em massa)
