# ADR 0019 — Conformidade executável e catálogo de artefatos

- **Status**: Aceito · **Data**: 2026-08-07
- **Ciclo**: 042 · **Decisor**: Steward
- **Emenda**: `docs/governance/axioms.md` 1.1.0 → 1.2.0 (corolários C12 e C13)

## Contexto

Uma agente companheira, trabalhando noutro repositório com o Maestro instalado, foi
perguntada se tinha seguido o método. Respondeu honestamente que **em parte**, e o
diagnóstico dela é melhor que o sintoma: o `plan.md` listava a ordem de implementação e
parava em "docs e fitness verdes". A cauda do método — revisão independente, security, gate
humano — estava na spec e na memória de trabalho, **não no checklist que ela executava**. A
compactação de contexto promoveu a versão truncada a fonte de verdade, e ela dirigiu até o
pull request obedecendo com fidelidade.

Medido neste repositório, o mesmo defeito é pior:

| Medida | Valor |
|---|---|
| Ciclos cujo `tasks.md` perdeu o gate humano que o template carrega | **35 de 40** |
| Ciclos com `research.md` · `data-model.md` · `contracts/` · `checklist.md` · `ux-design.md` | **0 de 40** |
| O instalador copia o documento onde a regra de aplicação está escrita | **não** |
| O comando `/speckit.plan`, esse sim instalado, exige quatro desses artefatos | **sim** |

Quem instalava o Maestro recebia um comando exigindo quatro artefatos, template para um só,
e a regra de quando eles se aplicam num documento que não era entregue.

**Os dois problemas são o mesmo defeito**, e ele merece nome: o método instalado é uma
**cópia com perda** do método, e o executor segue a cópia com fidelidade. Omissão não viola
nada visível — o Constitution Check pergunta se o plano *viola* um princípio, nunca se ele
*omite* um passo.

## Decisão

**1. Dois corolários novos**, porque os mecanismos precisam derivar de algo estável:

- **C12** — o que sobrevive à compactação é o que está em **artefato consumido**; o resto é
  apagado, não degradado. (De A3 e A4.) É a forma dura do A3: não é que o contexto piora, é
  que o que estava só na memória some, enquanto a cópia com perda sobrevive intacta e com
  aparência de completa.
- **C13** — uma pergunta respondível de memória **será** respondida de memória, e memória de
  agente relata **intenção**, não fato. (De A4 e T4.)

**2. Omissão vira declaração.** Os cinco artefatos condicionais (`research`, `data-model`,
`contracts`, `checklist`, `ux-design`) são declarados no `plan.md` com token
`ART:<nome>=yes|no` e uma razão. Declarar `=yes` obriga o arquivo a existir.

**3. A cauda vira token no `tasks.md`**: `TAIL:review`, `TAIL:security`, `TAIL:gate`. Não se
apaga uma linha para dizer que não se aplica — escreve-se `n/a:` com a razão real. Um passo
ausente é invisível; uma exceção declarada é auditável.

**4. A evidência mora no `qa-report.md`**, e o portão a exige para todo passo que não seja
`n/a`. Marcação prova que alguém marcou.

**5. Token, não prosa.** Prosa é reescrita e traduzida, e o portão passaria a medir a palavra
em vez do fato (anti-padrão 13). Mesmo raciocínio do campo `fecha` do índice e do marcador
`PT-DATA` do portão de idioma.

**6. `docs/governance/artifacts.md`** entra na superfície **instalável**: o catálogo dos
quatro obrigatórios, dos cinco condicionais (com quando se aplicam) e dos três da cauda.

**7. `scripts/check-conformance.sh`** é a resposta executável para "estou seguindo o
Maestro?", e a instrução de **não responder de memória** entra no bloco que o instalador
gera para o `CLAUDE.md` do projeto de destino.

## Alternativas consideradas

- **Adicionar uma seção fixa ao `plan.md` do ciclo afetado**, que foi o que a agente
  propôs. Conserta **um** plano. É a família do ciclo 021: lista escrita à mão, nunca
  comparada com nada — o próximo plano nasce sem a seção e ninguém percebe.
- **Instruir melhor nos agentes e nas skills.** Instrução sem executável é norma sem efeito
  (C7), e a agente em questão estava sendo obediente, não desatenta.
- **Portão que force o humano a ler a evidência.** Não existe. Fingir que existiria seria
  vender garantia que o A2 não permite.
- **Retroagir aos 35 ciclos.** Rejeitada: retroatividade transforma portão em ruído. Piso no
  042, dívida declarada — mesmo precedente do `MAESTRO_MIN_CYCLE_RATIONALE`.

## Consequências

**Boas.** O passo obrigatório passa a existir onde o executor lê, e não onde o autor lembra.
O `ux-design.md` — o condicional mais fácil de pular e o mais caro de pular — deixa de sumir
em silêncio. E a pergunta "você está seguindo o método?" ganha uma resposta que não depende
da honestidade nem da memória de quem responde.

**Ruins, e assumidas.**

- **Token é feio.** `TAIL:review` num `tasks.md` é ruído visual num documento que se quer
  legível. É o preço de sobreviver à tradução; a alternativa legível não sobrevive.
- **Cinco declarações por ciclo é cerimônia**, e cerimônia se paga com atenção. A aposta é
  que declarar `=no` com uma razão curta custa menos que um `ux-design.md` que ninguém
  escreveu. Se em dez ciclos as razões virarem "não se aplica" copiado e colado, a cerimônia
  não pagou e deve ser podada (YAGNI) — fica escrito aqui como condição de revisão.
- **O portão não mede qualidade.** Um ciclo pode ter todos os tokens, toda a evidência e ser
  ruim. Ele mede se o método sobreviveu ao artefato, e nada além disso.
- **Não há template para `research`, `data-model` e `contracts`.** O catálogo diz quando se
  aplicam; o formato nasce do primeiro uso real, não da imaginação.

## Referências

- `docs/governance/artifacts.md` · `scripts/check-conformance.sh` · anti-padrão 22
- Corolários C12 e C13 em `docs/governance/axioms.md` · ADR 0015 (a camada de axiomas)
- Ciclo 021 (lista à mão que deriva) · ciclo 041 (a mesma família, no `retro.sh`)
