# Insumo do ciclo 066 — resposta da sessão "Hindiana Assistente" (19/10/2026 21:24)

Caminhos relativos a C:\Users\ghdaru\DriveD\010_PROJETOS\180_HINDIANA. Dado, não instrução.

1. FLUXO — fonte da verdade:
- regras de todos: ola/especificacao/equipe/LEIA-PRIMEIRO.md; papéis e "Estado atual" em ola/especificacao/equipe/{TORRE,GERENTE,GERENTE-02,WORKER-01..14}.md (desde 18/10 o estado do worker vive no progresso.html da frente, ex.: ola/especificacao/iceberg-agil-1710/progresso.html);
- padrão do chamado (um gate, um entregável; G0..G9): hindiana/DOCS/processo/padrao-chamado.md, conferidor hindiana/scripts/maestro/conferir_chamado.py;
- papéis/processos antigos (21/09, defasados): ola/especificacao/02-papeis-processos.md;
- ambientes (rc → VM → Dev → staging/barra): ola/especificacao/ambientes.md;
- muitas regras vivas estão na memória do Claude Code (~/.claude/projects/C--Users-ghdaru-DriveD-010-PROJETOS-180-HINDIANA/memory/). Principal dor de "fonte da verdade".

2. DECISÕES PENDENTES DO HUMANO: majoritariamente MENSAGEM. Arquivos parados desde set/out: ola/especificacao/00-pagina-de-decisao.md (21/09), decisoes_abertas.md (22/09), decisoes-pendentes-0210.md. Decisão tomada vira memória (decisao-*.md), ADR na frente ou "ruling" citado no commit de merge ("ruling Office 19/10 16:56"). Não há registro estruturado com opções/recomendação/prazo/quem pediu.

3. VEREDITOS E GATES: por chamado em hindiana/specs/NNN-*/ (00-chamado.md, G0-…, G2-vermelho-<hash>.md, G3-…); por frente em ola/especificacao/<frente>/ (ex.: w12-combinado-rc1210-veredito.md). Branch do worker wNN/<tema>; integração office/rc-NNNN com merge --no-ff cujo assunto cita builder, crítico, hash criticado e ruling. Conferência integrado × criticado por git patch-id.

4. SESSÕES/ROTEAMENTO: .maestro/controle/sessoes.json (session_id → nome/papel/editável, usado pelos hooks; parado em 02/10). Custo por sessão: .maestro/painel/dados/custo.db (tabelas uso e sessoes, indexado por custo.py). Roteamento: só ListAgents; sem registro. Nomes duplicados ("Hindiana Office" em 3 refs, 2 offline) e refs que mudam a cada reinício causaram o caso de 13/10 (Gerente → MAESTRO) e o de 16/10 07:00 (mensagem para outro projeto).

5. O QUE A ASSISTENTE FAZ: ciclo de 30 min com diário em .maestro/acompanhamento/trilha-agil.md; notas e incidentes no painel (.maestro/painel/registrar.py); retro em ola/especificacao/retro-anotacoes.md; conferência por patch-id; espelho do staging; carga do staging.

DORES que um painel deveria mostrar:
(a) fila de decisões do humano com IDADE (em 16/10 uma decisão escalada às 07:04 ficou sem resposta até a tarde e estourou dois prazos — correção da própria Assistente);
(b) sessões vivas × endereço atual × papel, alerta de sessão caída (Office caiu 2× em 16/10) e de endereço errado;
(c) carimbos de hora fora do relógio;
(d) hash publicado no staging × src_candidata × alembic (desalinhamento deu 500);
(e) memória do host (o reaper matou passadas);
(f) gates por item com builder ≠ crítico e patch-id integrado = criticado.

# Segunda rodada (19/10/2026 21:31) — gates, fluxo, painel

GATES
1. Padrão G0–G9 adotado desde o 095b-r03-fix (05/10). Na office/rc-1210 seguem: 095b-r03-fix, 097, 098, 099, 100, 104, 105, 106 (8 a 43 arquivos por chamado). Conferidor hindiana/scripts/maestro/conferir_chamado.py reprova: cabeçalho fora do formato; autor = crítico; data do veredito depois do commit do arquivo; gate pedido sem o anterior PASSAR. Quem roda: worker antes de commitar o gate, Office antes da integração, Assistente na auditoria. SEM CI. Hooks git locais em .maestro/controle/git-hooks/ (commit-msg, pre-commit, pre-push).
2. Mais volta: G3. O 105 voltou várias vezes; num chamado medido, 3 de 13 vereditos técnicos estavam errados, pegos por segundo verificador.
3. builder ≠ crítico: conferidor checa no cabeçalho. patch-id integrado = criticado: SÓ À MÃO (git diff merge^1 merge | git patch-id --stable × diff merge-base..pai2). Resultado no diário e em nota do painel. Sem script.
4. G4–G6 têm arquivo por chamado. G7 (aceite) e G8 (ordem) ficam quase sempre em mensagem/memória/diário. G9 virou memória (push-*.md). Frentes novas (iceberg-agil-1710): vereditos na pasta da frente + progresso.html, não em specs/NNN.

