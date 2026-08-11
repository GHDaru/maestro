# Changelog

Todas as mudanças notáveis do **Maestro** são registradas aqui. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento semântico.

> **Forcing function**: toda PR adiciona uma entrada em **[Unreleased]** — a CI
> (`.github/workflows/ci.yml`, job `changelog`) falha se o `CHANGELOG.md` não for
> alterado. Bypass: label `skip-changelog`.

## [Unreleased]

### Corrigido
- **Symlink no alvo deixa de ser porta de saída.** Um link dentro do repositório de destino
  fazia o `cp` escrever **fora** dele, e — desde que o ciclo 051 deu ao instalador o poder de
  remover — a poda apagaria fora também. O instalador passa a **recusar** escrever e remover
  quando o destino, ou qualquer diretório acima dele, é um link; a recusa é nomeada e contada
  no resumo. Fecha `achado-051-symlink-de-diretorio-no-alvo` (ciclo 052).
- **O instalador passa a atualizar uma instalação existente.** Ele pulava qualquer destino
  que já existisse — e um diretório sempre existe depois da primeira instalação —, então
  **reinstalar não entregava nada**; e `--force`, a saída documentada na v0.2.0, rodava
  `cp -r` sobre diretório existente e **aninhava** (`.claude/agents/agents`). Agora há um
  **manifesto** (`.maestro/manifest.tsv`, hash por arquivo escrito) que torna três estados
  distinguíveis: arquivo nosso e inalterado → **atualizado**; arquivo que o projeto modificou
  → **mantido**, com a versão nova ao lado como `.maestro-new`; arquivo que o método deixou
  de enviar → **removido**, só enquanto inalterado. Fecha `achado-050-upgrade-sem-force-nao-entrega`
  (ciclo 051).
- **O instalador reivindicava como seu um arquivo que nunca escreveu — e o apagava.** O
  caminho era gravado no manifesto **antes** de qualquer decisão, então um arquivo que o
  projeto já tinha e que fosse byte-idêntico ao nosso (quem rodou `specify init` por conta
  própria tem exatamente isso) virava nosso em silêncio, e a poda o removia no release
  seguinte. Reivindicar passou a ser consequência de **escrever** (achado da revisão
  independente, ciclo 051).
- **`--force --dry-run` ignorava o freio e destruía.** As flags eram lidas só de `$2`, então
  a combinação virava `FORCE=1 DRY=0` — no único script que apaga arquivo em repositório
  alheio. Agora qualquer flag, em qualquer ordem; `--force` guarda a sua versão como
  `.maestro-old`; e a poda **recusa** caminho de manifesto com `..` ou `/` inicial, que
  chegou a apagar arquivo fora do alvo na revisão (ciclo 051).


## [0.2.0] — 2026-08-11

**A versão em que o método passou a ser verificado onde ele cai.** A v0.1.0 provou que
"instalei o Maestro" significava alguma coisa; esta prova que a coisa **funciona no destino** —
e nasceu de um relato de quem instalou o método noutro repositório e bateu em duas paredes.

**O que ela é.** **Dezesseis** portões executáveis (eram onze na v0.1.0), **treze bloqueando**
na integração contínua ao lado do `package-plugin --verify` e do build do livro, e três
consultivos por desenho. Os cinco novos são de espécies que faltavam:

- **licença e atribuição** (`check-licensing`) — o repositório recusava licença de terceiro
  sem ter a sua; agora carrega MIT com titular, atribui `github/spec-kit` e `obra/superpowers`
  com o aviso de permissão reproduzido, e a obrigação viaja pelos **dois** canais de
  redistribuição, instalador e plugin;
- **catálogo do ecossistema** (`check-ecosystem`) — 40 ideias e 23 fontes, com a **ideia**
  como unidade e o **momento separado do estado**: o card é imutável e datado, o veredito
  corrente é a última linha de um índice append-only, e absorver exige um destino que é
  arquivo **e** uma prova literal encontrada dentro dele;
- **a cópia instalada** (`check-installed`) — instala num diretório vazio e exercita o
  resultado: todo portão enviado roda verde lá, e todo caminho que um arquivo instalado
  nomeia existe lá;
- **o índice de decisões** (`check-adr`) — uma linha por ADR, todo link real, e o status
  comparado por **estado** entre o índice e o corpo do ADR.

- **a versão** (`check-version`) — o quinto, escrito neste próprio corte: a versão era
  declarada em quatro lugares e nada garantia que concordassem.

Mais uma **constituição só**: a cópia com perda em `.specify/memory/` foi apagada, com a
divergência frente ao upstream declarada por token.

**O que ela reconhecidamente não tem**, porque versão que só lista conquistas é publicidade:

- o **serviço do companion** segue sem publicar (F6, desde o ciclo 015) — o widget existe, o
  backend depende de hospedagem, chave e banco;
- **a tag `v0.1.0` nunca chegou ao GitHub**: o push de tag recebe 403 do proxy de saída deste
  ambiente (push de branch passa). A versão anterior existe no CHANGELOG e não existe como
  tag pública — e esta só existirá quando alguém com rede liberada a criar;
- o corpus de **evals** continua com **um** caso provado por ablação e um aposentado sem
  substituto: a cobertura é declarada, não estimada;
- o portão de **conformidade** tem piso de ciclo (42) e os ciclos anteriores carregam dívida
  declarada — 35 dos 40 primeiros `tasks.md` nunca tiveram a cauda de fechamento;
- quatro das sete classes de risco **nunca ocorreram aqui**, então o gate proporcional
  segue sendo teoria para elas;
- **seis** ideias do catálogo constam como `observar` porque nunca foram absorvidas, apesar
  de registradas como absorvidas desde os ciclos 007 e 036 — entre elas as três de
  fatiamento, e a skill que as receberia continua não existindo;
- **atualizar uma instalação existente não entrega as correções**: o `install-maestro.sh`
  pula destino que já existe, e `.claude/commands` é copiado como diretório. Quem instalou a
  v0.1.0 e rodar o instalador sem `--force` **fica com o `/speckit.constitution` antigo** —
  aquele que manda sobrescrever a constituição. A compatibilidade para trás desta versão é
  verdadeira em parte porque o upgrade, sem `--force`, não faz nada;
- o objeto `outcome` e a skill de corte (pesquisa do ciclo 036) seguem como gatilho aberto no
  roadmap, esperando a primeira intenção grande que não caiba em um ciclo.

