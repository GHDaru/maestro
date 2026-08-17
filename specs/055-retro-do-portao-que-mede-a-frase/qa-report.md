# QA report 055 — Retro: o portão que mede a frase vira prova por mutação

- **Date**: 2026-08-16 · **Lane**: plena · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `scripts/check-retro.sh` | verde | ✅ `no open finding recorded` — 0 abertos |
| **mutação 1** — `TAIL:mutation` fora do `tasks.md` | reprova | ✅ `✗ tasks.md has no TAIL:mutation` |
| **mutação 2** — `n/a` num ciclo que mexeu em portão | reprova | ✅ `✗ TAIL:mutation says n/a, but this cycle changed a gate` |
| **mutação 3** — aplicável, sem evidência | reprova | ✅ `✗ … absent from qa-report.md — a tick is not a witness` |
| **mutação 4** — `N/A:` maiúsculo e `n/a —` com travessão | reprova **igual** | ✅ ambas |
| **mutação 5** — `MAESTRO_MIN_CYCLE_MUTATION=999` | falha | ✅ `✗ mutation floor 999 is above the newest cycle 055`, exit 1 |
| **mutação 6** — piso `abc` | falha na entrada | ✅ `✗ … is not a number — refusing to run` |
| **mutação 7** — commit citando `(Spec 055)` com maiúscula | continua atribuído | ✅ reprovou o `n/a` |
| **mutação 8** — ciclo 056 aberto, portão do 055 ainda por commitar | 055 continua cobrado | ✅ |
| **mutação 9** — tarefa citando `TAIL:review` em prosa | não vira a linha da cauda | ✅ leu a linha certa |
| **mutação 10** — `new-cycle.sh 056` | nasce com o passo nas duas saídas | ✅ 1 + 1 |
| contraprova A — ciclo 054 e anteriores | não são cobrados | ✅ zero ocorrências |
| contraprova B — `n/a` legítimo (ciclo sem portão) | aceito com motivo impresso | ✅ |
| bateria de 16 portões · plugin · build | verdes | ✅ plugin 33 arquivos; livro 39 páginas |

Tudo em cópia (`/tmp/m55`); árvore de trabalho conferida por `git status`.

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco, instruída a refutar e a rodar as
  mutações por conta própria. **Reprovou o ciclo**: onze achados, quatro bloqueantes. O ciclo
  que se propõe a impedir portão vazio entregou um portão furado em cinco frentes.

  1. **A dispensa era comprável com uma letra maiúscula.** A recusa testava `*"n/a:"*`
     literal, então `N/A:` e `n/a —` não entravam no ramo: caíam na checagem de evidência, que
     aceitava a própria frase como prova. Corrigido normalizando caixa e separador — e a
     correção vale para os quatro passos.
  2. **O piso era interruptor, e falhava aberto.** `MAESTRO_MIN_CYCLE_MUTATION=999` isentava
     todo mundo **e imprimia sucesso**; `=abc` quebrava a aritmética, derrubava o passo em
     silêncio e **também** saía 0. O `FLOOR` tinha essa proteção desde o ciclo 048; o piso
     novo nasceu sem. Agora valida a entrada e falha quando fica acima do ciclo mais novo.
  3. **`cycle_touched_a_gate` não discriminava, em três frentes.** A atribuição por commit
     era sensível a maiúscula enquanto o `check-cycle.sh` aceita `-i` — dois portões
     discordando sobre quais commits são de um ciclo. A árvore de trabalho parava de contar
     assim que o **próximo** ciclo era criado: um `new-cycle.sh` de distância da dispensa. E
     o conjunto de caminhos deixava de fora `boundary.json` (lido por quatro checagens),
     `publicar/sumario.json` — **o conjunto declarado, cujo ponto cego foi o defeito do
     054** —, o `package-plugin.sh` e os *workflows* da CI. Os três corrigidos, com
     `companion/` excluído por ser outro domínio.
  4. **O passo obrigatório existia numa cópia só.** Estava no template e ausente do gerador
     (nas duas saídas), do template de `qa-report`, do `docs/governance/artifacts.md` (que
     ainda dizia "**three** steps") e do bloco que o instalador escreve no `CLAUDE.md` de
     terceiro. O revisor provou: `new-cycle.sh 056` gerava um ciclo **nascido vermelho** num
     token que o gerador não sabia emitir. Isso é o anti-padrão 22 — o mesmo que o plano
     deste ciclo cita como motivo da mudança.
  5. **`package-plugin.sh --verify` estava vermelho**: o anti-padrão 23 entrou na fonte e não
     foi reempacotado. O ciclo que documenta *"porta nova, guarda antigo"* enviou o próprio
     conteúdo por um dos dois canais.

  Mais os factuais: *"seis ciclos seguidos (046, 047, 049, 050, 053, 054)"* estava errado nas
  duas palavras — o **053 não enviou portão nenhum**, e 048, 051 e 052 mexeram —, e a frase
  estava no **template instalável**, viajando para terceiros; a linha do índice que fecha o
  `achado-047` apontava para este relatório quando ele ainda era um esqueleto de 348 bytes; as
  quatro caixas da cauda estavam marcadas contra esse esqueleto — **exatamente o defeito que o
  parecer do 053 apontou**, repetido; *"sem evento de fechamento possível"* era exagero (o
  mecanismo `fecha` sempre esteve lá — faltou a **decisão**); *"zero achados pela primeira vez
  desde o 047"* era falso (no 047 eram três); a idade era 8, não 7; a re-ancoragem dos greps
  rejulga 13 ciclos e isso **não estava declarado**; três contagens de anti-padrão ficaram em
  22, uma delas no `CLAUDE.md` que a IA lê; e o `CHANGELOG` não fora tocado. Todos corrigidos —
  menos a contagem no card imutável do ecossistema, que **não se reescreve** por ser observação
  datada.

  Não refutado: o mérito de fechar o `achado-047` (as cinco ideias estão `observar` com gatilho
  no disco, `check-ecosystem` verde, e o `qa-report` do 047 registra a reclassificação); a
  ausência de anti-padrão 21 no código novo; e a retroatividade do `TAIL:mutation`, que isenta
  042–054 por desenho.

