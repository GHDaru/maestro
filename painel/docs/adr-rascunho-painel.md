# ADR 0021 (RASCUNHO): painel de coordenação multiagente como projeção dos arquivos

- **Status**: Proposto, aguardando o Gilsiley · **Data**: 2026-10-01 · **Ciclo**: (a definir)
- **Supersede**: em parte, a linha "Metrics dashboard — Later / YAGNI" de `docs/governance/operating-model.md` §6 e o item "Painel instrumentado de DORA — YAGNI agora" de `docs/handbook/02-dora-space.md`. **Superado por**: —
- **Rascunho**: W11 (painel de especialistas), consolidado pela Hindiana Assistente.

## Contexto

O Maestro recusou um painel de métricas por YAGNI: "sem a quem comparar, instrumentar é débito prematuro". A premissa era um humano regendo poucos agentes, com o estado legível em arquivos.

O projeto hindiana/ola mostrou outra escala. De 29/09 a 01/10 foram:
- 16 sessões simultâneas (Office, Assistente, 2 gerentes, 13 workers);
- cerca de 160 worktrees;
- 52 desvios de método registrados;
- 28 decisões numa única noite;
- 7 voltas da barra em um dia.

O controle se espalhou por dez arquivos e pelas mensagens entre sessões. O "Estado atual" de cada sessão é digitado à mão e desatualiza. O desvio mais caro (teste verde que não passa pelo caminho real) e o mais perigoso (branch com upstream na main: dez encontradas em 01/10) eram invisíveis até alguém procurar.

## Decisão

1. O Maestro passa a ter um **painel de coordenação** em `painel/`: Python stdlib mais um `index.html`, só em localhost. Ele mostra:
   - o board de agentes;
   - o fluxo de peças com evidência;
   - specs, decisões, DORA com a fonte de cada número, barra e desvios;
   - tempo por fase e higiene do git;
   - o relatório de lote para a retro;
   - os documentos do projeto e a linguagem ubíqua;
   - o estado derivado de cada sessão para a IA.
2. **O SQLite é projeção, nunca fonte (ADR 0008 continua valendo).** Toda tabela derivada é apagada e reconstruída a cada ingestão.
3. **A única escrita direta é a tabela `eventos`, que só aceita inclusão.** Ela guarda fatos que não existem em arquivo: status de sessão, transição de peça, deploy, incidente e recuperação. Triggers recusam UPDATE e DELETE.
4. **Transição de peça exige evidência parseável por estado.** Sem prova, o registro é recusado (Princípio IV, catálogo de provas enganosas).
5. **O painel nunca promove nada sozinho.** Todo evento tem autor humano ou de sessão identificada (Princípio II).
6. **DORA conta deploy registrado, nunca merge.** Merge aparece só como proxy rotulado.

## Por que isto não é o débito que o YAGNI temia

- **Não se instrumenta código nem produção.** O painel lê o que o método já obriga a escrever (specs, ADRs, retro, barra, git) e reconstrói tudo do zero.
- **O custo é um diretório sem dependências.** O descarte também é barato: apagar o diretório não perde nenhuma informação, salvo os eventos.
- **O "a quem comparar" existe.** A barra de cada peça e o histórico do próprio projeto servem de referência, e o relatório de lote compara lote com lote.

## Consequências

- `operating-model.md` §6: a linha "Metrics dashboard" passa a "Painel de coordenação: projeção dos arquivos (ADR 0021)".
- `boundary.json`: `painel/` entra no domínio toolkit.
- `docs/handbook/02-dora-space.md`: o painel calcula DORA com a fonte escrita ao lado de cada número, e o que falta registrar aparece como "—".
- Livro, capítulo 08 (entregáveis e artefatos): nova entrada "Painel de coordenação", com referências cruzadas aos capítulos de orquestração e rastreabilidade.
- Novas skills candidatas: `evidence-gate`, `critica-as-cegas` (com transcrição literal obrigatória), `dora-from-git`, `higiene-git`, `estado-atual-derivado`.
- **Risco aceito:** sem a disciplina de registrar status e deploy, o board fica "sem registro" e o DORA mostra "—". O painel mostra o vazio em vez de inventar número.

## Como desfazer

Remover `painel/` e reverter as três linhas de documentação acima. Nenhum arquivo de projeto depende do painel.