**Como ela é verificada.** Os treze portões bloqueantes rodam em toda PR e todo push; o
`promote-main.sh` recusa promover enquanto a conformidade estiver vermelha. E o que mais
importa nesta versão: **a revisão independente em contexto fresco reprovou os quatro ciclos
que a compõem** — 046, 047, 048 e 049 —, cada vez achando defeito que o executor não via.
Duas das reprovações foram graves e não são detalhe: numa, um comando instalável passou a
mandar **sobrescrever a constituição ratificada** tratando-a como template; noutra, seis
vereditos do catálogo foram **retrodatados**, na spec que existe para impedir exatamente
isso. As duas foram corrigidas antes de qualquer promoção, e estão escritas nos relatórios.
A cauda de fechamento deixou de ser norma e passou a ser forma.


### Adicionado
- **`scripts/check-version.sh`** (16º portão, bloqueante na CI, **não** instalado) — a versão
  era declarada em quatro lugares e nada garantia que concordassem. O portão lê a linha que
  **declara** a versão em cada um, nunca a primeira string com cara de versão do arquivo, e
  confere a ordem dos cabeçalhos do CHANGELOG, porque "mais nova" ali é posicional
  (ciclo 050).
- **`scripts/check-adr.sh`** (15º portão, bloqueante na CI, **instalado**) — o índice de
  decisões passa a ter portão: todo ADR com **exatamente uma** linha de tabela, todo link
  apontando para arquivo real, e o **status comparado por estado** entre o índice e o corpo do
  ADR, num vocabulário fechado de quatro que mapeia sinônimos nas duas línguas. Fecha o
  achado do ciclo 046, e foi visto acusar aquele defeito exato — índice sem 0018/0019 e 0017
  como "Aceito" — reconstruído por mutação. Um índice que lista uma decisão **revertida como
  corrente** não é incompleto: é errado, e quem o consulta decide por ele (ciclo 049).
- **`.specify/templates/adr-index-template.md`** — o formato do índice como contrato
  explícito, citado na mensagem de falha do portão: o primeiro ADR de um projeto instalado
  tinha portão vermelho e nenhuma receita (ciclo 049).
- **`scripts/check-installed.sh`** (14º portão, bloqueante na CI) — **instala o método num
  diretório vazio e exercita o resultado**: todo portão enviado roda lá e sai verde, e todo
  caminho que um arquivo instalado nomeia existe lá. Os treze portões anteriores mediam o
  repositório de **origem**, onde o alvo por acaso existe; ninguém nunca tinha rodado a cópia
  instalada — que é exatamente onde o anti-padrão 22 vive (ciclo 048).
- **`docs/ecosystem/` — o catálogo do ecossistema, com a IDEIA como unidade.** Trinta cards
  imutáveis e datados (um por ideia, não por ferramenta), dezoito fontes com licença, e um
  índice de estado append-only onde o veredito corrente é a última linha. **Momento e estado
  passam a ser artefatos diferentes**: o card diz o que se julgou naquele dia, o índice diz o
  que vale hoje — antes, o estado morava dentro da observação, e ou a observação virava
  mentira ou a história era reescrita. Publicado no livro, em "Bastidores" (ciclo 047).
- **`scripts/check-ecosystem.sh`** (13º portão, bloqueante na CI) — toda fonte com licença e
  data · todo card com as sete dimensões · todo card com estado e todo estado com card ·
  **`absorver`/`adotar` exigem um destino que existe, e um arquivo, não uma pasta** ·
  `observar` exige gatilho. Doze mutações, todas acusadas (ciclo 047).
- **`.specify/templates/evaluation-template.md`** — o template de avaliação com as **sete
  dimensões** e o vocabulário fechado de veredito, instalável e em inglês (ADR 0014). Duas
  dimensões reprovam sozinhas — licença incompatível e conflito insanável de princípio —, e
  por isso **não há nota agregada**: uma média esconderia qual dimensão decidiu (ciclo 047).
- **ADR 0020 — MIT, e a atribuição viaja com a cópia** — registra a escolha e o que ela
  custa: Apache-2.0 foi considerada e recusada, e a **ausência de concessão de patente é
  consequência aceita, não esquecida** (ciclo 046).
- **`LICENSE` (MIT, Copyright (c) 2026 GHDaru)** — por 45 ciclos o Maestro recusou uma
  coleção de terceiros **por licença** enquanto não tinha a sua. Repositório sem licença não
  é neutro: é *todos os direitos reservados*, mais restritivo que a licença recusada
  (ciclo 046).
- **`THIRD-PARTY-NOTICES.md`** — atribui `github/spec-kit` (speckit 0.4.3, fork
  `GHDaru/spec-kit @ 0117a7b`, MIT, *Copyright GitHub, Inc.*), separando o que é **verbatim**
  do que foi **modificado**, e declarando o que é ideia citada e não redistribuída (EARS) e o
  que é dependência apenas de build (ciclo 046).
- **`scripts/check-licensing.sh`** (12º portão) — cinco invariantes: o `LICENSE` existe · o
  que o manifesto do plugin declara é o que o `LICENSE` diz · **todo** upstream nomeado em
  `.specify/UPSTREAM.md` está atribuído, e **cada projeto atribuído nomeia o seu próprio
  titular** · o instalador leva os dois arquivos · o plugin empacotado também. Entrada
  ausente é falha, nunca aprovação. Visto acusar em **dez mutações** que quebram o
  repositório de verdade (ciclo 046).

### Corrigido
- **Enviávamos coisas que apontavam para o que não enviávamos.** Dois defeitos relatados por
  quem instalou o método noutro repositório — `check-roles.sh` lendo `docs/agents/README.md`,
  que não viaja, e os comandos `/speckit.*` apontando para `.specify/memory/constitution.md`,
  que a instalação nunca cria — e **mais sete** da mesma forma, achados pelo portão novo.
  Cada um recebeu a menor correção que o torna verdadeiro: enviado, ou deixado de citar
  (ciclo 048).
- **Uma constituição só.** As 8 citações dos comandos vendorizados passam a apontar para
  `docs/governance/principles.md`; o resumo derivado em `.specify/memory/constitution.md`
  foi **apagado** — duas constituições é o anti-padrão 22 dentro do repositório que o nomeou.
  Divergência declarada em `.specify/UPSTREAM.md`, com token `UP:state=verbatim|adapted`
  (ciclo 048).
