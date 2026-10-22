# ADR 0025 — Hooks de terceiro gravando no SQLite do painel

- **Status**: Proposto · **Data**: 2026-10-22 · **Ciclo**: 070 (integra o workflow SQLite da linha paralela)
- **Supersede**: nada; complementa o ADR 0022 (o painel é projeção reconstruível dos arquivos). **Superado por**: —
- **Origem**: decisão 5 e tabela § 3 de `specs/066-painel-de-regencia/plano-integracao-linha-paralela.md` (Opus, 19/10, só leitura) e o ponto de retomada § 3c do handoff do longrun. O código veio pronto da branch `w07-064-integrate` (`b33bb81`, 02/10/2026) e já rodava no Hindiana; este ADR registra a decisão de método que ele embute, para o Darú aceitar ou recusar no gate do ciclo. O handoff citava "ADR 0024" para esta decisão; o 0024 foi tomado em 20/10 pelo cabeçalho conferível, daí 0025.
- **Implementação**: ciclo 070 (`f37bf89`, `8ef082f`); evidência em `specs/070-workflow-sqlite/qa-report.md`.

## Contexto

O ADR 0022 fixou que o painel é uma **projeção** dos arquivos do repositório: o `ingest.py` lê
specs, decisões e roadmap e reconstrói o SQLite; `eventos` só acrescenta; o painel nunca
promove. Até o ciclo 069 só dois processos escreviam nesse banco: o próprio `ingest.py` e o
servidor, pela tabela `eventos`.

O workflow do ciclo (spec 070, FR1 a FR3 e FR7 a FR9) pede algo que nenhum arquivo do
repositório registra: a **entrada e a saída de cada passo de cada sessão**, com hora, branch,
hash de partida e evidência. Isso só existe no momento em que a sessão abre ou fecha, e quem
sabe disso é o Claude Code, pelos hooks `SessionStart` e `Stop`. Ou os hooks gravam direto no
SQLite, ou a sessão escreveria um arquivo que o ingest leria depois (uma reconstrução a mais, com
atraso de até uma hora, que é o intervalo do aviso de leitura velha).

Siglas: SQLite WAL (*write-ahead log*, modo que permite leitores concorrentes a um escritor);
FR (*functional requirement*, requisito funcional); ADR (*Architecture Decision Record*).

## Opções avaliadas

- **(a) Hooks gravam direto no SQLite do painel, em tabelas próprias.** Dado em tempo real, sem
  reconstrução; a escrita concorrente é resolvida pelo modo WAL com transações curtas (FR13). Custo:
  um segundo escritor fora do servidor, schema que cada hook precisa garantir (`_ensure_schema`),
  e o painel deixa de ser projeção **só** de arquivos.
- **(b) Hooks escrevem um arquivo por evento (`.maestro/passos/*.json`) e o ingest os projeta.**
  Mantém o ADR 0022 à letra. Custo: atraso, um formato de arquivo a mais, e a regra FR2 (recusar
  a entrada se o passo anterior não saiu) precisaria ler esses arquivos a cada início de sessão.
- **(c) Não registrar passos; o painel continua lendo só specs e decisões.** Deixa FR1 a FR3 e
  FR7 sem executável; o roadmap continua vazio, que é a dor de origem da spec.

## Decisão

**(a), com três condições.** Os hooks do Claude Code gravam direto no SQLite do painel, em
tabelas **próprias, só de acréscimo por convenção** (`rodadas`, `passos`, `transicoes`, `fila`), nunca nas tabelas
derivadas que o ingest reconstrói. Condições:

1. **Separação de escritores.** O ingest só reconstrói as tabelas derivadas, com troca atômica
   (FR12, FR14); as tabelas do workflow sobrevivem à reconstrução e nenhum hook as apaga.
   O "append-only" dessas tabelas é hoje convenção dos hooks, não gatilho: o
   `schema_workflow.sql` não tem `TRIGGER` contra `UPDATE`/`DELETE` (dívida 5 do plano do 070;
   impor por gatilho é tarefa do 072).
2. **Os hooks são ferramenta, não método.** Vivem em `painel/hooks/`, fora de `scripts/` (o
   instalador do Maestro) e fora do `check-language.sh`; instalam-se por opção
   (`specs/070-workflow-sqlite/install_hooks.py`), nunca pelo `setup` do método.
3. **O painel continua sem promover.** Registrar a entrada e cobrar a saída de um passo não é
   aprovar nada; o gate humano continua em `TAIL:gate` e em `promote-main.sh` (ADR 0009).

O ADR 0022 fica em pé com uma ressalva registrada aqui: o painel é projeção dos arquivos **mais**
o registro de passos que só os hooks têm.

## Consequências

- O roadmap mostra rodada, passo atual, tempo e quem (FR4) sem depender de memória de ninguém.
- Mais um escritor no mesmo arquivo SQLite: `test_eventos_escrita_concorrente_nao_trava` (FR13)
  é o teste que protege contra "database is locked"; se ele cair, esta decisão é revista.
- Dívidas declaradas no plano do 070: FR2 e FR3 sem teste nomeado e a regra FR2 dentro do hook
  (adaptador) em vez de função pura; `_ensure_schema` em três cópias; instalador sem dry run.
- A fila outbox (`fila`) nasce no mesmo banco; quando houver mais de uma máquina, a spec já
  aponta Redis Streams, e esse será outro ADR.

## Como desfazer

`git revert -m 1 f37bf89` e `git revert 8ef082f` removem código, hooks e spec; o banco SQLite
não está no git (`painel/.gitignore`), então nada precisa ser migrado. Se só a decisão cair
(voltar à opção b), as tabelas do workflow passam a ser preenchidas pelo ingest a partir de
arquivos, e os hooks passam a escrever esses arquivos: o schema fica, muda o escritor.
