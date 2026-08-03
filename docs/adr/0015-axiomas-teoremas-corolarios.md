# ADR 0015 — Axiomas, teoremas e corolários como camada de derivação

- **Status**: Aceito · **Data**: 2026-08-03
- **Ciclo**: 035 · **Decisor**: Steward

## Contexto

O Maestro tem oito princípios, um modelo operacional, seis skills, dezoito anti-padrões e
oito portões. Cada um nasceu de dor real — mas o corpo de regras chegou ao tamanho em que a
pergunta "de onde vem esta regra?" passou a ter respostas diferentes conforme quem responde.

Duas consequências práticas já aparecem no repositório: (a) regra nova é argumentada por
analogia ("parece com o princípio IV") em vez de por derivação; e (b) a poda por YAGNI não
tem critério positivo — só o negativo "não pagou o custo".

O Steward pediu **um conjunto de verdades assumidas** para todo o projeto. Não é decoração
filosófica: é a base contra a qual uma regra nova é discutida e uma regra velha é podada.

## Decisão

1. **Criar `docs/governance/axioms.md`** com três camadas explícitas:
   **axiomas** (assumidos, não provados — cinco), **teoremas** (derivados, cada um com
   evidência deste repositório — seis) e **corolários** (consequências imediatas, que é de
   onde saem as regras do dia a dia — dez).
2. **Os cinco axiomas**: A1 intenção é humana · A2 consequência precisa de dono ·
   A3 contexto é finito e degrada · A4 o que está escrito é o que sobrevive · A5 o custo é
   assimétrico entre fazer e desfazer.
3. **Todo teorema traz evidência do repositório.** Teorema que não pode ser mostrado
   falhando quando violado é crença, não teorema — o próprio teorema T4 aplicado ao documento.
4. **A constituição continua sendo a norma operativa**; os axiomas são a camada de
   *derivação*. O Constitution Check segue checando os princípios, não os axiomas.
5. **Regra nova é argumentada contra os axiomas**: a que não deriva de nenhum é axioma novo
   (raro, entra por ADR) ou cerimônia (podada por YAGNI).
6. **O documento é instalável** e, portanto, escrito em inglês (ADR 0014).

## Alternativas consideradas

- **Não ter camada de derivação**: era o estado até aqui. Funciona enquanto o corpo de regras
  é pequeno; com 8 princípios + 18 anti-padrões + 8 portões, "de onde vem isto?" já tinha
  respostas divergentes.
- **Transformar os princípios em axiomas** (renomear a constituição): perderia a distinção
  útil entre *o que se assume* e *o que se manda fazer* — e quebraria o Constitution Check,
  que é executável e já cobre os oito princípios.
- **Axiomas sem teoremas** (só uma lista de crenças): barato e inútil — sem derivação
  explícita, ninguém consegue checar se uma regra realmente vem dali.
- **Dez ou quinze axiomas**: quanto mais axiomas, menos poder de corte. Cinco é a aposta no
  menor conjunto que sustenta o método atual; se um princípio não derivar de nenhum, ou falta
  axioma (entra por ADR) ou sobra princípio (poda).

## Consequências

- (+) Regra nova passa a ser discutida contra algo estável, não contra a última analogia.
- (+) A poda ganha critério positivo: o que não deriva de axioma é candidato natural.
- (+) Cada teorema carrega evidência do repositório — inclusive a evidência incômoda
   (nove defeitos escapados com portão verde, sob T4).
- (−) **Mais um documento de governança para manter vivo.** Mitigado por ser curto, por
   nascer com versão e por ter os teoremas amarrados a fatos verificáveis.
- (−) O risco de virar retórica é real: axioma é fácil de escrever e difícil de refutar.
   O antídoto adotado é a exigência de **independência declarada** (o que quebra se o axioma
   sair) e de evidência em todo teorema.

## Registro

- `docs/governance/axioms.md` (novo, v1.0.0) · constituição v1.3.0 aponta para ele
- `scripts/install-maestro.sh` passa a copiá-lo · publicado no livro (trilha Referência)
- BPMN v4: a trilha de artefatos termina em `achado aberto → axioma/teorema → regra nova`
- Ciclo: `specs/035-axiomas-e-bpmn-v4/`
