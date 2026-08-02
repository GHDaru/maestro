# Changelog

Todas as mudanças notáveis do **Maestro** são registradas aqui. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento semântico.

> **Forcing function**: toda PR adiciona uma entrada em **[Unreleased]** — a CI
> (`.github/workflows/ci.yml`, job `changelog`) falha se o `CHANGELOG.md` não for
> alterado. Bypass: label `skip-changelog`.

## [Unreleased]

### Added
- **Capítulo 11 migrado ao padrão editorial v2 (spec 031)**: a rastreabilidade passa a ser
  percorrida **de trás para frente** com dados reais — linha do gate no índice de decisões →
  commit → pasta do ciclo → registro de decisão, quatro saltos e nenhuma ferramenta. E o
  capítulo nomeia o elo frágil em vez de exibi-lo como virtude: a citação `spec NNN` na
  mensagem de commit aparece em 28 commits e **nenhum portão a exige** — candidato a portão,
  com o critério esboçado no próprio exercício de verificação.
- **Capítulo 10 migrado ao padrão editorial v2 (spec 030)**: os gates passam a aparecer como
  são — o `promover-main.sh` abortando de verdade, os **21 gates de merge registrados** e a
  explicação de por que promovemos com frequência sem dupla aprovação (classe baixa por
  reversibilidade, não gate frouxo). O capítulo declara também o que **não** exercitamos:
  quatro das sete classes de risco nunca ocorreram aqui. A seção "6b" enxertada no ciclo 008
  foi absorvida na regra vigente — fases com gate valem em qualquer granularidade.
- **Capítulo 09 migrado ao padrão editorial v2 (spec 029)**: a Definição de Pronto (DoD)
  passa a vir com o inventário dos **seis portões executáveis** do repositório (quatro
  scripts `verificar-*`, duas saídas de erro no gerador do livro, onze testes do companion)
  e com a **segunda lei** — "um check que você nunca viu acusar não é um check" —, que
  existia desde o ciclo 017 na skill e nunca tinha entrado no livro. Fecha com o limite do
  verde: nove defeitos escaparam com o gate verde, e a resposta certa é ampliar a família
  coberta, não revisar com mais cuidado.
- **Capítulo 08 migrado ao padrão editorial v2 (spec 028)**: o critério "consumidor +
  forcing function, ou imutabilidade" passa a vir com as cobranças reais — o trecho literal
  do gate de changelog na integração contínua (com a válvula `skip-changelog` explicada), a
  imutabilidade dos registros de decisão **contada** (nove dos dez com um único commit; o
  décimo mudou só a linha de status) e 26 dos 28 ciclos com os quatro artefatos completos.
  O índice de decisões entrou no catálogo, de onde faltava.
- **Capítulo 07 migrado ao padrão editorial v2 (spec 027)**: cerimônias por **função**, com
  a retrospectiva provada em vez de elogiada — as quatro levas do catálogo de anti-padrões
  aparecem datadas no histórico do arquivo (specs 008, 011, 017, 020), incluindo o
  anti-padrão 14, que nasceu de duas retros **não executadas**. Trabalho em curso igual a
  um, confirmado por `git branch -a` (duas branches em 26 ciclos). Achado aberto: a
  retrospectiva não tem gatilho definido.
- **Capítulo 06 migrado ao padrão editorial v2 (spec 026)**: papéis e RACI (*Responsible,
  Accountable, Consulted, Informed*) com a prova em vez da promessa — a independência de
  quem verifica é **linha de configuração** (três dos treze agentes, os que julgam, não têm
  `Write`/`Edit`, e `verificar-agentes.sh` falha se ganharem), o responsável final humano
  deixa **21 gates registrados** em 38 decisões, e o caso do papel prescrito por catorze
  ciclos sem executável (ciclo 018) entra no livro junto com a verificação que nasceu dele.
- **Capítulo 05 migrado ao padrão editorial v2 (spec 025)**: o catálogo de padrões de
  orquestração passa a dizer **quais usamos**. Em 25 ciclos: encadeamento fixo domina (os
  11 comandos versionados), avaliador-otimizador aparece em quatro relatórios de qualidade
  (portão provado falhando — ciclos 017, 018, 020, 021) e o padrão **autônomo nunca foi
  usado**. Os seis nomes vêm traduzidos (Princípio VIII) e o achado das raias é retomado:
  roteamento que manda quase tudo para o mesmo tratamento não está roteando.
