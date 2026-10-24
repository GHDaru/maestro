# Pareceres dos especialistas — decisão "7 sessões via gateway MaaS" (19/10/2026)

## 1. Guardião do processo (process-guardian) — veredito NON-COMPLIANT

Fontes: principles.md (III, V, VI), operating-model.md §7–§8, skills/anti-patterns, .claude/settings.json.

**D1 — token no .claude/settings.local.json deste repo**
- Classe: leitura sensível → ação externa (§8 exige política e mascaramento). Raio: credencial em 2 repos e 7 sessões; git-ignore global evita commit, não evita logs/transcrições/screenshots.
- Reversibilidade: token em variável de ambiente do usuário ou gestor de segredos; o arquivo do repo sem valor literal; rotação prevista.
- Decisão: HUMANA (segredo = sensitive read). Anti-padrões 2 (contexto tribal), 10 (mudança silenciosa de escopo — 066 é painel, não troca de provedor).
- Recomendação: humano configura o token fora do repo; o agente não o escreve.

**D2 — sondar o gateway com curl**
- Classe: ação externa (§8: confirmação forte). Envia o token a endpoint nunca avaliado em ADR; precedente de o agente redirecionar o próprio tráfego.
- Reversibilidade: dry run sem credencial (docs do gateway) ou o humano roda o curl e cola só a lista de ids.
- Decisão: delegável só após confirmação forte; "este gateway é aceitável?" é humana e cabe num ADR. Anti-padrões 7, 5.
- Recomendação: humano roda a sonda ou fornece a lista.

**D3 — copiar permissions.allow = Bash, PowerShell, Edit, Write sem prompts**
- Classe: batch/admin → BLOQUEADO (§8): elimina todos os `ask` de 7 sessões; raio = disco inteiro.
- Reversibilidade: allowlist mínima por tarefa, deny explícito (rm, git push), worktree por Worker, guard-immutables ativo → baixa para "criação reversível".
- Decisão: HUMANA, não delegável ("autorização vive fora do modelo"). Anti-padrões 4 (7 agentes para um painel local), 6 (Gerente que delega e revisa os próprios Workers), 23 (porta nova sem avisar os guardas).
- Recomendação: não copiar; allowlist mínima própria deste repo, aprovada pelo humano.

**Hooks da Hindiana: NÃO copiar** (Princípio VI — função já servida por guard-immutables.py, session-state.sh, stop-conformance.py; caminhos absolutos para outro repo; escrevem no SQLite da Hindiana; bloqueiam edições fora de um mapa de worktrees que não existe aqui). Anti-padrões 13, 22. Status por sessão, se preciso, é artefato do ciclo 066 nascido da spec.

**Nota de processo:** troca de provedor e topologia 1+6 devem ir à spec e a um ADR antes de qualquer sessão abrir.

## 2. Segurança (security) — 6 achados

1. ALTA — token no arquivo do repo. Protegido só pelo ignore global do usuário (não está no .gitignore do Maestro). `env` do settings vira variável herdada por TODO subprocesso (Bash, PowerShell, hooks, o painel web dos workers): qualquer `env`, log de erro ou página de depuração grava o token nos transcripts em ~/.claude/projects. O allow `Bash(grep -inE "password|…|token…")` sobre .claude/ imprime a linha do token. Mínimo: tirar ANTHROPIC_AUTH_TOKEN do repo; no repo só BASE_URL e modelos. Gate humano; irreversível (vazou = rotacionar).
2. ALTA — PowerShell sem guarda. allow libera Bash, PowerShell, Edit, Write em branco; guarda_bash.py tem matcher só `Bash` → `powershell git push --force` passa limpo; também gh, python -c subprocess, Remove-Item -Recurse. Deny mínimo: Bash(git push *), PowerShell(git push *), Bash(git tag -d *), Bash(git push --delete *), Bash(gh *), Bash(rm -rf *), PowerShell(Remove-Item *), Edit(docs/records/**), Edit(docs/adr/**), Read(**/.env), Read(**/settings.local.json). WORKTREE POR SESSÃO É NECESSÁRIA: guarda_edicao.py deriva escopo do toplevel do cwd → 6 workers no mesmo checkout = zero isolamento.
3. ALTA — hooks falham abertos e apontam para a Hindiana. session_id do Maestro não está no sessoes.json da Hindiana → return 0 (guardas silenciosamente inativas); sessao.py com MAESTRO_SESSAO grava no painel/dados/hindiana.db e injeta estado da Hindiana no contexto do Maestro. Recomendação: ADAPTAR, não copiar: .maestro/controle/hooks/ deste repo, caminhos via $CLAUDE_PROJECT_DIR, matcher Bash|PowerShell, sessão não mapeada = bloquear (fail-closed) ao menos push/rebase/amend.
4. MÉDIA — allows de produção da Hindiana (railway, ssh runner2, az pipelines, prod_leitura/prod_para_dev) não têm função aqui. Remover.
5. MÉDIA — residência de dados: código, CLAUDE.md, prompts e dados da Hindiana passam a gateway terceiro em ap-southeast-1 (GLM/DeepSeek). Dado pessoal = transferência internacional (LGPD), decisão humana em ADR. Robustez a prompt injection desconhecida: autorização nos hooks/deny, nunca no modelo.
6. BAIXA — regras .env/backups_producao são da Hindiana; reescrever para este repo.

Configuração recomendada: env só com BASE_URL e modelos; allow mínimo; deny do achado 2; hooks adaptados; token fora do repo; .claude/settings.local.json no .gitignore do Maestro; um worktree por worker; só o Gerente tem push, e só após gate humano.

## 3. Guia do Claude Code (docs oficiais)

1. Precedência de modelo: /model > `claude --model` > ANTHROPIC_MODEL > `model` em settings > ANTHROPIC_DEFAULT_MODEL. Flag e env valem só para a sessão iniciada com elas. → `--model` por sessão funciona.
2. Gateway: ANTHROPIC_BASE_URL; ANTHROPIC_AUTH_TOKEN (Bearer) para gateways bearer; ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL remapeiam os aliases (frontmatter de subagente: inferência, não confirmado). ANTHROPIC_SMALL_FAST_MODEL está DEPRECATED.
3. Token: precedência cloud > ANTHROPIC_AUTH_TOKEN > ANTHROPIC_API_KEY > apiKeyHelper. Local mais seguro fora do repo: `~/.claude/settings.json` bloco `env` (escopo de usuário) ou variável do shell. apiKeyHelper para bearer: NÃO confirmado.
4. `claude --name <n>` existe (nome da sessão; `--resume <nome>`); CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 é documentada (força persistência quando lançado dentro de outra sessão).
5. Permissões: sintaxe atual `"Bash(git push *)"`; a forma `:*` não aparece na doc atual. Limite: `git -C . push` não casa. Ordem: deny → ask → allow; o primeiro que casa decide, deny vence allow.
