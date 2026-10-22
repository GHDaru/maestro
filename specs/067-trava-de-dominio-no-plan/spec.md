# Spec 067 — Trava de domínio no plan (o modelo de domínio é declarado, nunca omitido)

> **Spec retroativa.** O código já existe: branch `trava-dominio-plan`, ponta `db6b89c`, 3 commits
> de 02 e 03/10/2026 pela equipe do projeto Hindiana (`14f77a5` trava de método no template e
> no painel; `a94574a` forma itemizada das invariantes; `db6b89c` DORA só com deploy de produção).
> Esta spec registra o QUÊ e o PORQUÊ que o código obedece, para que o plano, a revisão em
> contexto fresco e o portão humano tenham contra o que medir. Nada aqui foi inventado além do
> que a branch faz; o que o código traz e a spec não pediu está em "Limites declarados".

- **Status**: Implementado retroativamente na branch `trava-dominio-plan` (`db6b89c`); ciclo 067 pela decisão do Darú (decisao-066-daru-20-10, mapa de integração) · **Raia**: plena · **Data**: 2026-10-20
- **Origem**: achado de 03/10/2026 no projeto Hindiana (mensagens dos commits `14f77a5` e
  `a94574a`): **uma rodada inteira entregou regras de negócio dentro de rotas porque o plano foi
  pulado** — a linguagem ubíqua e os agregados nunca foram discutidos. O `plan.md` é o único
  lugar do fluxo onde o domínio se decide; pulá-lo não produz sintoma (anti-padrão 22, a cópia
  com perdas), e o painel do ciclo 066 não mostrava quem tinha pulado.

> **Raia**: plena, e não infra. Regra aplicada: `docs/governance/operating-model.md` §3 reserva a
> raia infra para "infraestrutura, migração, deploy" — o que muda estado fora do repositório e
> precisa de backup, dry run e rollback (§7). Este ciclo muda um **portão do método**
> (`check-conformance.sh`), um template e o painel: tudo texto versionado, desfeito por
> `git revert`, sem dado migrado nem ambiente tocado. O `artifacts.md` não classifica portões
> como infra; ele só exige que a mutação do portão seja mostrada (`TAIL:mutation`), e isso a
> raia plena carrega. **Ambiguidade** média (onde a invariante "pode" morar na borda é juízo);
> **raio** amplo (todo ciclo deste repositório e de todo projeto instalado a partir do 067 passa
> a ser cobrado); **irreversibilidade** baixa (um revert em três arquivos; o piso impede apenas
> afrouxar por variável de ambiente, nunca reverter o código).

## Glossário deste ciclo

| Termo | O que é aqui |
|---|---|
| **DDD** (*domain-driven design*, projeto dirigido pelo domínio) | A disciplina de desenhar o software a partir do modelo do negócio e da língua que o negócio fala. Os quatro conceitos abaixo vêm dela. |
| **Linguagem ubíqua** | O vocabulário único, acordado entre quem pede e quem constrói, usado no código, nos testes e na conversa. No Maestro mora no glossário do projeto. |
| **Raiz de agregado** (*aggregate root*) | A entidade que guarda a consistência de um grupo de objetos: toda mudança entra por ela, e é ela quem garante as invariantes. |
| **Invariante** | Regra de negócio que precisa valer sempre ("peça sem evidência não muda de estado"). Mora no **domínio** (agregado, objeto de valor, serviço de domínio) ou, por exceção justificada, na **borda** (rota, adaptador, tela). |
| **Porta / adaptador** (*port/adapter*) | A porta é a interface que o domínio expõe ou exige; o adaptador é quem a implementa com tecnologia (HTTP, SQLite, arquivo). |
| **DOM** | Prefixo dos quatro tokens legíveis por máquina no `plan.md`: `DOM:aggregate=`, `DOM:invariants=`, `DOM:glossary=`, `DOM:ports=`. Mesma forma dos `ART:*` do ciclo 042. |
| **DORA** (*DevOps Research and Assessment*, as quatro métricas de entrega) | Frequência de deploy, tempo de entrega, taxa de falha e tempo de recuperação. O painel mostra cada número com a fonte ao lado. |
| **Piso** (*floor*) | O número do ciclo a partir do qual uma regra do portão é cobrada; ciclos anteriores carregam dívida declarada, nunca ruído. |

## O quê e por quê

### 1. O domínio só se decide no plano — e o plano era pulável sem sintoma

O fluxo é `spec → plan → tasks → implement`. A spec diz o quê; o plano é onde se decide **qual
agregado muda, onde as regras moram, que termo entra na linguagem ubíqua e que porta se abre**.
No Hindiana, uma rodada inteira pulou o plano e o código saiu com regras em rotas e termos que
ninguém combinou. Nenhum portão reclamou: o `check-conformance.sh` cobrava os cinco artefatos
condicionais (`ART:*`), mas nada cobrava o domínio.

### 2. O remédio é o mesmo do ciclo 042: declarar, nunca omitir

