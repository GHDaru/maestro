# ADRs — Maestro

Architecture/Methodology Decision Records: decisões **imutáveis** (podem ser superadas
por um ADR posterior, nunca editadas no mérito). Formato: contexto → decisão →
consequências → fontes.

| ADR | Título | Status |
|---|---|---|
| 0004 | [Modelo operacional (papéis, cerimônias, artefatos)](0004-modelo-operacional.md) | Aceito |
| 0005 | [Raias de trabalho e specs de infra](0005-raias-de-trabalho-e-specs-de-infra.md) | Aceito |
| 0006 | [Enforcement da DoD e forcing function do CHANGELOG](0006-enforcement-dod-changelog.md) | Aceito |
| 0007 | [Separação do Maestro em repositório próprio](0007-separacao-repo-maestro.md) | Aceito |
| 0008 | [Avaliação do ecossistema SDD (Superpowers, BMAD, Kiro…)](0008-avaliacao-ecossistema-sdd.md) | Aceito |
| 0009 | [Registro automático do gate de merge](0009-registro-automatico-gate-merge.md) | Aceito |
| 0010 | [Princípio VIII — comunicação inteligível (sigla nunca nasce nua)](0010-principio-viii-comunicacao-inteligivel.md) | Aceito |
| 0011 | [Livro: padrão editorial, navegação e companion com backend](0011-livro-padrao-editorial-e-companion.md) | Aceito |
| 0012 | [Distribuição em três camadas (script · plugin · skills CLI)](0012-distribuicao-em-tres-camadas.md) | Aceito |
| 0013 | [Instrução para a IA: fonte única e gerada do disco](0013-instrucao-para-ia-gerada-e-fonte-unica.md) | Aceito |
| 0014 | [Inglês como idioma do método instalável](0014-ingles-no-instalavel.md) | Aceito |
| 0015 | [Axiomas, teoremas e corolários como camada de derivação](0015-axiomas-teoremas-corolarios.md) | Aceito |
| 0016 | [Evals como critério para saída não-determinística](0016-evals-para-saida-nao-deterministica.md) | Aceito |
| 0017 | [Divisão em dois repositórios: toolkit e guia](0017-divisao-em-dois-repositorios.md) | **Superado pelo 0018** |
| 0018 | [Fronteira interna em vez de divisão em dois repositórios](0018-fronteira-interna-em-vez-de-divisao.md) | Aceito |
| 0019 | [Conformidade executável e catálogo de artefatos](0019-conformidade-executavel-e-catalogo-de-artefatos.md) | Aceito |
| 0020 | [MIT, e a atribuição viaja com a cópia](0020-licenca-mit-e-atribuicao-que-viaja.md) | Aceito |

> Índice consultável por máquina (append-only): [`../records/decisoes.jsonl`](../records/decisoes.jsonl) — ver [protocolo](../records/README.md).

## Nota de numeração

A sequência começa em **0004** porque os ADRs 0001–0003 do repositório de origem
(`ghdaru`) eram específicos daquela plataforma (curadoria de skills, hospedagem,
integração) e **não** pertencem à metodologia — não foram migrados. Os números 0004–0006
foram **preservados** para não quebrar as referências cruzadas no modelo e no handbook.
