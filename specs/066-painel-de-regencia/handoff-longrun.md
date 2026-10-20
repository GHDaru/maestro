# Longrun do ciclo 066 — estado e pendências do Darú

> Escrito em 19/10/2026 23:30 pela sessão MAESTRO, quando o Darú foi descansar. Regras do
> longrun: parar em **90 % do consumo semanal** (medido por `get_usage`; estava em 68 %);
> acordador **PACE** a cada 30 min (cron `db780fb2`, expira em 7 dias); nada que dependa do
> Darú é decidido por mim — vai para a lista abaixo. Toda decisão passa por especialistas em
> contexto fresco e é registrada em `docs/records/decisoes.jsonl`.

## 1. O que está feito

| Item | Estado |
|---|---|
| Ciclos 064 (capa) e 065 (livro de ponto) | promovidos à `main` `af6fd1b`, CI verde |
| 42 branches da linha paralela (`DriveD\maestro`) | **publicadas no GitHub** (autorizado pelo Darú) |
| Plano de integração da linha paralela (Opus) | pronto, em `plano-integracao-linha-paralela.md` |
| Jira como barra | site `ghdaru.atlassian.net`, projeto **Painel de Regencia (REG)**, quadro 2, colunas G0–G9 |
| Decisão "sessões via gateway" | `decisao-066-sessoes-via-gateway` (3 pareceres: guardião, segurança, guia) |
| Insumos do Hindiana (Assistente + agente explorador) | `insumo-hindiana.md` |

## 1b. Feito na madrugada de 20/10 (depois das suas seis respostas)

