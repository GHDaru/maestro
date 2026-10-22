# TAIL:security — ciclo 068 (chamados gate a gate)

Passagem independente em contexto fresco (agente `security`, 20/10/2026, só leitura; sem shell,
grep sobre HEAD `120a32c`). Classe de risco declarada no plano: **média** (lê o diretório home do
usuário). Resultado: **nenhum achado alto ou médio; seis baixos**.

## Achados

1. **(baixa) `custo.py` — leitura do home.** Caminhos: `~/.claude/projects/*` (`custo.py:47-49`),
   depois `<pasta>/*.jsonl` (`:56`). O filtro `custo_pastas` é **substring no basename**
   (`:49`): `"180"` casaria qualquer projeto; o default embutido `["180-HINDIANA"]` (`:48`) é um
   nome de projeto real num repositório público. O SQLite guarda **só contagens**:
   `INSERT INTO uso (sessao, minuto, turnos, entrada, saida, cache_lido, cache_escrito)`
   (`:109-112`), `sessoes (sessao, titulo, nome, pasta)` (`:114-115`), `arquivos (caminho,
   offset, sessao, ultimo_id)` (`:116-117`). **Nenhum prompt ou saída de ferramenta é
   persistido.** HTTP: `trilha()` devolve só `custo.janela()` → somatórios (`chamados.py:395-398`);
   `titulo` e `caminho` nunca saem do banco; o navegador não lê transcript. `painel/dados/` em
   `painel/.gitignore:1`. Mitigação: filtro por igualdade ou prefixo; sem default de projeto real.
2. **(baixa) `chamados.py` — subprocess.** Sempre lista, sem `shell` (`_git`, `:42-44`). Args de
   conteúdo (`apelidos`, `data` do `00-chamado.md`) entram como `--grep=<a>` e `--since=<d>`
   (`:357-360`), prefixados — não viram opções nem comandos; `objeto @ hash` passa por
   `[0-9a-f]{7,40}` antes de `git log -1 <h>` (`:38`, `:273`); `cid`/`n` vêm do `git log
   --name-only`, não do texto. Sem traversal; nada lido fora de `raiz` além de `chamados_manuais`
   (caminho de config, `:284`).
3. **(baixa) `chamados-manuais-exemplo.json` (Princípio II).** Entradas manuais recebem
   `registro="manual"` (`:289`) e só entram se o id não existe no git (`:291-292`); a tela rotula
   "registro manual" (`index.html:607, :666`). Porém o `estado` digitado aparece como posição no
   board sem distinção visual de um estado derivado. Fix: selo distinto e gates vazios explícitos.
4. **(baixa) Rotas.** As três são GET (`server.py:429-440`); nenhum POST novo; nenhuma recebe
   caminho de arquivo. `/api/chamados?atualizar` dispara varredura git e leitura do home por GET
   sem Origin/Host (mesma exposição do achado 066-1; só custo). `/trilha` devolve o texto
   integral dos arquivos de gate do repo (`chamados.py:383`), renderizado com `esc()`
   (`index.html:656`). `_docs` global escrito em thread e lido sem lock (`:233, :276, :350`):
   corrida, não segurança.
5. **(baixa) pre-commit.** `python "$HOOK_DIR/veredito_hook.py" --pre-commit` (`pre-commit:4-5`);
   valida `Objeto @ hash` e `Data:` contra o relógio local (`veredito_hook.py:367-381`).
   Instalação manual por `cp`; o `.py` precisa ir junto, senão falha silenciosa. Bypass:
   `--no-verify`, não instalar, relógio local. Portão do lado do cliente, não enforcement.
6. **(baixa) Dados e segredos em HEAD.** `chamados-manuais-hindiana.json` ausente. Nenhum
   segredo, IP ou host. Residual: `exemplo.json:95` traz caminho com nome de usuário
   (`C--Users-ghdaru-…`); `custo.py:33-34,48`, `chamados.py:28,154-155` e o BPMN (`:2,:22,:27`)
   nomeiam pessoa e projeto reais — acoplamento já declarado na spec (`:157-162`).

## Veredito

TAIL:security OK — nenhum achado alto ou médio; seis baixos (filtro substring e default de
projeto real em `custo.py`; GET `?atualizar` sem Origin; hook contornável; nomes reais residuais).
Nenhum bloqueia o gate. **Para a pergunta do Darú sobre privacidade**: o índice de custo guarda só
contagens; o risco é o filtro por substring ler pastas de outros projetos, e a correção é uma
linha (igualdade em vez de substring), dívida do 072.