- **Capítulo 04 migrado ao padrão editorial v2 (spec 024)**: economia de contexto deixa de
  ser afirmação e vira medida — os 13 subagentes somam **267 linhas** (média de 20), e a
  independência do revisor aparece na linha `tools:` (sem `Write`/`Edit`), verificada por
  `verificar-agentes.sh`. A seção ⭐ também registra o limite honesto: nem todos os treze
  papéis são acionados em todo ciclo. A antiga seção "6b — economia de contexto medida",
  que só recomendava medir, saiu.
- **Capítulo 03 migrado ao padrão editorial v2 (spec 023)**: o capítulo que explica por que
  existe spec passa a seguir a própria norma. Ganhou a explicação de **EARS** (*Easy
  Approach to Requirements Syntax*) com frase real e o caminho completo de **um requisito**
  — FR3 do ciclo 021 → laço em `verificar-instalacao.sh` → a primeira execução, vermelha.
  A seção ⭐ publica também o dado que nos desabona: **19 das 22 specs marcadas como
  plena, só 2 como leve** — sinal de que a régua de raias não está sendo aplicada, achado
  registrado com pergunta objetiva para a retrospectiva.
- **Capítulo 02 migrado ao padrão editorial v2 (spec 022)**: "A evidência: velocidade e
  estabilidade andam juntas" nas nove seções do guia. A seção ⭐ traz o retrato DORA
  (*DevOps Research and Assessment*) do **próprio repositório**, inclusive a métrica ruim:
  17 promoções em três dias, cada ciclo num commit, zero reversões — e **nove defeitos
  escapados** para a linha principal, ~1 a cada 2 entregas, nenhum pego por revisão e
  todos pegos por um check escrito depois.
- **`scripts/verificar-capitulos.sh`**: a Iron Law editorial vira executável — nove seções
  na ordem, cabeçalho de datação e seção 6 com evidência real, além de listar por nome os
  capítulos que faltam migrar. Provado falhando em quatro modos; o quarto só apareceu ao
  provar os outros: o capítulo **saía do check** ao perder a frase "migrado ao padrão v2",
  então a detecção passou a ser estrutural.
- **O Maestro instalado no próprio Maestro (spec 021, ADR 0013)**: nova fitness function
  **`scripts/verificar-instalacao.sh`** — o método está no disco *e* a Inteligência
  Artificial (IA) sabe que deve segui-lo? Falha se `CLAUDE.md`/`AGENTS.md` não apontar
  para a constituição, o fluxo e as raias, e falha se uma skill existir em `skills/` sem
  ser citada na instrução. **`instalar-maestro.sh --bloco`** passa a gerar o bloco de
  instrução **lendo as skills do disco** (nome + primeira frase), em vez de um texto fixo
  que envelhece. `verificar-papeis.sh` ganhou a contagem princípios da constituição ×
  linhas do Constitution Check (provada falhando).

- **BPMN navegável no livro (spec 020)**: o diagrama do processo virou **navegação** — as
  seis raias em HTML do próprio tema, com **38 links**: cada caixa leva ao capítulo,
  receita ou norma que define aquele passo (Especificar → cap. 03 · Gate de merge → cap. 10
  · DoD verde? → cap. 09 · três camadas → receita de instalação). A imagem única continua
  logo abaixo, rotulada como versão para apresentação e impressão. Humano se distingue por
  barra sólida (a paleta é ouro+verde: cor sozinha não separava humano de agente); a DoD
  aparece em verde por ser o único losango mecânico.

- **Distribuição em três camadas + templates faltantes (spec 019, ADR 0012)**: templates
  de **ADR** e **qa-report** (artefatos de todo ciclo que eram reescritos à mão);
  **plugin do Claude Code** (`scripts/empacotar-plugin.sh` gera `plugin/maestro/` das
  fontes; `.claude-plugin/marketplace.json` publica) com fitness function de sincronia
  provada falhando; compatibilidade com **`npx skills add GHDaru/maestro`** verificada
  (o layout já era o padrão da comunidade — 75+ agentes, sem mudança); README com os três
  caminhos e o que cada um **não** leva. CLI próprio estilo Spec Kit descartado com
  racional (~6.900 linhas para o que um script de 90 entrega).
