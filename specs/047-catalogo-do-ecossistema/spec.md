# Spec 047 — Catálogo do ecossistema: a ideia como unidade, o momento separado do estado

- **Status**: Em andamento · **Raia**: plena · **Data**: 2026-08-10
- **Origem**: pergunta do Steward — *"temos em algum lugar todos os repositórios que
  avaliamos e as decisões que tomamos em relação a cada um? Se sim, está no livro? Se não,
  temos que fazer, e inclusive criar um template de avaliação e dimensões."* Objeto redesenhado
  pelo painel de catorze especialistas.

> **Raia**: plena. **Ambiguidade** média (o objeto certo não era óbvio — a primeira proposta
> foi invalidada pelo painel); **raio** amplo (governa toda absorção futura e entra no livro);
> **irreversibilidade** baixa — arquivos de texto e um portão.

## O quê e por quê

A resposta honesta à pergunta é **"em parte, e espalhado"**. Hoje o julgamento de terceiros
vive em quatro lugares que não se conhecem:

| Onde | O que tem | Quando parou |
|---|---|---|
| ADR 0005 | OpenSpec descartado | ciclo 005 |
| ADR 0008 + `docs/research/avaliacao-ecossistema-sdd.md` | 7 ferramentas com veredito | ciclo 007 |
| `docs/handbook/apendice-c-panorama-templates.md` | 9 itens de triagem | ciclo 012 |
| `docs/research/upstream-decomposicao.md` | `Product-Manager-Skills` (CC BY-NC-SA), `spec-decompose` | ciclo 036 |

Três defeitos, e nenhum deles se resolve juntando os arquivos:

1. **A unidade errada.** As fichas julgam **ferramentas**, mas o Maestro quase nunca adota
   uma ferramenta: ele **absorve ideias**. "Superpowers: absorver + observar" não é
   acionável. "Worktree isolado por task: absorver, destino `scripts/`" é — e é falsificável.
2. **Momento e estado misturados.** Uma ficha datada de 2026-07-30 afirma o veredito **de
   hoje**. Enquanto o estado mora dentro da observação, ou a observação vira mentira ou a
   história é reescrita. Os dois são necessários e **não são o mesmo artefato**.
3. **Absorção declarada sob condição, e nenhum lugar onde o estado morasse.** Verificado em
   2026-08-10, contra o disco:

   | Ideia, sob o cabeçalho "absorver ideias com destino concreto" (ADR 0008) | Destino escrito | Está lá? |
   |---|---|---|
   | EARS | `skills/verifiable-dod`, `spec-template.md` | ✅ nos dois |
   | Rigor mandatório nas skills | Iron Law nas skills | ✅ |
   | **Worktree isolado por task** | `scripts/`/`skills/` **"quando houver dor real"** | ❌ nada |
   | **Standards por camada** | `docs/standards/` **"apenas quando o Maestro reger codebase de produto (gatilho, não agora — YAGNI)"** | ❌ nada |

   O defeito é o **destino condicional escrito sob um cabeçalho de absorção**. Não houve
   ocultação: o mesmo ADR 0008, três linhas abaixo, lista GSD e **Agent OS** no item
   "observar com gatilho explícito" — as duas leituras convivem em itens adjacentes, e nada
   diz qual é o estado. O Apêndice B, no ciclo 011, escreveu worktree como `👁 observar` com
   a nota **"gatilho F3 inalterado"** e **"mantém ADR 0008"**: é deferência, não
   reclassificação contra o ADR.

   Nenhuma das quatro chegou ao disco por engano. O que faltou foi **um lugar onde o estado
   corrente vivesse**, separado da observação que o originou — e, sem esse lugar, "absorver
   quando doer" e "observar até doer" são a mesma frase escrita em duas colunas diferentes,
   por 39 ciclos. É a mesma família de defeito do ciclo 046 (a alegação sem o texto) e do 042
   (a norma sem forcing function), e é o argumento inteiro para separar momento de estado.

## Requisitos funcionais

- **FR1**: QUANDO uma fonte de terceiro for avaliada, O SISTEMA DEVERÁ registrá-la numa
  linha fina com `owner/repo`, o que é, **licença** e a data e a versão/commit **observados**.
- **FR2**: QUANDO uma ideia for julgada, O SISTEMA DEVERÁ produzir um **card imutável e
  datado** com a ideia, a fonte, o veredito **daquele momento**, o destino e as dimensões.
- **FR3**: QUANDO o veredito de uma ideia mudar, O SISTEMA DEVERÁ registrar a mudança no
  **índice de estado** (append-only), sem editar o card — momento e estado são artefatos
  distintos.
- **FR4**: QUANDO uma ideia estiver como `adotar` ou `absorver`, O SISTEMA DEVERÁ falhar se
  o **destino declarado não existir no disco**: absorção sem destino é intenção registrada
  como fato.
- **FR5**: QUANDO uma ideia estiver como `observar`, O SISTEMA DEVERÁ falhar se ela não
  carregar **gatilho de reavaliação** — "observar" sem gatilho é esquecer com cerimônia.
- **FR6**: QUANDO uma fonte não permitir redistribuição (licença incompatível), O SISTEMA
  DEVERÁ marcá-la como **citável, não copiável**, e essa marca DEVERÁ estar na linha da fonte.
- **FR7**: QUANDO alguém for avaliar algo novo, O SISTEMA DEVERÁ oferecer um **template com
  as dimensões**, para que a avaliação não dependa de quem a escreve.

## Fora de escopo

- **Reavaliar os vereditos de 2026.** Este ciclo migra o que já foi julgado e mede a
  coerência do que foi prometido. Rejulgar nove ferramentas seria trocar o objeto do ciclo.
- **Absorver o que faltou.** Worktree por task e standards por camada voltam ao estado
  honesto (`observar`, com gatilho); implementá-los é decisão de outro ciclo, com dor real.
- **Ranking ou pontuação agregada.** As dimensões existem para tornar a avaliação
  comparável, não para produzir uma nota. Nota única esconde a dimensão que decidiu.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `docs/ecosystem/` existe com: índice, fontes, um card por ideia e o índice de estado.
- **Toda** fonte já avaliada no repositório está na lista de fontes, com licença — as quatro
  origens da tabela acima, sem perda.
- Cada ideia tem card datado com as sete dimensões preenchidas.
- `scripts/check-ecosystem.sh` cobre FR1 a FR6 e foi **visto acusar por mutação** em cada um.
- O portão acusa hoje as duas absorções que nunca aconteceram — e passa a verde só depois de
  elas voltarem ao estado honesto, não por exceção no portão.
- `.specify/templates/evaluation-template.md` traz as sete dimensões e o vocabulário de
  veredito, e é copiado pelo instalador.
- O índice entra no livro (`publicar/sumario.json`, parte "Bastidores").

## Clarify

1. **Por que a ideia, e não a ferramenta?** Porque é a ideia que atravessa a fronteira. A
   ferramenta é o lugar onde a vimos. Catalogar por ferramenta produz um veredito que não
   cabe em nenhum lugar do método; catalogar por ideia produz um destino verificável.
2. **Por que append-only no estado?** Mesmo motivo de `docs/records/decisoes.jsonl`: mudar
   de ideia é legítimo, apagar o registro de que se pensava diferente não é. O estado
   corrente é a **última linha** de cada id.
3. **Por que sete dimensões, e não uma nota?** Uma nota agregada esconde qual dimensão
   decidiu. A licença sozinha reprova (ciclo 046); o conflito com princípio sozinho reprova.
   Dimensão que reprova sozinha não pode ser diluída numa média.
