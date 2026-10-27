# DONE — `073-T3-correcao-administracao` (attempt=2, ciclo 073)

> **Fallback durável**: a mensagem `[[DONE]]` foi enviada ao Gerente por cross-session; este arquivo
> existe porque o canal de mensagens ficou indisponível (limite temporário do classificador) no
> momento do fechamento. Conteúdo idêntico ao da mensagem.
>
> **Data**: 2026-10-26 · **Worker**: Worker04 (worktree `w/worker04`) · **Base**: `dbfe3f2`
> (`git merge --ff-only` feito antes de mexer) · **Commit**: `9fbbad3` · 4 arquivos, 49 inserções,
> 25 remoções · **Limites**: sem push, sem merge, sem código de produto, sem segredo.

## Corrigido — telas da Administração (revisão fresca, `revisao-073-rodada-3.md` §1)

| # | Onde | Correção |
|---|---|---|
| **R5** | `administracao-politicas.html:62, :92, :98, :110, :122, :123` | `hooks/guard-immutables.py` → `scripts/hooks/guard-immutables.py` (6×). Conferido: não existe `hooks/` na raiz; o arquivo está em `scripts/hooks/` |
| **R2b** | `administracao-politicas.html:105` | "portão do humano" → "portão do regente" — grafia do mapa §7 (`mapa-de-contextos.md:296`); o sentido é o do *ask* (ação irreversível espera o humano) |
| **R6** | as 3 telas | `data-exemplo="true"` nos 18 valores ilustrativos (5 + 8 + 5), além de `class="exemplo"` e da palavra no texto |

R1, R1b, R2, R3 e R4 **não** tocam estas telas (são de `mensageria-*` e `workflow-03`).

## Declarado como dívida da rodada 4 (no `qa-report.md`)

- **R8** — prefixo numérico: renomear arquivo é decisão da regente (uniformizou o Workflow em
  `af81499` e deixou a Administração como está). **Não renomeei.**
- **R9** — base única de citação: a revisão não listou estas telas, mas o padrão ocorre — o mesmo
  rodapé mistura citação relativa ao ciclo (`ux-design 066 §4`) com relativa à raiz
  (`specs/066-painel-de-regencia/ux-design.md §4 e §7`), e cita `tasks.md` sem diretório. Escolher a
  base é decisão (recomendação 5 da revisão). **Não mudei 20 citações em silêncio.**

## Verificação

- `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → **11 telas, 0 achados, exit 0**.
- Auto-checagem própria re-rodada **só nas 3 telas** (cópia temporária): `fit073.py` **PASS**
  (R1–R9 verdes) e `mut073.py` **PASS** (9/9); a mutação do R4 foi reapontada para a marcação nova.
- Nota para a rodada 4: a regra 4 do gate ainda não foi ampliada a `<p>`/`<td>`/atributos (§2.3 da
  revisão); quando for, nenhuma destas 3 acusa termo de colisão nu — "portão" só aparece qualificado
  ("portão do regente") e "fila" não aparece.

## Tokens da tentativa (piso)

Somados de `message.usage` no transcript da sessão, da primeira ocorrência de
`[[TASK id=073-T3-correcao-administracao]]` até o fim · 43 requisições · `deepseek-v4.1-flash`:

| input | output | cache_read | total_in |
|---|---|---|---|
| 1.473.761 | 43.177 | 4.228.096 | 5.701.857 |