- **Instalação visível + UX e jornadas executáveis (spec 018)**: seção de instalação no
  `README.md` (com nota para IA: instalar = copiar o toolkit, não empacotar); agente
  **`ux-semantica`** e skill **`jornada-viva`** — os papéis que o modelo operacional
  prescrevia havia catorze ciclos sem nada que os entregasse; templates `ux-design` e
  `journey`; **`scripts/verificar-papeis.sh`**, fitness function que compara o que a norma
  manda com o que o toolkit entrega (provada falhando); BPMN ganha o **ramo de interface**
  (tem UI? → semântica → gate de UX → captura do build real → heurística datada → journey).
  Toolkit: 13 agentes · 6 skills · 6 scripts.
- **Retrospectiva executada — anti-padrões 13/14/15 e BPMN (spec 017)**: auditoria do
  Steward expôs duas falhas de processo (achado que morre em "candidato" e roadmap
  congelado desde o ciclo 009) e um padrão com três ocorrências (**check que mede o proxy,
  não o fato**). Convertidos em regra: anti-padrões 13, 14 e 15 no catálogo; **segunda lei**
  na skill `dod-verificavel` (*um check que você nunca viu acusar não é um check, é uma
  esperança* — prove-o falhando); roadmap descongelado com F5/F6/F7, gatilhos abertos e
  regra de manutenção no cabeçalho. Novo diagrama **BPMN** do processo (quatro raias, os
  gates onde o fluxo para) em imagem, fonte e página do livro.
- **Fitness function do corpus do companion (spec 016)**: teste que compara as páginas do
  sumário com o corpus indexado — se o livro ganhar página e o corpus não for regenerado,
  o conjunto falha com a instrução do comando. A regra de papel do README virou verificação.
- **Companion — o tutor do livro (spec 015)**: serviço FastAPI que responde sobre o método
  **a partir do livro**, citando a página. Busca lexical em 259 trechos gerados do sumário
  (sem embeddings — YAGNI); prompt que aplica as regras do próprio livro (citar fonte,
  sigla por extenso, não inventar); porta do modelo compatível com OpenAI (NVIDIA NIM) com
  modo `echo` sem chave e BYOK por requisição (nunca persistida); persistência em
  Postgres/Neon com queda para memória; 6 endpoints com CORS restrito e limites por sessão.
  Widget flutuante em HTML/JavaScript puro, com fontes clicáveis, injetado no site **apenas**
  quando `MAESTRO_COMPANION_URL` está definida — sem ela, o site é idêntico ao anterior.
  10 testes (feliz + falha) e evidência visual nos dois temas.
- **Livro em cinco trilhas (spec 014)**: navegação por tipo de texto (Diátaxis) — A Jornada
  (tutorial), Os Capítulos (explicação), Receitas (como-fazer), Referência e Bastidores —
  cada trilha com tipo e descrição na barra lateral e no sumário; **cadência educacional**
  no topo do sumário (Entender ~20 min · Aprender ~2 h · Aplicar ~1 dia · Aprofundar);
  quatro receitas novas (instalar o Maestro, abrir um ciclo, escrever critério verificável,
  rodar a retrospectiva) e o mapa da Jornada (12 paradas: tensão → pergunta → regra).
  A capa passa a apontar para as trilhas; nenhum link de conteúdo sai para o GitHub.
- **Livro Maestro: padrão editorial + capítulo-piloto + instalador (spec 013, ADR 0011)**:
  guia editorial (`docs/livro/guia-editorial.md`) com projeto pedagógico (Backward Design,
  Diátaxis, carga cognitiva, 4C/ID), esqueleto de capítulo em 9 seções — com exemplo de
  ciclo real e verificação obrigatórios — cinco trilhas de navegação e cadência
  educacional; capítulo 13 (decisões de engenharia) como piloto, com 14 decisões no
  formato quando/por quê/o que faz/o que provoca; `scripts/instalar-maestro.sh` para
  instalar o método (agentes, skills, scripts, comandos, templates, governança) em outro
  repositório, idempotente e com `--dry-run`. Companion decidido (backend próprio,
  NVIDIA NIM + Neon) — construção em ciclo próprio.
- **Princípio VIII — comunicação inteligível (ADR 0010, constituição v1.1.0)**: em cada
  resposta/documento, a primeira ocorrência de uma sigla vem por extenso (contagem
  reinicia a cada resposta); brechas fechadas; alimenta o glossário.
- **Apêndice C — panorama exploratório de templates (spec 012)**: varredura do resto do
  ecossistema (PRP, CCPM, claude-code-spec-workflow, memory banks, claude-flow, ADK,
  marketplaces) com triagem 🔬/👁/⛔ e gatilhos explícitos; formaliza o funil
  exploratório → gatilho → hands-on → absorção por gate. Achados novos com gatilho:
  PRP (código de produto) e CCPM (multi-dev com Issues).