- **`/speckit.constitution` mandava sobrescrever a constituição real tratando-a como
  template.** O reapontamento acima moveu instruções destrutivas do upstream — "este arquivo
  é um TEMPLATE", "escreva de volta (overwrite)" — de um resumo de 27 linhas para a **única
  fonte de verdade**, instalada em repositórios de terceiros. O comando passa a mandar
  **emendar no lugar, nunca regenerar**. Achado da revisão independente (ciclo 048).
- **`check-retro.sh` morria em silêncio numa instalação nova** — `exit 2`, zero bytes de
  saída: `ls` sem match falha sob `pipefail` e `set -e` matava o script. Invisível aqui,
  onde `specs/` sempre existe. Anti-padrão 21, terceira ocorrência (ciclo 048).
- **Dois portões chegavam vermelhos em toda instalação nova.** `check-roles.sh` e
  `check-conformance.sh` agora **dizem** quando não têm o que medir — e só saem verdes quando
  a ausência é legítima: o primeiro consulta o `boundary.json`, o segundo distingue "nenhum
  ciclo" de "ciclos fora do alcance do piso". Portão que chega vermelho ensina quem instalou
  o método a ignorar vermelho (ciclo 048).
- **`check-links.sh` passa a ser instalado**, e com ele some a classe inteira de link
  relativo quebrado no destino — sete deles existiam (ciclo 048).
- **Cinco ideias estavam registradas como absorvidas com destino condicional, e nenhuma
  chegou a um arquivo**: worktree por task, standards por camada, padrões de fatiamento,
  fatia vertical e contrato por fatia. Os destinos vinham escritos como "quando houver dor
  real" sob um cabeçalho de absorção — o que as torna `observar` com gatilho. Todas voltaram
  ao estado honesto em linha nova, datada de 2026-08-10, sem reescrever o registro original
  (ciclo 047).
- **O plugin era o segundo canal de redistribuição e saía nu.** `plugin/maestro/` empacota
  dez comandos `speckit.*` derivados do `github/spec-kit` e não continha texto de licença
  nenhum — só o campo `"license": "MIT"` no manifesto, que é exatamente a "alegação sem
  texto" que este ciclo abriu acusando. O ADR 0020 nomeia os dois canais no Contexto e a
  primeira versão corrigia só um. `package-plugin.sh` passa a empacotar os dois arquivos
  (achado da revisão independente, ciclo 046).
- **Três vacuidades no portão novo**, cada uma demonstrada por uma mutação que deixava o
  repositório quebrado e o portão verde: a checagem de copyright casava com a **própria
  prosa** do arquivo; o nome do upstream estava **hard-coded**, então um upstream novo entrava
  em silêncio e renomear o existente fazia o laço rodar zero vezes ainda dizendo "attributed";
  e a checagem do instalador casava com um **comentário**, num bloco sem `else` que dava
  exit 0 se o instalador fosse apagado (achados da revisão independente, ciclo 046).
- **`THIRD-PARTY-NOTICES.md` afirmava que o aviso de permissão estava "reproduzido"** sob
  `github/spec-kit` quando não estava, e seus links relativos quebravam **no destino
  instalado** (`docs/governance/LICENSE` não existe; o arquivo chama-se `MAESTRO-LICENSE`).
  O aviso passa a ser reproduzido por inteiro e os caminhos deixam de ser links (ciclo 046).
- **`obra/superpowers` (MIT, Copyright (c) 2025 Jesse Vincent) passa a ser atribuído.**
  `skills/diagnose-before-fix`, redistribuída pelos dois canais, declara "Superpowers,
  adapted" e reimplementa a técnica — mas duas linhas curtas são próximas do original.
  Errar para o lado da atribuição custa um parágrafo; errar para o outro custa a obrigação
  (ciclo 046).

### Modificado
- **`scripts/install-maestro.sh`** — a obrigação do MIT viaja com a cópia: `LICENSE` →
  `docs/governance/MAESTRO-LICENSE` e `THIRD-PARTY-NOTICES.md` →
  `docs/governance/MAESTRO-THIRD-PARTY-NOTICES.md`. **Renomeados de propósito**: um `LICENSE`
  solto na raiz alheia afirmaria que o projeto de destino inteiro é MIT do Maestro, o que é
  falso (ciclo 046).
- **`docs/governance/glossary.md`** — EARS, BMAD e SBOM, os três usados em documentos nossos
  sem nunca terem sido registrados (ciclo 046).
- **`scripts/check-language.sh`** — `LICENSE` e `THIRD-PARTY-NOTICES.md` entram na superfície
  instalável guardada pelo portão: viraram superfície neste ciclo e nada os mantinha em
  inglês (ciclo 046).
- **`boundary.json`** — `LICENSE` e `THIRD-PARTY-NOTICES.md` declarados no domínio `toolkit`
  (ciclo 046).
- **`docs/adr/README.md`** — o índice tinha congelado: faltavam os ADRs **0018 e 0019** e o
  0017 aparecia como "Aceito" tendo sido superado. Corrigido junto (anti-padrão 15:
  artefato de planejamento que congela) (ciclo 046).
- **`.github/workflows/ci.yml`** — `check-licensing` entra no job `gates` como bloqueante:
  são **doze portões**, **nove** bloqueando na integração contínua. Portão que só roda quando
  alguém lembra não é *forcing function* (ciclo 046).

## [0.1.0] — 2026-08-09

**A primeira linha de base.** Até aqui o Maestro era sempre "o que estiver no `main` hoje":
o cabeçalho deste arquivo declarava versionamento semântico (*Semantic Versioning*, SemVer)
desde o ciclo 001 e havia **zero** versões fechadas e **zero** tags em 44 ciclos. Esta é a
versão em que "instalei o Maestro" passa a significar alguma coisa.

**O que ela é.** Um método instalável em três camadas (script, plugin, catálogo de skills),
com treze agentes, seis skills, uma constituição de oito princípios, uma camada de derivação
(cinco axiomas, sete teoremas, treze corolários), vinte e dois anti-padrões vindos de
retrospectivas reais, **onze portões executáveis** — oito deles bloqueando na integração
contínua desde o ciclo 043, ao lado do `package-plugin --verify` e do build do livro — e um corpus de avaliação com **um caso provado por
ablação**.

**O que ela reconhecidamente não tem**, porque versão que só lista conquistas é publicidade:

- o **serviço do companion** nunca foi publicado (fase F6, marcada ✅ no roadmap com a
  ressalva "falta publicar o serviço", desde o ciclo 015) — o
  widget existe, o backend depende de hospedagem, chave e banco;
