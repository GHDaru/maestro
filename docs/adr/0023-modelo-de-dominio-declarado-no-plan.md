# ADR 0023 — O modelo de domínio é declarado no plan, e o portão o lê

- **Status**: Aceito · **Data**: 2026-10-20 · **Ciclo**: 067
- **Supersede**: nada. **Superado por**: —
- **Origem**: branch `trava-dominio-plan` da linha paralela (`14f77a5`, `a94574a`, `db6b89c`,
  02–03/10/2026, equipe Hindiana), integrada em `b5775ac`. O merge não trouxe ADR; a revisão
  independente do ciclo 067 apontou que a constituição (§ Governance: "every material
  methodology decision becomes an ADR") o exige, e este registro foi escrito para o gate.

## Contexto

Em 03/10/2026, no projeto Hindiana, uma rodada inteira entregou regras de negócio dentro de
rotas HTTP (HyperText Transfer Protocol) porque o `plan.md` foi pulado: ninguém discutiu a
linguagem ubíqua nem as raízes de agregado antes de codar. O teste ficou verde pelo caminho
errado, e o defeito só apareceu na barra. O Maestro já tinha a lição equivalente para os
artefatos condicionais: desde o ciclo 042, o plan declara `ART:*` com um motivo, e o portão
`check-conformance.sh` lê a declaração, porque silêncio não é decisão (corolário C12).

O mesmo mecanismo faltava para o domínio. O plan dizia "use DDD" (Domain-Driven Design, projeto
orientado ao domínio) em prosa, e nada media se a decisão fora tomada.

## Decisão

1. O template do plan (`.specify/templates/plan-template.md`) ganha a seção **"Domain model
   (declare all four — silence is not a decision)"**, com quatro declarações obrigatórias, cada
   uma com um motivo: `DOM:aggregate=` (raiz de agregado tocada, ou `none` e por quê),
   `DOM:invariants=` (`domain` ou `edge(por que não pode ser domínio)`, ou a forma itemizada
   `regra_a=domain | regra_b=edge(porquê)`), `DOM:glossary=` (`changed` com os termos, ou
   `none`), `DOM:ports=` (`changed` com as portas, ou `none`).
2. `scripts/check-conformance.sh` lê as quatro declarações (bloco 3b) a partir do **ciclo 067**
   (`DOM_FLOOR=67`), como lê os `ART:*`: declaração ausente, sem valor ou sem motivo é falha
   suave, e `edge` sem o porquê é recusado. A falha é suave, não dura, pela lição do ciclo 043:
   um portão sempre vermelho em trabalho em andamento é um portão que as pessoas aprendem a
   ignorar; a promoção para a `main` é o momento em que ele bloqueia.
3. O piso é um botão que **só aperta**: `MAESTRO_MIN_CYCLE_DOMAIN` aceita só número e só valores
   ≤ 67; qualquer outra coisa encerra com código 2, nunca abre o portão.
4. No painel de coordenação, o DORA (as quatro métricas de entrega) conta **só deploy de
   produção**; staging e dev saem da conta. E o painel marca spec sem plan ou sem tasks.

## Por que isto deriva dos axiomas e não é cerimônia

- **T6** (a correção que não vira regra se repete): o achado de 03/10 era a segunda vez que
  regra de negócio nascia na borda sem decisão; a terceira estava a caminho.
- **T4 / C7** (norma sem executável não tem efeito): por isso o portão lê o token, em vez de o
  handbook pedir "pense no domínio".
- **C12** (o mesmo mecanismo dos `ART:*`): nenhuma peça nova no método; a mesma tabela, o mesmo
  grep, o mesmo piso.
- **YAGNI**: o que ficou de fora — validar o conteúdo do motivo, exigir um `domain-model.md`
  separado, um portão duro na CI.

## Consequências

- Todo ciclo ≥ 067 declara os quatro `DOM:*` no plan; o 066 e anteriores ficam como estão.
- Cinco termos entram no glossário: aggregate root, declared domain model, invariant,
  port/adapter, ubiquitous language.
- **Defeito conhecido, com dono**: a forma itemizada divide por `|`, que é também o separador da
  tabela Markdown; numa linha de tabela com a célula "Why" preenchida, a célula vira item falso
  e reprova com mensagem confusa (medido na mutação (b') do ciclo 067). Também: `grep -m1` pega
  a primeira linha com `DOM:x=`, então uma menção em prosa antes da tabela vence a linha real.
  Dono: o próximo ciclo que tocar o bloco 3b (dívida registrada no plan do 067).
- **Risco aceito**: um motivo vazio de conteúdo ("porque sim") passa; o portão mede a
  existência da decisão, não a sua qualidade — essa é do revisor em contexto fresco.

## Como desfazer

Remover a seção do template e o bloco 3b do portão; o piso deixa de existir. Os plans já
escritos com `DOM:*` continuam válidos como texto.