- **Absorções do Superpowers (spec 011)**: Iron Laws em todas as 5 skills (enforcement
  linguístico com brechas fechadas), protocolo TDD-para-skills no `skill-author`
  (baseline RED sem a skill antes de publicar), skill nova `diagnostico-antes-do-fix`
  (causa raiz antes de correção), checkpoint leve por task (raia plena >3 tasks),
  regra de zero-contexto por task no template e enforcement "Skills primeiro" no
  CLAUDE.md. Vereditos do Apêndice B aprovados integralmente (`gate-010-vereditos`).
- **Apêndice B — estudo hands-on do Superpowers (spec 010)**: avaliação do fork
  `GHDaru/superpowers` (obra/superpowers v6.2.0) com 10 vereditos propostos — Iron Laws,
  TDD para skills, root cause antes de fix, review por task, zero-contexto, bootstrap de
  enforcement — e a tensão HARD-GATE × raias registrada. Vereditos aguardam gate.
- **Spec Kit vendorizado (spec 009, F4)**: templates `spec/plan/tasks` reescritos como
  fonte nossa (PT, raias, critérios EARS, Constitution Check I–VII, gates explícitos —
  formato provado nos ciclos 003–008), comando `/speckit.converge` trazido do fork
  (sem extension hooks) e proveniência registrada em `.specify/UPSTREAM.md` (sync
  deliberada; templates mandam sobre o esqueleto do `novo-ciclo.sh`).
- **Registro automático do gate de merge (ADR 0009, modelo v1.3.0)**: `promover-main.sh`
  anexa `gate-main-<sha>` ao índice `docs/registro/decisoes.jsonl` a cada promoção;
  gates dos ciclos 003–007 registrados retroativamente; `retro.sh` cruza pendências dos
  qa-reports com o registro. Regra nascida do primeiro run da retro executável.
- **Absorções do estudo maestro-02 (spec 008)**: registro de decisões consultável por
  máquina (`docs/registro/decisoes.jsonl` + protocolo + `scripts/registrar-decisao.sh`),
  retro executável (`scripts/retro.sh`), skill `anti-padroes`, gates em nível de task
  (handbook cap. 10 §6b), economia de contexto medida (cap. 04 §6b) e sintaxe **EARS**
  na skill `dod-verificavel` (fecha absorção do ciclo 007). ADR 0008 aceito.
- **Toolkit dos ciclos 003–007**: 12 subagentes executáveis (`.claude/agents/`), 3 skills
  agentskills.io (`skills/`), 3 scripts do ritual (`scripts/`), diagramas do método
  (`docs/diagramas/`, md+PDF), avaliação do ecossistema SDD (`docs/research/` + ADR 0008)
  e Apêndice A do handbook (estudo do maestro-02).
- **Site V0 (storytelling + pipeline)**: capa narrativa `site/index.html` + motor
  `publicar/` (Markdown→site multipágina, sidebar, tema, callouts, gate de link quebrado)
  + roadmap de agentes (`docs/agents/perfis.md`, `comunicacao.md`) + deploy no GitHub Pages
  (`.github/workflows/pages.yml`).
- **Camada didática (spec 001)**: guia narrativo [`docs/comece-por-aqui.md`](docs/comece-por-aqui.md)
  (dor → jornada → sistema) + [`docs/governance/glossario.md`](docs/governance/glossario.md)
  (dicionário de todas as siglas); links no `README.md` e banners nos docs de governança.
  Compêndio PDF regenerado com Introdução + Apêndice Glossário (57 páginas).

### Fixed
- **A instrução da IA tinha derivado em três pontos** — achados da auto-instalação, todos
  da mesma família (lista à mão sem comparação com o disco): `AGENTS.md` estava sem a
  regra "skills primeiro" (do ciclo 011) e agora é **link simbólico** para `CLAUDE.md`
  (fonte única); a skill `jornada-viva` existia desde o ciclo 018 e era **invisível** para
  a IA; o Constitution Check dizia "I–VII" na skill, em `plan-arquiteto` e em
  `guardiao-processo` — o princípio VIII existe desde o ciclo 013, ou seja, **oito ciclos
  de planos sem onde marcá-lo**.