A omissão não viola nada visivelmente — por isso precisa de contagem. O template do plano ganha
uma seção "Domain model (declare all four — silence is not a decision)" com quatro tokens, cada
um com valor e motivo, e o portão os lê como lê os `ART:*`. `edge` (borda) é permitido, mas só
com o motivo de por que a regra não pode morar no domínio: o que se proíbe é a borda **por
descuido**, não a borda **decidida**.

### 3. O painel aponta quem pulou; o DORA para de contar staging

Dois ajustes no painel do ciclo 066, no mesmo lote: a tela de specs marca a spec sem `plan.md`
ou sem tarefas (é a spec que pulou o passo onde o domínio se decide), e a frequência de deploy
do DORA conta **só deploy de produção** — staging e dev inflavam o número.

## Requisitos funcionais (FR, de *functional requirement*)

- **FR1 — O template do plano carrega as quatro declarações.** `.specify/templates/plan-template.md`
  DEVERÁ ter uma seção de modelo de domínio com os tokens `DOM:aggregate=`, `DOM:invariants=`,
  `DOM:glossary=` e `DOM:ports=`, cada um numa linha de tabela com coluna de motivo, e um
  comentário que diz o que cada valor significa (`none`/`changed`; `domain`/`edge`).
- **FR2 — O portão lê as declarações a partir do ciclo 067.** `scripts/check-conformance.sh`
  DEVERÁ, para todo ciclo ≥ piso, exigir os quatro tokens no `plan.md`, cada um com valor e
  motivo não-esqueleto; `DOM:invariants=edge` sem motivo DEVERÁ reprovar. A falha é **soft**
  (reprova na corrida padrão; é só nota em `--ticked-only`), como as `ART:*`. Abaixo do piso,
  o portão DEVERÁ imprimir que não checou, nunca silenciar.
- **FR3 — O piso é um botão que só aperta.** `MAESTRO_MIN_CYCLE_DOMAIN` DEVERÁ aceitar apenas
  número; valor não numérico ou acima do piso embutido (67) DEVERÁ abortar com código 2 e
  mensagem — falha fechada, mesmo precedente dos pisos de mutação e de ausência.
- **FR4 — Forma itemizada das invariantes.** Além de `domain` e `edge`, `DOM:invariants=`
  DEVERÁ aceitar `regra_a=domain | regra_b=edge(motivo)`: cada item é `regra=domain` ou
  `regra=edge(porquê)`; item `=edge` sem parênteses ou em forma desconhecida DEVERÁ reprovar,
  nomeando o item.
- **FR5 — O painel marca a spec sem plano ou sem tarefas.** Na tela de specs, o cabeçalho de
  cada repositório DEVERÁ mostrar o contador "N sem plan ou tasks" quando houver spec sem
  `tem_plan` ou sem `tasks_total`, e a linha da spec DEVERÁ mostrar "falta" na coluna Plan.
- **FR6 — DORA conta só deploy de produção.** `v_dora` DEVERÁ incluir na frequência de deploy
  apenas eventos `deploy` cujo `ambiente` na evidência seja produção ou esteja ausente (ausente
  = produção, para não apagar os registros anteriores a esta regra); `staging`, `dev` e
  qualquer outro DEVERÃO ficar fora.

## Fora de escopo

- Ensinar DDD: o template aponta para a linguagem ubíqua e os agregados **existentes** do
  projeto; não há capítulo nem skill de domínio neste ciclo.
- Validar o **conteúdo** das declarações (se o agregado existe, se o motivo é bom) — isso é a
  revisão em contexto fresco e o portão humano, não o grep.
- Renomear os termos do painel (`tem_plan`, `tasks_total`) ou mudar o esquema do SQLite
  (*Structured Query Language*, banco em um arquivo): nenhuma coluna nova.
- Reescrever os planos dos ciclos 042–066 com tokens `DOM` — dívida declarada, piso 67.
- Exigir `ambiente` no registro de deploy (`registrar.py`): o campo continua opcional.

## Artefatos condicionais que o plano DEVERÁ declarar (`docs/governance/artifacts.md`)

| Artefato | Declaração | Motivo em uma linha |
|---|---|---|
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova: os tokens são texto num template; o painel não ganha coluna nem tabela. |
| `contracts/` | `ART:contracts=no` | Nenhuma rota, porta ou evento novo; os tokens são lidos do disco pelo mesmo script que já lê `ART:*`. |
| `ux-design.md` | `ART:ux-design=no` | O painel muda um contador e um filtro em telas que o ciclo 066 já desenhou (`ux-design.md` de lá); nenhum papel semântico novo, nenhuma visão nova. |
| `research.md` | `ART:research=no` | Nenhuma incógnita técnica: a forma dos tokens e dos pisos copia o que o portão já faz desde 042/055/061. |
| `checklist.md` | `ART:checklist=no` | A DoD (*Definition of Done*, definição de pronto) abaixo cobre o que há para checar. |

## Critérios de aceite

- `grep -c 'DOM:' .specify/templates/plan-template.md` → `4` (`plan-template.md:66-69`), e
  `grep -c '^## Domain model' .specify/templates/plan-template.md` → `1`.