| Item | Estado |
|---|---|
| Suas decisões registradas | `decisao-066-daru-20-10` (modelo 4.1, allowlist, plano integral, fixture, numeração) |
| Segredos fora do repo | `.gitignore` cobre `.env` e `.claude/settings.local.json`; `settings.local.json` sem token (só gateway, modelos, allow/deny) |
| Lançador de sessões | `scripts/multi-session.py`: `--model` por sessão, uma worktree por Worker, dry-run testado (`d5feef2`) |
| **Ciclo 066 = painel v0** | worktree `.claude/worktrees/integra-066`, branch `integra/linha-paralela-066`, 16 commits sobre a `dev`: merge `023694b` de `a1172a2`; spec retroativa (revisada, RETURN → corrigida); ADR 0022 (rascunho promovido por `git mv`); `boundary.json` com `painel/` e `.maestro/`; fixture `exemplo.json` no lugar do dado real; plan (CC 8/8, IV violado e justificado), tasks, data-model, contracts, ux-design; qa-report com saídas reais; `check-conformance.sh 066` **verde**; `fafae7d` |
| **Ciclo 067 = trava de domínio** | merge `b5775ac` de `db6b89c`; spec, plan com os quatro `DOM:*` (primeiro acima do piso), ADR **0023** (a revisão apontou que a constituição o exige), CHANGELOG, roadmap F31, glossário +5; três mutações do bloco 3b observadas (inclusive o defeito da forma itemizada numa linha de tabela, registrado com dono); security verde; `check-conformance.sh 067` **verde**; `bb90987` |`n| **Ciclo 068 = chamados gate a gate** | merge `120a32c` do trecho `db6b89c..2796cbf`; dado real do Hindiana trocado por fixture; spec, plan com `DOM:*`, data-model, contracts, ux-design apontador; 6 + 12 testes verdes; 4 mutações; security classe média, 6 baixos (`custo.py` guarda **só contagens** — resposta à sua pergunta de privacidade; falta filtro por igualdade); review RETURN → 2 bloqueantes tratados; CHANGELOG, roadmap F32, glossário +9; conformance **verde** |`n| **Ciclo 069 = conferidor pela data** | merge `23f8325` de `aa0efd1` (chamado 070 do Hindiana; `699bddb` deixado fora, só perde arquivos); veredito vigente pela data do cabeçalho (`ordem_veredito`, função pura); 10 testes; o primeiro ciclo integrado em que o Princípio IV vale (vermelho `6741315` → verde `d2822ef`); a pasta `specs/070-conferidor-ordem-veredito/` entra como evidência imutável; security OK (um médio pré-existente: `data()` deixa `strptime` estourar); review APPROVE_WITH_NOTES, dois itens tratados (um era eu nomeando teste sem ler a saída); CHANGELOG, roadmap F33, glossário +2; conformance **verde** |`n| Cauda do 066 | review APPROVE_WITH_NOTES (notas tratadas); security classe média, **2 achados médios viram dívida do 072** (CSRF no POST, `autor` forjável via MCP — `security-pass.md`); mutação do `boundary.json` provada |
| Medido nesta máquina | painel 12 OK; hook 34 passed; ingest da fixture lê 64 specs / 155 decisões / 143 commits; boundary, language, adr, version, links, flags verdes |

## 2. Pendências do Darú (nada disso é feito sem você)

0. **Gate do ciclo 066** (`TAIL:gate` em `specs/066-painel-de-coordenacao-v0/tasks.md`) e o
   merge de `integra/linha-paralela-066` na `dev`. **O push dessa branch está bloqueado** pelo
   `deny: Bash(git push *)` que eu escrevi em `.claude/settings.local.json` para os Workers — ele
   vale também para a sessão MAESTRO. Você decide: (a) excepciona esta sessão (remove a linha do
   deny, ou muda o modo e aprova o push), ou (b) faz o push à mão:
   `git -C .claude/worktrees/integra-066 push -u origin integra/linha-paralela-066`.
   Aceite também as duas dívidas médias de segurança como dívida do 072.

1. **Token do gateway MaaS fora do repositório.** Ponha `ANTHROPIC_AUTH_TOKEN` no bloco `env`
   de `~/.claude/settings.json` (escopo de usuário). Eu não escrevo o token: o classificador
   bloqueou e os três pareceres concordam que é sua decisão (segredo = leitura sensível).
2. **Ids de modelo no gateway.** Confirme os nomes aceitos (o Hindiana usa `glm-5.3`, `glm-5.2`,
   `deepseek-v4.1-flash`; você pediu "deepseek 4.4 flash"). Eu não sondo o gateway.
3. **Aceitabilidade do gateway (ADR).** Residência `ap-southeast-1`, LGPD se dados da Hindiana
   passarem por ele; robustez a prompt injection desconhecida. Recomendação: aceitar para o
   painel do Maestro (código público), **não** para dados pessoais da Hindiana.
4. **Allowlist das 7 sessões.** Aprovar a lista mínima proposta em `pareceres-…md` §2
   (deny: git push, gh, rm -rf, Remove-Item, docs/records, docs/adr, .env, settings.local.json;
   uma worktree por Worker; só o Gerente faz push, e só após o seu gate).
5. **Plano de integração — decisões 1–5 e 9 do plano** (resumo): `painel/` e `.maestro/`
   entram no `boundary.json`? 068 e 069 (WhatsApp, receptor) vão para o repo da Hindiana?
   Trocar dados reais da Hindiana por fixture (o repo é público)? 066-custeio vira só insumo?
   Mover `scripts/hooks/workflow_*.py` para `painel/hooks/`? Apagar as branches remotas
   depois das tags `arquivo/paralela/*`?
6. **Numeração final.** O plano propõe 066 = painel v0 … 072 = painel de regência. O esqueleto
   local `specs/066-painel-de-regencia` será renumerado quando você aprovar o mapa.
7. **Jira:** o quadro REG está vazio; se quiser cartões de exemplo (um chamado por coluna),
   autorize — é escrita na sua conta.
8. **TAIL:gate** de cada ciclo integrado é seu, por ciclo.

## 3. O que eu faço sozinho no longrun (reversível, dentro do repositório)

- Spec, plan (Constitution Check) e tasks do **primeiro ciclo da integração** (painel v0 +
  ADR 0022 a partir do rascunho), em branch própria, **sem merge**.
- Tags `arquivo/paralela/<branch>` nas 42 pontas — **locais**, sem push.
- `ux-design.md` do painel de regência (agente `ux-semantics`), a partir dos insumos.
- Portões rodados e registrados; nada promovido.
- Respostas ao PACE a cada 30 min, com consumo medido.

## 3b. Por que parei antes do 070 (decisão de ritmo, 20/10 07:50)

O consumo semanal estava em 74 % (limite 90 %), mas o **contexto desta sessão em 78 %**. O 070
(workflow SQLite + hooks, linhagem A) é o ciclo com o conflito real entre as duas linhagens, e
custaria o espaço que falta para fechar com handoff íntegro. Quatro ciclos fechados e verdes
valem mais que um quinto pela metade. Nada do 070 foi iniciado.

## 3c. Ponto de retomada exato: ciclo 070 (e 071)

Tudo medido em 20/10 07:50 na worktree `.claude/worktrees/integra-066` (branch
`integra/linha-paralela-066`, HEAD `7d57e27`, 56 commits sobre a `dev`):

- **070 = workflow SQLite + hooks**: `git merge --no-ff --no-commit b33bb81`. Dois conflitos,
  já conhecidos: (a) `painel/projetos/hindiana.json` — modify/delete; resolver por `git rm`
  (a fixture `exemplo.json` já absorve as chaves; conferir com o mesmo diff de chaves do 068);
  (b) `painel/index.html` — conflito de conteúdo A × B; **B prevalece** (decisão 7 do plano de
  integração), A se adapta até os testes da linhagem A ficarem verdes. Depois do merge:
  `git mv scripts/hooks/workflow_*.py painel/hooks/` (decisão 5: tira do instalador e do
  `check-language`), ADR **0024** (hooks de terceiro gravando SQLite), roadmap F34, e a spec
  retroativa parte de `specs/064-workflow-painel/` (spec, plan, tasks, ux-design já existem na
  branch — renumerar para 070, como o 066 fez com o rascunho do ADR).
- **071 = board/rodada navegável**: `6e9788f` **contém** `b33bb81`, então 070 e 071 podem ser um
  merge só de `6e9788f`, se o Darú preferir um ciclo em vez de dois; a spec do 065-board está em
  `specs/065-board-rodada-navegavel/` na branch.
- **Padrão que funcionou nos quatro ciclos** (seguir à risca, economiza uma rodada cada):
  1. `git merge --no-ff` → testes dos dois lados → portões de índice (`gates-after.sh`).
  2. **Criar o `qa-report.md` esqueleto antes de qualquer mutação** — sem ele o portão para em
     "missing qa-report" e nunca chega ao bloco 3b nem às caudas.
  3. spec-agent → plan-architect (com `DOM:*`; sem `|`, `<` ou `[` nas células; nenhum
     `DOM:x=` em prosa antes da tabela) → security e review em contexto fresco em paralelo.
  4. Mutação: **mudar a condição, não o nome** (068-b foi um rename e sobreviveu); capturar os
     nomes dos testes que falham **da saída**, nunca inferir (069: o review me pegou).
  5. Nas caudas do qa-report, nenhum `<` nem `[` literal: o `is_placeholder` do portão os lê
     como esqueleto (custou uma rodada em 066, 067, 068 e 069).
  6. Tudo que atravessa PowerShell → bash vai em arquivo `.sh` no scratchpad (`|`, `$(` e `✓`
     dentro de aspas são reescritos).
- **Scripts prontos no scratchpad desta sessão** (efêmero; recriar se sumirem): `gate067.sh`
  (parametrizar o número), `gates-after.sh`, `gate-all.sh`, `readlog.sh`, `mutate-dom.sh`,
  `record_decision.py` (o `record-decision.sh` não roda do PowerShell: BOM e aspas).

## 4. Como retomar

Branch `066-painel-de-regencia`. Leia este arquivo, depois `plano-integracao-linha-paralela.md`
e `pareceres-sessoes-via-gateway.md`. Decida a seção 2 na ordem; a 1 e a 4 destravam as sessões.