- **Referências de princípio erradas no modelo operacional**: quatro linhas citavam
  "(P. VII)" com a numeração de outra constituição; corrigidas para P. VI (artefatos
  vivos) e para a seção do próprio modelo.
- **A imagem do BPMN não aparecia no site publicado**: o motor de publicação nunca copiava
  os arquivos referenciados por `![...](...)`, e o portão de links validava só `<a href>` —
  a página quebrada passava verde. O motor passa a copiar as imagens de cada página e o
  portão a validar `<img src>` (**provado falhando** com imagem inexistente).
- **Link em HTML embutido no Markdown não era reescrito**: `resolverHref()` foi extraída da
  regra de link e agora se aplica também ao HTML bruto, então o mesmo `href="../x.md"` vale
  no GitHub (fonte) e no livro (vira `x.html`). Terceiro portão: `.md` relativo que sobrar
  no HTML publicado falha o build (**provado falhando** com a reescrita desligada).
- **Template de plano parado em I–VII**: o Constitution Check não tinha linha para o
  princípio VIII (comunicação inteligível, ADR 0010) desde 01/08 — norma sem forcing
  function outra vez. Corrigido em `.specify/templates/plan-template.md` e `novo-ciclo.sh`.
- **Widget no tema claro**: o CSS usava `var(--fg,…)`, variável inexistente no tema do
  livro (é `--text`) — todo o texto caía no fallback escuro e ficava ilegível no tema
  claro. Descoberto em verificação visual com navegador real.
- **Assets órfãos do companion**: `companion.{css,js}` permaneciam em `site/` após remover
  `MAESTRO_COMPANION_URL` (o build limpava apenas `.html`); agora são removidos.
- **Colisão de slug no motor do site**: os cinco `README.md` do livro (handbook, receitas,
  jornada, adr, registro) resolviam todos para `readme.html`, sobrescrevendo-se em
  silêncio — o portão de links não pegava porque o alvo existia. Slug de `README.md`/
  `index.md` passa a usar o diretório pai; o resolvedor de links resolve o caminho
  relativo antes de derivar o slug; adicionada fitness function que falha o build em
  qualquer colisão (testada com colisão deliberada).
- **Links da capa do site**: `site/index.html` (escrita à mão na V0, antes das páginas
  existirem) apontava para arquivos `.md` no GitHub em 6 links; agora aponta para as
  páginas internas do livro. Permanece um único link externo, deliberado ("ver no GitHub").

### Changed
- **Capítulo 01 migrado ao padrão editorial v2 (spec 016)**: "O princípio central: quem
  decide o quê" ganha objetivos de aprendizagem, ideia central em uma frase, exemplo de
  **ciclo real** (o `promover-main.sh` como materialização do princípio, com saída de
  comando verificada), anti-padrões, verificação e "o que roubar" — preservando os 5
  frameworks avaliados, as 6 fontes e os conceitos do v1. Primeiro dos 12 a migrar.

- **Rebasing (FR4)**: referências a "Constituição / Princípio IV/V/VII" nos docs migrados
  passam a apontar para `docs/governance/principios-maestro.md` (via mapa de linhagem).

### Anterior
- **Fundação do repositório Maestro** (ADR 0007): metodologia extraída de `ghdaru`/
  `flowbuilder` para repositório próprio.
- `docs/governance/principios-maestro.md` — constituição própria da metodologia (v1.0.0).
- `docs/governance/modelo-operacional.md` (v1.2.0) — papéis, cerimônias, artefatos,
  raias, gates, DoR/DoD e enforcement.
- `docs/handbook/` — 12 capítulos de fundamentos + apresentações executiva e técnica
  (decks HTML) + prompts de imagem.
- `docs/adr/` — ADRs 0004–0006 (preservados) + 0007 (separação) + índice.
- `docs/research/` — pesquisa citada + diário de aprendizado.
- Templates/boas práticas: PR template com a DoD, comando `/dod`, gate de CHANGELOG na CI.
- **PDF do handbook** (livro A4, capa + 12 capítulos) — `docs/handbook/maestro-handbook.pdf`.
- **PDF compêndio de governança** (visão geral: Princípios + Modelo operacional + Handbook +
  ADRs, 51 páginas) — `docs/handbook/maestro-compendio-governanca.pdf`.

### Follow-up
- Rebaixar referências "Constituição / Princípio IV/V/VII" nos docs migrados para
  `principios-maestro.md` (mapa de linhagem no fim daquele doc).
- Remover as cópias redundantes da metodologia em `ghdaru` após validação desta migração.