- `MAESTRO_MIN_CYCLE_DOMAIN=abc scripts/check-conformance.sh 067` → exit `2`, saída contém
  `is not a number`.
- `MAESTRO_MIN_CYCLE_DOMAIN=99 scripts/check-conformance.sh 067` → exit `2`, saída contém
  `above the built-in floor 67`.
- `MAESTRO_MIN_CYCLE_DOMAIN=60 scripts/check-conformance.sh 066` → o bloco 3b **roda** sobre o
  066 (o botão apertou) e reprova com `domain model never declared in plan.md`.
- WHEN o `plan.md` de 067 não tem nenhuma linha `DOM:` THE SYSTEM SHALL imprimir
  `domain model never declared in plan.md: aggregate invariants glossary ports` e sair com
  código 1 na corrida padrão; em `--ticked-only` a mesma linha sai com `·` e exit 0.
- WHEN o `plan.md` tem `DOM:invariants=edge` sem motivo THE SYSTEM SHALL imprimir
  `domain invariants: declared DOM:invariants=edge with no reason`.
- WHEN o `plan.md` tem `` `DOM:invariants=transicao=domain | consulta=edge(só leitura, sem regra)` ``
  THE SYSTEM SHALL aceitar (nenhuma linha `✗` do bloco 3b); com
  `transicao=domain | consulta=edge` THE SYSTEM SHALL imprimir
  `'consulta=edge' is edge with no reason`.
- WHEN os quatro tokens têm valor e motivo THE SYSTEM SHALL imprimir
  `domain model declared (aggregate, invariants, glossary, ports) with a reason`.
- `scripts/check-conformance.sh 066` → continua verde e imprime
  `domain-model declarations: not checked below cycle 67` (o piso deixa o 066 em paz).
- `python -m unittest discover -s painel/tests -p test_painel.py` → `Ran 12 tests`, `OK`
  (medido: 12 `def test_` em `test_painel.py`; `db6b89c` não acrescentou teste).
- `grep -c 'DORA counts production only' painel/server.py` → `1` (`server.py:158`, em `v_dora`;
  o filtro é `_ambiente(e) in ("", "production", "producao", "produção")`, `_ambiente` em
  `server.py:141`). Lacuna declarada: `test_dora_nao_conta_merge_como_deploy` prova "merge não é
  deploy", **não** "staging não é deploy" — o teste do filtro de ambiente é dívida do plano.
- `grep -c 'sem plan ou tasks' painel/index.html` → `1` (`index.html:293`) e
  `grep -c 'tem_plan' painel/ingest.py` → `1` (a coluna já existia no 066; só a tela mudou).
- `scripts/check-language.sh` → verde (template, script e comentários do painel em inglês).
- `scripts/check-conformance.sh 067` → verde após o plano (com os quatro `DOM`), as tasks e o
  `qa-report.md`.

## Limites declarados

- **Este ciclo é o primeiro acima do piso — o próprio `plan.md` do 067 DEVERÁ carregar os
  quatro tokens `DOM` com motivo.** Essa é a mutação a rodar no `TAIL:mutation`: apagar uma
  linha `DOM:` do plano do 067 e ver o portão reprovar; trocar um `edge(motivo)` por `edge` e
  ver a linha nomeando o item; restaurar e ver verde. O ciclo que cria o portão não pode ser
  o primeiro a dispensá-lo.
- **A borda é permitida com motivo; o motivo não é lido.** `edge(porque sim)` passa pelo grep.
  O que o portão garante é que a decisão foi **escrita**, para a revisão ler — não que foi boa.
- **`ambiente` ausente conta como produção** (`_ambiente` devolve `""`). É compatibilidade com
  os deploys registrados antes desta regra, e é também um furo: um deploy de staging registrado
  sem `ambiente` entra na conta. Fechá-lo é exigir o campo no `registrar.py` — fora de escopo.
- **Testes depois do código**, como no 066 (Princípio IV): `db6b89c` muda o `v_dora` sem teste
  do filtro. Registrado aqui e no `qa-report.md`; o plano decide se o teste entra neste ciclo.
- **Códigos de saída desiguais entre pisos**: o piso de domínio aborta com `2`; os de ausência
  e mutação, com `1`. É o que o código faz; uniformizar é ciclo de manutenção do portão.
- **Escopo que `14f77a5` traz e esta spec não pediu**: a contagem "N sem qa-report" no mesmo
  cabeçalho do painel. É marcador irmão do FR5 e fica declarado como entregue.

## Ambiguidades para o Darú

Nenhuma encontrada. O número do ciclo (067) e a branch de origem vêm da decisão
`decisao-066-daru-20-10`; a raia está justificada acima pela regra do §3; os seis requisitos
são lidos do diff, não inferidos. Se o Darú discordar de **`ambiente` ausente = produção**
(limite 3), isso vira requisito do ciclo seguinte, não desta spec.

<!--
  GATE (DoR — não delegável): esta spec só vira plano depois da aprovação do Darú.
  Handoff: spec-agent → (aprovação) → plan-architect.
-->
