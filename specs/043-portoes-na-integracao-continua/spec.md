# Spec 043 — Os portões entram na integração contínua

- **Status**: Concluída · **Raia**: infra · **Data**: 2026-08-07
- **Origem**: `achado-042-portoes-fora-da-ci`, levantado pela revisão independente do ciclo
  042 — *"a gate that runs only when an agent chooses to run it is the memory this cycle is
  trying to replace"*.

> **Raia**: infra. **Ambiguidade** baixa (os portões existem e são determinísticos);
> **raio** total (passa a bloquear merge para qualquer um que trabalhe no repositório);
> **irreversibilidade** média — desfazer é apagar um job, mas enquanto estiver de pé ele
> decide o que entra. Por isso leva bloco de reversibilidade explícito.

## O quê e por quê

O método tem **onze portões** e a integração contínua (CI) roda **um**: o do `CHANGELOG`.
Os outros dez dependem de alguém lembrar de executá-los antes de fechar o ciclo.

Isso é o corolário **C13** aplicado ao próprio enforcement: uma verificação que depende de
memória é uma verificação que relata intenção. E há evidência recente e local — no ciclo 041
dois commits citaram um "ciclo 040" que não tem spec, e no 042 o `qa-report.md` do próprio
ciclo era um esqueleto vazio com a cauda marcada. Nos dois casos, o portão certo existia;
ele só não tinha sido executado no momento em que valeria.

## Requisitos funcionais

- **FR1**: QUANDO houver push ou pull request, O SISTEMA DEVERÁ executar os portões
  estruturais e **falhar** o job se qualquer um reprovar.
- **FR2**: QUANDO um portão reprovar por razão legítima de trabalho em andamento
  (`check-cycle` contra a linha principal, `check-retro` como dívida), O SISTEMA DEVERÁ
  **avisar sem bloquear** — decisão humana registrada neste ciclo.
- **FR3**: QUANDO o job rodar, O SISTEMA DEVERÁ operar com **privilégio mínimo**: nenhum
  segredo, nenhuma permissão de escrita.
- **FR4**: QUANDO o `check-cycle` rodar em CI, O SISTEMA DEVERÁ apontá-lo para a referência
  remota da linha principal — numa branch de PR não existe `main` local.

## Fora de escopo

- Rodar `/eval` na integração contínua. Exige modelo no laço, chave e custo por execução —
  rejeitado por decisão no ADR 0016 e não reaberto aqui.
- Proteção de branch no GitHub (exigir o job verde para permitir merge). É configuração de
  repositório, não de arquivo — fica como decisão do Steward, registrada no roadmap.
- Fixar as *actions* por SHA em vez de tag maior. Ver a ressalva na seção de segurança do
  relatório: é endurecimento real e é troca de manutenção, então entra por gatilho.

## Critérios de aceite (DoD)

- [x] `.github/workflows/ci.yml` tem o job `gates` com os nove portões estruturais mais o
      `package-plugin --verify` e o build do livro, todos bloqueantes.
- [x] `check-cycle` e `check-retro` rodam como aviso e **não** derrubam o job.
- [x] `permissions: contents: read` no topo do arquivo, valendo para todo job.
- [x] `MAESTRO_TRACE_BASE=origin/main` com o fetch correspondente.
- [x] O job foi **simulado localmente** comando a comando, com a saída no relatório.
- [x] O `grep -q` no fim de pipe do job de `CHANGELOG` foi endurecido (anti-padrão 21).

## Clarify

1. Por que `check-cycle` e `check-retro` não bloqueiam? Porque ficam vermelhos por razões
   legítimas enquanto há trabalho em voo — a dívida de achados é um **sinal**, e bloquear
   merge por sinal transforma sinal em obstáculo. Decisão do Steward neste ciclo.
