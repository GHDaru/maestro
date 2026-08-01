# Spec 013 — Livro: guia editorial, capítulo-piloto e instalador

- **Status**: Aprovada (decisões 1/2/3 do Steward) · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: crítica do Steward ao site V0 ("quase um PPT", links saindo para o GitHub),
  pedido de explicitar didaticamente as decisões de engenharia, e pergunta "como instalo
  o Maestro como skill + scripts?".

## O quê e por quê

Três entregas de um mesmo movimento — transformar o Maestro de **repositório que se lê**
em **livro que ensina + método que se instala**:
(1) o padrão editorial aprovado; (2) o capítulo-piloto que o materializa e responde ao
pedido "quando decidimos, por quê, o que faz e o que provoca"; (3) o instalador.

## Requisitos funcionais

- **FR1 — Guia editorial** (`docs/livro/guia-editorial.md`): projeto pedagógico
  (Backward Design, Diátaxis, carga cognitiva, 4C/ID), esqueleto de 9 seções, regras de
  escrita, datação de livro vivo, 5 trilhas, cadência educacional, Iron Law editorial.
- **FR2 — Capítulo-piloto** (`docs/handbook/13-decisoes-de-engenharia.md`): 14 decisões de
  engenharia, cada uma com **quando · por quê · o que faz · o que provoca**, no esqueleto
  de 9 seções, com exemplo de ciclo real e verificação.
- **FR3 — Instalador** (`scripts/instalar-maestro.sh`): instala agentes, skills, scripts,
  comandos, templates e governança em outro repositório; **não sobrescreve** sem `--forcar`;
  suporta `--dry-run`; imprime os próximos passos.
- **FR4 — Integração ao livro**: capítulo 13 e guia editorial no sumário do site e no
  índice do handbook, com nota da coexistência dos dois padrões.
- **FR5 — Registro**: ADR 0011 (padrão editorial + navegação + companion com backend +
  instalador) e índice de decisões.

## Fora de escopo

- Implementar o companion (backend/widget) — decidido no ADR 0011, construção em ciclo
  próprio.
- Migrar os capítulos 01–12 para o esqueleto v2 (um por ciclo, depois).
- Reescrever a capa/navegação em 5 trilhas (ciclo seguinte).

## Critérios de aceite (DoD)

- [ ] QUANDO o site for construído, O SISTEMA DEVE gerar 25 páginas com links internos OK.
- [ ] QUANDO `instalar-maestro.sh` rodar duas vezes no mesmo destino, O SISTEMA DEVE
      manter os arquivos existentes (idempotência) e relatar cada um.
- [ ] `grep -c "O que provoca" 13-decisoes-de-engenharia.md` ≥ 14 (uma por decisão).
- [ ] O capítulo 13 tem as 9 seções do esqueleto (`grep -c "^## "` = 9).
- [ ] `ls docs/adr/0011-*.md` existe; decisão no índice consultável.

## Clarify (resolvido pelo Steward)

1. **Esqueleto de 9 seções?** Serve.
2. **Chat**: opção **(c)** — backend real (cota NVIDIA gratuita, demanda baixa, Neon
   disponível). Referência: `chat-companion` do harness (FastAPI + Railway).
3. **Piloto**: fazer — escolhido o capítulo de decisões de engenharia, que era o próprio
   pedido do Steward.