- o corpus de evals tem **um** caso provado e **um aposentado** sem substituto: a cobertura
  é declarada, não estimada;
- cada portão tem um **piso de ciclo** e os ciclos anteriores carregam dívida declarada —
  35 dos 40 primeiros `tasks.md` não têm a cauda que o template sempre carregou;
- quatro das sete classes de risco do modelo **nunca ocorreram aqui**, então o gate
  proporcional é teoria para elas;
- as onze subseções desta versão acumularam repetição em 44 ciclos de append e não foram
  reorganizadas — edição em massa junto de corte de versão é o anti-padrão 18;
- as datas dos ciclos 040–044 foram gravadas como 2026-08-07 e o dia era outro: erro meu,
  repetido, corrigido a partir desta linha e não reescrito para trás.

**Como ela é verificada.** Os onze portões precisam estar verdes para a promoção acontecer:
o `promote-main.sh` recusa promover enquanto a conformidade estiver vermelha. E os quatro
últimos ciclos passaram por revisão independente em contexto fresco, que **reprovou todos os
quatro** e mudou o desenho de três — inclusive este, cujo portão novo cobria uma forma de
caixa e deixava quatro passarem.

### Changed
- **Os critérios de aceite da spec perdem a caixa de marcação (spec 045)**. Marcar caixa
  antes de a evidência existir aconteceu **quatro vezes** entre os ciclos 042 e 044, em dois
  tokens diferentes, com o mesmo autor e a mesma intenção — e instruir já tinha sido tentado
  no 043, falhando no 044. Então a forma mudou em vez da instrução: a spec **declara
  critérios**, o `qa-report` diz **se valeram**, e uma caixa duplica a função do relatório
  (princípio VI). `check-conformance.sh` reprova caixa nos critérios de qualquer spec ≥045,
  cobrindo a família inteira de grafias (`-`, `*`, `+`, indentada, `[x]` ou `[X]`) e
  **falhando quando não encontra a seção** — um portão que não distingue "limpo" de "não
  olhei" é a falha que este repositório já nomeou duas vezes.
  Na revisão apareceu a **quinta** ocorrência, agora num log append-only: duas linhas do
  índice de decisões citavam um `qa-report.md` ainda em branco. O `record-decision.sh` passa
  a **recusar** uma linha cujo `registro` aponte para arquivo com placeholder — uma linha que
  cita evidência inexistente não pode ser retirada depois.
- **O `/speckit.plan` passa a deferir à tabela de declaração (spec 044)**. Fecha o
  `achado-042-speckit-plan-contraditorio`: quem instalava o Maestro recebia **duas ordens
  contraditórias** — o `plan-template.md` mandando *declarar* os cinco artefatos
  condicionais e o comando vendorizado mandando *gerar* quatro deles incondicionalmente,
  sem nada dizendo qual vencia. As fases 0 e 1 agora produzem **apenas** o declarado `=yes`,
  e o `quickstart.md` sai por princípio VI (a função "como alguém experimenta isto" já é
  servida pela jornada e pelas receitas). `UPSTREAM.md` move `speckit.plan.md` de *Verbatim*
  para **Adaptado** e ganha a regra **"divergência declarada, nunca silenciosa"** — divergir
  sem registrar é o que transforma vendorizar em bifurcar.
  **A revisão independente reprovou** ("do not merge as-is") com seis lacunas, e a
  bloqueante estava **fora do diff**: `plugin/maestro/` é build commitado e continuava
  distribuindo o texto contraditório — reprovando o portão bloqueante da CI escrito uma hora
  antes, no ciclo 043. Três outras eram **da mesma classe que o ciclo combatia**, agora
  dentro do remédio: um portão novo que engolia o passo sem token, uma linha upstream
  competindo com a tabela, e a fase 0 com a ordem antes da ressalva.
- **Os onze portões entram na integração contínua (spec 043)**. Fecha o
  `achado-042-portoes-fora-da-ci`, levantado pela revisão independente do ciclo anterior: a
  CI rodava **um** job (o do `CHANGELOG`) e os outros dez dependiam de alguém lembrar — o
  corolário C13 aplicado ao próprio enforcement. Entra o job `gates`: oito portões
  estruturais mais `package-plugin --verify` e o build do livro, **bloqueantes**; e
  `check-cycle`, `check-retro` e `check-conformance` **consultivos**, porque os três ficam
  vermelhos por razões legítimas enquanto há trabalho em voo. O job **consome** os scripts
  em vez de reimplementar a lógica em YAML, que é onde ela apodreceria fora de vista.
  **A revisão independente reprovou de novo** ("do not merge as-is") e o achado que mais
  valeu foi de desenho: `check-conformance` estava bloqueante, e o `new-cycle.sh` gera o
  `qa-report.md` como placeholder **por desenho** — logo a CI ficaria vermelha da primeira à
  última linha de qualquer branch, e portão sempre vermelho é portão que se aprende a
  ignorar. Conformidade passou a ser aplicada **onde um ciclo de fato termina**: o
  `promote-main.sh` agora **recusa promover** enquanto ela estiver vermelha.
  Segurança conferida e não dispensada: `pull_request` (não `pull_request_target`), nenhum
  segredo, `permissions: contents: read`, SHA da base por `env`, `npm ci --ignore-scripts`,
  `concurrency` e `timeout-minutes`. Riscos residuais declarados no relatório: *actions* por
  tag maior e não por SHA, e `push: ["**"]` executando scripts do repositório.
  E o `grep -q` no fim de pipe do job de `CHANGELOG` foi endurecido — era a forma exata do
  anti-padrão 21 que escrevemos hoje.