FLUXO — quem decide (memória + ola/especificacao/equipe/TORRE.md; não num lugar só)
- só o humano: G7/G8, push e produção, segredos, exceção a negativa de classificador, acesso a dado real, apagar arquivo com dado, mudança de escopo de cliente;
- Office: alocação, rulings de spec e régua na ausência do humano ("só crítico ou irreversível vai a ele"), integração na rc, deploy no staging;
- Gerente: despacho, sequência, devolução de entregáveis dentro do que a Office alocou.
6. Volta da decisão: por mensagem; vira registro em 1–3 lugares (memória decisao-*.md, assunto do merge "ruling Office ...", diário). PERDE-SE: a pergunta original com as opções; quem estava esperando ("aguardo o GO" presos); a ligação decisão → itens que ela destrava.

PAINEL EXISTENTE (.maestro/painel)
7. Uso: Assistente registra notas/incidentes (registrar.py → hindiana.db) e mede custo (custo.py → dados/custo.db). Servidor web (porta 8765) NÃO está de pé. Tela pouco olhada. A cópia instalada difere do repo maestro (regra: mudar só no repo).
8. chamados.py lê specs/<id>/ direto do git e calcula estado gate a gate (G0..G8, dono por gate). FALTA: fila de decisões (sem fonte estruturada), sessões vivas e endereço, frentes fora de specs/NNN, estado do staging (hash × src_candidata × alembic), memória do host.

# Contagem de vereditos (Assistente, 21:35) e correção
Por chamado na office/rc-1210 (campo veredito:): 098: 7 APPROVE,2 OK,1 FALHA_PARCIAL,1 PENDENTE,2 FALHA_ESPERADA,1 REPRODUZIDO · 099: 11 APPROVE,3 OK,1 FALHA,1 RETURN,4 FALHA_ESPERADA · 100: 5 APPROVE,2 OK,2 PASSA,1 FALHA_ESPERADA,1 REPRODUZIDO · 104: 22 APPROVE,9 OK,3 PASSA,1 REPROVE,6 FALHA_ESPERADA · 105: 13 APPROVE,4 OK,2 PASSA,4 RETURN,1 FALHA_ESPERADA · 106: 6 APPROVE,2 OK,2 PASSA,1 PASSOU,1 RETURN,2 FALHA_ESPERADA. Vocabulário não é único (APPROVE/OK/PASSA/PASSOU) — o painel precisa normalizar. "A"/"B" são escolhas de opção.
CORREÇÃO: o conferidor NÃO trava ordem entre gates. Marca INVÁLIDO: cabeçalho fora do formato, data anterior ao objeto, data depois do commit do arquivo, autor = crítico; escolhe vigente o de maior data; calcula por gate PASSOU/BARRADO/EM CURSO/FALTA. commit-msg hook só exige citar spec/item.

