# Data model 047 — fonte · ideia · estado

> Três entidades, porque o momento e o estado **não são a mesma coisa**. Este arquivo é o
> contrato que `scripts/check-ecosystem.sh` lê; mudar um campo aqui é mudar o portão.

## As entidades

```
FONTE  1 ──── N  IDEIA  1 ──── N  ESTADO
(onde vimos)     (o que          (o que vale
                  atravessa)      hoje)
```

| Entidade | Mutável? | Onde vive | Por quê |
|---|---|---|---|
| **Fonte** | linha fina, atualizável | `docs/ecosystem/fontes.md` | é um endereço: `owner/repo`, o que é, licença. Muda pouco. |
| **Ideia** | **imutável** | `docs/ecosystem/ideias/NNN-<slug>.md` | é uma **observação datada**: o que vimos, quando, em que versão, e o que julgamos naquele momento. Reescrever é apagar história. |
| **Estado** | **append-only** | `docs/ecosystem/estado.jsonl` | o veredito corrente muda. Corrigir é linha nova; o estado corrente é a **última linha** de cada `ideia`. |

Mesma separação que o repositório já usa entre `docs/adr/` (prosa imutável) e
`docs/records/decisoes.jsonl` (índice consultável append-only). Não é padrão novo: é o
padrão da casa aplicado a outro domínio.

## Fonte — a linha fina

Uma linha de tabela em `docs/ecosystem/fontes.md`:

| Campo | Obrigatório | Conteúdo |
|---|---|---|
| `owner/repo` | ✅ | identificador canônico (ou `nome (proprietário)` quando não há repositório público) |
| o que é | ✅ | uma frase |
| licença | ✅ | SPDX quando houver; **`citável, não copiável`** quando a licença impedir redistribuição (FR6) |
| observado em | ✅ | `YYYY-MM-DD` + versão/commit quando aplicável |

`sem licença declarada` é um valor **legítimo e informativo** — significa "todos os direitos
reservados", que é o pior caso para copiar (lição do ciclo 046).

## Ideia — o card imutável

Anatomia obrigatória de `docs/ecosystem/ideias/NNN-<slug>.md`, lida pelo portão:

```markdown
# NNN — <a ideia, em uma frase>

- **Id**: `<slug>`                     <- casa com o estado.jsonl
- **Fonte**: `owner/repo`              <- tem de existir em fontes.md
- **Observado em**: 2026-07-30         <- a data DA OBSERVAÇÃO, não a de hoje
- **Veredito no momento**: absorver    <- congelado; o de hoje está no índice
- **Destino**: `skills/verifiable-dod/SKILL.md`   <- ou `—` quando não houver
- **Gatilho de reavaliação**: <condição observável>   <- ou `—`

## A ideia
## Por que atravessa (ou não)
## Dimensões
| # | Dimensão | Leitura |
```

As sete dimensões, sempre todas, sempre nesta ordem:

| # | Dimensão | Pergunta | Reprova sozinha? |
|---|---|---|---|
| 1 | Conflito com princípio | qual princípio, e é insanável? | **sim** |
| 2 | Licença e redistribuição | dá para copiar, ou só citar? | **sim** |
| 3 | Função já servida | duplica algo que já temos (Princípio VI)? | não |
| 4 | Custo de contexto | quanto custa carregar? | não |
| 5 | Reversibilidade | quanto custa sair (lock-in)? | não |
| 6 | Maturidade e evidência | o que **nós** observamos, em que versão | não |
| 7 | Dor real hoje | a dor existe aqui, agora (YAGNI)? | não |

Sem nota agregada, por decisão: duas dimensões reprovam sozinhas e uma média as diluiria.

## Estado — o índice append-only

Uma linha JSON por mudança de estado:

```json
{"ideia":"ears","estado":"absorver","data":"2026-08-10","destino":"skills/verifiable-dod/SKILL.md","gatilho":"","ciclo":"047"}
```

| Campo | Obrigatório | Conteúdo |
|---|---|---|
| `ideia` | ✅ | o `Id` do card |
| `estado` | ✅ | `adotar` · `absorver` · `observar` · `descartar` — vocabulário **fechado** |
| `data` | ✅ | `YYYY-MM-DD` |
| `destino` | condicional | caminho no repositório; **obrigatório e tem de existir** quando `estado` é `adotar` ou `absorver` (FR4) |
| `gatilho` | condicional | condição observável de reavaliação; **obrigatório** quando `estado` é `observar` (FR5) |
| `ciclo` | — | `NNN` de onde veio |

### Vocabulário de veredito (fechado)

| Estado | Significa | O que o portão exige |
|---|---|---|
| `adotar` | a ferramenta entra, como dependência do método | destino existente |
| `absorver` | a **ideia** entra, reimplementada em artefato nosso | destino existente |
| `observar` | não agora; pode mudar | gatilho não vazio |
| `descartar` | não entra; conflito de princípio ou licença | nada — mas o card diz qual |

**Por que `adotar`/`absorver` exigem destino que existe**: é o invariante que dá sentido ao
catálogo. Sem ele, "absorvemos a ideia X" é intenção registrada como fato — e foi
exatamente o que aconteceu com duas das quatro absorções do ADR 0008, por 39 ciclos.

## Invariantes (o que o portão verifica)

1. Toda fonte tem `owner/repo`, licença e data de observação.
2. Todo card tem a anatomia acima e as sete dimensões.
3. Todo card tem estado, e todo estado tem card — **nos dois sentidos**.
4. Toda fonte citada por um card existe em `fontes.md`.
5. `adotar`/`absorver` ⇒ destino declarado existe no disco.
6. `observar` ⇒ gatilho não vazio.
7. Estado fora do vocabulário é falha.
8. Catálogo vazio é falha, nunca aprovação.