- **Conformidade executável: a cauda sobrevive ao artefato (spec 042, ADR 0019)**. Origem:
  uma agente companheira noutro repositório, perguntada se tinha seguido o Maestro,
  respondeu honestamente que **em parte** — o `plan.md` dela parava em "docs e fitness
  verdes", a cauda do método vivia na spec e na memória de trabalho, e a compactação de
  contexto promoveu a versão truncada a fonte de verdade. Ela dirigiu até o pull request
  **obedecendo com fidelidade**. Medido aqui, o mesmo defeito é pior: **35 de 40** ciclos
  cujo `tasks.md` perdeu o gate humano que o template carrega, **0 de 40** com qualquer dos
  cinco artefatos condicionais, e a regra de quando eles se aplicam guardada num documento
  que o instalador **não copia** — enquanto o `/speckit.plan` copiado exige quatro deles.
  O defeito ganhou nome: **anti-padrão 22, o método instalado como cópia com perda**.
  Corolários **C12** (o que sobrevive à compactação é o que está em artefato consumido — o
  resto é apagado, não degradado) e **C13** (pergunta respondível de memória será respondida
  de memória, e memória relata intenção) — axiomas 1.1.0 → 1.2.0.
  O movimento é **transformar omissão em declaração**: tokens `ART:<artefato>=yes|no` com
  razão no `plan.md`, e `TAIL:review` · `TAIL:security` · `TAIL:gate` no `tasks.md`, com a
  evidência no `qa-report.md`. Token e não prosa, porque prosa é traduzida e reescrita.
  Entra `docs/governance/artifacts.md` — **instalável** — como fonte única do catálogo; a
  tabela do roadmap §3 virou ponteiro. E `scripts/check-conformance.sh` responde "estou
  seguindo o Maestro?" pelos artefatos, com a instrução de **não responder de memória**
  chegando ao `CLAUDE.md` de todo projeto de destino.
  **A revisão independente reprovou este ciclo** ("do not promote", 7 achados, 2
  bloqueadores) e é a primeira vez que a cauda é cumprida em vez de marcada. O pior achado:
  um esqueleto vazio recém-gerado passava verde, porque o portão testava a *presença* do
  token e o gerador escrevia os tokens — e o `qa-report.md` deste próprio ciclo era esse
  esqueleto, com o `TAIL:review` já marcado. Anti-padrão 22 cometido dentro do ciclo que o
  criou, mais o 16 (corrigi um ramo e deixei o irmão). Tudo corrigido antes do commit;
  o relato completo está no `qa-report.md`.

### Changed
- **Retro executada pelo gatilho, não pela memória (spec 041)**. O `check-retro.sh` foi a
  vermelho sozinho — `✗ 4 open findings (limit 4)` — sete ciclos depois de ganhar gatilho.
  E a retro achou um quinto achado que ninguém tinha registrado: **a própria ferramenta da
  retro mentia**. O `retro.sh` casava ids no formato `gate-NNN-*`, que só **sete** gates
  usaram; desde o ADR 0009 o `promote-main.sh` grava `gate-main-<sha>`, e são **33**. Todo
  ciclo de 011 em diante era reportado como gate pendente — por 29 ciclos, dentro do
  instrumento que alimenta a cerimônia. A correção **quebrou na primeira tentativa** pelo
  mesmo motivo que já matara o `check-cycle.sh`: `grep -q` no fim de um pipe sob `pipefail`.
  Segunda ocorrência ⇒ virou regra.
  Três anti-padrões novos: **19** (caso de eval que ninguém reprova — pode estar medindo
  capacidade que o alvo não perde), **20** (fixture que carrega o próprio veredito ou cuja
  premissa não foi conferida) e **21** (`grep -q` encerrando pipe sob `pipefail`).
  Os achados viraram **forma, não conselho**: `Axis:` obrigatório no `case.md`, `Ablation:`
  e `Premise-checked:` obrigatórios na linha de base, pré-voo e ablação obrigatórios no
  `/eval`. O caso 002 foi **aposentado com motivo** — e a aposentadoria é desenhada contra o
  abuso: exige `Retired-because:`, é impressa em toda execução e contada à parte, então o
  verde diz "um provado, um aposentado", nunca "dois casos bons".
  O índice ganhou a forma que faltava para **achado encontrado e corrigido no mesmo ciclo**:
  o `fecha` auto-referente apareceu duas vezes (039 e 041, a segunda enquanto se
  retrospectava a primeira) porque o protocolo não oferecia essa forma. Dívida de retro em
  **zero**.
- **Os dois casos-semente de eval foram executados (ciclo 040)**. O `001` passou nas seis
  asserções e a rodada de discriminação **funcionou**: o mesmo agente **sem a instrução de
  comparar o diff com o plano** devolveu cinco defeitos reais e mesmo assim reprovou —
  achou que faltava validação, atribuiu isso ao comentário de cabeçalho do script e propôs
  *apagar a promessa* em vez de implementá-la. `First-red` datado e merecido. Rodar também
  consertou duas asserções mal escritas do próprio caso: a `MUST-FIND` #1 misturava "nomeia
  o FR2" (discrimina) com "percebe que falta validação" (não discrimina), e a
  `MUST-NOT-CLAIM` #3 era mais rígida que o papel — `review.md` proíbe **aplicar** edição,
  não citar um idioma em prosa.
- **O caso `002` não discriminou, e isso ficou registrado como está**. O alvo passou nas
  sete asserções, mas a ablação **falhou**: o alvo sem a instrução de checar raia rejeitou a
  raia do mesmo jeito, chegando nela pelo princípio III sozinho. A fixture é flagrante
  demais — reescrita em arquivo documentado como append-only — e testa "enxergar operação
  destrutiva óbvia", não "julgar uma raia". `First-red` **continua pendente** e o portão
  continua vermelho; a resposta não é ablar até algo ficar vermelho (vermelho tirado
  removendo o princípio III seria forjado), é uma fixture limítrofe de verdade. Achado
  aberto no índice.
  Antes de rodar, inspeção pegou um defeito que teria anulado a rodada: o enunciado do 002
  terminava declarando duas das quatro `MUST-FIND`. Fato entra na fixture; conclusão é o
  que o agente tem de produzir.
- **O caso `002` foi redesenhado e continua sem discriminar (ciclo 040)**. A fixture
  flagrante virou uma **limítrofe**: um *fix* de uma linha, num arquivo, trivialmente
  reversível — em que o defeito é a linha editada ser a **regra de casamento de um portão**,
  logo o raio é os quinze caminhos que ele cobre, não o diff. O alvo real acertou o raio e
  a circularidade da DoD; a ablação **acertou igual**. Duas fixtures, duas ablações, mesmo
  resultado: tirar *"check the declared lane"* do `process-guardian.md` não muda nada — o
  achado é **sobredeterminado**, o princípio III o produz sozinho. Isso é evidência sobre o
  agente (a linha pode ser redundante), não sobre a fixture, e é por isso que ajustar o
  enunciado não resolve. Dois achados abertos.
  E o alvo ablado achou, sem ser perguntado, que a **premissa da minha fixture é falsa**: na
  linha citada nenhuma alternativa do `PATTERN` casa. Duas fixtures escritas à mão, dois
  defeitos encontrados pelos próprios agentes avaliados.
