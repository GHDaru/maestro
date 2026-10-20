# ADR 0022 — Painel de coordenação multiagente como projeção dos arquivos

- **Status**: Aceito · **Data**: 2026-10-20 · **Ciclo**: 066
- **Supersede**: em parte, a linha "Metrics dashboard — Later / YAGNI" de
  `docs/governance/operating-model.md` §6. **Superado por**: —
- **Origem**: rascunho escrito em 01/10/2026 pelo painel de especialistas do projeto Hindiana
  (W11, consolidado pela Hindiana Assistente) na branch `painel-controle`, como "ADR 0021
  (RASCUNHO)" em `painel/docs/`. O número 0021 foi ocupado pelo ciclo 065 antes de este entrar;
  este arquivo é o rascunho movido com `git mv` (histórico preservado), com a decisão do Darú
  registrada em `decisao-066-daru-20-10`.

## Contexto

O Maestro recusou um painel de métricas por YAGNI ("you aren't gonna need it"): "sem a quem
comparar, instrumentar é débito prematuro". A premissa era um humano regendo poucos agentes,
com o estado legível em arquivos.

O projeto Hindiana mostrou outra escala. De 29/09 a 01/10/2026 foram:

- 16 sessões simultâneas (Office, Assistente, 2 gerentes, 13 workers);
- cerca de 160 worktrees;
- 52 desvios de método registrados;
- 28 decisões numa única noite;
- 7 voltas da barra em um dia.

O controle se espalhou por dez arquivos e pelas mensagens entre sessões. O "Estado atual" de
cada sessão é digitado à mão e desatualiza. O desvio mais caro (teste verde que não passa pelo
caminho real) e o mais perigoso (branch com upstream na produção: dez encontradas em 01/10)
eram invisíveis até alguém procurar.

Entre 01 e 19/10 o painel foi construído e usado diariamente no Hindiana, e a mesma dor
apareceu no próprio Maestro: em 13/10 e 14/10, mensagens de gerentes caíram em sessões de
outro projeto, e em 16/10 uma decisão escalada às 07:04 ficou sem resposta até a tarde
(`specs/066-painel-de-regencia/insumo-hindiana.md`).

## Decisão

1. O Maestro passa a ter um **painel de coordenação** em `painel/`: Python da biblioteca
   padrão (stdlib) mais um `index.html`, só em localhost. Ele mostra o board de agentes, o
   fluxo de peças com evidência, specs, decisões, DORA (as quatro métricas de entrega de
   software: frequência de deploy, lead time, taxa de falha, tempo de restauração) com a fonte
   de cada número, barra e desvios, tempo por fase, higiene do git, o relatório de lote para a
   retro, os documentos do projeto e o estado derivado de cada sessão para a IA.
2. **O SQLite é projeção, nunca fonte (ADR 0008 continua valendo).** Toda tabela derivada é
   apagada e reconstruída a cada ingestão.
3. **A única escrita direta é a tabela `eventos`, que só aceita inclusão.** Ela guarda fatos
   que não existem em arquivo: status de sessão, transição de peça, deploy, incidente e
   recuperação. Triggers recusam UPDATE e DELETE.
4. **Transição de peça exige evidência parseável por estado.** Sem prova, o registro é recusado
   (Princípio IV).
5. **O painel nunca promove nada sozinho.** Todo evento tem autor humano ou de sessão
   identificada (Princípio II).
6. **DORA conta deploy registrado, nunca merge.** Merge aparece só como proxy rotulado.
7. `painel/` e `.maestro/` pertencem ao domínio **toolkit** de `boundary.json` (ADR 0018):
   são lidos por máquinas e viajam com o método.

## Por que isto não é o débito que o YAGNI temia

- **Não se instrumenta código nem produção.** O painel lê o que o método já obriga a escrever
  (specs, ADRs, retro, barra, git) e reconstrói tudo do zero.
- **O custo é um diretório sem dependências.** O descarte também é barato: apagar o diretório
  não perde nenhuma informação, salvo os eventos.
- **O "a quem comparar" existe.** A barra de cada peça e o histórico do próprio projeto servem
  de referência, e o relatório de lote compara lote com lote.

## Consequências

- `operating-model.md` §6: a linha "Metrics dashboard — Later / YAGNI" passa a "Coordination
  panel" (ADR 0022).
- `boundary.json`: `painel/` e `.maestro/` entram em `toolkit.owns`.
- A spec retroativa `specs/066-painel-de-coordenacao-v0/spec.md` registra o que o v0 entrega,
  os limites (testes escritos depois do código; acoplamento ao Hindiana em três módulos;
  escopo não pedido) e os critérios de aceite medidos no código.
- O painel de regência (ciclo 072 no mapa de integração) nasce em cima deste v0 e paga a dívida
  do acoplamento.
- **Risco aceito:** sem a disciplina de registrar status e deploy, o board fica "sem registro"
  e o DORA mostra "—". O painel mostra o vazio em vez de inventar número.

## Como desfazer

Remover `painel/` e `.maestro/`, reverter as duas entradas de `boundary.json` e a linha do
operating-model. Nenhum arquivo de projeto depende do painel.
