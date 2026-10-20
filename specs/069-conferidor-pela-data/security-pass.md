# TAIL:security — ciclo 069 (conferidor pela data)

Passagem independente em contexto fresco (agente `security`, 20/10/2026, só leitura sobre HEAD
`23f8325`). Classe de risco declarada: **baixa** (função pura; arquivos de evidência).

## Achados

1. **(média, pré-existente, não introduzida por esta fatia)** `painel/chamados.py:74-78` `data()`:
   a regex `RE_DATA` (`:39`) aceita `2026-13-01 00:00`, `2026-02-30 00:00` ou fuso `+2500`;
   `strptime` levanta `ValueError` dentro de `valida()` (`:86`), antes de `ordem_veredito`. A
   exceção sobe por `confere()` → `le_chamados()` e cai no `except` de `_atualiza` (`:323`): **o
   painel inteiro fica em erro**, não só o chamado. Requer direito de commit em qualquer branch
   (`git log --all`). Classe III: leitura; raio = a vista do painel. Fix mínimo:
   `try/except ValueError: return None` em `data()`. Dívida do 072.
2. **(baixa)** `:118` e `:140`: `fromisoformat(quando)` recebe só `%aI` do git (`:256/:286`),
   nunca conteúdo de arquivo. Porém a author date é forjável (`GIT_AUTHOR_DATE`) e a trava "hora
   digitada" (`:139-142`) confia nela: quem commita pode fazer um veredito forjado vencer. Dentro
   do modelo de confiança (quem commita já é crítico). Fix opcional: `%cI`, ou os dois.
3. **(baixa)** `specs/070-*`: sem segredo, token, IP, URL ou caminho com usuário
   (`/dev/shm/070-hindiana` em `G3-runner2-W13-d2822ef-8adb545a.md:43` é genérico). Dados de
   outro projeto: nome do repo, `specs/099-filtros-multiselecao`, hashes e caminhos
   `scripts/maestro/*.py` (`G0-reproducao.md:13`, `G3-codigo-W10.md:44-51`); nenhum código ou
   dado de negócio copiado. Nomes: "Hindiana Office", "Assistente", W01/W10/W11/W13 — papéis,
   não pessoas. Aceitável; se o Hindiana for privado, registrar o consentimento.
4. Nada de rede, subprocess novo ou escrita: `ordem_veredito` é pura; o teste R4
   (`test_chamados.py:115-124`) faz monkeypatch de `_git` e restaura em `finally`.

## Veredito

TAIL:security OK — sem bloqueio; o achado 1 é dívida pré-existente a registrar (fix de uma
linha), e a observação sobre a author date forjável fica no modelo de confiança declarado.