- **A divisão em dois repositórios foi revertida antes de mover qualquer arquivo (spec 039,
  ADR 0018 supersede o 0017)**. A medição pedida pelo Steward mudou a decisão — e o próprio
  número teve de ser corrigido durante a medição: o acoplamento bruto de 40% caía para
  **20%** ao descontar `CHANGELOG`, roadmap, índice e `specs/`, que toda entrega toca por
  forcing function. Três supostos ganhos não sobreviveram: o instalável **já** é separado
  pelo `install-maestro.sh` (copia 0 arquivos do guia), "cada um libera no seu ritmo" é
  teórico (0 tags, 0 versões fechadas) e não há segundo contribuidor. Contra três ganhos
  reais mas não urgentes (contexto do agente, 7× de peso de clone, dependências isoladas),
  quatro perdas mensuráveis — atomicidade dos 20% acoplados, 252 links verificados virando
  35 externos sem verificação, a evidência de código do livro sem portão possível, e um
  espelho novo com defasagem própria. **A fronteira ficou**, como fronteira **interna**:
  `boundary.json` passa a declarar `domains`/`shared` e a terceira invariante muda de razão
  (não protege mais contra perder páginas na mudança; protege contra o site publicar um
  documento voltado a máquina sem declaração). Gatilhos de reabertura no roadmap.

### Added
- **Portão para os perfis de agente (spec 039)**. A auditoria de organização encontrou o
  último lugar do repositório que dependia de memória: `docs/agents/README.md` documenta 13
  agentes com suas *tools*, `.claude/agents/` tem 13 executáveis, e **nenhum script comparava
  os dois** — `check-roles.sh` olhava o modelo operacional, nunca o índice de perfis. Os 13
  batiam com os 13 no dia da auditoria, que é exatamente por que era perigoso: parecia
  saudável e a saúde dependia de alguém lembrar (a família do ciclo 021, três derivas de
  uma vez). O `check-roles.sh` passa a comparar **nos dois sentidos**, pelo link markdown e
  não pelo rótulo em prosa: agente sem documentação · índice apontando para arquivo
  inexistente · **tool no disco fora da linha do índice** (o caso caro — agente ganha `Edit`
  e o índice segue dizendo read-only) · total declarado em prosa diferente da contagem.
- **Divisão em dois repositórios — fatia 1: a fronteira decidível (spec 038, ADR 0017)**.
  O corte é o corolário **C10** executado: *o que é instalado é lido por máquinas; o que é
  publicado é lido por pessoas*. A medição impediu o corte ingênuo — o site publica **37
  páginas e 9 nascem no lado instalável**; o livro atravessa a fronteira em **35 links** e
  cita **22 caminhos de código** como evidência. Duas incógnitas foram ao **gate humano**
  antes de qualquer código: a memória (`specs/`, ADRs, índice, changelog, roadmap) **fica
  toda no toolkit**, e o site **continua completo por consumo**, nunca por cópia manual
  (rejeitada com o precedente do ciclo 021). Entra `boundary.json` como fonte única e
  `check-boundary.sh` com três invariantes: um dono por arquivo · espelho tem fonte no
  toolkit · toda página publicada tem origem reclamada. Classificação: **282 arquivos do
  toolkit, 79 do guia, 5 caminhos espelhados**, zero órfãos.
  **Nenhum arquivo mudou de lugar** — divisão de repositório é irreversibilidade alta, então
  a fatia 1 entrega o critério e a fatia 2 executa, com o portão verde como pré-condição.
- **Evals: linha de base para saída não-determinística (spec 037, ADR 0016)**. Os oito
  portões mediam só o que se compara por igualdade; **treze agentes operaram trinta e seis
  ciclos sem nenhuma linha de base**. O limite já estava escrito e ignorado: a única
  ocorrência de `judge` em `scripts/` é o comentário do `check-cycle.sh:8` admitindo que o
  portão *"cannot judge the answer"*. Entra o **teorema T7** (onde a saída não se compara,
  o critério é uma linha de base registrada) e o **corolário C11** (um eval nomeia seu alvo
  e defasa quando o alvo muda) — axiomas 1.0.0 → 1.1.0. A anatomia de um caso são três
  arquivos em `evals/<NNN-slug>/`, com dois campos carregando o desenho: `MUST-NOT-CLAIM`
  (sem o lado negativo, o caso passa com qualquer resposta prolixa) e `First-red` (a segunda
  lei da `verifiable-dod` virada campo). A verificação é partida em duas: `check-evals.sh`
  é determinístico e gratuito; `/eval` roda o julgamento em contexto fresco, sob demanda,
  **fora da integração contínua** — um portão que exige chave deixa de ser portão. Dois
  casos-semente: `review` diante de um requisito silenciosamente descartado e
  `process-guardian` diante de uma raia subdeclarada.
  **O portão entrega vermelho, de propósito** — as duas linhas de base exigem modelo no
  laço, que este ciclo não executou; a dívida está no índice como achado aberto. Precedente:
  o `check-install.sh` nasceu vermelho no ciclo 021 com deriva real de três ciclos.
- **Pesquisa do upstream (spec 036)**: `docs/research/upstream-decomposicao.md` responde se
  existe método pronto para ir de uma intenção grande até o conjunto de specs. **O gap foi
  medido, não afirmado**: 20 das 34 specs deste repositório nasceram de pedido pontual, e
  nenhum agente, skill, template ou portão cobre o que vem antes da spec — o **Spec Kit não
  tem upstream**, confirmado comando a comando. Fichadas quatro famílias com 16 fontes:
  frameworks agênticos (BMAD, Agent OS), skills publicadas (o catálogo de 70 skills de
  produto é **CC BY-NC-SA**, incompatível com a nossa distribuição — citar sim, copiar não),
  relatos de decomposição para agentes (três passadas: superfície, jornada, risco) e a
  literatura de corte (nove padrões de fatiamento, SPIDR, INVEST, fatia vertical). Proposta
  contida em **um objeto** (`outcome`), **um verbo** (skill `slice-outcome`), **um portão**
  (`check-outcomes.sh`) e **um gate humano** (aprovar o corte) — com a recomendação honesta
  de **não construir sem dor real** e um gatilho aberto no roadmap.