- **TAIL:security** — classe de risco: o ciclo altera **dois portões** (`check-conformance.sh`
  e, por reempacotamento, o plugin) e o **bloco que o instalador escreve em repositório de
  terceiro**. Superfície: nenhuma entrada não confiável — os insumos são commits, caminhos do
  próprio repositório e variáveis de ambiente de quem roda. O único vetor real seria a
  variável `MAESTRO_MIN_CYCLE_MUTATION`, e ele foi fechado: entrada não numérica **recusa**, e
  piso acima do ciclo mais novo **falha**. `git log --grep` recebe `${n}`, que vem do nome do
  diretório e casa `[0-9]{3}` pelo glob — não há interpolação de conteúdo externo.

- **TAIL:mutation** — dez mutações, todas em cópia da árvore, cada uma **vista reprovar** (ou
  aceitar, nas duas contraprovas); a tabela acima lista comando e saída de cada. Duas delas
  acharam defeito real **neste ciclo**, e é o argumento inteiro da regra: a mutação 2 revelou
  que `grep -m1 "TAIL:x"` casava a primeira linha que **mencionava** o token — a minha própria
  tarefa T3 — e nunca lia a linha da cauda, de modo que a recusa do `n/a` não podia disparar;
  e a mutação 5 revelou que eu havia deixado `NEWEST_CYCLE` sem atribuição, o que sob `set -u`
  matava o script na checagem do piso. Nenhuma das duas apareceria por leitura.

- **TAIL:gate** — DoD verde, 16 portões verdes, plugin em dia, livro em 39 páginas.
  **Aguarda o gate humano.**

## Requirement coverage

- **FR1/FR2/FR4** — `achado-047` fechado com gatilho nomeado; `TAIL:mutation` na cauda, com
  evidência exigida no `qa-report` pela máquina que já existia.
- **FR3/FR3b** — recusa lida do diff, com escopo de portão ampliado e `companion/` fora;
  grafia de `n/a` não compra dispensa; piso validado e não silenciável.
- **FR5** — anti-padrão 23 no catálogo, com o ciclo de origem.
- **FR6** — o passo existe no template, no gerador (duas saídas), no template de `qa-report`,
  no catálogo de artefatos e no bloco do instalador.
- **FR7** — a leitura casa a linha da cauda nos dois arquivos; os 13 ciclos no piso foram
  reconferidos e passam.

## Achado aberto neste ciclo

- `achado-055-linguagem-ubiqua-prometida-e-ausente` — o `plan-architect`, na **superfície
  instalável**, é instruído a consumir *"the ubiquitous language"*; o `docs/agents/perfis.md`
  repete, e o SIPOC a lista como entrada do processo. O artefato **não existe** em projeto
  nenhum, e o `docs/roadmap.md` o mantém como *"se/quando houver domínio"*. Instrução sem
  artefato é o espelho da norma sem função de força. Duas saídas honestas — criar o artefato,
  ou tirar a promessa da instrução —, e escolher é decisão do Steward.

## Limite declarado, não corrigido

- **Nada mantém em sincronia as contagens em prosa** ("23 anti-padrões", "13 agentes"). Três
  ficaram em 22 e foram achadas por leitura, não por portão. É a mesma família que o
  `check-version.sh` resolve para a versão. Fica registrado como limite: virar portão é ciclo
  próprio, e este já cresceu além do que a raia comporta.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
