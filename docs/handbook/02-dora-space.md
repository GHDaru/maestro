# Capítulo 02 — Evidência: DORA / SPACE (elemento `[10]`)

> A base empírica embaixo do `[1]`: **velocidade e estabilidade não são um trade-off.**

## 1. Pergunta central

A intuição comum diz "quanto mais rápido eu entrego, mais eu quebro". **Velocidade e
estabilidade são mesmo opostas — ou andam juntas?**

## 2. Fundamentação teórica

O programa DORA (DevOps Research and Assessment) mediu milhares de equipes e definiu
**quatro métricas**, em dois pares:

- **Throughput**: frequência de deploy · lead time (commit→produção)
- **Estabilidade**: change fail rate · tempo de recuperação (rollback) — hoje às vezes
  com uma 5ª, *rework rate*.

Achado central, contraintuitivo: os **mesmos** times de elite são rápidos **e** estáveis,
simultaneamente. "O trade-off real, no longo prazo, é entre *software melhor mais rápido*
e *software pior mais devagar*." As quatro métricas são **outcomes** dirigidos por
**capacidades**: CI, trunk-based development, testes automatizados, revisão de código,
deploys pequenos.

**A alavanca única: tamanho de lote pequeno.** Mudança pequena → deploya mais vezes
(frequência↑), lead time curto, fácil de testar/revisar (falha↓) e, quando falha, fácil
de reverter (recuperação↑). Padronização + automação é o que torna o lote pequeno barato;
**reversibilidade** (`[1]`) é o que torna a falha barata. Por isso as quatro se movem
juntas em vez de brigar.

## 3. Frameworks / abordagens avaliados

| Framework | Foco | Veredito para solo+IA |
|---|---|---|
| **DORA (4 keys + capabilities)** | Desempenho de entrega + capacidades causais | **Adotado como bússola qualitativa** — lead time e change fail rate são os dois que mais importam para um solo |
| **SPACE** | Produtividade multidimensional (Satisfação/Performance/Atividade/Comunicação/Eficiência) | **Referência** — lembra que "não há uma métrica única de produtividade"; pouca prescrição |
| **DX Core 4** | 4 métricas prescritivas (Speed/Effectiveness/Quality/Impact) | **Observado** — cuidado com métricas gaméaveis (ex.: "PRs por dev") |
| **Painel instrumentado de métricas** | Dashboards de DORA | **YAGNI agora** — sem a quem comparar; instrumentar é débito prematuro |

## 4. Recomendação de utilização (1 humano + N agentes)

- Usar DORA como **bússola de saúde do fluxo**, não como painel de RH ("consigo levar
  uma spec a produção rápido e sem quebrar?").
- Focar **lead time** e **change fail rate**; recuperação vem da reversibilidade (`[1]`).
- **Não instrumentar métricas** ainda (YAGNI). As capacidades (CI verde, trunk-based,
  testes, diffs pequenos, revisão independente) já são princípio da Constituição (V) e
  da DoD — a evidência só confirma que são as certas.

## 5. Conexões

- **`[1]`** — "recuperável > cauteloso" é a leitura empírica da reversibilidade.
- **`[3]`** — rollback rápido = o checkpoint/rewind do fluxo agentic.
- **`[8]` DoR/DoD** — as capacidades DORA são exatamente os itens da DoD.

## 6. Insight da jornada e impacto no modelo

Analogia do aprendiz: **linha de produção cognitiva** — como a fábrica pré-Ford era lenta
até padronizar componentes, aqui a padronização de processo/entregáveis reduz fricção e
variação. Complemento: a linha do Ford *não tinha undo barato*; a cognitiva tem — **lote
pequeno + reversibilidade = rápido e estável.** Sem impacto normativo (confirma o modelo);
justifica por que a DoD e as raias não são burocracia. Diário: `[10]`.

## 7. Fontes

- DORA — *DORA metrics (four keys)*: https://dora.dev/guides/dora-metrics-four-keys/
- Swarmia — *Comparing DORA, SPACE and DX Core 4*: https://www.swarmia.com/blog/comparing-developer-productivity-frameworks/