### Added
- **Axiomas, teoremas e corolários (spec 035, ADR 0015)**: `docs/governance/axioms.md` traz a
  camada de **derivação** que faltava — cinco verdades assumidas (intenção é humana ·
  consequência precisa de dono · contexto é finito e degrada · o que está escrito sobrevive ·
  o custo é assimétrico entre fazer e desfazer), seis teoremas **com evidência deste
  repositório** e dez corolários amarrados a artefatos existentes. Cada axioma declara sua
  **independência** (o que quebra se ele sair) e cada teorema traz o fato que o sustenta,
  inclusive o desfavorável: os nove defeitos escapados com portão verde entram como evidência
  do teorema 4. A constituição vai a 1.3.0 e aponta para lá; o Constitution Check continua
  checando os oito princípios.
- **BPMN v4**: o desenho do processo ganha o **gatilho da retrospectiva** (o losango "dívida
  de achados?"), a **raia de portões** com os oito checks e os nomes em inglês; a trilha de
  artefatos passa a terminar em `achado aberto → axioma/teorema → regra nova`. Atualizado nas
  duas versões — o bloco navegável do livro e a imagem, regenerada do fonte versionado.

### Added
- **Retrospectiva executada: cinco achados abertos viram portão (spec 034)**. O mais velho
  estava aberto havia **onze ciclos** — literalmente o anti-padrão 14. Cada um virou
  executável: **`check-retro.sh`** (a retro passa a ser cobrada por **dívida de achados**,
  não por calendário: falha com ≥4 abertos ou um aberto há ≥6 ciclos), **`check-cycle.sh`**
  (a raia precisa vir **justificada** pelos três fatores, a distribuição é impressa, e todo
  commit à frente de `main` precisa citar `spec NNN` ou `ADR NNNN`), **`check-links.sh`**
  (todo link relativo do repositório resolve — não só as páginas publicadas) e a comparação
  **data da skill × revisão do capítulo** dentro de `check-chapters.sh`. Anti-padrões **17**
  (cerimônia sem gatilho) e **18** (renome em massa por substituição de texto) entram no
  catálogo, com o ciclo de origem.

### Changed
- **O método instalável passa a ser escrito em inglês (spec 033, ADR 0014)**: agentes,
  skills, scripts, comandos, templates e `docs/governance/` — nome de arquivo, conteúdo,
  mensagens e flags (`--verify`, `--block`, `--force`). Renomeados 6 agentes, 5 skills,
  9 scripts, os três documentos de governança e `docs/registro/` → `docs/records/`; a
  constituição vai a 1.2.0 e o modelo operacional a 1.4.0. **O livro segue em português** —
  a fronteira é exatamente o que o instalador copia. O índice de decisões mantém os nomes de
  campo originais: é append-only, e traduzir chaves exigiria reescrever linhas imutáveis.

### Added
- **`scripts/check-language.sh`**: a fronteira de idioma vira portão — falha quando há
  **resíduo de português** na superfície instalável, com arquivo e linha. Nasceu vermelho
  (os dois `README` do toolkit haviam escapado da tradução) e foi provado falhando com
  resíduo injetado. Linha que legitimamente carrega português declara `PT-DATA` nela mesma —
  exceção visível onde se aplica, nunca allowlist escondida.
- **Capítulo 12 migrado ao padrão editorial v2 (spec 032) — a migração fecha em 13/13**: a
  governança leve mostra as duas forças com dado real — a constituição tocada **três vezes**
  em 32 ciclos enquanto a periferia executável cresceu para 6 skills e 10 scripts — e a poda
  com a lista do que foi recusado (três dos dez registros de decisão existem para
  descartar). Fecha com a governança se auditando (o princípio VIII sem linha no
  Constitution Check, ciclo 021) e com os **quatro achados abertos** declarados no próprio
  livro, em vez de conclusão redonda. `scripts/check-chapters.sh` passa a reportar
  **0 pendentes**.
- **Capítulo 11 migrado ao padrão editorial v2 (spec 031)**: a rastreabilidade passa a ser
  percorrida **de trás para frente** com dados reais — linha do gate no índice de decisões →
  commit → pasta do ciclo → registro de decisão, quatro saltos e nenhuma ferramenta. E o
  capítulo nomeia o elo frágil em vez de exibi-lo como virtude: a citação `spec NNN` na
  mensagem de commit aparece em 28 commits e **nenhum portão a exige** — candidato a portão,
  com o critério esboçado no próprio exercício de verificação.
- **Capítulo 10 migrado ao padrão editorial v2 (spec 030)**: os gates passam a aparecer como
  são — o `promote-main.sh` abortando de verdade, os **21 gates de merge registrados** e a
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
  `Write`/`Edit`, e `check-agents.sh` falha se ganharem), o responsável final humano
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
  `check-agents.sh`. A seção ⭐ também registra o limite honesto: nem todos os treze
  papéis são acionados em todo ciclo. A antiga seção "6b — economia de contexto medida",
  que só recomendava medir, saiu.
- **Capítulo 03 migrado ao padrão editorial v2 (spec 023)**: o capítulo que explica por que
  existe spec passa a seguir a própria norma. Ganhou a explicação de **EARS** (*Easy
  Approach to Requirements Syntax*) com frase real e o caminho completo de **um requisito**
  — FR3 do ciclo 021 → laço em `check-install.sh` → a primeira execução, vermelha.
  A seção ⭐ publica também o dado que nos desabona: **19 das 22 specs marcadas como
  plena, só 2 como leve** — sinal de que a régua de raias não está sendo aplicada, achado
  registrado com pergunta objetiva para a retrospectiva.
- **Capítulo 02 migrado ao padrão editorial v2 (spec 022)**: "A evidência: velocidade e
  estabilidade andam juntas" nas nove seções do guia. A seção ⭐ traz o retrato DORA
  (*DevOps Research and Assessment*) do **próprio repositório**, inclusive a métrica ruim:
  17 promoções em três dias, cada ciclo num commit, zero reversões — e **nove defeitos
  escapados** para a linha principal, ~1 a cada 2 entregas, nenhum pego por revisão e
  todos pegos por um check escrito depois.
- **`scripts/check-chapters.sh`**: a Iron Law editorial vira executável — nove seções
  na ordem, cabeçalho de datação e seção 6 com evidência real, além de listar por nome os
  capítulos que faltam migrar. Provado falhando em quatro modos; o quarto só apareceu ao
  provar os outros: o capítulo **saía do check** ao perder a frase "migrado ao padrão v2",
  então a detecção passou a ser estrutural.