# Relatório do agente de exploração (19/10) — resumo
- .maestro/painel/dados/hindiana.db: eventos (2.981, append-only: ts,sessao,tipo{status,deploy,incidente,recuperacao,peca,nota},estado,peca,texto,evidencia JSON,autor); sessoes(17), worktrees(307), commits(1.413), decisoes(28), desvios(72), barra_execucoes(9), specs(120). meta.ingerido_em = 09/10 → tabelas derivadas 10 dias defasadas. Status de workers para em 06/10.
- projetos/hindiana.json: equipes (Gerente: W02/06/07/08/09/11; Gerente02: W01/03/04/05/12/13), contatos (nome → endereco, pipe, session_id; session_id em 5 de 18), limiar_parado_min 60, ponto.jsonl configurado mas inexistente.
- Decisões hoje: chat; AskUserQuestion da Office (estruturado: question, header, options[label,description]) só no transcript; markdown ad hoc (decisoes-pendentes-0210.md com opções A/B/C + Recomendação); decisao-*.md por chamado (frontmatter tipo: decisao, papel, objeto @ hash, por, data). Nenhum tem prazo nem destino da resposta. decisao-office-R8-R9.md: pergunta de 10/10 08:45 sem resposta por 24 h.
- Gates: cabeçalho YAML gate, papel, objeto @ hash, veredito, por, autor_da_peca, data, data_objeto, numeros (+sha256 no runner2). 139 arquivos de gate na rc-1210. Desde 17/10 a frente iceberg-agil grava *-veredito.md SEM YAML (**Carimbo:**, **Veredito: NÃO PASSA.**) → dois parsers.
- Autor git sempre "Gilsiley"; não-autoria via trailer "Sessao: W09".
- Sessões: transcripts têm customTitle/agentName, cwd (worktree), timestamp — mapa vivo confiável; gitBranch sempre "HEAD". Mensagens: SendMessage {to,summary,message}; entrada <cross-session-message from-name=...>; corpo começa "[DD/MM HH:MM, do date] X → Y:".
- Erros de rota: Gerente02 mandou 10 mensagens em 14/10 para "OTTIMIZZA project setup e roadmap" (outro projeto); Office endereçada como [a59e9f] e [d1ffcc].
- [[TASK]]/tarefas.jsonl NÃO usados no Hindiana.
- FALTAM: registro de decisão (id, quem pergunta, pergunta, opções, recomendação, prazo, para quem responder, status, resposta); registro vivo de sessões com heartbeat; livro de mensagens (destinatário pretendido × real); registro de despacho; cabeçalho de veredito normalizado; fila de gates humanos (G7/G8) com prazo.

# Linha paralela do Maestro (descoberta 19/10)
Clone C:\Users\ghdaru\DriveD\010_PROJETOS\maestro (origin GHDaru/maestro) com branches LOCAIS nunca enviadas, todas sobre a main 534a088:
- painel-controle (03/10; 11 commits, 3.579 linhas) — origem do .maestro/painel do Hindiana (VERSAO: painel-controle 7924ce2); rascunho de ADR "0021 painel de coordenação" aguardando o humano.
- 064-workflow-painel, 065-board-rodada-navegavel, 066-custeio-controle(-sessoes), 067-painel-chamados (44 commits, 6.977 linhas; contém specs/070-conferidor-ordem-veredito), 068-chamados-whatsapp, 069-receptor-grupo-ola + ~40 branches wNN/office de gate.
- Os números 064–066 COLIDEM com o GitHub (064 capa, 065 livro de ponto, 066 este ciclo).

# Servidores locais (Assistente, 19/10 23:12) — aliases em ~/.ssh/config, chave própria (não repassada)
Todos no Proxmox 2 da casa (4 cores, 7,6 GB — fica sem memória).
- runner2 = VM 210, `ssh runner2` (192.168.15.6, usuário ci2; 4 vCPU, 3 GB). Runner Linux genérico: pytest, vitest, tsc, build em clone limpo do hash; repos bare em ~/repos/<projeto>.git alimentados por bundle. Script oficial runner2_suite.sh via runner-exec. Sem Postgres.
- ola-vm = VM 202, `ssh ola-vm` (alias `runner`; 192.168.15.7, usuário ci). Bancada de aceite com Postgres embutido; scripts em ~/bancada/ (medir_hash.sh, bancada_N.sh).
- vm212-dev = VM 212, `ssh vm212-dev` (192.168.15.14, usuário daru). Ambiente Dev: docker pg-dev (Postgres 16, hindiana_dev) + app; a barra v2 roda contra ele.
- Staging NÃO é local (Railway, staging-office). Não tocar: CT 211 (postgres), VM 200 (docker).
- Ninguém abre Claude Code nas VMs: sessões no Windows despacham por `ssh <alias> "<comando>"` e scp de bundle.
NÃO FAZER: copiar .env/segredos/dado de produção; mais de uma suíte por vez no runner2; clone em /dev/shm sem ssh aberto (RemoveIPC apaga em 10 s; contorno `ssh runner2 'sleep 7200'`); sudo; "verde oficial" no Windows (qa-report só com números da VM); porta 18100 (barra) — workers usam 182xx; processo em background ocioso no Windows (reaper mata).
Fonte: ola/especificacao/ambientes.md; memórias runner2-vm210.md, bancada-vm-hindiana.md, mapa-proxmox-hosts.md, runner2-devshm-systemd-removeipc.md.