- **O Maestro instalado no próprio Maestro (spec 021, ADR 0013)**: nova fitness function
  **`scripts/check-install.sh`** — o método está no disco *e* a Inteligência
  Artificial (IA) sabe que deve segui-lo? Falha se `CLAUDE.md`/`AGENTS.md` não apontar
  para a constituição, o fluxo e as raias, e falha se uma skill existir em `skills/` sem
  ser citada na instrução. **`install-maestro.sh --block`** passa a gerar o bloco de
  instrução **lendo as skills do disco** (nome + primeira frase), em vez de um texto fixo
  que envelhece. `check-roles.sh` ganhou a contagem princípios da constituição ×
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
  **plugin do Claude Code** (`scripts/package-plugin.sh` gera `plugin/maestro/` das
  fontes; `.claude-plugin/marketplace.json` publica) com fitness function de sincronia
  provada falhando; compatibilidade com **`npx skills add GHDaru/maestro`** verificada
  (o layout já era o padrão da comunidade — 75+ agentes, sem mudança); README com os três
  caminhos e o que cada um **não** leva. CLI próprio estilo Spec Kit descartado com
  racional (~6.900 linhas para o que um script de 90 entrega).
- **Instalação visível + UX e jornadas executáveis (spec 018)**: seção de instalação no
  `README.md` (com nota para IA: instalar = copiar o toolkit, não empacotar); agente
  **`ux-semantics`** e skill **`living-journey`** — os papéis que o modelo operacional
  prescrevia havia catorze ciclos sem nada que os entregasse; templates `ux-design` e
  `journey`; **`scripts/check-roles.sh`**, fitness function que compara o que a norma
  manda com o que o toolkit entrega (provada falhando); BPMN ganha o **ramo de interface**
  (tem UI? → semântica → gate de UX → captura do build real → heurística datada → journey).
  Toolkit: 13 agentes · 6 skills · 6 scripts.
- **Retrospectiva executada — anti-padrões 13/14/15 e BPMN (spec 017)**: auditoria do
  Steward expôs duas falhas de processo (achado que morre em "candidato" e roadmap
  congelado desde o ciclo 009) e um padrão com três ocorrências (**check que mede o proxy,
  não o fato**). Convertidos em regra: anti-padrões 13, 14 e 15 no catálogo; **segunda lei**
  na skill `verifiable-dod` (*um check que você nunca viu acusar não é um check, é uma
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
  formato quando/por quê/o que faz/o que provoca; `scripts/install-maestro.sh` para
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
  (baseline RED sem a skill antes de publicar), skill nova `diagnose-before-fix`
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
  deliberada; templates mandam sobre o esqueleto do `new-cycle.sh`).
- **Registro automático do gate de merge (ADR 0009, modelo v1.3.0)**: `promote-main.sh`
  anexa `gate-main-<sha>` ao índice `docs/records/decisoes.jsonl` a cada promoção;
  gates dos ciclos 003–007 registrados retroativamente; `retro.sh` cruza pendências dos
  qa-reports com o registro. Regra nascida do primeiro run da retro executável.
- **Absorções do estudo maestro-02 (spec 008)**: registro de decisões consultável por
  máquina (`docs/records/decisoes.jsonl` + protocolo + `scripts/record-decision.sh`),
  retro executável (`scripts/retro.sh`), skill `anti-patterns`, gates em nível de task
  (handbook cap. 10 §6b), economia de contexto medida (cap. 04 §6b) e sintaxe **EARS**
  na skill `verifiable-dod` (fecha absorção do ciclo 007). ADR 0008 aceito.
- **Toolkit dos ciclos 003–007**: 12 subagentes executáveis (`.claude/agents/`), 3 skills
  agentskills.io (`skills/`), 3 scripts do ritual (`scripts/`), diagramas do método
  (`docs/diagramas/`, md+PDF), avaliação do ecossistema SDD (`docs/research/` + ADR 0008)
  e Apêndice A do handbook (estudo do maestro-02).
- **Site V0 (storytelling + pipeline)**: capa narrativa `site/index.html` + motor
  `publicar/` (Markdown→site multipágina, sidebar, tema, callouts, gate de link quebrado)
  + roadmap de agentes (`docs/agents/perfis.md`, `comunicacao.md`) + deploy no GitHub Pages
  (`.github/workflows/pages.yml`).
- **Camada didática (spec 001)**: guia narrativo [`docs/comece-por-aqui.md`](docs/comece-por-aqui.md)
  (dor → jornada → sistema) + [`docs/governance/glossary.md`](docs/governance/glossary.md)
  (dicionário de todas as siglas); links no `README.md` e banners nos docs de governança.
  Compêndio PDF regenerado com Introdução + Apêndice Glossário (57 páginas).

### Fixed
- **A instrução da IA tinha derivado em três pontos** — achados da auto-instalação, todos
  da mesma família (lista à mão sem comparação com o disco): `AGENTS.md` estava sem a
  regra "skills primeiro" (do ciclo 011) e agora é **link simbólico** para `CLAUDE.md`
  (fonte única); a skill `living-journey` existia desde o ciclo 018 e era **invisível** para
  a IA; o Constitution Check dizia "I–VII" na skill, em `plan-architect` e em
  `process-guardian` — o princípio VIII existe desde o ciclo 013, ou seja, **oito ciclos
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
  function outra vez. Corrigido em `.specify/templates/plan-template.md` e `new-cycle.sh`.
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
  **ciclo real** (o `promote-main.sh` como materialização do princípio, com saída de
  comando verificada), anti-padrões, verificação e "o que roubar" — preservando os 5
  frameworks avaliados, as 6 fontes e os conceitos do v1. Primeiro dos 12 a migrar.

- **Rebasing (FR4)**: referências a "Constituição / Princípio IV/V/VII" nos docs migrados
  passam a apontar para `docs/governance/principles.md` (via mapa de linhagem).

### Anterior
- **Fundação do repositório Maestro** (ADR 0007): metodologia extraída de `ghdaru`/
  `flowbuilder` para repositório próprio.
- `docs/governance/principles.md` — constituição própria da metodologia (v1.0.0).
- `docs/governance/operating-model.md` (v1.2.0) — papéis, cerimônias, artefatos,
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
  `principles.md` (mapa de linhagem no fim daquele doc).
- Remover as cópias redundantes da metodologia em `ghdaru` após validação desta migração.
